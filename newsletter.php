<?php
declare(strict_types=1);

header('Content-Type: application/json; charset=utf-8');

function sendSubscriptionsFile(string $csvFile): bool
{
    if (!function_exists('mail') || !is_readable($csvFile)) {
        return false;
    }

    $to = 'cognac@mdpierre.com';
    $subject = 'Newsletter Cognac Esprit Organic - fichier mis a jour';
    $boundary = 'ceo-newsletter-' . bin2hex(random_bytes(12));
    $csvContent = chunk_split(base64_encode((string)file_get_contents($csvFile)));

    $headers = [
        'From: Cognac Esprit Organic <no-reply@cognac-esprit-organic.com>',
        'MIME-Version: 1.0',
        'Content-Type: multipart/mixed; boundary="' . $boundary . '"'
    ];

    $message = "--{$boundary}\r\n";
    $message .= "Content-Type: text/plain; charset=utf-8\r\n";
    $message .= "Content-Transfer-Encoding: 8bit\r\n\r\n";
    $message .= "Bonjour,\r\n\r\n";
    $message .= "Une nouvelle adresse e-mail vient d'etre ajoutee a la newsletter Cognac Esprit Organic.\r\n";
    $message .= "Le fichier complet subscriptions.csv est joint a cet e-mail.\r\n\r\n";
    $message .= "--{$boundary}\r\n";
    $message .= "Content-Type: text/csv; name=\"subscriptions.csv\"\r\n";
    $message .= "Content-Transfer-Encoding: base64\r\n";
    $message .= "Content-Disposition: attachment; filename=\"subscriptions.csv\"\r\n\r\n";
    $message .= $csvContent . "\r\n";
    $message .= "--{$boundary}--\r\n";

    return mail($to, $subject, $message, implode("\r\n", $headers));
}

if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    http_response_code(405);
    echo json_encode(['ok' => false, 'error' => 'method_not_allowed']);
    exit;
}

$rawBody = file_get_contents('php://input');
$payload = json_decode($rawBody ?: '', true);
if (!is_array($payload)) {
    $payload = $_POST;
}

$email = strtolower(trim((string)($payload['email'] ?? '')));
if (!filter_var($email, FILTER_VALIDATE_EMAIL)) {
    http_response_code(422);
    echo json_encode(['ok' => false, 'error' => 'invalid_email']);
    exit;
}

$language = preg_replace('/[^a-z-]/i', '', (string)($payload['language'] ?? ''));
$market = preg_replace('/[^a-z-]/i', '', (string)($payload['market'] ?? ''));
$page = trim((string)($payload['page'] ?? ''));
$page = substr($page, 0, 500);

$storageDir = __DIR__ . '/newsletter-data';
if (!is_dir($storageDir) && !mkdir($storageDir, 0750, true)) {
    http_response_code(500);
    echo json_encode(['ok' => false, 'error' => 'storage_unavailable']);
    exit;
}

$file = $storageDir . '/subscriptions.csv';
$isNewFile = !file_exists($file);
$handle = fopen($file, 'ab');
if (!$handle) {
    http_response_code(500);
    echo json_encode(['ok' => false, 'error' => 'file_unavailable']);
    exit;
}

if (!flock($handle, LOCK_EX)) {
    fclose($handle);
    http_response_code(500);
    echo json_encode(['ok' => false, 'error' => 'lock_unavailable']);
    exit;
}

if ($isNewFile) {
    fputcsv($handle, ['registered_at', 'email', 'language', 'market', 'page']);
}

fputcsv($handle, [gmdate('c'), $email, $language, $market, $page]);
flock($handle, LOCK_UN);
fclose($handle);

$mailSent = sendSubscriptionsFile($file);

echo json_encode(['ok' => true, 'mail_sent' => $mailSent]);
