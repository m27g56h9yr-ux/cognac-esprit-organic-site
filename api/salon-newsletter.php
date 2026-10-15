<?php
declare(strict_types=1);
require_once __DIR__ . '/newsletter-lib.php';

/** Encrypted outbox; success is returned only after the common CSV is durable. */
function salon_queue(array $store, array $operation): int
{
    $q = $store['db']->prepare('INSERT INTO newsletter_pending(cipher) VALUES (?)');
    $q->execute([salon_encrypt($store, $operation)]);
    return (int) $store['db']->lastInsertId();
}

function salon_sync_newsletter(array $store): array
{
    // Uploaded last by deployment, after both writers and their dependencies.
    if (!$store['newsletter_ready']) throw new RuntimeException('Newsletter deployment in progress');
    $lock = newsletter_lock();
    $db = $store['db'];
    $applied = [];
    try {
        $migrated = (bool) $db->query("SELECT value FROM newsletter_bridge WHERE name='imported'")->fetchColumn();
        if (!$migrated) {
            // Commit the encrypted original BEFORE replacing the historical file.
            // A failed migration can therefore be recovered without losing rows.
            $original = is_file(newsletter_path()) ? file_get_contents(newsletter_path()) : '';
            if ($original === false) throw new RuntimeException('Newsletter backup unavailable');
            $q = $db->prepare('INSERT OR IGNORE INTO newsletter_backup VALUES (1, ?, ?)');
            $q->execute([salon_encrypt($store, ['csv_base64' => base64_encode($original)]), gmdate('c', strtotime('+7 days'))]);
        }
        // Every sync uses CSV lock -> SQLite lock. Callers commit their mutations first.
        $db->exec('BEGIN IMMEDIATE');
        try {
            [$header, $rows] = newsletter_read();
            if (!$migrated) {
                $legacyRows = count($rows);
                foreach ($db->query('SELECT * FROM contacts ORDER BY changed_at')->fetchAll() as $r) {
                    if ($r['state'] !== 'active') {
                        newsletter_apply($store, $rows, ['action' => 'remove', 'ids' => [$r['id']]]);
                        continue;
                    }
                    $data = salon_decrypt($store, $r['cipher']);
                    newsletter_apply($store, $rows, ['action' => 'add', 'selected' => [$r['channel'] => $data['contact']],
                        'context' => ['registered_at' => $data['consented_at'], 'page' => $data['page'],
                            'language' => $data['language'] ?? 'fr', 'market' => $data['market'] ?? '',
                            'consent_version' => $data['consent_version'], 'source' => $data['source']],
                        'texts' => [$r['channel'] => $data['consent_text']]]);
                }
            }
            foreach ($db->query('SELECT * FROM newsletter_pending ORDER BY id')->fetchAll() as $item) {
                $applied[$item['id']] = newsletter_apply($store, $rows, salon_decrypt($store, $item['cipher']));
            }
            $expired = newsletter_expire($rows);
            if (!$migrated || $applied || $expired || !is_file(newsletter_path())) newsletter_write($header, $rows);
            if (!$migrated) {
                $q = $db->prepare('INSERT OR REPLACE INTO newsletter_bridge VALUES (?, ?)');
                $q->execute(['legacy_rows', (string) $legacyRows]);
                $q->execute(['imported', '1']);
            }
            $db->exec('DELETE FROM newsletter_pending');
            $db->exec('COMMIT');
        } catch (Throwable $e) { $db->exec('ROLLBACK'); throw $e; }
    } finally { flock($lock, LOCK_UN); fclose($lock); }
    // Neither migration, maintenance nor a Se retrouver registration sends mail.
    return $applied;
}

/** Metadata only: never expose a coordinate through the status endpoint. */
function salon_newsletter_status(array $store): array
{
    $lock = newsletter_lock();
    try {
        [, $rows] = newsletter_read();
        $file = fopen(newsletter_path(), 'rb');
        if (!$file) throw new RuntimeException('Newsletter header unavailable');
        try { $header = fgetcsv($file, 0, ',', '"', ''); }
        finally { fclose($file); }
        if (!is_array($header)) throw new RuntimeException('Newsletter header unavailable');
    }
    finally { flock($lock, LOCK_UN); fclose($lock); }
    $sources = $emails = $phones = [];
    foreach ($rows as $row) {
        if (!empty($row['email'])) $emails[strtolower(trim($row['email']))] = true;
        if (!empty($row['phone'])) $phones[$row['phone']] = true;
        $page = newsletter_page((string) ($row['page'] ?? '')) ?: '(non renseignée)';
        $sources[$page] = ($sources[$page] ?? 0) + 1;
    }
    return ['schema_version' => 2, 'rows' => count($rows), 'active_emails' => count($emails),
        'active_phones' => count($phones), 'columns' => $header, 'pages' => $sources,
        'legacy_rows' => (int) $store['db']->query("SELECT value FROM newsletter_bridge WHERE name='legacy_rows'")->fetchColumn(),
        'pending' => (int) $store['db']->query('SELECT COUNT(*) FROM newsletter_pending')->fetchColumn(),
        'storage' => 'protected_newsletter_csv',
        'migration_backup_expires_at' => $store['db']->query('SELECT expires_at FROM newsletter_backup WHERE id=1')->fetchColumn() ?: null];
}

function salon_newsletter_states(array $store, string $token): array
{
    $ids = salon_manage_ids($store, $token);
    $lock = newsletter_lock();
    try { [, $rows] = newsletter_read(); }
    finally { flock($lock, LOCK_UN); fclose($lock); }
    $states = [];
    foreach ($rows as $row) foreach (['email' => 'email', 'sms' => 'phone'] as $channel => $field) {
        if (empty($row[$field])) continue;
        $id = salon_id($store, $channel, strtolower(trim((string) $row[$field])));
        if (in_array($id, $ids, true)) $states[$id] = 'active';
    }
    return $states;
}

function salon_newsletter_export(array $store): void
{
    $lock = newsletter_lock();
    try { [$header, $rows] = newsletter_read(); }
    finally { flock($lock, LOCK_UN); fclose($lock); }
    $header = array_values(array_unique(array_merge($header, ['email_unsubscribe_url', 'phone_unsubscribe_url'])));
    header('Content-Type: text/csv; charset=utf-8');
    header('Content-Disposition: attachment; filename="cognac-esprit-organic-contacts-' . gmdate('Ymd-His') . '-utc.csv"');
    $out = fopen('php://output', 'wb');
    if (!$out || fputcsv($out, $header, ',', '"', '') === false) throw new RuntimeException('Export unavailable');
    foreach ($rows as $row) {
        foreach (['email' => 'email', 'sms' => 'phone'] as $channel => $field) {
            if (empty($row[$field])) continue;
            $value = strtolower(trim((string) $row[$field]));
            $id = salon_id($store, $channel, $value);
            // Signed channel also permits managing a historical CSV-only contact.
            $token = salon_sign($store, 'manage', ['ids' => [$id], 'channels' => [$id => $channel]]);
            $row[$field . '_unsubscribe_url'] = EO_SALON_ORIGIN . '/se-retrouver/desinscription/#' . $token;
        }
        newsletter_csv_row($out, $header, $row);
    }
    fclose($out);
}
