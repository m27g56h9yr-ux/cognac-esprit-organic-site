<?php
declare(strict_types=1);

if (!defined('JSON_INVALID_UTF8_SUBSTITUTE')) {
    define('JSON_INVALID_UTF8_SUBSTITUTE', 0);
}

function ceo_market_html($value): string
{
    return htmlspecialchars((string) $value, ENT_QUOTES | ENT_SUBSTITUTE, 'UTF-8');
}

function ceo_market_is_assoc(array $value): bool
{
    if ($value === []) {
        return false;
    }
    return array_keys($value) !== range(0, count($value) - 1);
}

function ceo_market_first_object($value): array
{
    if (!is_array($value)) {
        return [];
    }
    if (ceo_market_is_assoc($value)) {
        return $value;
    }
    foreach ($value as $item) {
        if (is_array($item)) {
            return $item;
        }
    }
    return [];
}

function ceo_market_fetch_partner_payload(string $product, string $market, string $pageUrl): array
{
    $endpoint = 'https://cognac-esprit-organic.com/partner-product-schema.php?product=' . rawurlencode($product) . '&market=' . rawurlencode($market) . '&ts=' . rawurlencode((string) time());
    $context = stream_context_create([
        'http' => [
            'method' => 'GET',
            'timeout' => 14,
            'ignore_errors' => true,
            'header' => "Accept: application/json\r\nUser-Agent: CognacEspritOrganicMarketSeo/1.0 (+https://cognac-esprit-organic.com/)\r\n",
        ],
    ]);
    $json = @file_get_contents($endpoint, false, $context);
    $payload = is_string($json) ? json_decode($json, true) : null;
    if (!is_array($payload)) {
        return [
            'ok' => false,
            'hasSchema' => false,
            'seller' => '',
            'market' => $market,
            'product' => $product,
            'schema' => null,
            'error' => 'Lecture des données partenaire impossible.',
        ];
    }
    if (isset($payload['schema']) && is_array($payload['schema'])) {
        $payload['schema']['@id'] = $pageUrl . '#product';
        $payload['schema']['url'] = $pageUrl;
    }
    return $payload;
}

function ceo_market_partner_schema_script(array $payload): string
{
    if (($payload['ok'] ?? false) !== true || ($payload['hasSchema'] ?? false) !== true || !isset($payload['schema']) || !is_array($payload['schema'])) {
        return '';
    }
    return '<script type="application/ld+json" data-server-partner-product-schema="true">' .
        json_encode($payload['schema'], JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES | JSON_INVALID_UTF8_SUBSTITUTE) .
        '</script>';
}

function ceo_market_labels(string $market): array
{
    $labels = [
        'qc' => [
            'title' => 'Boutique partenaire',
            'price' => 'Prix publié',
            'availability' => 'Disponibilité publiée',
            'rating' => 'Note publiée',
            'source' => 'Source partenaire',
            'no_data' => 'Le distributeur ne publie actuellement pas de données Product/Offer/Review/AggregateRating exploitables sur cette page.',
            'updated' => 'Actualisé à chaque chargement de la page.',
        ],
        'dk' => [
            'title' => 'Partnerforhandler',
            'price' => 'Offentliggjort pris',
            'availability' => 'Offentliggjort tilgængelighed',
            'rating' => 'Offentliggjort vurdering',
            'source' => 'Partnerkilde',
            'no_data' => 'Distributøren offentliggør i øjeblikket ikke brugbare Product/Offer/Review/AggregateRating-data på denne side.',
            'updated' => 'Opdateres ved hver sideindlæsning.',
        ],
        'no' => [
            'title' => 'Partnerforhandler',
            'price' => 'Publisert pris',
            'availability' => 'Publisert tilgjengelighet',
            'rating' => 'Publisert vurdering',
            'source' => 'Partnerkilde',
            'no_data' => 'Distributøren publiserer for øyeblikket ikke brukbare Product/Offer/Review/AggregateRating-data på denne siden.',
            'updated' => 'Oppdateres ved hver sideinnlasting.',
        ],
    ];
    return $labels[$market] ?? $labels['qc'];
}

function ceo_market_availability_label(string $availability): string
{
    $availability = strtolower($availability);
    $labels = [
        'https://schema.org/instock' => 'InStock',
        'https://schema.org/outofstock' => 'OutOfStock',
        'https://schema.org/preorder' => 'PreOrder',
        'https://schema.org/backorder' => 'BackOrder',
        'https://schema.org/limitedavailability' => 'LimitedAvailability',
    ];
    return $labels[$availability] ?? $availability;
}

function ceo_market_partner_offer_html(array $payload): string
{
    $market = (string) ($payload['market'] ?? '');
    $labels = ceo_market_labels($market);
    $seller = (string) ($payload['seller'] ?? '');
    $source = (string) ($payload['source_url'] ?? '');
    $hasSchema = ($payload['hasSchema'] ?? false) === true;
    $schema = isset($payload['schema']) && is_array($payload['schema']) ? $payload['schema'] : [];
    $offer = ceo_market_first_object($schema['offers'] ?? []);
    $rating = ceo_market_first_object($schema['aggregateRating'] ?? []);
    $items = [];
    if (!$hasSchema) {
        $body = '<p>' . ceo_market_html($labels['no_data']) . '</p>';
        if ($source !== '') {
            $body .= '<p><a href="' . ceo_market_html($source) . '" target="_blank" rel="noopener noreferrer">' . ceo_market_html($seller ?: parse_url($source, PHP_URL_HOST)) . '</a></p>';
        }
    } else {
        if (isset($offer['price'])) {
            $price = ceo_market_html($offer['price']);
            $currency = isset($offer['priceCurrency']) ? ' ' . ceo_market_html($offer['priceCurrency']) : '';
            $items[] = '<li><span>' . ceo_market_html($labels['price']) . '</span><strong>' . $price . $currency . '</strong></li>';
        }
        if (isset($offer['availability'])) {
            $items[] = '<li><span>' . ceo_market_html($labels['availability']) . '</span><strong>' . ceo_market_html(ceo_market_availability_label((string) $offer['availability'])) . '</strong></li>';
        }
        if (isset($rating['ratingValue'])) {
            $count = $rating['reviewCount'] ?? $rating['ratingCount'] ?? null;
            $countText = $count ? ' (' . ceo_market_html($count) . ')' : '';
            $items[] = '<li><span>' . ceo_market_html($labels['rating']) . '</span><strong>' . ceo_market_html($rating['ratingValue']) . $countText . '</strong></li>';
        }
        if ($source !== '') {
            $items[] = '<li><span>' . ceo_market_html($labels['source']) . '</span><strong><a href="' . ceo_market_html($source) . '" target="_blank" rel="noopener noreferrer">' . ceo_market_html($seller ?: parse_url($source, PHP_URL_HOST)) . '</a></strong></li>';
        }
        $body = $items
            ? '<ul>' . implode('', $items) . '</ul>'
            : '<p>' . ceo_market_html($labels['no_data']) . '</p>';
    }
    return '<section class="partner-offer-panel" aria-label="' . ceo_market_html($labels['title']) . '">' .
        '<p class="eyebrow">' . ceo_market_html($labels['title']) . '</p>' .
        $body .
        '<p class="partner-offer-note">' . ceo_market_html($labels['updated']) . '</p>' .
        '</section>';
}
