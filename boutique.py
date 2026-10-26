"""Static purchase blocks, populated only from the verified shop catalogue."""
from html import escape
import json
from pathlib import Path
import re
from urllib.parse import urlencode

CATALOGUE_PATH = Path(__file__).resolve().parent / "data/boutique.json"
BLOCK_RE = re.compile(r'\n?<!-- eo-shop-start -->[\s\S]*?<!-- eo-shop-end -->')
COPY = {
    "fr": ("Acheter", "TTC", "Vendu par Maison des Pierres."),
    "en": ("Buy", "incl. VAT", "Sold by Maison des Pierres. Delivery in mainland France; shipping calculated in the shop."),
    "da": ("Køb", "inkl. moms", "Sælges af Maison des Pierres. Levering i det franske fastland; fragt beregnes i butikken."),
    "no": ("Kjøp", "inkl. mva.", "Selges av Maison des Pierres. Levering i det franske fastlandet; frakt beregnes i nettbutikken."),
    "sv": ("Köp", "inkl. moms", "Säljs av Maison des Pierres. Leverans inom det franska fastlandet; frakt beräknas i butiken."),
}


def purchase_block(product, lang="fr", catalogue=None):
    if lang != "fr":
        return ""
    if catalogue is None:
        catalogue = json.loads(CATALOGUE_PATH.read_text(encoding="utf-8"))
    if not catalogue.get("enabled"):
        return ""
    if not catalogue.get("verified_at") or not catalogue.get("source"):
        raise ValueError("Le catalogue boutique doit avoir une source et une date de vérification.")
    variants = catalogue["products"].get(product["slug"], [])
    if not variants:
        return ""
    buy, tax, note = COPY.get(lang, COPY["en"])
    rows = []
    seen = set()
    for variant in variants:
        code, volume, cents = variant["reference"], variant["volume_ml"], variant["price_cents"]
        if not isinstance(code, str) or not re.fullmatch(r"[A-Z0-9_-]+", code):
            raise ValueError("Référence boutique invalide")
        if type(cents) is not int or cents <= 0 or type(volume) is not int or volume <= 0:
            raise ValueError("Prix TTC et contenance doivent être des entiers positifs")
        if code in seen:
            raise ValueError("Référence boutique dupliquée")
        seen.add(code)
        url = "https://boutique.mdpierre.com/commander/?" + urlencode({"mdp_ref": code, "mdp_lang": lang})
        price = f"{cents // 100},{cents % 100:02d} €"
        size = f"{volume / 10:g} cl"
        label = f"{buy} {product['name']} — {size} — {price} {tax}"
        rows.append(
            f'<div class="eo-shop-row" data-shop-volume="{volume} ml">'
            f'<span>{escape(size)}</span><strong>{escape(price)} <small>{escape(tax)}</small></strong>'
            f'<a href="{escape(url, quote=True)}" aria-label="{escape(label, quote=True)}">{escape(buy)}</a>'
            '</div>'
        )
    return ('\n<!-- eo-shop-start -->\n<section id="mdp-direct-order" class="eo-shop" aria-label="' + escape(buy, quote=True) + '">'
            + ''.join(rows) + '<p data-shop-unavailable hidden role="status">Ce format n’est pas encore disponible en ligne.</p><p>' + escape(note) + '</p></section>\n<!-- eo-shop-end -->')


def purchase_offers(product, lang="fr"):
    """Match the visible verified prices; never invent live stock or delivery rates."""
    if not purchase_block(product, lang):
        return []
    catalogue = json.loads(CATALOGUE_PATH.read_text(encoding="utf-8"))
    return [{"@type": "Offer", "sku": v["reference"],
             "url": "https://boutique.mdpierre.com/commander/?" + urlencode({"mdp_ref": v["reference"], "mdp_lang": lang}),
             "price": f'{v["price_cents"] / 100:.2f}', "priceCurrency": "EUR",
             "seller": {"@type": "Organization", "name": "Maison des Pierres", "url": "https://mdpierre.com/"},
             "eligibleRegion": {"@type": "Place", "name": "France métropolitaine"},
             "itemCondition": "https://schema.org/NewCondition"}
            for v in catalogue["products"].get(product["slug"], [])]
