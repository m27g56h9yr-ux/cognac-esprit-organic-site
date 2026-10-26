#!/usr/bin/env python3
"""Guard shop SKU/format/price pairing and the generated public pages."""
import copy
import json
from pathlib import Path
import re
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import boutique
import build_static_site as site


class PurchaseTests(unittest.TestCase):
    def setUp(self):
        self.catalogue = json.loads(boutique.CATALOGUE_PATH.read_text())

    def test_catalogue_matches_published_blocks(self):
        for product in site.PRODUCTS:
            html = (site.ROOT / 'produits' / (product['slug'] + '.html')).read_text()
            block = boutique.purchase_block(product)
            self.assertIn(block, html)
            self.assertEqual(html.count('id="mdp-direct-order"'), int(bool(block)))
            for variant in self.catalogue['products'].get(product['slug'], []):
                self.assertIn('mdp_ref=' + variant['reference'] + '&amp;mdp_lang=fr', block)
                self.assertIn(f'data-shop-volume="{variant["volume_ml"]} ml"', block)
                self.assertIn(f'{variant["price_cents"] // 100},{variant["price_cents"] % 100:02d} €', block)
            for variant in self.catalogue['unavailable'].get(product['slug'], []):
                if variant.get('reference'):
                    self.assertNotIn('mdp_ref=' + variant['reference'], html)
            self.assertEqual(site.sync_product_buy_links(html, product, 'fr'), html)

    def test_missing_verification_or_invalid_price_blocks_build(self):
        p = site.PRODUCTS[0]
        for field in ['source', 'verified_at']:
            broken = copy.deepcopy(self.catalogue)
            broken[field] = None
            with self.assertRaises(ValueError):
                boutique.purchase_block(p, catalogue=broken)
        for value in [-1, 0, 12.50, True]:
            broken = copy.deepcopy(self.catalogue)
            broken['products'][p['slug']][0]['price_cents'] = value
            with self.assertRaises(ValueError):
                boutique.purchase_block(p, catalogue=broken)

    def test_single_cask_50cl_does_not_inherit_70cl_gtin(self):
        html = (site.ROOT / 'produits/single-cask.html').read_text()
        objects = [json.loads(s) for s in re.findall(r'<script type="application/ld\+json">(.*?)</script>', html)]
        product = next(o for o in objects if o.get('@type') == 'Product')
        self.assertEqual(product['size'], '500 ml')
        self.assertNotIn('gtin13', product)
        original = next(v for v in product['hasVariant'] if v['size'] == '700 ml')
        self.assertEqual(original['gtin13'], '3322870011458')

    def test_disabled_and_international_catalogue(self):
        self.assertEqual(boutique.purchase_block(site.PRODUCTS[0], catalogue={'enabled': False}), '')
        self.assertEqual(boutique.purchase_block(site.PRODUCTS[0], 'da'), '')


if __name__ == '__main__':
    unittest.main()
