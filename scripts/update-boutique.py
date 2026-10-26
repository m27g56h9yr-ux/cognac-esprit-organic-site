#!/usr/bin/env python3
"""Refresh French purchase blocks without rebuilding unrelated site pages."""
from pathlib import Path
import re
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import build_static_site as site


def update():
    for product in site.PRODUCTS:
        path = site.ROOT / "produits" / (product["slug"] + ".html")
        html = path.read_text(encoding="utf-8")
        html = site.sync_product_buy_links(html, product, "fr")
        html = site.sync_css_version(site.sync_js_version(html))
        if product["slug"] == "single-cask":
            html = re.sub(r'<details class="product-details-discreet">[\s\S]*?</details>',
                          lambda _: site.product_details_block(product).strip(), html, count=1)
            # Keep the 70 cl GTIN attached to its own variant, never to the 50 cl.
            generated = site.product_page(product)
            pattern = r'<script type="application/ld\+json">\{"@context":"https://schema.org","@type":"Product"[\s\S]*?</script>'
            schema = re.search(pattern, generated).group(0)
            html = re.sub(pattern, lambda _: schema, html, count=1)
        path.write_text(html, encoding="utf-8")


if __name__ == "__main__":
    update()
