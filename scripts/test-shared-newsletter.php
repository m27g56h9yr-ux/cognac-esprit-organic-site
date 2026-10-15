<?php
declare(strict_types=1);

// Isolated fixtures only. Transports below are in-memory callbacks, never mail().
$fixture = sys_get_temp_dir() . '/eo-newsletter-test-' . bin2hex(random_bytes(8));
mkdir($fixture . '/www/site/api', 0700, true);
mkdir($fixture . '/www/site/newsletter-data', 0700, true);
foreach (['salon-lib.php', 'salon-newsletter.php', 'newsletter-lib.php'] as $name) {
    copy(dirname(__DIR__) . '/api/' . $name, $fixture . '/www/site/api/' . $name);
}
file_put_contents($fixture . '/www/site/api/salon-config.php', "<?php return ['admin_token_hash' => '" . str_repeat('1', 64) . "', 'newsletter_schema' => 2];");
putenv('EO_SALON_PRIVATE_DIR=' . $fixture . '/private');
require $fixture . '/www/site/api/salon-lib.php';

function check(bool $ok, string $label): void
{
    if (!$ok) throw new RuntimeException('FAIL: ' . $label);
    echo 'PASS: ' . $label . "\n";
}
function subscribe_fixture(array $store, string $email, string $phone = ''): array
{
    $store['db']->exec('BEGIN IMMEDIATE');
    try {
        $challenge = salon_challenge($store);
        salon_consume($store, $challenge);
        $result = salon_subscribe($store, ['email' => $email, 'phone' => $phone,
            'consent_email' => $email !== '', 'consent_sms' => $phone !== '',
            'consent_version' => EO_SALON_VERSION, 'challenge' => $challenge]);
        $store['db']->exec('COMMIT');
    } catch (Throwable $e) { $store['db']->exec('ROLLBACK'); throw $e; }
    salon_sync_newsletter($store);
    return $result;
}
function withdraw_fixture(array $store, array $input): void
{
    $store['db']->exec('BEGIN IMMEDIATE');
    try { salon_withdraw($store, $input); $store['db']->exec('COMMIT'); }
    catch (Throwable $e) { $store['db']->exec('ROLLBACK'); throw $e; }
    salon_sync_newsletter($store);
}
function read_fixture(): array
{
    $lock = newsletter_lock();
    try { return newsletter_read()[1]; }
    finally { flock($lock, LOCK_UN); fclose($lock); }
}

try {
    $csv = fopen(newsletter_path(), 'wb');
    fputcsv($csv, ['registered_at', 'email', 'language', 'market', 'page'], ',', '"', '');
    fputcsv($csv, [gmdate('c'), 'historical@example.invalid', 'no', 'no', 'https://cognac-esprit-organic.com/no/produits/transmission-xo.html'], ',', '"', '');
    fclose($csv);
    $store = salon_store();
    salon_sync_newsletter($store);
    $status = salon_newsletter_status($store);
    check($status['rows'] === 1 && $status['legacy_rows'] === 1 && !$status['notification']['pending'], 'historical row preserved; migration sends no notification');
    $first = subscribe_fixture($store, 'First@example.invalid', '+44 7700 900123');
    $rows = read_fixture();
    check(count($rows) === 2 && $rows[1]['email'] === 'first@example.invalid' && $rows[1]['phone'] === '+447700900123', 'email and phone stored together and normalized');
    check($rows[1]['page'] === '/se-retrouver/' && $rows[1]['phone_page'] === '/se-retrouver/', 'source pages persisted');
    $revision = $store['db']->query('SELECT revision FROM newsletter_mail_state')->fetchColumn();
    subscribe_fixture($store, 'first@example.invalid', '+447700900123');
    check(count(read_fixture()) === 2 && $store['db']->query('SELECT revision FROM newsletter_mail_state')->fetchColumn() === $revision, 'duplicate creates neither row nor notification');
    $token = parse_url($first['manage_url'], PHP_URL_FRAGMENT);
    $inspect = salon_inspect($store, ['token' => $token], salon_newsletter_states($store, $token));
    check(count($inspect['channels']) === 2, 'private link recognizes both channels');
    withdraw_fixture($store, ['token' => $token, 'channels' => ['email']]);
    $rows = read_fixture();
    check(count($rows) === 2 && $rows[1]['email'] === '' && $rows[1]['phone'] === '+447700900123', 'email withdrawal preserves selected phone subscription');
    withdraw_fixture($store, ['phone' => '+447700900123', 'channels' => ['sms']]);
    check(count(read_fixture()) === 1, 'coordinate withdrawal removes phone from common CSV');
    withdraw_fixture($store, ['email' => 'historical@example.invalid', 'channels' => ['email']]);
    check(count(read_fixture()) === 0, 'historical CSV-only address can unsubscribe');

    subscribe_fixture($store, 'hour-one@example.invalid');
    $clockNow = time() + 10;
    $clock = static function () use (&$clockNow): int { return $clockNow; };
    $sent = [];
    $transport = static function ($csv, $id) use (&$sent, &$clockNow): bool { $sent[] = [$clockNow, $csv, $id]; return true; };
    check(salon_notify_newsletter($store, $transport, $clock) === 'sent' && count($sent) === 1, 'first new registration sends full list');
    subscribe_fixture($store, 'hour-two@example.invalid');
    $clockNow += 3599;
    $store = salon_store(); // New connection simulates a process restart.
    check(salon_notify_newsletter($store, $transport, $clock) === 'pending' && count($sent) === 1, '3599 seconds and process restart do not bypass hourly limit');
    withdraw_fixture($store, ['email' => 'hour-one@example.invalid', 'channels' => ['email']]);
    $clockNow++;
    check(salon_notify_newsletter($store, $transport, $clock) === 'sent' && count($sent) === 2, 'deferred list sends at 3600 seconds without another signup');
    check(strpos($sent[1][1], 'hour-two@example.invalid') !== false && strpos($sent[1][1], 'hour-one@example.invalid') === false, 'deferred list includes new contacts and excludes withdrawals');
    check(salon_notify_newsletter($store, $transport, $clock) === 'idle', 'unchanged list is not resent');

    subscribe_fixture($store, 'failure@example.invalid');
    $clockNow += 3600;
    check(salon_notify_newsletter($store, static fn (): bool => false, $clock) === 'failed', 'transport failure is retained');
    $clockNow += 3599;
    check(salon_notify_newsletter($store, $transport, $clock) === 'pending', 'failed transport retains one-hour reservation');
    $clockNow++;
    check(salon_notify_newsletter($store, $transport, $clock) === 'sent', 'failed notification retries after one hour');

    subscribe_fixture($store, 'during-send@example.invalid');
    $clockNow += 3600;
    $nested = '';
    $slow = static function ($csv, $id) use ($store, $transport, $clock, &$nested): bool {
        subscribe_fixture($store, 'concurrent-signup@example.invalid');
        $nested = salon_notify_newsletter($store, $transport, $clock);
        return $transport($csv, $id);
    };
    check(salon_notify_newsletter($store, $slow, $clock) === 'sent' && $nested === 'pending', 'mail lock prevents overlapping send');
    check(salon_newsletter_notification_status($store)['pending'], 'signup during transport remains pending');
    $clockNow += 3600;
    check(salon_notify_newsletter($store, $transport, $clock) === 'sent', 'concurrent signup appears in next batch');

    if (function_exists('pcntl_fork')) {
        subscribe_fixture($store, 'parallel@example.invalid');
        $clockNow += 3600;
        $children = [];
        for ($i = 0; $i < 4; $i++) {
            $pid = pcntl_fork();
            if ($pid === 0) {
                $childStore = salon_store();
                salon_notify_newsletter($childStore, static function () use ($fixture): bool {
                    file_put_contents($fixture . '/parallel-sends', "sent\n", FILE_APPEND | LOCK_EX);
                    usleep(100000);
                    return true;
                }, $clock);
                exit(0);
            }
            if ($pid < 0) throw new RuntimeException('Fork unavailable');
            $children[] = $pid;
        }
        foreach ($children as $pid) { pcntl_waitpid($pid, $childStatus); check(pcntl_wexitstatus($childStatus) === 0, 'parallel worker completed'); }
        check(file_get_contents($fixture . '/parallel-sends') === "sent\n", 'four simultaneous processes send only one list');
    }
    check((fileperms(newsletter_path()) & 0077) === 0, 'common CSV permissions remain private');
    echo "All shared newsletter checks passed; no real email sent.\n";
} finally {
    // Only delete this invocation's disposable fixture directory.
    foreach (new RecursiveIteratorIterator(new RecursiveDirectoryIterator($fixture, FilesystemIterator::SKIP_DOTS), RecursiveIteratorIterator::CHILD_FIRST) as $entry) {
        $entry->isDir() ? rmdir($entry->getPathname()) : unlink($entry->getPathname());
    }
    rmdir($fixture);
}
