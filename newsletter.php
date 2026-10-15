<?php
declare(strict_types=1);
require_once __DIR__ . '/api/salon-lib.php';
salon_headers();


try {
    if (($_SERVER['REQUEST_METHOD'] ?? '') !== 'POST') throw new SalonError('method_not_allowed', 405);
    salon_guard_origin();
    $input = salon_input();
    $email = salon_normalize('email', $input['email'] ?? '');
    if (!empty($input['company_url'])) throw new SalonError('submission_rejected', 422);
    $store = salon_store();
    salon_limit($store, 'newsletter', 12);
    salon_cleanup($store);
    salon_sync_newsletter($store);
    $context = newsletter_context((string) ($input['page'] ?? $_SERVER['HTTP_REFERER'] ?? ''),
        (string) ($input['language'] ?? 'fr'), (string) ($input['market'] ?? ''),
        'eo-footer-news-2026-10-15-v1', 'site-newsletter');
    $texts = [
        'fr' => 'En renseignant votre adresse e-mail, vous acceptez de recevoir nos dernières actualités sur nos produits et vous prenez connaissance de nos mentions légales.',
        'en' => 'By entering your e-mail address, you agree to receive occasional news about our products and acknowledge our legal notice.',
        'da' => 'Ved at angive din e-mailadresse accepterer du at modtage nyheder om vores produkter og bekræfter vores juridiske oplysninger.',
        'no' => 'Ved å skrive inn e-postadressen din samtykker du til å motta nyheter om produktene våre og bekrefter våre juridiske opplysninger.',
        'sv' => 'Genom att ange din e-postadress godkänner du att få nyheter om våra produkter och bekräftar vår juridiska information.',
    ];
    $text = $texts[$context['language']] ?? $texts['fr'];
    $db = $store['db'];
    $db->exec('BEGIN IMMEDIATE');
    try {
        $now = $context['registered_at'];
        $id = salon_id($store, 'email', $email);
        $record = ['brand' => EO_SALON_BRAND, 'channel' => 'email', 'contact' => $email,
            'consented_at' => $now, 'consent_version' => $context['consent_version'],
            'consent_text' => $text, 'source' => 'site-newsletter', 'page' => $context['page'],
            'language' => $context['language'], 'market' => $context['market'], 'ownership' => 'declared_not_verified'];
        $q = $db->prepare('INSERT INTO contacts VALUES (?, "email", "active", ?, ?, ?, ?, "declared")
            ON CONFLICT(id) DO UPDATE SET state="active", cipher=excluded.cipher,
            changed_at=excluded.changed_at, expires_at=excluded.expires_at');
        $q->execute([$id, salon_encrypt($store, $record), $now, $now, gmdate('c', strtotime('+3 years'))]);
        salon_event($store, $id, 'email', 'consent_granted', ['consent_version' => $context['consent_version'],
            'source' => 'site-newsletter', 'page' => $context['page'], 'language' => $context['language'],
            'text' => $text, 'positive_action' => 'newsletter_form_submit']);
        salon_queue($store, ['action' => 'add', 'selected' => ['email' => $email],
            'context' => $context, 'texts' => ['email' => $text]]);
        $db->exec('COMMIT');
    } catch (Throwable $e) { $db->exec('ROLLBACK'); throw $e; }
    salon_sync_newsletter($store);
    $notification = salon_notify_newsletter($store);
    salon_response(200, ['ok' => true, 'status' => 'saved', 'notification' => $notification, 'mail_sent' => $notification === 'sent']);
} catch (SalonError $e) {
    if ($e->httpStatus === 429) header('Retry-After: 900');
    salon_response($e->httpStatus, ['ok' => false, 'status' => $e->getMessage(), 'error' => $e->getMessage()]);
} catch (Throwable $e) {
    error_log('Shared newsletter storage unavailable [' . get_class($e) . ']');
    salon_response(503, ['ok' => false, 'status' => 'temporarily_unavailable']);
}
