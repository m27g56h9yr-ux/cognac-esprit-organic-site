<?php
declare(strict_types=1);
require_once __DIR__ . '/newsletter-lib.php';
const EO_NEWSLETTER_NOTIFICATION_INTERVAL = 3600;
const EO_NEWSLETTER_NOTIFICATION_TO = 'cognac@mdpierre.com';

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
        $upgradeCards = $db->query("SELECT value FROM newsletter_bridge WHERE name='nfc_columns'")->fetchColumn() !== '1';
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
                            'consent_version' => $data['consent_version'], 'source' => $data['source'],
                            'card_id' => $data['card_id'] ?? ''],
                        'texts' => [$r['channel'] => $data['consent_text']]]);
                }
            }
            $pending = $db->query('SELECT * FROM newsletter_pending ORDER BY id')->fetchAll();
            foreach ($pending as $item) {
                $applied[$item['id']] = newsletter_apply($store, $rows, salon_decrypt($store, $item['cipher']));
            }
            $expired = newsletter_expire($rows);
            // Persist notification intent before touching the CSV. If a replacement
            // succeeds but acknowledgement fails, replay cannot lose the notification.
            if (in_array(true, $applied, true)) $db->exec('UPDATE newsletter_mail_state SET revision=revision+1 WHERE singleton=1');
            $db->exec('COMMIT');
        } catch (Throwable $e) { $db->exec('ROLLBACK'); throw $e; }
        if (!$migrated || $upgradeCards || $applied || $expired || !is_file(newsletter_path())) newsletter_write($header, $rows);
        $db->exec('BEGIN IMMEDIATE');
        try {
            if (!$migrated) {
                $q = $db->prepare('INSERT OR REPLACE INTO newsletter_bridge VALUES (?, ?)');
                $q->execute(['legacy_rows', (string) $legacyRows]);
                $q->execute(['imported', '1']);
            }
            if ($upgradeCards) $db->exec("INSERT OR REPLACE INTO newsletter_bridge VALUES ('nfc_columns', '1')");
            $q = $db->prepare('DELETE FROM newsletter_pending WHERE id=?');
            foreach ($pending as $item) $q->execute([$item['id']]);
            $db->exec('COMMIT');
        } catch (Throwable $e) { $db->exec('ROLLBACK'); throw $e; }
    } finally { flock($lock, LOCK_UN); fclose($lock); }
    // Transport is separate: an administration read never sends a message.
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
        'migration_backup_expires_at' => $store['db']->query('SELECT expires_at FROM newsletter_backup WHERE id=1')->fetchColumn() ?: null,
        'notification' => salon_newsletter_notification_status($store)];
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

function salon_newsletter_notification_status(array $store): array
{
    $state = $store['db']->query('SELECT * FROM newsletter_mail_state WHERE singleton=1')->fetch();
    $pending = (int) $state['revision'] > (int) $state['sent_revision'];
    $eligibleAt = max((int) $state['last_attempt_at'], (int) $state['last_sent_at']) + EO_NEWSLETTER_NOTIFICATION_INTERVAL;
    return ['to' => EO_NEWSLETTER_NOTIFICATION_TO, 'min_interval_seconds' => EO_NEWSLETTER_NOTIFICATION_INTERVAL,
        'pending' => $pending, 'last_status' => $state['last_status'],
        'last_sent_at' => $state['last_sent_at'] ? gmdate('c', (int) $state['last_sent_at']) : null,
        'next_eligible_at' => $pending ? gmdate('c', max(time(), $eligibleAt)) : null,
        'sent_count' => (int) $state['sent_count'], 'last_message_id' => $state['last_message_id']];
}

/** Separate process lock + durable reservation: never more than one send per hour. */
function salon_notify_newsletter(array $store, ?callable $transport = null, ?callable $clock = null): string
{
    $transport = $transport ?? 'salon_send_newsletter_list';
    $clock = $clock ?? static fn (): int => time();
    $mailLock = null;
    $db = $store['db'];
    $reserved = false;
    try {
        $lockPath = newsletter_path() . '.mail.lock';
        if (is_link($lockPath)) throw new RuntimeException('Unsafe notification lock');
        $mailLock = fopen($lockPath, 'c+b');
        if (!$mailLock || !chmod($lockPath, 0600)) throw new RuntimeException('Notification lock unavailable');
        if (!flock($mailLock, LOCK_EX | LOCK_NB)) return 'pending';
        $csvLock = newsletter_lock();
        try {
            $db->exec('BEGIN IMMEDIATE');
            try {
                $state = $db->query('SELECT * FROM newsletter_mail_state WHERE singleton=1')->fetch();
                $revision = (int) $state['revision'];
                $pending = $revision > (int) $state['sent_revision'];
                $now = $clock();
                $eligible = $now >= max((int) $state['last_attempt_at'], (int) $state['last_sent_at']) + EO_NEWSLETTER_NOTIFICATION_INTERVAL;
                $unflushed = (int) $db->query('SELECT COUNT(*) FROM newsletter_pending')->fetchColumn() > 0;
                if ($pending && $eligible && !$unflushed) {
                    $csv = file_get_contents(newsletter_path());
                    if ($csv === false) throw new RuntimeException('Notification snapshot unavailable');
                    $cardsCsv = nfc_report_csv(nfc_report($store));
                    $messageId = '<eo-list-' . bin2hex(random_bytes(16)) . '@cognac-esprit-organic.com>';
                    $q = $db->prepare('UPDATE newsletter_mail_state SET last_attempt_at=?, last_status="sending", last_message_id=? WHERE singleton=1');
                    $q->execute([$now, $messageId]);
                    $reserved = true;
                }
                $db->exec('COMMIT');
            } catch (Throwable $e) { $db->exec('ROLLBACK'); throw $e; }
        } finally { flock($csvLock, LOCK_UN); fclose($csvLock); }
        if (!$pending) return 'idle';
        if (!$reserved) return 'pending';
        // The CSV lock is released before transport. The dedicated mail lock stays
        // held until completion, including across slow transport or concurrent calls.
        if (!$transport($csv, $messageId, $cardsCsv)) throw new RuntimeException('Notification transport rejected');
        $q = $db->prepare('UPDATE newsletter_mail_state SET sent_revision=MAX(sent_revision, ?),
            last_sent_at=?, last_status="sent", sent_count=sent_count+1 WHERE singleton=1');
        $q->execute([$revision, $clock()]);
        return 'sent';
    } catch (Throwable $e) {
        if ($reserved) {
            try { $db->exec('UPDATE newsletter_mail_state SET last_status="failed" WHERE singleton=1'); }
            catch (Throwable $ignored) { /* Keep the existing durable reservation. */ }
        }
        error_log('Esprit Organic newsletter notification delayed [' . get_class($e) . ']');
        return 'failed';
    } finally {
        if (is_resource($mailLock)) { flock($mailLock, LOCK_UN); fclose($mailLock); }
    }
}

function salon_send_newsletter_list(string $csv, string $messageId, ?string $cardsCsv = null): bool
{
    if (!function_exists('mail')) return false;
    $boundary = 'eo-newsletter-' . bin2hex(random_bytes(12));
    $filename = 'contacts-esprit-organic-' . gmdate('Ymd-His') . '-UTC.csv';
    $subject = '=?UTF-8?B?' . base64_encode('Inscriptions Esprit Organic — liste actualisée') . '?=';
    $headers = [
        'From: Cognac Esprit Organic <no-reply@cognac-esprit-organic.com>',
        'MIME-Version: 1.0', 'Message-ID: ' . $messageId,
        'Content-Type: multipart/mixed; boundary="' . $boundary . '"',
    ];
    $message = implode("\r\n", [
        '--' . $boundary, 'Content-Type: text/plain; charset=utf-8',
        'Content-Transfer-Encoding: 8bit', '', 'Bonjour Léopold,', '',
        'De nouvelles inscriptions ont été enregistrées sur le site Esprit Organic.',
        'Voici la liste complète à jour, avec les e-mails, les téléphones et les pages d’inscription.',
        'Le bilan par carte NFC est également joint : ouvertures, clics Instagram et inscriptions.',
        'Ces compteurs ne mesurent ni les visiteurs uniques ni les abonnements Instagram.',
        'Les inscriptions rapprochées sont regroupées : au maximum une liste par heure.',
        'Les coordonnées désinscrites sont retirées de la liste avant chaque nouvel envoi.', '',
        'Date de la liste : ' . gmdate('Y-m-d H:i:s') . ' UTC.', '',
        '--' . $boundary, 'Content-Type: text/csv; charset=utf-8; name="' . $filename . '"',
        'Content-Transfer-Encoding: base64', 'Content-Disposition: attachment; filename="' . $filename . '"', '',
        chunk_split(base64_encode($csv)),
    ]);
    if ($cardsCsv !== null) {
        $cardsFilename = 'cognac-esprit-organic-cartes-nfc-' . gmdate('Ymd-His') . '-utc.csv';
        $message .= implode("\r\n", [
            '--' . $boundary, 'Content-Type: text/csv; charset=utf-8; name="' . $cardsFilename . '"',
            'Content-Transfer-Encoding: base64', 'Content-Disposition: attachment; filename="' . $cardsFilename . '"', '',
            chunk_split(base64_encode($cardsCsv)),
        ]);
    }
    $message .= '--' . $boundary . '--' . "\r\n";
    return mail(EO_NEWSLETTER_NOTIFICATION_TO, $subject, $message, implode("\r\n", $headers));
}
