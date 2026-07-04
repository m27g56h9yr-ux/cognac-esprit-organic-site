<?php
declare(strict_types=1);

function ceo_normalize_market(?string $value): string
{
    $value = strtolower(trim((string)$value));
    $value = str_replace(['_', ' '], '-', $value);

    $markets = [
        'qc' => 'qc',
        'quebec' => 'qc',
        'ca-qc' => 'qc',
        'dk' => 'dk',
        'danmark' => 'dk',
        'denmark' => 'dk',
        'no' => 'no',
        'norway' => 'no',
        'norge' => 'no',
        'sj' => 'no',
    ];

    return $markets[$value] ?? '';
}

function ceo_first_server_value(array $keys): string
{
    foreach ($keys as $key) {
        if (!empty($_SERVER[$key])) {
            return trim((string)$_SERVER[$key]);
        }
    }
    return '';
}

function ceo_detect_market(): array
{
    $directMarket = ceo_first_server_value([
        'HTTP_X_CEO_MARKET',
        'HTTP_X_MARKET',
        'HTTP_X_GEO_MARKET',
        'REDIRECT_CEO_MARKET',
        'CEO_MARKET',
    ]);
    $market = ceo_normalize_market($directMarket);
    if ($market !== '') {
        return ['market' => $market, 'source' => 'direct-market-header'];
    }

    $country = strtoupper(ceo_first_server_value([
        'HTTP_CF_IPCOUNTRY',
        'HTTP_X_COUNTRY_CODE',
        'HTTP_X_GEOIP_COUNTRY',
        'HTTP_X_GEO_COUNTRY',
        'GEOIP_COUNTRY_CODE',
        'COUNTRY_CODE',
        'MM_COUNTRY_CODE',
    ]));
    $region = strtoupper(ceo_first_server_value([
        'HTTP_CF_REGION_CODE',
        'HTTP_X_REGION_CODE',
        'HTTP_X_GEOIP_REGION',
        'HTTP_X_GEO_REGION',
        'HTTP_CLOUDFRONT_VIEWER_COUNTRY_REGION',
        'GEOIP_REGION',
        'REGION_CODE',
    ]));

    if ($country === 'DK') {
        return ['market' => 'dk', 'source' => 'country'];
    }
    if ($country === 'NO' || $country === 'SJ') {
        return ['market' => 'no', 'source' => 'country'];
    }
    if ($country === 'CA' && ($region === 'QC' || $region === 'QUEBEC')) {
        return ['market' => 'qc', 'source' => 'country-region'];
    }

    return ['market' => '', 'source' => 'none'];
}

$result = ceo_detect_market();
$format = strtolower((string)($_GET['format'] ?? 'js'));

header('Cache-Control: private, no-store, max-age=0');
header('Vary: CF-IPCountry, X-CEO-Market, X-Market, X-Geo-Country, X-Geo-Region, X-Country-Code, X-Region-Code');

if ($format === 'json') {
    header('Content-Type: application/json; charset=utf-8');
    echo json_encode(['ok' => true] + $result, JSON_UNESCAPED_SLASHES);
    exit;
}

header('Content-Type: application/javascript; charset=utf-8');
echo 'window.CEO_SERVER_MARKET=' . json_encode($result['market']) . ';' . "\n";
echo 'window.CEO_SERVER_MARKET_SOURCE=' . json_encode($result['source']) . ';' . "\n";
echo 'document.documentElement.dataset.serverMarket=' . json_encode($result['market']) . ';' . "\n";
