<?php
declare(strict_types=1);

if (!defined('JSON_INVALID_UTF8_SUBSTITUTE')) {
    define('JSON_INVALID_UTF8_SUBSTITUTE', 0);
}

function ceo_json_response(array $payload, int $status = 200): void
{
    http_response_code($status);
    header('Content-Type: application/json; charset=utf-8');
    header('Cache-Control: no-store, no-cache, must-revalidate, max-age=0');
    header('Pragma: no-cache');
    header('Expires: 0');
    echo json_encode($payload, JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES | JSON_INVALID_UTF8_SUBSTITUTE);
    exit;
}

$seedJson = <<<'JSON'
{
  "updatedAt": "4 juillet 2026",
  "updatedAtLabel": "4 juillet 2026",
  "rows": [
    {
      "product_slug": "conviction-vsop",
      "market_key": "qc",
      "market": "Québec",
      "seller": "SAQ",
      "product": "Conviction VSOP",
      "source_url": "https://www.saq.com/fr/15548546",
      "schema_status": "Product JSON-LD détecté",
      "offers": {
        "@type": "Offer",
        "price": "88.25",
        "priceCurrency": "CAD",
        "availability": "https://schema.org/OutOfStock",
        "url": "https://www.saq.com/fr/15548546",
        "itemCondition": "https://schema.org/NewCondition",
        "seller": {
          "@type": "LiquorStore",
          "name": "SAQ"
        }
      },
      "review": null,
      "aggregateRating": {
        "@type": "AggregateRating",
        "ratingValue": "0,0",
        "ratingCount": null,
        "reviewCount": null
      },
      "notes": "Bloc AggregateRating publié par SAQ, mais sans compteur exploitable."
    },
    {
      "product_slug": "xxo",
      "market_key": "qc",
      "market": "Québec",
      "seller": "SAQ",
      "product": "XXO",
      "source_url": "https://www.saq.com/fr/15263655",
      "schema_status": "Product JSON-LD détecté",
      "offers": {
        "@type": "Offer",
        "price": "295.75",
        "priceCurrency": "CAD",
        "availability": "https://schema.org/OutOfStock",
        "url": "https://www.saq.com/fr/15263655",
        "itemCondition": "https://schema.org/NewCondition",
        "seller": {
          "@type": "LiquorStore",
          "name": "SAQ"
        }
      },
      "review": null,
      "aggregateRating": {
        "@type": "AggregateRating",
        "ratingValue": "5,0",
        "ratingCount": "1",
        "reviewCount": "1"
      },
      "notes": "SAQ publie une note agrégée, sans objet Review détaillé détecté."
    },
    {
      "product_slug": "conviction-vsop",
      "market_key": "dk",
      "market": "Danemark",
      "seller": "Vinoble",
      "product": "Conviction VSOP",
      "source_url": "https://vinoble.dk/vare/cognac-conviction-vsop-gb-oeko-40-esprit-organic-maison-des-pierres-gift-box-fins-bois/",
      "schema_status": "Aucun Product/Offer/Review/AggregateRating détecté",
      "offers": null,
      "review": null,
      "aggregateRating": null,
      "notes": "La page expose des données WebPage/Breadcrumb/Image/Organization, mais pas de Product rich result exploitable."
    },
    {
      "product_slug": "transmission-xo",
      "market_key": "dk",
      "market": "Danemark",
      "seller": "Vinoble",
      "product": "Transmission XO",
      "source_url": "https://vinoble.dk/vare/cognac-transmission-xo-gb-oeko-40-esprit-organic-maison-des-pierres-gift-box-fins-bois/",
      "schema_status": "Aucun Product/Offer/Review/AggregateRating détecté",
      "offers": null,
      "review": null,
      "aggregateRating": null,
      "notes": "La page expose des données WebPage/Breadcrumb/Image/Organization, mais pas de Product rich result exploitable."
    },
    {
      "product_slug": "pineau",
      "market_key": "dk",
      "market": "Danemark",
      "seller": "Vinoble",
      "product": "Pineau blanc",
      "source_url": "https://vinoble.dk/vare/pineau-des-charentes-oeko-175-esprit-organic-maison-des-pierres/",
      "schema_status": "Aucun Product/Offer/Review/AggregateRating détecté",
      "offers": null,
      "review": null,
      "aggregateRating": null,
      "notes": "La page expose des données WebPage/Breadcrumb/Image/Organization, mais pas de Product rich result exploitable."
    },
    {
      "product_slug": "conviction-vsop",
      "market_key": "no",
      "market": "Norvège",
      "seller": "Vinmonopolet",
      "product": "Conviction VSOP",
      "source_url": "https://www.vinmonopolet.no/Land/Frankrike/Cognac-Tradisjonell/Fins-Bois/Esprit-Organic-Cognac-Conviction-VSOP/p/15346001",
      "schema_status": "Product JSON-LD détecté",
      "offers": {
        "@type": "Offer",
        "price": 500,
        "priceCurrency": "NOK"
      },
      "review": null,
      "aggregateRating": null,
      "notes": "Offer détectée, sans availability, Review ni AggregateRating dans le JSON-LD publié."
    }
  ]
}
JSON;

$seed = json_decode($seedJson, true);
if (!is_array($seed) || !isset($seed['rows']) || !is_array($seed['rows'])) {
    ceo_json_response(['ok' => false, 'error' => 'Configuration partenaire invalide.'], 500);
}

function ceo_normalize_market($value): string
{
    $normalized = strtolower(trim((string) $value));
    $normalized = preg_replace('/[_\s]+/', '-', $normalized) ?: '';
    $markets = [
        'qc' => 'qc',
        'quebec' => 'qc',
        'québec' => 'qc',
        'ca-qc' => 'qc',
        'dk' => 'dk',
        'danmark' => 'dk',
        'denmark' => 'dk',
        'danemark' => 'dk',
        'no' => 'no',
        'norway' => 'no',
        'norge' => 'no',
        'norvège' => 'no',
        'norvege' => 'no',
        'sj' => 'no',
    ];
    return $markets[$normalized] ?? '';
}

function ceo_request_value(string $key): string
{
    $value = $_GET[$key] ?? '';
    return is_string($value) ? trim($value) : '';
}

function ceo_fetch_url(string $url): array
{
    $userAgent = 'Mozilla/5.0 (compatible; CognacEspritOrganicPartnerSchema/1.0; +https://cognac-esprit-organic.com/)';
    if (function_exists('curl_init')) {
        $ch = curl_init($url);
        curl_setopt_array($ch, [
            CURLOPT_RETURNTRANSFER => true,
            CURLOPT_FOLLOWLOCATION => true,
            CURLOPT_MAXREDIRS => 5,
            CURLOPT_CONNECTTIMEOUT => 5,
            CURLOPT_TIMEOUT => 10,
            CURLOPT_USERAGENT => $userAgent,
            CURLOPT_HTTPHEADER => [
                'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Language: fr-FR,fr;q=0.9,en;q=0.8',
            ],
        ]);
        $body = curl_exec($ch);
        $error = curl_error($ch);
        $httpCode = (int) curl_getinfo($ch, CURLINFO_RESPONSE_CODE);
        curl_close($ch);
        return [
            'ok' => $body !== false && $httpCode >= 200 && $httpCode < 400,
            'body' => $body === false ? '' : (string) $body,
            'httpCode' => $httpCode,
            'error' => $error,
        ];
    }

    $context = stream_context_create([
        'http' => [
            'method' => 'GET',
            'timeout' => 10,
            'ignore_errors' => true,
            'header' => "User-Agent: {$userAgent}\r\nAccept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8\r\nAccept-Language: fr-FR,fr;q=0.9,en;q=0.8\r\n",
        ],
    ]);
    $body = @file_get_contents($url, false, $context);
    $httpCode = 0;
    if (isset($http_response_header) && is_array($http_response_header)) {
        foreach ($http_response_header as $headerLine) {
            if (preg_match('/^HTTP\/\S+\s+(\d{3})/', $headerLine, $match)) {
                $httpCode = (int) $match[1];
            }
        }
    }
    return [
        'ok' => $body !== false && $httpCode >= 200 && $httpCode < 400,
        'body' => $body === false ? '' : (string) $body,
        'httpCode' => $httpCode,
        'error' => $body === false ? 'fetch_failed' : '',
    ];
}

function ceo_is_assoc(array $value): bool
{
    if ($value === []) {
        return false;
    }
    return array_keys($value) !== range(0, count($value) - 1);
}

function ceo_type_matches($type, string $expected): bool
{
    if (is_array($type)) {
        foreach ($type as $item) {
            if (ceo_type_matches($item, $expected)) {
                return true;
            }
        }
        return false;
    }
    if (!is_string($type)) {
        return false;
    }
    $normalized = strtolower(trim($type));
    $expected = strtolower($expected);
    return $normalized === $expected || $normalized === 'https://schema.org/' . $expected;
}

function ceo_find_products($node, array &$products): void
{
    if (!is_array($node)) {
        return;
    }
    if (ceo_is_assoc($node) && isset($node['@type']) && ceo_type_matches($node['@type'], 'Product')) {
        $products[] = $node;
    }
    foreach ($node as $child) {
        ceo_find_products($child, $products);
    }
}

function ceo_json_ld_blocks(string $html): array
{
    $blocks = [];
    if (!preg_match_all('/<script\b([^>]*)>(.*?)<\/script>/is', $html, $matches, PREG_SET_ORDER)) {
        return $blocks;
    }
    foreach ($matches as $match) {
        if (stripos($match[1], 'application/ld+json') === false) {
            continue;
        }
        $json = trim(html_entity_decode($match[2], ENT_QUOTES | ENT_HTML5, 'UTF-8'));
        $json = preg_replace('/^\s*<!--/', '', $json);
        $json = preg_replace('/-->\s*$/', '', $json);
        $decoded = json_decode(trim($json), true);
        if (json_last_error() === JSON_ERROR_NONE && is_array($decoded)) {
            $blocks[] = $decoded;
        }
    }
    return $blocks;
}

function ceo_extract_product(string $html): ?array
{
    $products = [];
    foreach (ceo_json_ld_blocks($html) as $block) {
        ceo_find_products($block, $products);
    }
    usort($products, function (array $a, array $b): int {
        return ceo_product_score($b) <=> ceo_product_score($a);
    });
    return $products[0] ?? null;
}

function ceo_product_score(array $product): int
{
    $score = 0;
    if (array_key_exists('offers', $product) && !ceo_is_empty_schema_value($product['offers'])) {
        $score += 4;
    }
    if (array_key_exists('aggregateRating', $product) && !ceo_is_empty_schema_value($product['aggregateRating'])) {
        $score += 3;
    }
    if (array_key_exists('review', $product) && !ceo_is_empty_schema_value($product['review'])) {
        $score += 2;
    }
    return $score;
}

function ceo_clean_schema_value($value)
{
    if ($value === null || is_bool($value) || is_int($value) || is_float($value) || is_string($value)) {
        return $value;
    }
    if (!is_array($value)) {
        return null;
    }
    $clean = [];
    foreach ($value as $key => $child) {
        $clean[$key] = ceo_clean_schema_value($child);
    }
    return $clean;
}

function ceo_is_empty_schema_value($value): bool
{
    if ($value === null) {
        return true;
    }
    if (is_array($value) && count($value) === 0) {
        return true;
    }
    return false;
}

function ceo_schema_part(array $product, string $key)
{
    return array_key_exists($key, $product) ? ceo_clean_schema_value($product[$key]) : null;
}

function ceo_find_partner_row(array $rows, string $slug, string $market): ?array
{
    foreach ($rows as $row) {
        if (!is_array($row)) {
            continue;
        }
        $rowSlug = (string) ($row['product_slug'] ?? '');
        $rowMarket = ceo_normalize_market($row['market_key'] ?? $row['market'] ?? '');
        if ($rowSlug === $slug && $rowMarket === $market) {
            return $row;
        }
    }
    return null;
}

function ceo_product_page_url(string $slug): string
{
    return 'https://cognac-esprit-organic.com/produits/' . rawurlencode($slug) . '.html';
}

function ceo_partner_schema_from_row(array $row): ?array
{
    $schema = [
        '@context' => 'https://schema.org',
        '@type' => 'Product',
        '@id' => ceo_product_page_url((string) $row['product_slug']) . '#product',
        'name' => (string) $row['product'],
        'brand' => [
            '@type' => 'Brand',
            'name' => 'Cognac Esprit Organic',
            '@id' => 'https://cognac-esprit-organic.com/#brand',
        ],
        'url' => ceo_product_page_url((string) $row['product_slug']),
        'sameAs' => (string) $row['source_url'],
    ];
    $hasPartnerRichData = false;
    foreach (['offers', 'review', 'aggregateRating'] as $key) {
        if (!ceo_is_empty_schema_value($row[$key] ?? null)) {
            $schema[$key] = $row[$key];
            $hasPartnerRichData = true;
        }
    }
    return $hasPartnerRichData ? $schema : null;
}

$slug = ceo_request_value('product');
$market = ceo_normalize_market(ceo_request_value('market'));
if (!preg_match('/^[a-z0-9-]+$/', $slug) || $market === '') {
    ceo_json_response(['ok' => false, 'error' => 'Paramètres product/market invalides.'], 400);
}

$row = ceo_find_partner_row($seed['rows'], $slug, $market);
if ($row === null) {
    ceo_json_response([
        'ok' => false,
        'error' => 'Aucune page partenaire configurée pour ce produit et ce marché.',
        'product' => $slug,
        'market' => $market,
    ], 404);
}

$row['refreshed_at'] = gmdate('c');
$fetch = ceo_fetch_url((string) $row['source_url']);
$row['source_http_code'] = $fetch['httpCode'];
if (!$fetch['ok']) {
    $details = $fetch['httpCode'] ? 'HTTP ' . $fetch['httpCode'] : ($fetch['error'] ?: 'erreur inconnue');
    ceo_json_response([
        'ok' => false,
        'error' => 'Actualisation impossible : ' . $details,
        'product' => $slug,
        'market' => $market,
        'seller' => $row['seller'] ?? '',
        'source_url' => $row['source_url'] ?? '',
        'source_http_code' => $row['source_http_code'],
        'refreshed_at' => $row['refreshed_at'],
    ], 502);
}

$product = ceo_extract_product($fetch['body']);
if ($product === null) {
    $row['refresh_status'] = 'ok';
    $row['schema_status'] = 'Aucun Product/Offer/Review/AggregateRating détecté';
    $row['offers'] = null;
    $row['review'] = null;
    $row['aggregateRating'] = null;
} else {
    $row['refresh_status'] = 'ok';
    $row['schema_status'] = 'Product JSON-LD détecté';
    $row['offers'] = ceo_schema_part($product, 'offers');
    $row['review'] = ceo_schema_part($product, 'review');
    $row['aggregateRating'] = ceo_schema_part($product, 'aggregateRating');
}

$schema = ceo_partner_schema_from_row($row);
ceo_json_response([
    'ok' => true,
    'product' => $slug,
    'market' => $market,
    'seller' => $row['seller'] ?? '',
    'source_url' => $row['source_url'] ?? '',
    'source_http_code' => $row['source_http_code'],
    'refresh_status' => $row['refresh_status'] ?? 'ok',
    'schema_status' => $row['schema_status'] ?? '',
    'hasSchema' => $schema !== null,
    'schema' => $schema,
    'refreshed_at' => $row['refreshed_at'],
]);
