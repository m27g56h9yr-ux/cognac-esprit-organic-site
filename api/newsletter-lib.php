<?php
declare(strict_types=1);

/** Existing Esprit Organic address book, shared by both signup forms. */
function newsletter_path(): string
{
    return dirname(__DIR__) . '/newsletter-data/subscriptions.csv';
}

function newsletter_header(): array
{
    // Keep the five historical columns first, with their original values.
    return ['registered_at', 'email', 'language', 'market', 'page', 'phone',
        'consent_email', 'consent_sms', 'email_page', 'phone_page', 'last_page',
        'updated_at', 'email_consented_at', 'phone_consented_at',
        'email_consent_version', 'phone_consent_version',
        'email_consent_text', 'phone_consent_text', 'source', 'last_source', 'record_version',
        'card_id', 'email_card_id', 'phone_card_id'];
}

function newsletter_page(string $value): string
{
    if ($value === '' || strlen($value) > 4096) return '';
    $parts = parse_url($value);
    if ($parts === false || (isset($parts['host']) && !in_array(strtolower($parts['host']),
        ['cognac-esprit-organic.com', 'www.cognac-esprit-organic.com'], true))) return '';
    $path = $parts['path'] ?? '/';
    return strpos($path, '/') === 0 ? substr(preg_replace('/[\x00-\x20\x7f]/', '', $path) ?? '', 0, 500) : '';
}

function newsletter_context(string $page, string $language, string $market, string $version, string $source): array
{
    return ['registered_at' => gmdate('c'), 'page' => newsletter_page($page),
        'language' => substr(preg_replace('/[^a-z-]/i', '', $language) ?? '', 0, 12),
        'market' => substr(preg_replace('/[^a-z-]/i', '', $market) ?? '', 0, 12),
        'consent_version' => $version, 'source' => $source];
}

function newsletter_lock()
{
    $path = newsletter_path();
    $dir = dirname($path);
    if (is_link($dir) || is_link($path) || is_link($path . '.lock')) throw new RuntimeException('Unsafe newsletter link');
    if (!is_dir($dir) && !mkdir($dir, 0700, true) && !is_dir($dir)) throw new RuntimeException('Newsletter directory unavailable');
    if (!chmod($dir, 0700)) throw new RuntimeException('Newsletter permissions unavailable');
    $lock = fopen($path . '.lock', 'c+b');
    if (!$lock) throw new RuntimeException('Newsletter lock unavailable');
    if (!chmod($path . '.lock', 0600) || !flock($lock, LOCK_EX)) {
        fclose($lock);
        throw new RuntimeException('Newsletter lock unavailable');
    }
    return $lock;
}

/** The stable sidecar lock must be held throughout reads and replacements. */
function newsletter_read(): array
{
    $header = newsletter_header();
    $rows = [];
    $path = newsletter_path();
    if (!is_file($path)) return [$header, $rows];
    $file = fopen($path, 'rb');
    if (!$file) throw new RuntimeException('Newsletter read unavailable');
    try {
        $oldHeader = fgetcsv($file, 0, ',', '"', '');
        if ($oldHeader === false && fstat($file)['size'] === 0) return [$header, $rows];
        if (!is_array($oldHeader)) throw new RuntimeException('Invalid newsletter header');
        $oldHeader[0] = preg_replace('/^\xEF\xBB\xBF/', '', (string) $oldHeader[0]);
        if (!in_array('email', $oldHeader, true) || count(array_unique($oldHeader)) !== count($oldHeader)) {
            throw new RuntimeException('Unrecognized newsletter header');
        }
        $header = array_values(array_unique(array_merge($oldHeader, $header)));
        $escape = in_array('record_version', $oldHeader, true) ? '' : '\\';
        while (($cells = fgetcsv($file, 0, ',', '"', $escape)) !== false) {
            if ($cells === [null]) continue;
            if (count($cells) !== count($oldHeader)) throw new RuntimeException('Invalid newsletter row');
            $row = array_combine($oldHeader, $cells);
            if (($row['record_version'] ?? '') === '2') {
                foreach ($row as &$cell) if (preg_match('/^\'[=+@\-\t\r\']/u', (string) $cell)) $cell = substr($cell, 1);
                unset($cell);
            } else {
                // Preserve historical evidence; never invent a version or SMS consent.
                $row['consent_email'] = empty($row['email']) ? '' : 'yes';
                $row['consent_sms'] = '';
                $row['email_page'] = $row['page'] ?? '';
                $row['email_consented_at'] = $row['registered_at'] ?? '';
                $row['source'] = 'site-newsletter';
            }
            $rows[] = $row;
        }
        if (!feof($file)) throw new RuntimeException('Newsletter read incomplete');
    } finally { fclose($file); }
    return [$header, $rows];
}

function newsletter_csv_row($file, array $header, array $row): void
{
    $row['record_version'] = '2';
    $cells = array_map(static function ($key) use ($row) {
        $value = (string) ($row[$key] ?? '');
        // Reversible spreadsheet escaping, including international phone numbers.
        return preg_match('/^[=+@\-\t\r\']/u', $value) ? "'" . $value : $value;
    }, $header);
    if (fputcsv($file, $cells, ',', '"', '') === false) throw new RuntimeException('Newsletter write failed');
}

function newsletter_write(array $header, array $rows): void
{
    $path = newsletter_path();
    $temp = tempnam(dirname($path), '.subscriptions-');
    if ($temp === false) throw new RuntimeException('Newsletter temporary file unavailable');
    $file = fopen($temp, 'wb');
    try {
        if (!$file || !chmod($temp, 0600)) throw new RuntimeException('Newsletter write unavailable');
        if (fputcsv($file, $header, ',', '"', '') === false) throw new RuntimeException('Newsletter write failed');
        foreach ($rows as $row) newsletter_csv_row($file, $header, $row);
        if (!fflush($file) || (function_exists('fsync') && !fsync($file))) throw new RuntimeException('Newsletter flush failed');
        fclose($file); $file = null;
        if (!rename($temp, $path)) throw new RuntimeException('Newsletter replace failed');
    } finally {
        if (is_resource($file)) fclose($file);
        if (is_file($temp)) unlink($temp);
    }
}

function newsletter_clear(array &$row, string $channel): void
{
    $field = $channel === 'sms' ? 'phone' : 'email';
    $row[$field] = '';
    $row[$channel === 'sms' ? 'consent_sms' : 'consent_email'] = '';
    foreach (['_page', '_consented_at', '_consent_version', '_consent_text', '_card_id'] as $suffix) $row[$field . $suffix] = '';
}

/** Idempotent application: retries never add a duplicate coordinate. */
function newsletter_apply(array $store, array &$rows, array $operation): bool
{
    if ($operation['action'] === 'remove') {
        foreach ($rows as &$row) foreach (['email' => 'email', 'sms' => 'phone'] as $channel => $field) {
            $value = strtolower(trim((string) ($row[$field] ?? '')));
            if ($value !== '' && in_array(salon_id($store, $channel, $value), $operation['ids'], true)) newsletter_clear($row, $channel);
        }
        unset($row);
        $rows = array_values(array_filter($rows, static fn ($r) => !empty($r['email']) || !empty($r['phone'])));
        return false;
    }
    $selected = $operation['selected'];
    $context = $operation['context'];
    $card = nfc_card_id($context['card_id'] ?? null);
    $targets = [];
    foreach ($selected as $channel => $value) {
        $field = $channel === 'sms' ? 'phone' : 'email';
        foreach ($rows as $i => $row) if (strtolower(trim((string) ($row[$field] ?? ''))) === $value) $targets[$channel][] = $i;
    }
    $created = false;
    foreach ($selected as $channel => $value) {
        $field = $channel === 'sms' ? 'phone' : 'email';
        if (empty($targets[$channel])) {
            $created = true;
            $target = null;
            // Pair coordinates submitted together, without overwriting a different one.
            foreach ($targets as $indexes) foreach ($indexes as $i) {
                if (empty($rows[$i][$field]) || $rows[$i][$field] === $value) { $target = $i; break 2; }
            }
            if ($target === null) { $target = count($rows); $rows[] = $context; }
            $targets[$channel] = [$target];
        }
        foreach ($targets[$channel] as $i) {
            if (empty($rows[$i]['page'])) $rows[$i]['page'] = $context['page'];
            if (empty($rows[$i]['source'])) $rows[$i]['source'] = $context['source'];
            $rows[$i][$field] = $value;
            $rows[$i][$channel === 'sms' ? 'consent_sms' : 'consent_email'] = 'yes';
            $rows[$i][$field . '_page'] = $context['page'];
            $rows[$i][$field . '_card_id'] = $card;
            $rows[$i]['card_id'] = $card;
            $rows[$i][$field . '_consented_at'] = $context['registered_at'];
            $rows[$i][$field . '_consent_version'] = $context['consent_version'];
            $rows[$i][$field . '_consent_text'] = $operation['texts'][$channel] ?? '';
            $rows[$i]['last_page'] = $context['page'];
            $rows[$i]['last_source'] = $context['source'];
            $rows[$i]['updated_at'] = $context['registered_at'];
        }
    }
    return $created;
}

function newsletter_expire(array &$rows): bool
{
    $changed = false;
    foreach ($rows as &$row) foreach (['email' => 'email', 'sms' => 'phone'] as $channel => $field) {
        // The old file has no versioned evidence. Preserve those rows during this
        // migration; only the explicit new/renewed agreements use this retention.
        if (empty($row[$field]) || empty($row[$field . '_consented_at']) || empty($row[$field . '_consent_version'])) continue;
        $date = strtotime($row[$field . '_consented_at']);
        if ($date !== false && strtotime('+3 years', $date) < time()) {
            newsletter_clear($row, $channel);
            $changed = true;
        }
    }
    unset($row);
    $rows = array_values(array_filter($rows, static fn ($r) => !empty($r['email']) || !empty($r['phone'])));
    return $changed;
}
