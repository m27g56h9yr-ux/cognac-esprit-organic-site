<?php
declare(strict_types=1);

header('Content-Type: application/json; charset=utf-8');

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

echo json_encode(['ok' => true]);
