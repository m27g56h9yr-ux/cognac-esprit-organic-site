<?php
require __DIR__.'/mdp-catalogue-lib.php';
$routes=json_decode('{"/produits/transmission-xo.html":"produits/transmission-xo.html","/produits/conviction-vsop.html":"produits/conviction-vsop.html","/produits/cohesion-napoleon.html":"produits/cohesion-napoleon.html","/produits/fondation-vs.html":"produits/fondation-vs.html","/produits/pineau-rouge.html":"produits/pineau-rouge.html","/produits/xxo.html":"produits/xxo.html","/produits/single-cask.html":"produits/single-cask.html","/produits/pineau.html":"produits/pineau.html"}',true);
$path=parse_url($_SERVER['REQUEST_URI']??'',PHP_URL_PATH);
if(!is_string($path)||!isset($routes[$path])){http_response_code(404);exit('Page introuvable');}
if(($_SERVER['REQUEST_METHOD']??'GET')!=='GET' && ($_SERVER['REQUEST_METHOD']??'')!=='HEAD'){http_response_code(405);header('Allow: GET, HEAD');exit;}
$html=file_get_contents(dirname(__DIR__).'/'.$routes[$path]);
try{$catalogue=mdp_catalogue_fetch('eo');}catch(Throwable){$catalogue=null;}
header('Content-Type: text/html; charset=UTF-8');header('Cache-Control: no-cache, max-age=0');
header('X-MDP-Catalogue: '.($catalogue?'fresh':'unavailable'));
echo mdp_catalogue_render($html,$catalogue,'https://cognac-esprit-organic.com'.$path,'eo');
