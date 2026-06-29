from html import escape
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DOMAIN = "https://cognac-esprit-organic.com"
NOINDEX = False

CONTACT = {
    "email": "Cognac@mdpierre.com",
    "phone": "+33 5 45 35 88 10",
    "address": "30 Rue d'Angoulême, 16200 Triac-Lautrait, France",
}

AWARD_PROOF_URLS = {
    "fondation-vs-sfwsc-2019": "https://web.archive.org/web/20200630220024/http://www.sfspiritscomp.com/wp-content/uploads/2020/04/2019-SFWSC-RESULTS-BY-BRAND.pdf",
    "transmission-xo-wwsa-2022": "https://wineawards.org/womens-wine-spirits-awards-2022-results/",
    "pineau-blanc-cmb-2025": "https://resultats.concoursmondial.com/fr/resultats/2025/240534-pineau-des-charentes-esprit-organic-2011",
}

PRODUCTS = [
    {
        "name": "Fondation VS",
        "slug": "fondation-vs",
        "short": "Cognac biologique jeune, fruité et expressif, pensé pour une lecture directe du fruit.",
        "en_short": "A young, fruity and expressive organic Cognac with a direct fruit-forward profile.",
        "notes": ["Poire", "Pêche", "Brioche", "Vanille"],
        "category": "Cognac VS",
        "image": "assets/img/products/fondation-vs.jpg",
        "scene": "assets/img/product-scenes/fondation-01.jpg",
        "menu": "assets/img/product-menu/vs.png",
        "tone": "#704019",
        "volume": "700 ml",
        "abv": "40 % vol",
        "grapes": "Ugni Blanc, Colombard, Folle Blanche",
    },
    {
        "name": "Conviction VSOP",
        "slug": "conviction-vsop",
        "short": "Cognac biologique rond et gourmand, avec une expression souple des fruits confits, du bois et des épices.",
        "en_short": "A rounded and generous organic Cognac, expressing candied fruit, warm oak and spice.",
        "notes": ["Fruits confits", "Vanille", "Bois chaud", "Épices"],
        "category": "Cognac VSOP",
        "image": "assets/img/products/conviction-vsop.jpg",
        "scene": "assets/img/product-scenes/conviction-01.jpg",
        "menu": "assets/img/product-menu/vsop.png",
        "tone": "#5e3d23",
        "volume": "700 ml",
        "abv": "40 % vol",
        "grapes": "Ugni Blanc, Colombard, Folle Blanche",
    },
    {
        "name": "Cohesion Napoléon",
        "slug": "cohesion-napoleon",
        "short": "Cognac biologique équilibré, long et poivré, autour des fruits secs et d'une finale mentholée.",
        "en_short": "A balanced organic Cognac with length, peppery notes, dried fruit and a fresh finish.",
        "notes": ["Fruits secs", "Bois chaud", "Poivre", "Finale mentholée"],
        "category": "Cognac Napoléon",
        "image": "assets/img/products/cohesion-napoleon.jpg",
        "scene": "assets/img/products/cohesion-napoleon.jpg",
        "menu": "assets/img/product-menu/napoleon.png",
        "tone": "#895006",
        "volume": "700 ml",
        "abv": "40 % vol",
        "grapes": "Ugni Blanc, Colombard, Folle Blanche",
    },
    {
        "name": "Transmission XO",
        "slug": "transmission-xo",
        "short": "Cognac biologique structuré et généreux, marqué par la cerise noire, les fleurs séchées et le rancio.",
        "en_short": "A structured and generous organic Cognac with black cherry, dried flowers and rancio notes.",
        "notes": ["Cerise noire", "Fleurs séchées", "Rancio", "Structure"],
        "category": "Cognac XO",
        "image": "assets/img/products/transmission-xo.jpg",
        "scene": "assets/img/product-scenes/transmission-01.jpg",
        "tasting_image": "assets/img/tasting/xo.jpg",
        "menu": "assets/img/product-menu/xo.png",
        "tone": "#513213",
        "volume": "700 ml",
        "abv": "40 % vol",
        "grapes": "Ugni Blanc, Colombard, Folle Blanche",
    },
    {
        "name": "XXO",
        "slug": "xxo",
        "short": "Premier XXO en agriculture biologique, doux, structuré et très fruité.",
        "en_short": "Presented as the first XXO in organic agriculture, soft, structured and fruit-forward.",
        "notes": ["Doux", "Structuré", "Très fruité", "Plus jeune eau-de-vie 14 ans"],
        "category": "Cognac XXO",
        "image": "assets/img/products/xxo.jpg",
        "scene": "assets/img/product-scenes/xxo-01.jpg",
        "detail_image": "assets/img/products/xxo.jpg",
        "tasting_image": "assets/img/product-scenes/xxo-01.jpg",
        "menu": "assets/img/product-menu/xxo.png",
        "tone": "#49321e",
        "volume": "700 ml",
        "abv": "43,5 % vol",
        "grapes": "Ugni Blanc, Colombard, Folle Blanche",
    },
    {
        "name": "Single Cask",
        "slug": "single-cask",
        "short": "Édition limitée, 51 %, sélectionnée par Fanny.",
        "en_short": "Limited edition, 51%, selected by Fanny.",
        "notes": ["Édition limitée", "51 %", "Sélectionné par Fanny"],
        "category": "Cognac Single Cask",
        "image": "assets/img/products/single-cask.jpg",
        "scene": "assets/img/product-scenes/single-cask-01.jpg",
        "detail_image": "assets/img/products/single-cask.jpg",
        "tasting_image": "assets/img/product-scenes/single-cask-01.jpg",
        "menu": "assets/img/product-menu/single-cask.png",
        "tone": "#522e03",
        "volume": "700 ml",
        "abv": "51 % vol",
        "grapes": "Ugni Blanc, Colombard, Folle Blanche",
    },
    {
        "name": "Pineau blanc",
        "slug": "pineau",
        "short": "Pineau blanc des Charentes biologique élaboré avec Colombard et Ugni Blanc, sans sulfites ajoutés.",
        "en_short": "Organic white Pineau des Charentes made with Colombard and Ugni Blanc, with no added sulphites.",
        "notes": ["Pineau des Charentes", "Colombard", "Ugni Blanc", "Sans sulfites ajoutés"],
        "category": "Pineau des Charentes blanc",
        "image": "assets/img/products/pineau.jpg",
        "scene": "assets/img/product-scenes/pineau-01.jpg",
        "detail_image": "assets/img/products/pineau.jpg",
        "tasting_image": "assets/img/product-scenes/pineau-01.jpg",
        "menu": "assets/img/product-menu/pineau.png",
        "tone": "#6b4d13",
        "volume": "750 ml",
        "abv": "17,5 % vol",
        "grapes": "Ugni Blanc, Colombard, Folle Blanche",
    },
    {
        "name": "Pineau rouge",
        "slug": "pineau-rouge",
        "short": "Pineau des Charentes rouge issu de Merlot et d'Ugni Blanc, avec une expression fruitée, souple et gourmande.",
        "en_short": "Red Pineau des Charentes made with Merlot and Ugni Blanc, with a supple, generous fruit expression.",
        "notes": ["Merlot", "Ugni Blanc", "Fruits rouges", "Souple"],
        "category": "Pineau des Charentes rouge",
        "image": "assets/img/products/pineau-rouge.png",
        "scene": "assets/img/products/pineau-rouge-scene-floral-clean.png",
        "detail_image": "assets/img/products/pineau-rouge-scene-floral-clean.png",
        "tasting_image": "assets/img/old-site/img_pineau_degustation.jpg",
        "menu": "assets/img/product-menu/pineau-rouge.png?v=20260612-menu03",
        "tone": "#6b4d13",
        "volume": "750 ml",
        "abv": "17,5 % vol",
        "grapes": "Merlot, Ugni Blanc",
    },
]

PRODUCT_TRADE_PDFS = {
    "fondation-vs": {
        "href": "assets/pdf/fiches-degustation/cognac-esprit-organic-fondation-vs-fiche-degustation.pdf",
        "localized_hrefs": {
            "fr": "assets/pdf/fiches-degustation/cognac-esprit-organic-fondation-vs-fiche-degustation.pdf",
            "en": "assets/pdf/fiches-degustation/cognac-esprit-organic-fondation-vs-fiche-degustation-en.pdf",
            "da": "assets/pdf/fiches-degustation/cognac-esprit-organic-fondation-vs-fiche-degustation-da.pdf",
            "no": "assets/pdf/fiches-degustation/cognac-esprit-organic-fondation-vs-fiche-degustation-no.pdf",
            "sv": "assets/pdf/fiches-degustation/cognac-esprit-organic-fondation-vs-fiche-degustation-sv.pdf",
        },
        "label": "Fiche dégustation Fondation VS",
        "en_label": "Fondation VS tasting sheet",
    },
    "conviction-vsop": {
        "href": "assets/pdf/fiches-degustation/cognac-esprit-organic-conviction-vsop-fiche-degustation.pdf",
        "localized_hrefs": {
            "fr": "assets/pdf/fiches-degustation/cognac-esprit-organic-conviction-vsop-fiche-degustation.pdf",
            "en": "assets/pdf/fiches-degustation/cognac-esprit-organic-conviction-vsop-fiche-degustation-en.pdf",
            "da": "assets/pdf/fiches-degustation/cognac-esprit-organic-conviction-vsop-fiche-degustation-da.pdf",
            "no": "assets/pdf/fiches-degustation/cognac-esprit-organic-conviction-vsop-fiche-degustation-no.pdf",
            "sv": "assets/pdf/fiches-degustation/cognac-esprit-organic-conviction-vsop-fiche-degustation-sv.pdf",
        },
        "label": "Fiche dégustation Conviction VSOP",
        "en_label": "Conviction VSOP tasting sheet",
    },
    "cohesion-napoleon": {
        "href": "assets/pdf/fiches-degustation/cognac-esprit-organic-cohesion-napoleon-fiche-degustation.pdf",
        "localized_hrefs": {
            "fr": "assets/pdf/fiches-degustation/cognac-esprit-organic-cohesion-napoleon-fiche-degustation.pdf",
            "en": "assets/pdf/fiches-degustation/cognac-esprit-organic-cohesion-napoleon-fiche-degustation-en.pdf",
            "da": "assets/pdf/fiches-degustation/cognac-esprit-organic-cohesion-napoleon-fiche-degustation-da.pdf",
            "no": "assets/pdf/fiches-degustation/cognac-esprit-organic-cohesion-napoleon-fiche-degustation-no.pdf",
            "sv": "assets/pdf/fiches-degustation/cognac-esprit-organic-cohesion-napoleon-fiche-degustation-sv.pdf",
        },
        "label": "Fiche dégustation Cohesion Napoléon",
        "en_label": "Cohesion Napoléon tasting sheet",
    },
    "transmission-xo": {
        "href": "assets/pdf/fiches-degustation/cognac-esprit-organic-transmission-xo-fiche-degustation.pdf",
        "localized_hrefs": {
            "fr": "assets/pdf/fiches-degustation/cognac-esprit-organic-transmission-xo-fiche-degustation.pdf",
            "en": "assets/pdf/fiches-degustation/cognac-esprit-organic-transmission-xo-fiche-degustation-en.pdf",
            "da": "assets/pdf/fiches-degustation/cognac-esprit-organic-transmission-xo-fiche-degustation-da.pdf",
            "no": "assets/pdf/fiches-degustation/cognac-esprit-organic-transmission-xo-fiche-degustation-no.pdf",
            "sv": "assets/pdf/fiches-degustation/cognac-esprit-organic-transmission-xo-fiche-degustation-sv.pdf",
        },
        "label": "Fiche dégustation Transmission XO",
        "en_label": "Transmission XO tasting sheet",
    },
}

NAV = [
    ("produits/transmission-xo.html", "La gamme", "The range"),
    ("production/", "La maison", "The house"),
    ("visiter.html", "Visiter", "Visit"),
]

PRODUCT_EXTRAS = {
    "fondation-vs": {
        "legacy_url": "fondation-vs",
        "gallery_color": "#eae7da",
        "detail_image": "assets/img/old-site/VS-FONDATION.jpg",
        "tasting_image": "assets/img/old-site/img_degustation_vs.jpg",
        "story": "Je dédie FONDATION à ma grand-mère Germaine, pionnière de la famille, qui me répétait sans cesse : Ce patrimoine est solide car il est sain, la terre n’a pas besoin d’autre chose que le travail de l’homme et ses connaissances. Les produits chimiques ne sont pas nécessaires pour que la vigne pousse et produise. C’est ce discours impactant qui m’a poussé à crée cette marque.",
        "degustation_text": "FONDATION se caractérise par une belle fraîcheur en bouche des notes fruitées de poire et de pêche ou encore de fleur de vigne. Les premiers tannins du bois révèlent des arômes briochés. Idéal pour réaliser des cocktails ou être consommé sur glace.",
        "sensory": {
            "Bouche": "Bois de chêne, brioche, fleur de vigne, pêche, poire, vanille",
            "Couleur": "Jaune or, jaune paille",
            "Nez": "Arômes de fruits frais tels que poire, pêche et fruits compotés (pommes au four et raisins secs dorés)",
            "Palais": "Subtil mélange de fraîcheur et de fruité suivi par la rondeur de notes briochées et vanillées",
            "Finale": "Fraîcheur fruitée de raisin frais et de poire",
        },
        "medals": [
            {
                "src": "assets/img/old-site/img_prod_fondation_medaile.png",
                "href": AWARD_PROOF_URLS["fondation-vs-sfwsc-2019"],
                "label": "résultats officiels 2019 du San Francisco World Spirits Competition pour Fondation VS",
            }
        ],
        "gallery": ["assets/img/old-site/img_prod_fondation_02.jpg"],
        "colors": ["#557647", "#4e6a3f", "#628552"],
        "accent": "#a3b541",
    },
    "conviction-vsop": {
        "legacy_url": "conviction",
        "gallery_color": "#eae7da",
        "detail_image": "assets/img/old-site/VSOP-CONVICTION.jpg",
        "tasting_image": "assets/img/old-site/cocktail_vsop.jpg",
        "story": "Fanny et moi-même sommes convaincus qu’un « mieux produire » est la meilleure solution pour préserver notre vignoble et nous permettre de continuer à travailler de manière passionnée dans le respect de la terre. CONVICTION c’est un hommage à notre vision d’une vie saine, d’un bon sens paysan mais aussi à notre alliance dans le travail et dans la vie.",
        "degustation_text": "CONVICTION est un cognac rond et gourmand. Les premières années en fûts lui confèrent des notes de fruits confits et de vanille. On y trouve en bouche des notes de fruits secs, de bois chaud et d’épices. CONVICTION offre une finale fraîche de clou de girofle.",
        "sensory": {
            "Bouche": "Abricot sec, clou de girofle, prune, rose, vanille",
            "Couleur": "Jaune doré",
            "Nez": "Équilibré et rond : bois de chêne et de vanille. Subtile touche de fruits compotés (pruneau, abricot).",
            "Palais": "Riche et ample avec un beau caractère fruité typique du cru Fins Bois",
            "Finale": "Fraîche, clou de girofle",
        },
        "medals": ["assets/img/old-site/vsop-1.png"],
        "gallery": ["assets/img/old-site/img_prod_conviction_02.jpg"],
        "colors": ["#87833a", "#76722e", "#938a3c"],
        "accent": "#d1c864",
    },
    "cohesion-napoleon": {
        "legacy_url": "cohesion",
        "gallery_color": "#eae7da",
        "detail_image": "assets/img/old-site/NAPO-COHESION.jpg",
        "tasting_image": "assets/img/old-site/img_degustation_xo.jpg",
        "story": "La réussite de cette gamme tient aussi dans la force dont chacun d’entre nous a su faire preuve. Mon grand-père Marc et son frère Roger, ma grand-mère Germaine et mes parents Pierre et Eliane ont largement contribué à l’aboutissement de cet engagement dans l’agriculture biologique. C’est un travail d’équipe qui remonte à plusieurs générations. COHESION leur rend hommage.",
        "degustation_title": "Une finale masculine, équilibrée, légèrement poivrée et mentholée",
        "degustation_text": "Un vieillissement généreux en barriques lui confère de belles notes de fruits secs (cacahuète, amande, noisette) et de bois chaud et d’épices. Finale longue et poivrée.",
        "sensory": {
            "Bouche": "Amande, bois chaud légèrement vanillé, cacahouète, noisette, poire, toffee",
            "Couleur": "Jaune orangé",
            "Nez": "Un vieillissement en barrique laissant apparaitre les premières notes boisées et vanillées.",
            "Palais": "De fins tanins de chêne se lient aux notes de fruits secs : amande, noisette et noix",
            "Finale": "Masculine, équilibrée, légèrement poivrée et mentholée",
        },
        "medals": ["assets/img/old-site/Sans-titre-15.png"],
        "gallery": ["assets/img/old-site/img_prod_cohesion_02.jpg"],
        "colors": ["#ba762b", "#a46925", "#bc8131"],
        "accent": "#f9bd63",
    },
    "transmission-xo": {
        "legacy_url": "transmission",
        "gallery_color": "#eae7da",
        "detail_image": "assets/img/old-site/XO-TRANSMISSION.jpg",
        "tasting_image": "assets/img/old-site/img_fanny.jpg",
        "story": "Le respect de l’environnement doit être un des engagements majeurs des générations futures. Quelle terre allons-nous laisser à nos enfants demain ? J’aimerai dédier ce cognac aux générations à venir et à mes enfants plus particulièrement. La transmission symbolise pour moi le fruit d’un travail soigné et consciencieux d’une génération prête à passer le relai à la suivante. Nous ne sommes que des passeurs.",
        "degustation_title": "Structurée avec une belle rondeur en bouche",
        "degustation_text": "De nombreuses années de vieillissement ont été nécessaires pour élaborer TRANSMISSION. On y trouve en bouche des notes fruitées (cerise noire) et fleuries (fleurs séchées). Les premières notes du rancio apparaissent en finale.",
        "sensory": {
            "Bouche": "Bois, cannelle, gingembre confit, pruneau, tabac, vanille",
            "Couleur": "Ambre doré",
            "Nez": "Complexe de fruits (cerise noire) accompagné de notes fleuries (fleurs sauvages) et de quelques épices chaudes. Avec le temps, les arômes évoluent vers des notes de fruits confits et d'épices et de vieux bois",
            "Palais": "Explosion de saveurs et d'arômes épicés",
            "Finale": "Épicée de noix de muscade et de cannelle. Le rancio apparait en finale et mentholée",
        },
        "medals": [
            {
                "src": "assets/img/old-site/img_prod_fondation_medaille_02.png",
                "href": AWARD_PROOF_URLS["transmission-xo-wwsa-2022"],
                "label": "preuve de la récompense Women's Wine & Spirits Awards pour Transmission XO",
            }
        ],
        "gallery": ["assets/img/old-site/img_prod_transmission_02.jpg", "assets/img/old-site/img_prod_transmission_03.jpg"],
        "colors": ["#c78d0b", "#b9780e", "#d09a25"],
        "accent": "#f9d872",
    },
    "xxo": {
        "legacy_url": "xxo",
        "gallery_color": "#ebe8da",
        "detail_image": "assets/img/old-site/XXO-scaled.jpg",
        "tasting_image": "assets/img/old-site/img_XXO_leopold.jpg",
        "story": "Nous sommes très fiers de présenter le Premier XXO en agriculture Biologique. Ce cognac est issu d’un assemblage d’eaux de vie dont la plus jeune à 14 ans. C’est un cognac structuré, très fruité. Les eaux de vie qui composent ce XXO ont vieilli dans des barriques neuves de chêne de gros grains type Limousin.",
        "degustation_title": "Rondeur, douceur et délicatesse",
        "degustation_text": "Après une extraction tannique de quelques années, elles ont terminé de vieillir dans des barriques rousses, dans les chais humides du domaine familial. Ce type d’environnement offre aux eaux de vie de la rondeur et de la douceur. C’est cette douceur qui nous a permis conserver son titre à 43,5% plutôt que 40%. Nous évitons ainsi toutes dilution excessive des arômes délicats qui le composent. Léopold CROIZET",
        "sensory": {
            "Bouche": "Cannelle, tabac et fleurs séchées, fruits confits",
            "Couleur": "Ambrée, aux reflets dorés",
            "Nez": "Notes explosives de fruits confits et compotées, d’épices douces de cannelle",
            "Palais": "C’est un cognac rond et riche, structuré",
            "Finale": "Finale fraiche, notes de réglisse",
        },
        "medals": ["assets/img/old-site/img_deco_xxo.png"],
        "gallery": [],
        "colors": ["#cd9a22", "#be831d", "#d7a72f"],
        "accent": "#ffe475",
    },
    "single-cask": {
        "legacy_url": "single-cask",
        "gallery_color": "#ebe4da",
        "detail_image": "assets/img/old-site/SINGLE-CASK.jpg",
        "tasting_image": "assets/img/old-site/SINGLE-CASK_tonneau.jpg",
        "story": "Proposé en édition limitée ce brut de fût a été sélectionné par Fanny notre maitre de chai pour ses qualités propres et son fort potentiel aromatique. Les eaux de vie de ce millésime exceptionnel ont débuté leur vieillissement en barriques neuves de chêne français sur un mix de grains. Elles ont ensuite fini de se « patiner » dans nos vieilles barriques rousses afin que le temps œuvre et que la magie de l’oxydation et de l’évaporation opère. Cet échange, obtenu après de longues années de vieillissement offre un résultat exceptionnel : une palette aromatique fondue, harmonieuse et riche !",
        "degustation_title": "Naturellement boisé",
        "degustation_text": "Une seule barrique a été retenue pour l’incroyable richesse aromatique qu’elle dégageait et pour la douceur de ses parfums. Elle n’a subi aucune adjonction de boisé ni de sucre et a subi une réduction douce et régulière d’eau distillée afin d’amener le cognac à un vieillissement final de 52%. Ce premier Single Cask est déjà une belle réussite, titrant à 51%.",
        "sensory": {
            "Bouche": "Tabac et fleurs séchées, fruits confits",
            "Couleur": "Ambre foncée, aux reflets rouges",
            "Nez": "Notes intense d’orange confite et de gingembre, de pruneaux. On y retrouve également des notes de clou de girofle",
            "Palais": "C’est un cognac fort, épicé, les fruits confits sont très présents",
            "Finale": "Finale fraiche de clou de girofle",
        },
        "medals": ["assets/img/old-site/img_deco_singlecask-1.png"],
        "gallery": [],
        "colors": ["#cd7522", "#be601d", "#d7822f"],
        "accent": "#ffc675",
    },
    "pineau": {
        "legacy_url": "pineau",
        "gallery_color": "#eae7db",
        "detail_image": "assets/img/old-site/visuel_pineau.jpg",
        "tasting_image": "assets/img/old-site/img_pineau_degustation.jpg",
        "degustation_text": "Ce pineau blanc des Charentes est élaboré à partir d’un assemblage d'eaux-de-vie de cognac et de moût de raisins issus de nos cépages de Colombard et d'Ugni Blanc. Il a vieilli pendant de nombreuses années en fûts de chêne, ce qui lui donne sa couleur ambrée et brillante. On retrouve en bouche des notes de fruits confits et de vanille. C’est un pineau riche et gourmand, bien structuré avec des notes intenses et harmonieuses.",
        "sensory": {
            "Bouche": "Brioche, jus de raisin frais, poire, pruneau, vanille",
            "Couleur": "Jaune or, jaune paille, brillant",
            "Nez": "Élaboré, équilibré. Belle association de notes fruitées (raisins frais, poire) et vanillées",
            "Palais": "Riche, gourmand, complexe",
            "Finale": "Fruité, intense, gourmand",
        },
        "medals": ["assets/img/old-site/deco_pineau-1.png"],
        "gallery": ["assets/img/old-site/visuel_pineau_02.jpg"],
        "colors": ["#565083", "#3e3b59", "#6e6baf"],
        "accent": "#ecb038",
    },
    "pineau-rouge": {
        "legacy_url": "pineau-rouge",
        "gallery_color": "#eae7db",
        "detail_image": "assets/img/products/pineau-rouge-scene-floral-clean.png",
        "tasting_image": "assets/img/old-site/img_pineau_degustation.jpg",
        "story": "Ce Pineau rouge prolonge l'esprit de la gamme Esprit Organic dans un registre plus coloré : une bouche ronde, fraîche et fruitée, pensée pour l'apéritif, les desserts aux fruits ou un service légèrement rafraîchi.",
        "degustation_text": "Ce Pineau rouge des Charentes est élaboré à partir de Merlot et d'Ugni Blanc. Il présente une robe rouge profonde et brillante. Le nez évoque les fruits rouges mûrs, la cerise et une touche de prune. La bouche est souple, ample et gourmande, avec une finale fruitée et légèrement épicée.",
        "sensory": {
            "Bouche": "Fruits rouges mûrs, cerise, prune, douceur du raisin",
            "Couleur": "Rouge profond, reflets rubis, brillant",
            "Nez": "Fruité et gourmand, autour de la cerise, de la mûre et des fruits rouges confits",
            "Palais": "Souple, rond, fruité, avec une belle fraîcheur",
            "Finale": "Gourmande, fruitée, légèrement épicée",
        },
        "gallery": ["assets/img/products/pineau-rouge-label.png"],
        "colors": ["#565083", "#3e3b59", "#6e6baf"],
        "accent": "#ecb038",
    },
}

DOCUMENTED_AWARDS = {
    "fondation-vs": {
        "name": "San Francisco World Spirits Competition 2019",
        "en_name": "San Francisco World Spirits Competition 2019",
        "proof_label": "Résultats officiels 2019 du San Francisco World Spirits Competition",
        "en_proof_label": "Official 2019 San Francisco World Spirits Competition results",
        "url": AWARD_PROOF_URLS["fondation-vs-sfwsc-2019"],
    },
    "transmission-xo": {
        "name": "Women's Wine & Spirits Awards 2022",
        "en_name": "Women's Wine & Spirits Awards 2022",
        "proof_label": "Résultats Women's Wine & Spirits Awards 2022",
        "en_proof_label": "Women's Wine & Spirits Awards 2022 results",
        "url": AWARD_PROOF_URLS["transmission-xo-wwsa-2022"],
    },
    "pineau": {
        "name": "Médaille d'argent - Concours Mondial de Bruxelles 2025",
        "en_name": "Silver Medal - Concours Mondial de Bruxelles 2025",
        "proof_label": "Résultat officiel Concours Mondial de Bruxelles 2025 pour Pineau des Charentes Esprit Organic 2011",
        "en_proof_label": "Official Concours Mondial de Bruxelles 2025 result for Pineau des Charentes Esprit Organic 2011",
        "url": AWARD_PROOF_URLS["pineau-blanc-cmb-2025"],
    },
}

EN_SENSORY = {
    "fondation-vs": {
        "Mouth": "Oak, brioche, vine flower, peach, pear, vanilla",
        "Colour": "Golden yellow, straw yellow",
        "Nose": "Aromas of fresh fruit such as pear, peach and stewed fruit, including baked apples and golden raisins",
        "Palate": "A subtle blend of freshness and fruit followed by rounded brioche and vanilla notes",
        "Finish": "Fresh fruit notes of fresh grape and pear",
    },
    "conviction-vsop": {
        "Mouth": "Dried apricot, clove, plum, rose, vanilla",
        "Colour": "Golden yellow",
        "Nose": "Balanced and round: oak and vanilla, with a subtle touch of stewed fruit such as prune and apricot",
        "Palate": "Rich and ample, with a fine fruity character typical of the Fins Bois cru",
        "Finish": "Fresh, clove",
    },
    "cohesion-napoleon": {
        "Mouth": "Almond, lightly vanilla warm oak, peanut, hazelnut, pear, toffee",
        "Colour": "Orange-yellow",
        "Nose": "Barrel ageing reveals the first woody and vanilla notes",
        "Palate": "Fine oak tannins combine with dried fruit notes: almond, hazelnut and walnut",
        "Finish": "Balanced, slightly peppery and mentholated",
    },
    "transmission-xo": {
        "Mouth": "Wood, cinnamon, candied ginger, prune, tobacco, vanilla",
        "Colour": "Golden amber",
        "Nose": "Complex fruit, black cherry, with floral notes of wild flowers and warm spices. Over time the aromas evolve toward candied fruit, spices and old wood",
        "Palate": "An explosion of spicy flavours and aromas",
        "Finish": "Spiced with nutmeg and cinnamon. Rancio appears on the fresh mentholated finish",
    },
    "xxo": {
        "Mouth": "Cinnamon, tobacco and dried flowers, candied fruit",
        "Colour": "Amber with golden highlights",
        "Nose": "Explosive notes of candied and stewed fruit, with sweet cinnamon spices",
        "Palate": "A round, rich and structured Cognac",
        "Finish": "Fresh finish with liquorice notes",
    },
    "single-cask": {
        "Mouth": "Tobacco and dried flowers, candied fruit",
        "Colour": "Dark amber with red highlights",
        "Nose": "Intense notes of candied orange, ginger and prunes, with clove notes",
        "Palate": "A powerful, spicy Cognac with a strong presence of candied fruit",
        "Finish": "Fresh clove finish",
    },
    "pineau": {
        "Mouth": "Brioche, fresh grape juice, pear, prune, vanilla",
        "Colour": "Golden yellow, straw yellow, bright",
        "Nose": "Balanced and expressive, combining fresh grape, pear and vanilla notes",
        "Palate": "Rich, generous and complex",
        "Finish": "Fruity, intense and generous",
    },
    "pineau-rouge": {
        "Mouth": "Ripe red fruit, cherry, plum, grape sweetness",
        "Colour": "Deep red with ruby highlights, bright",
        "Nose": "Fruity and generous, around cherry, blackberry and candied red fruit",
        "Palate": "Supple, round and fruity, with good freshness",
        "Finish": "Generous, fruity and lightly spicy",
    },
}

COGNAC_NUTRITION_ROWS = [
    ("energy", "Valeur énergétique", "Energy", "", ""),
    ("alcohol", "Alcool", "Alcohol", "", ""),
    ("fat", "Matières grasses", "Fat", "0 g", "0 g"),
    ("saturates", "dont acides gras saturés", "of which saturates", "0 g", "0 g"),
    ("carbs", "Glucides", "Carbohydrate", "0 g", "0,3 g"),
    ("sugars", "dont sucres", "of which sugars", "0 g", "0,3 g"),
    ("protein", "Protéines", "Protein", "0 g", "0 g"),
    ("salt", "Sel", "Salt", "0 g", "0 g"),
]

PINEAU_NUTRITION_ROWS = [
    ("energy", "Valeur énergétique", "Energy", "", ""),
    ("alcohol", "Alcool", "Alcohol", "4,14 g", "13,8 g"),
    ("fat", "Matières grasses", "Fat", "0,5 g", "0,5 g"),
    ("saturates", "dont acides gras saturés", "of which saturates", "0,5 g", "0,5 g"),
    ("carbs", "Glucides", "Carbohydrate", "4,2 g", "14 g"),
    ("sugars", "dont sucres", "of which sugars", "4,2 g", "14 g"),
    ("protein", "Protéines", "Protein", "0,5 g", "0,5 g"),
    ("salt", "Sel", "Salt", "0 g", "0 g"),
]

PINEAU_ROUGE_NUTRITION_ROWS = [
    ("energy", "Valeur énergétique", "Energy", "", ""),
    ("alcohol", "Alcool", "Alcohol", "4,14 g", "13,8 g"),
    ("fat", "Matières grasses", "Fat", "0,5 g", "0,5 g"),
    ("saturates", "dont acides gras saturés", "of which saturates", "0,5 g", "0,5 g"),
    ("carbs", "Glucides", "Carbohydrate", "4,8 g", "16 g"),
    ("sugars", "dont sucres", "of which sugars", "4,8 g", "16 g"),
    ("protein", "Protéines", "Protein", "0,5 g", "0,5 g"),
    ("salt", "Sel", "Salt", "0 g", "0 g"),
]

NUTRITION_VALUES = {
    "fondation-vs": {
        "rows": [(key, fr, en, "279 kJ / 68 kcal" if key == "energy" else ("9,5 g" if key == "alcohol" else per_30), "931 kJ / 225 kcal" if key == "energy" else ("31,6 g" if key == "alcohol" else per_100)) for key, fr, en, per_30, per_100 in COGNAC_NUTRITION_ROWS],
        "ingredients_fr": "Vin distillé ; eau",
        "ingredients_en": "Distilled wine; water",
        "statement_fr": "Sans sulfites ajoutés",
        "statement_en": "No added sulphites",
    },
    "conviction-vsop": {
        "rows": [(key, fr, en, "279 kJ / 68 kcal" if key == "energy" else ("9,5 g" if key == "alcohol" else per_30), "931 kJ / 225 kcal" if key == "energy" else ("31,6 g" if key == "alcohol" else per_100)) for key, fr, en, per_30, per_100 in COGNAC_NUTRITION_ROWS],
        "ingredients_fr": "Vin distillé ; eau",
        "ingredients_en": "Distilled wine; water",
        "statement_fr": "Sans sulfites ajoutés",
        "statement_en": "No added sulphites",
    },
    "cohesion-napoleon": {
        "rows": [(key, fr, en, "285 kJ / 68 kcal" if key == "energy" else ("9,5 g" if key == "alcohol" else per_30), "951 kJ / 227 kcal" if key == "energy" else ("31,6 g" if key == "alcohol" else per_100)) for key, fr, en, per_30, per_100 in COGNAC_NUTRITION_ROWS],
        "ingredients_fr": "Vin distillé ; eau",
        "ingredients_en": "Distilled wine; water",
        "statement_fr": "Sans sulfites ajoutés",
        "statement_en": "No added sulphites",
    },
    "transmission-xo": {
        "rows": [(key, fr, en, "285 kJ / 68 kcal" if key == "energy" else ("9,5 g" if key == "alcohol" else per_30), "951 kJ / 227 kcal" if key == "energy" else ("31,6 g" if key == "alcohol" else per_100)) for key, fr, en, per_30, per_100 in COGNAC_NUTRITION_ROWS],
        "ingredients_fr": "Vin distillé ; eau",
        "ingredients_en": "Distilled wine; water",
        "statement_fr": "Sans sulfites ajoutés",
        "statement_en": "No added sulphites",
    },
    "xxo": {
        "rows": [(key, fr, en, "285 kJ / 68 kcal" if key == "energy" else ("10,2 g" if key == "alcohol" else per_30), "951 kJ / 227 kcal" if key == "energy" else ("34,3 g" if key == "alcohol" else per_100)) for key, fr, en, per_30, per_100 in COGNAC_NUTRITION_ROWS],
        "ingredients_fr": "Vin distillé ; eau",
        "ingredients_en": "Distilled wine; water",
        "statement_fr": "Sans sulfites ajoutés",
        "statement_en": "No added sulphites",
    },
    "single-cask": {
        "rows": [(key, fr, en, "285 kJ / 68 kcal" if key == "energy" else ("12,1 g" if key == "alcohol" else per_30), "951 kJ / 227 kcal" if key == "energy" else ("40,6 g" if key == "alcohol" else per_100)) for key, fr, en, per_30, per_100 in COGNAC_NUTRITION_ROWS],
        "ingredients_fr": "Vin distillé ; eau",
        "ingredients_en": "Distilled wine; water",
        "statement_fr": "Sans sulfites ajoutés",
        "statement_en": "No added sulphites",
    },
    "pineau": {
        "rows": [(key, fr, en, "198 kJ / 46,2 kcal" if key == "energy" else per_30, "660 kJ / 154 kcal" if key == "energy" else per_100) for key, fr, en, per_30, per_100 in PINEAU_NUTRITION_ROWS],
        "ingredients_fr": "Moût de raisin ; eau-de-vie de Cognac",
        "ingredients_en": "Grape must; Cognac eau-de-vie",
        "statement_fr": "Sans sulfites ajoutés",
        "statement_en": "No added sulphites",
    },
    "pineau-rouge": {
        "rows": [(key, fr, en, "196,5 kJ / 47,1 kcal" if key == "energy" else per_30, "655 kJ / 157 kcal" if key == "energy" else per_100) for key, fr, en, per_30, per_100 in PINEAU_ROUGE_NUTRITION_ROWS],
        "ingredients_fr": "Moût de raisin ; eau-de-vie de Cognac",
        "ingredients_en": "Grape must; Cognac eau-de-vie",
        "statement_fr": "Sans sulfites ajoutés",
        "statement_en": "No added sulphites",
    },
}


def bilingual(fr: str, en: str) -> str:
    return f'<span data-fr>{escape(fr)}</span><span data-en>{escape(en)}</span>'


def nutrition_table(slug: str, product_name: str) -> str:
    nutrition = NUTRITION_VALUES[slug]
    rows = "".join(
        f"<tr><th>{bilingual(row_fr, row_en)}</th><td>{escape(per_30)}</td><td>{escape(per_100)}</td></tr>"
        for _, row_fr, row_en, per_30, per_100 in nutrition["rows"]
    )
    return f"""
        <div class="nutrition-table-wrap">
          <table class="nutrition-table">
            <caption>{bilingual("Valeurs nutritionnelles moyennes", "Average nutritional values")}</caption>
            <thead>
              <tr>
                <th>{bilingual("Nutriment", "Nutrient")}</th>
                <th>{bilingual("Pour 30 ml", "Per 30 ml")}</th>
                <th>{bilingual("Pour 100 ml", "Per 100 ml")}</th>
              </tr>
            </thead>
            <tbody>{rows}</tbody>
          </table>
        </div>
        <div class="nutrition-meta">
          <p><strong>{bilingual("Ingrédients", "Ingredients")}</strong><span>{bilingual(nutrition["ingredients_fr"], nutrition["ingredients_en"])}</span></p>
          <p><strong>{bilingual("Mention", "Statement")}</strong><span>{bilingual(nutrition["statement_fr"], nutrition["statement_en"])}</span></p>
        </div>
"""


def rel_prefix(path: str) -> str:
    return "../" if "/" in path else ""


def lang_for_path(path: str) -> str:
    first_segment = path.split("/", 1)[0]
    return first_segment if first_segment in {"en", "da", "no", "sv"} else "fr"


def canonical_home_href(path: str) -> str:
    lang = lang_for_path(path)
    return "/" if lang == "fr" else f"/{lang}/"


def page_url(path: str) -> str:
    if path == "index.html":
        return DOMAIN + "/"
    if path.endswith("/index.html"):
        return f"{DOMAIN}/{path[:-10]}"
    if path.endswith("/"):
        return f"{DOMAIN}/{path}"
    return f"{DOMAIN}/{path}"


def breadcrumb_schema(path: str, title: str):
    items = [
        {"@type": "ListItem", "position": 1, "name": "Accueil", "item": DOMAIN + "/"},
    ]
    if path != "index.html":
        items.append({"@type": "ListItem", "position": 2, "name": title, "item": page_url(path)})
    return {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": items,
        "@id": page_url(path) + "#breadcrumb",
    }


def organization_schema():
    return {
        "@context": "https://schema.org",
        "@type": "Organization",
        "name": "Cognac Esprit Organic",
        "url": DOMAIN + "/",
        "email": CONTACT["email"],
        "telephone": CONTACT["phone"],
        "@id": DOMAIN + "/#organization",
        "address": {
            "@type": "PostalAddress",
            "streetAddress": "30 Rue d'Angoulême",
            "postalCode": "16200",
            "addressLocality": "Triac-Lautrait",
            "addressCountry": "FR",
        },
        "brand": {"@type": "Brand", "name": "Cognac Esprit Organic", "@id": DOMAIN + "/#brand"},
    }


def json_ld(items):
    if not isinstance(items, list):
        items = [items]
    return "\n".join(
        f'<script type="application/ld+json">{json.dumps(item, ensure_ascii=False, separators=(",", ":"))}</script>'
        for item in items
    )


def nav_html(current: str, prefix: str) -> str:
    product_current = current.startswith("produits/")
    house_current = current.startswith("production/") or current.startswith("demarche/") or current.startswith("leopold-et-fanny/") or current.startswith("equipe/")
    range_items = "".join(
        f'<a href="{prefix}produits/{p["slug"]}.html">{escape(p["name"])}</a>'
        for p in PRODUCTS
    )
    house_items = (
        f'<a href="{prefix}production/"><span data-fr>Notre démarche</span><span data-en>Our approach</span></a>'
        f'<a href="{prefix}demarche/"><span data-fr>La production</span><span data-en>Production</span></a>'
        f'<a href="{prefix}leopold-et-fanny/"><span data-fr>Léopold et Fanny</span><span data-en>Léopold and Fanny</span></a>'
        f'<a href="{prefix}equipe/"><span data-fr>L’équipe</span><span data-en>The team</span></a>'
    )
    visit_current = ' aria-current="page"' if current == "visiter.html" else ""
    product_aria = ' aria-current="page"' if product_current else ""
    house_aria = ' aria-current="page"' if house_current else ""
    return f"""
<div class="nav-dropdown">
  <a{product_aria} href="{prefix}produits/transmission-xo.html"><span data-fr>La gamme</span><span data-en>The range</span></a>
  <div class="dropdown-menu" role="menu">{range_items}</div>
</div>
<div class="nav-dropdown">
  <a{house_aria} href="{prefix}production/"><span data-fr>La maison</span><span data-en>The house</span></a>
  <div class="dropdown-menu" role="menu">{house_items}</div>
</div>
<a{visit_current} href="{prefix}visiter.html"><span data-fr>Visiter</span><span data-en>Visit</span></a>
"""


def layout(path: str, title: str, description: str, h1: str, intro_fr: str, intro_en: str, body: str, schemas=None, image="assets/img/products/gamme-esprit-organic.jpg", page_class="", hero_actions="", hero_video="", show_hero=True, robots=None, head_extra=""):
    prefix = rel_prefix(path)
    canonical = page_url(path)
    robots_content = robots or ("noindex,nofollow" if NOINDEX else "index,follow")
    noindex = f'<meta name="robots" content="{robots_content}">'
    schema_items = [organization_schema(), breadcrumb_schema(path, h1)]
    if schemas:
        schema_items.extend(schemas)
    root_image = "/" + image
    hero_class = "page-hero video-hero" if hero_video else "page-hero"
    hero_video_html = f"""<video class="hero-bg-video" autoplay muted loop playsinline preload="metadata" poster="{prefix}{image}">
        <source src="{prefix}{hero_video}" type="video/mp4">
      </video>""" if hero_video else ""
    home_slideshow = ""
    if "home-page" in page_class:
        home_slides = [
            "assets/img/old-site/img_home_01.jpg",
            "assets/img/old-site/img_home_02.jpg",
            "assets/img/old-site/img_home_03.jpg",
        ]
        home_slideshow = '<div class="home-hero-slideshow" aria-hidden="true">' + "".join(
            f'<span class="{"is-active" if i == 0 else ""}" style="background-image:url({prefix}{src})"></span>'
            for i, src in enumerate(home_slides)
        ) + "</div>"
    hero_html = f"""
    <section class="{hero_class}" style="--hero-image: url('{root_image}')">
      {home_slideshow}
      {hero_video_html}
      <div class="section-inner narrow">
        <p class="eyebrow">Cognac Esprit Organic</p>
        <h1>{h1}</h1>
        <p class="lead" data-fr>{intro_fr}</p>
        <p class="lead" data-en>{intro_en}</p>
        {hero_actions}
      </div>
    </section>""" if show_hero else ""
    return f"""<!doctype html>
<html lang="fr" data-default-lang="fr">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{escape(title)}</title>
  <meta name="description" content="{escape(description)}">
  {noindex}
  <link rel="canonical" href="{canonical}">
  {head_extra}
  <meta property="og:title" content="{escape(title)}">
  <meta property="og:description" content="{escape(description)}">
  <meta property="og:type" content="website">
  <meta property="og:image" content="{DOMAIN}/{image}">
  <link rel="icon" href="{prefix}assets/img/fav_organic.png">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@300;400;500;600;700;800;900&family=Raleway:wght@200;300;400;500;600;700;800;900&family=Roboto+Slab:wght@200;300;400;500;600;700;800&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="{prefix}assets/css/styles.css?v=20260627-technical-facts01">
  {json_ld(schema_items)}
</head>
<body class="{page_class}">
  <a class="skip-link" href="#contenu">Aller au contenu</a>
  <header class="site-header">
    <nav class="nav" aria-label="Navigation principale">
      <a class="brand" href="{canonical_home_href(path)}" aria-label="Cognac Esprit Organic">
        <img src="{prefix}assets/img/logo-esprit-organic-brown.svg" alt="Cognac Esprit Organic">
      </a>
      <button class="nav-toggle" type="button" data-nav-toggle aria-expanded="false" aria-label="Ouvrir le menu">Menu</button>
      <div class="nav-links" data-nav-links>{nav_html(path, prefix)}<div class="lang-menu" data-lang-menu><button class="lang-toggle" type="button" data-lang-toggle aria-haspopup="true" aria-expanded="false">{lang_for_path(path).upper()}</button><div class="lang-menu-panel" role="menu" aria-label="Choisir la langue"><button type="button" class="lang-option" data-lang-option="fr" role="menuitem">FR</button><button type="button" class="lang-option" data-lang-option="en" role="menuitem">EN</button><button type="button" class="lang-option" data-lang-option="da" role="menuitem">DA</button><button type="button" class="lang-option" data-lang-option="no" role="menuitem">NO</button><button type="button" class="lang-option" data-lang-option="sv" role="menuitem">SV</button></div></div><a class="header-bio-link" href="{prefix}agriculture-biologique.html" aria-label="Agriculture biologique"><img class="header-bio" src="{prefix}assets/img/logo-bio-home-tight.png" alt="Agriculture biologique"></a></div>
    </nav>
  </header>
  <main id="contenu">
    {hero_html}
    {body}
  </main>
  <footer class="site-footer">
    <div class="footer-grid">
      <div>
        <img class="footer-logo" src="{prefix}assets/img/logo-esprit-organic-white.svg" alt="Cognac Esprit Organic">
        <p class="small">L'abus d'alcool est dangereux pour la santé. A consommer avec modération.</p>
      </div>
      <div class="footer-links">
        <a href="{prefix}produits/transmission-xo.html">Gamme</a>
        <a href="{prefix}faq.html">FAQ</a>
        <a href="{prefix}cocktails.html">Cocktails</a>
      </div>
    </div>
  </footer>
  <script src="{prefix}assets/js/main.js?v=20260629-faq01"></script>
</body>
</html>
"""


def redirect_page(path: str, title: str, target: str):
    prefix = rel_prefix(path)
    noindex = '<meta name="robots" content="noindex,nofollow">' if NOINDEX else '<meta name="robots" content="index,follow">'
    return f"""<!doctype html>
<html lang="fr">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{escape(title)}</title>
  <meta name="description" content="Redirection vers la nouvelle page Cognac Esprit Organic.">
  {noindex}
  <link rel="canonical" href="{DOMAIN}/{target}">
  <meta http-equiv="refresh" content="0; url={prefix}{target}">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@300;400;500;600;700;800;900&family=Raleway:wght@200;300;400;500;600;700;800;900&family=Roboto+Slab:wght@200;300;400;500;600;700;800&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="{prefix}assets/css/styles.css?v=20260627-technical-facts01">
</head>
<body>
  <main class="redirect-page">
    <section>
      <div class="section-inner">
        <h1>{escape(title)}</h1>
        <p>Cette page a été déplacée.</p>
        <a class="button" href="{prefix}{target}">Ouvrir la nouvelle page</a>
      </div>
    </section>
  </main>
</body>
</html>
"""


def product_card(product, prefix=""):
    href = f"{prefix}produits/{product['slug']}.html"
    return f"""<a class="product-card old-tile" href="{href}">
  <img src="{prefix}{product['image']}" alt="Bouteille {escape(product['name'])}" loading="lazy">
  <span class="tile-shade"></span>
  <span class="tile-copy">
    <span class="tag">{escape(product['category'])}</span>
    <strong>{escape(product['name'])}</strong>
  </span>
</a>"""


def product_text_tile(product, prefix=""):
    return f"""<a class="product-text-tile" style="--tile-tone: {product['tone']}" href="{prefix}produits/{product['slug']}.html">
  <span>{escape(product['category'])}</span>
  <strong>{escape(product['name'])}</strong>
  <em data-fr>{escape(product['short'])}</em>
  <em data-en>{escape(product['en_short'])}</em>
</a>"""


def product_menu(prefix=""):
    return '<div class="bottle-menu" aria-label="Gamme Cognac Esprit Organic">' + "".join(
        f'<a href="{prefix}produits/{p["slug"]}.html" title="{escape(p["name"])}"><img src="{prefix}{p["menu"]}" alt="{escape(p["name"])}"></a>'
        for p in PRODUCTS
    ) + "</div>"


def section(content, cls=""):
    return f'<section class="{cls}"><div class="section-inner">{content}</div></section>'


def split(left, right, cls=""):
    return section(f'<div class="split {cls}"><div>{left}</div><div>{right}</div></div>')


def medal_html(medal, product_name: str, prefix: str) -> str:
    if isinstance(medal, str):
        src = medal
        return f'<img src="{prefix}{src}" alt="Récompense {escape(product_name)}" loading="lazy">'
    src = medal["src"]
    alt = medal.get("alt", f"Récompense {product_name}")
    href = medal.get("href")
    label = medal.get("label", f"Voir la preuve de la récompense {product_name}")
    image = f'<img src="{prefix}{src}" alt="{escape(alt)}" loading="lazy">'
    if href:
        return f'<a class="product-medal-link" href="{escape(href)}" target="_blank" rel="noopener noreferrer" aria-label="{escape(label)}">{image}</a>'
    return image


def property_value(name: str, value: str):
    return {"@type": "PropertyValue", "name": name, "value": value}


def write(path, content):
    target = ROOT / path
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(content, encoding="utf-8")


def home():
    hero_names = [
        ("produits/fondation-vs.html", "VS"),
        ("produits/conviction-vsop.html", "VSOP"),
        ("produits/cohesion-napoleon.html", "NAPOLEON"),
        ("produits/transmission-xo.html", "XO"),
        ("produits/xxo.html", "XXO"),
        ("produits/single-cask.html", "SINGLE CASK"),
    ]
    product_names = "".join(f'<li><a href="{href}">{label}</a></li>' for href, label in hero_names)
    product_tiles = "".join(product_card(p) for p in PRODUCTS)
    body = f"""
<section class="old-duo">
  <a class="old-panel image-panel" href="produits/transmission-xo.html">
    <img src="assets/img/old-site/img_home_part02_gamme.png" alt="Gamme Cognac Esprit Organic">
    <span class="panel-copy haut-gauche"><strong data-fr>Toute la nature de nos Cognacs</strong><strong data-en>All the nature of our Cognacs</strong><small data-fr>Organique et sans complexe</small><small data-en>Organic and uncomplicated</small></span>
  </a>
  <a class="old-panel image-panel" href="cocktails.html">
    <img src="assets/img/old-site/img_home_cocktail_01.jpg" alt="Cocktail Cognac Esprit Organic">
    <span class="panel-copy haut-gauche"><strong data-fr>Accompagner nos Cognacs</strong><strong data-en>Pair our Cognacs</strong><small data-fr>Laisser courir l'inspiration</small><small data-en>Let inspiration flow</small></span>
  </a>
</section>
<section class="cream-signature">
  <div>
    <img class="floral-left" src="assets/img/floral-01.svg" alt="" aria-hidden="true">
    <img class="floral-right" src="assets/img/floral-03.svg" alt="" aria-hidden="true">
    <p data-fr>Bienvenue sur nos terres</p>
    <p data-en>Welcome to our land</p>
    <span>•••</span>
    <strong data-fr>Depuis 20 ans, Léopold Croizet conduit son vignoble en agriculture biologique. Il distille, élève et met en bouteille sa production à la propriété.</strong>
    <strong data-en>For 20 years, Léopold Croizet has been managing his vineyard in organic agriculture. He distils, ages and bottles production at the estate.</strong>
    <a class="text-link home-team-link" href="equipe/"><span data-fr>L’équipe</span><span data-en>The team</span></a>
  </div>
</section>
<section class="old-grid">
  <a class="old-panel image-panel large" href="production/">
    <img src="assets/img/old-site/img_home_vigne.jpg" alt="Vignes Cognac Esprit Organic">
    <span class="panel-copy haut-gauche"><strong data-fr>Le cycle naturel</strong><strong data-en>The natural cycle</strong><small data-fr>Travailler dans la durabilité</small><small data-en>Working sustainably</small></span>
  </a>
  <a class="old-panel image-panel" href="leopold-et-fanny/">
    <img src="assets/img/old-site/histoire.jpg" alt="Léopold Croizet dans les vignes">
    <span class="panel-copy bas-droit"><strong data-fr>L'esprit organic</strong><strong data-en>The organic spirit</strong><small data-fr>Notre histoire</small><small data-en>Our story</small></span>
  </a>
</section>
<a class="home-video-signature" href="demarche/" aria-label="La production - Maîtriser et laisser faire">
  <video autoplay muted loop playsinline preload="metadata" poster="assets/img/brand/home-video-poster.jpg">
    <source src="assets/video/home-nature.mp4" type="video/mp4">
  </video>
  <div class="video-copy">
    <h2 data-fr>Maîtriser & laisser faire</h2>
    <h2 data-en>Mastering & letting nature work</h2>
    <p data-fr>Travailler dans le bon sens</p>
    <p data-en>Working in the right direction</p>
  </div>
</a>
<section class="home-transmission-block">
  <img class="transmission-floral-left" src="assets/img/floral-01.svg" alt="" aria-hidden="true">
  <img class="transmission-floral-right" src="assets/img/floral-03.svg" alt="" aria-hidden="true">
  <div>
    <h2 data-fr>Cultiver pour transmettre</h2>
    <h2 data-en>Cultivating to transmit</h2>
    <span>•••</span>
    <p data-fr><strong>ESPRIT ORGANIC</strong><br>est né d’une volonté<br>de transmission dans laquelle<br>Léopold et Fanny Croizet<br>mettent tout leur cœur,<br>leur énergie<br>et leur passion.</p>
    <p data-en><strong>ESPRIT ORGANIC</strong><br>was born from a desire<br>to transmit, carried by<br>Léopold and Fanny Croizet<br>with all their heart,<br>energy<br>and passion.</p>
  </div>
</section>
"""
    hero_actions = f'<nav class="hero-product-links" aria-label="Accès rapides produits"><ul>{product_names}</ul></nav>'
    return layout(
        "index.html",
        "Cognac Esprit Organic | Cognac bio familial en France",
        "Cognac Esprit Organic présente une gamme de Cognacs biologiques portée par Léopold et Fanny Croizet, avec une structure claire pour Google et l'export.",
        "Cognac Esprit Organic",
        "Cognac biologique familial, naturel et premium.",
        "Family, natural and premium organic Cognac.",
        body,
        image="assets/img/brand/hero-vine-02.jpg",
        page_class="home-page",
        hero_actions=hero_actions,
    )


def range_page():
    body = section(
        '<p class="eyebrow">Produits</p><h2 data-fr>Gamme Cognac Esprit Organic</h2><h2 data-en>Cognac Esprit Organic range</h2>'
        + '<p data-fr>Les produits disponibles aujourd’hui sont : VS, VSOP, Napoléon, XO, XXO, Single Cask, Pineau blanc et Pineau rouge.</p>'
        + '<p data-en>Products currently available are: VS, VSOP, Napoléon, XO, XXO, Single Cask, white Pineau and red Pineau.</p>'
        + product_menu()
        + f'<div class="product-text-grid">{"".join(product_text_tile(p) for p in PRODUCTS)}</div>'
    )
    return layout("produits.html", "Gamme produits | Cognac Esprit Organic", "Découvrez les Cognacs biologiques Esprit Organic : VS, VSOP, Napoléon, XO, XXO, Single Cask, Pineau blanc et Pineau rouge.", "Gamme produits Cognac Esprit Organic", "Une gamme biologique structurée pour une lecture simple, du VS au XXO.", "An organic range structured for clear reading, from VS to XXO.", body)


def product_page(product):
    prefix = "../"
    extra = PRODUCT_EXTRAS.get(product["slug"], {})
    trade_pdf = PRODUCT_TRADE_PDFS.get(product["slug"])
    detail_image = extra.get("detail_image", product.get("detail_image", product["scene"]))
    tasting_image = extra.get("tasting_image", product.get("tasting_image", product["image"]))
    colors = extra.get("colors", [product["tone"], product["tone"], product["tone"]])
    gallery_color = extra.get("gallery_color", product["tone"])
    accent = extra.get("accent", "#ffffff")
    sensory = extra.get("sensory", {})
    abv = product.get("abv", "")
    schema = {
        "@context": "https://schema.org",
        "@type": "Product",
        "name": product["name"],
        "brand": {"@type": "Brand", "name": "Cognac Esprit Organic", "@id": DOMAIN + "/#brand"},
        "manufacturer": {"@id": DOMAIN + "/#organization"},
        "category": product["category"],
        "image": DOMAIN + "/" + product["image"],
        "description": product["short"],
        "@id": page_url(f"produits/{product['slug']}.html") + "#product",
    }
    additional_properties = [property_value(label, value) for label, value in sensory.items()]
    if additional_properties:
        schema["additionalProperty"] = additional_properties
    if trade_pdf:
        schema["subjectOf"] = {
            "@type": "DigitalDocument",
            "name": trade_pdf["label"],
            "encodingFormat": "application/pdf",
            "url": DOMAIN + "/" + trade_pdf["href"],
        }
    notes = "".join(f"<li>{escape(note)}</li>" for note in product["notes"])
    story = extra.get("story", product["short"])
    degustation_title = extra.get("degustation_title", "Dégustation")
    degustation_text = extra.get("degustation_text", product["short"])
    nutrition = NUTRITION_VALUES.get(product["slug"])
    nutrition_placeholder = extra.get("nutrition_placeholder", "")
    sensory_items = "".join(
        f'<li><span>{escape(label)} :</span><strong>{escape(value)}</strong></li>'
        for label, value in sensory.items()
    )
    medals = "".join(
        medal_html(medal, product["name"], prefix)
        for medal in extra.get("medals", [])
    )
    medal_block = f'<div class="product-medals">{medals}</div>' if medals else ""
    gallery_images = [detail_image] + extra.get("gallery", [])
    gallery_buttons = "".join(
        f'<button type="button" data-gallery-thumb data-gallery-target="{prefix}{src}" aria-label="Afficher le visuel {idx + 1} de {escape(product["name"])}"><img src="{prefix}{src}" alt="" loading="lazy"></button>'
        for idx, src in enumerate(gallery_images)
    )
    nutrition_controls = f"""
      <button class="nutrition-link" type="button" data-nutrition-open data-fr>Valeurs nutritionnelles</button>
      <button class="nutrition-link" type="button" data-nutrition-open data-en>Nutritional values</button>
"""
    if nutrition:
        nutrition_controls += f"""
      <dialog class="nutrition-dialog" data-nutrition-dialog>
        <form method="dialog">
          <button type="submit" aria-label="Fermer">×</button>
        </form>
        <h2>Valeurs nutritionnelles - {escape(product["name"])}</h2>
{nutrition_table(product["slug"], product["name"])}
      </dialog>
"""
    elif nutrition_placeholder:
        nutrition_controls += f"""
      <dialog class="nutrition-dialog" data-nutrition-dialog>
        <form method="dialog">
          <button type="submit" aria-label="Fermer">×</button>
        </form>
        <h2>Valeurs nutritionnelles - {escape(product["name"])}</h2>
        <p>{escape(nutrition_placeholder)}</p>
      </dialog>
"""
    else:
        nutrition_controls = ""
    trade_pdf_download = ""
    if trade_pdf:
        trade_pdf_download = f"""
      <div class="product-downloads">
        <a class="product-pdf-link" href="{prefix}{escape(trade_pdf["href"])}" type="application/pdf" download aria-label="Télécharger {escape(trade_pdf["label"])} au format PDF">
          <span data-fr>Fiche dégustation</span>
          <span data-en>Tasting sheet</span>
        </a>
      </div>
"""
    section_class = f'product-old-detail {extra.get("section_class", "")}'.strip()
    body = f"""
<section class="product-menu-strip">
  <div class="section-inner">{product_menu(prefix)}</div>
</section>
<section class="{section_class}" style="--product-tone: {product['tone']}; --product-gallery: {gallery_color}; --product-top: {colors[0]}; --product-mid: {colors[1]}; --product-low: {colors[2]}; --product-accent: {accent};">
  <div class="product-gallery-rail">
    {gallery_buttons}
  </div>
  <div class="product-scene">
    <img src="{prefix}{detail_image}" alt="Visuel {escape(product['name'])}" data-gallery-main>
  </div>
  <div class="product-info-block">
    <div class="product-description">
      <p class="eyebrow">{escape(product['category'])}</p>
      <h1>{escape(product['name'])}</h1>
      <p data-fr>{escape(product['short'])}</p>
      <p data-en>{escape(product['en_short'])}</p>
      <p class="product-story">{escape(story)}</p>
      {medal_block}
    </div>
    <div class="product-bottle-inline">
      <img src="{prefix}{tasting_image}" alt="Illustration {escape(product['name'])}">
      <div>
        <h2 data-fr>Dégustation</h2>
        <h2 data-en>Tasting markers</h2>
        <h3>{escape(degustation_title)}</h3>
        <p>{escape(degustation_text)}</p>
      </div>
    </div>
    <div class="product-sensory">
      <h2 data-fr>Notes sensorielles</h2>
      <h2 data-en>Sensory notes</h2>
      <ul>
        {sensory_items}
      </ul>
      {nutrition_controls}
      {trade_pdf_download}
    </div>
  </div>
</section>
"""
    return layout(
        f"produits/{product['slug']}.html",
        f"{product['name']} | Cognac Esprit Organic",
        f"{product['name']} Cognac Esprit Organic : {product['short']}",
        product["name"],
        product["short"],
        product["en_short"],
        body,
        schemas=[schema],
        image=product["image"],
        page_class="product-page",
        show_hero=False,
    )


def approach_page(path="production/index.html"):
    body = """
<section class="legacy-content legacy-vertical">
  <div class="legacy-breadcrumb"><a href="/">Accueil</a><span>/ Notre démarche</span></div>
  <section class="legacy-video-block">
    <video autoplay muted loop playsinline preload="metadata" poster="../assets/img/old-site/domaine-scaled.jpg">
      <source src="../assets/video/approach-fins-bois.mp4" type="video/mp4">
    </video>
    <div>
      <p class="eyebrow">Cognac Esprit Organic</p>
      <h1>Prendre conscience, mieux produire</h1>
      <p>Pour mieux consommer, préserver et transmettre.</p>
    </div>
  </section>
  <div class="legacy-pair">
    <article class="legacy-text-block old-approach-brown">
      <h2>Déjà 20 ans de production durable</h2>
      <p>Esprit Organic est une marque de cognac familiale, dont la production est issue de l’agriculture biologique depuis plus de 20 ans. C’est un cognac de producteur implanté dans le cru des Fins Bois, au domaine de la Grande Versenne, à Triac-Lautrait et géré avec passion par Léopold et Fanny Croizet.</p>
      <p>On ne décide pas de faire du cognac « bio » par hasard. C’est une démarche personnelle mais aussi collective. C’est une bonne parole que l’on prêche et que l’on partage avec plaisir, comme un verre de cognac.</p>
      <p>Esprit Organic, c’est un état d’esprit dont le nom est un hommage à notre démarche.</p>
    </article>
    <div class="legacy-wide-media">
      <img src="../assets/img/old-site/domaine-scaled.jpg" alt="Domaine de la Grande Versenne">
    </div>
  </div>
  <div class="legacy-pair reverse">
    <article class="legacy-text-block old-approach-olive">
      <h2>Une gamme biologique</h2>
      <p>Un choix qui permet de suivre une évolution intéressante et qui fait la place libre à l’expression du terroir, au retour du « bon sens » paysan : une dynamique de travail que nous voulons remettre en avant.</p>
      <p>Chaque produit raconte une histoire, celle d’une lignée de vignerons passionnés, implantés depuis plusieurs générations à Triac Lautrait, qui à force de travail, de conviction et de passion a pu transmettre cet héritage de la cuture de la vigne et du cognac et façonner la vision qui transpire aujourd’hui à travers ESPRIT ORGANIC.</p>
    </article>
    <div class="legacy-wide-media">
      <img src="../assets/img/old-site/gamme_esprit_organic_nature-scaled.jpg" alt="Gamme Cognac Esprit Organic">
    </div>
  </div>
</section>
"""
    return layout(path, "Notre démarche | Cognac Esprit Organic", "Notre démarche Cognac Esprit Organic : production durable, agriculture biologique, Fins Bois et esprit de transmission.", "Prendre conscience, mieux produire", "Pour mieux consommer, préserver et transmettre.", "To consume better, preserve and transmit.", body, image="assets/img/old-site/domaine-scaled.jpg", page_class="legacy-page", show_hero=False)


def production_page(path="demarche/index.html"):
    body = f"""
<section class="legacy-content legacy-vertical production-steps">
  <div class="legacy-breadcrumb"><a href="/">Accueil</a><span>/ La Production</span></div>
  <section class="legacy-video-block">
    <video autoplay muted loop playsinline preload="metadata" poster="../assets/img/old-site/IMG_4079-scaled.jpg">
      <source src="../assets/video/production-abeille.mp4" type="video/mp4">
    </video>
    <div>
      <p class="eyebrow">Cognac Esprit Organic</p>
      <h1>Un savoir-faire générationnel</h1>
      <p>Il est là, depuis plus de 20 ans.</p>
    </div>
  </section>
  <div class="legacy-pair">
    <article class="legacy-text-block old-prod-cru">
      <h2>Un Cru, les Fins Bois</h2>
      <p>Nous sommes fiers d’être implantés dans le cru des Fins Bois, cru que nous revendiquons haut et fort. Il ne faut pas oublier que c’est le cru majoritaire de notre région, il coule dans les veines de nombreuses bouteilles de cognac.</p>
      <p>Notre domaine se situe à proximité de Jarnac et bénéficie des terres calcaires de champagne et des terres argilocalcaires et de « groies » des Fins Bois. Cette diversité apporte à nos eaux-de-vie une belle complexité aromatique.</p>
    </article>
    <div class="legacy-wide-media"><img src="../assets/img/old-site/domaine-scaled.jpg" alt="Domaine de la Grande Versenne"></div>
  </div>
  <div class="legacy-pair reverse">
    <article class="legacy-text-block old-prod-vineyard">
      <h2>Respect de nos terres et culture de la vigne</h2>
      <p>Nous respectons les sols en cultivant la vigne sans produits chimiques ni pesticides. Trèfle et fèverole habitent nos vignes et favorisent la régénération des sols. La conduite des vignes est étudiée en fonction du type de sol et des parcelles.</p>
      <p>Le but est d’obtenir des raisins sains de la meilleure qualité possible. Nous cultivons la diversité : le domaine se compose de 3 cépages de vins blancs : l’Ugni Blanc, le Colombard et la Folle Blanche.</p>
    </article>
    <div class="legacy-wide-media"><img src="../assets/img/old-site/IMG_4079-scaled.jpg" alt="Vignes Cognac Esprit Organic"></div>
  </div>
  <div class="legacy-pair">
    <article class="legacy-text-block old-prod-distillation">
      <h2>Distillation</h2>
      <p>C’est une technique propre à notre maison, que je tiens de mon père, qu’il tenait lui-même de sa mère. Elle souligne la rondeur des eaux-de-vie et développe l’intensité des parfums de notre cru.</p>
      <p>Nous distillons dans 2 alambics en cuivre de 16 hl et 20 hl pour souligner cette complexité aromatique que l’on chérit tant.</p>
    </article>
    <div class="legacy-wide-media"><img src="../assets/img/old-site/distillerie_02.jpg" alt="Alambics en cuivre"></div>
  </div>
  <div class="legacy-pair reverse">
    <article class="legacy-text-block old-prod-aging">
      <h2>Élevage soigné et suivi</h2>
      <p>Fanny s’occupe passionnément d’élever nos eaux-de-vie, elle prend son temps et laisse s’opérer cette étape magique. Elle sélectionne avec soin ses barriques, en fonction des grains du bois, des chauffes et des contenances.</p>
      <p>Elle mise sur la diversité pour acquérir de la complexité. Les potentiels tanniques du bois de chêne sont aussi riches et variés que les caractéristiques organoleptiques des cépages utilisés.</p>
    </article>
    <div class="legacy-wide-media"><img src="../assets/img/old-site/assemblage-scaled.jpg" alt="Fanny Croizet dégustant un Cognac"></div>
  </div>
  <div class="legacy-pair">
    <article class="legacy-text-block old-prod-blending">
      <h2>L’art subtil de l’assemblage</h2>
      <p>C’est la partie complexe qui fait appel à tous nos sens car il s’agit ici d’obtenir un cognac équilibré, rond, aromatique et surtout agréable à consommer.</p>
      <p>Francis, le père de Fanny, n’est jamais loin pour déguster avec nous. C’est important pour moi de partager, d’écouter. On prend tellement de plaisir à le faire ce cognac. Le partage, c’est la moitié du travail.</p>
    </article>
    <div class="legacy-wide-media"><img src="../assets/img/old-site/assemblage-1.jpg" alt="Travail d’assemblage Cognac Esprit Organic"></div>
  </div>
  <div class="legacy-pair reverse">
    <article class="legacy-text-block old-prod-bottling">
      <h2>La mise en bouteille</h2>
      <p>Comme toutes les étapes d’élaboration de ce cognac, la mise en bouteille s’effectue également sur la propriété. Elle est faite à la main comme autrefois.</p>
      <p>Nous portons un soin particulier à l’habillage de nos bouteilles.</p>
    </article>
    <div class="legacy-wide-media"><img src="../assets/img/old-site/mise-en-bouteille-scaled.jpg" alt="Mise en bouteille Cognac Esprit Organic"></div>
  </div>
</section>
"""
    return layout(path, "La production | Cognac Esprit Organic", "La production Cognac Esprit Organic : Fins Bois, culture de la vigne, distillation, élevage, assemblage et mise en bouteille.", "Un savoir-faire générationnel", "Il est là, depuis plus de 20 ans.", "A generational know-how, present for more than 20 years.", body, image="assets/img/old-site/IMG_4079-scaled.jpg", page_class="legacy-page production-page", show_hero=False)


def people_page(path="leopold-et-fanny/index.html"):
    body = """
<section class="legacy-content legacy-vertical people-content">
  <div class="legacy-breadcrumb"><a href="/">Accueil</a><span>/ Léopold et Fanny</span></div>
  <section class="legacy-video-block">
    <video autoplay muted loop playsinline preload="metadata" poster="../assets/img/old-site/leopold_croizet.jpg">
      <source src="../assets/video/people-fond.mp4" type="video/mp4">
    </video>
    <div>
      <p class="eyebrow">Cognac Esprit Organic</p>
      <h1>Travailler d’une même passion</h1>
      <p>Un héritage passionnant mis au profit des générations futures.</p>
    </div>
  </section>
  <div class="legacy-pair">
    <article class="legacy-text-block old-people-brown">
      <h2>Léopold Croizet</h2>
      <p>est issu d’une longue lignée de vignerons. 10e génération de la famille à travailler la vigne, en Algérie du côté maternel, en Charente du côté paternel. L’expérience et le savoir-faire coulent dans ses veines.</p>
      <p>Études de commerce international et MBA en poche, il est armé pour reprendre et développer la propriété familiale. Il commence par convertir son vignoble en AB.</p>
      <p>Pour lui, l’avenir se trouve dans la préservation de son patrimoine et la conviction profonde que la notion de « bon sens paysan » doit reprendre sa place dans le travail de la terre.</p>
    </article>
    <div class="legacy-wide-media"><img src="../assets/img/old-site/leopold_croizet.jpg" alt="Léopold Croizet"></div>
  </div>
  <div class="legacy-pair reverse">
    <article class="legacy-text-block old-people-olive">
      <h2>Fanny Croizet</h2>
      <p>est passionnée depuis petite par les métiers de la vigne en observant son grand-père récolter et distiller les fruits de ses vendanges. Son père, dégustateur dans une grande maison de négoce, lui a très vite transmis la sensibilité aux multiples saveurs du cognac.</p>
      <p>Ce qui au départ n’était qu’un simple jeu sensitif a débouché sur un master de commerce international des vins et spiritueux avec une prédominance pour la dégustation des eaux-de-vie.</p>
      <p>Après quelques années à parfaire son nez et ses connaissances du vieillissement des eaux-de-vie dans une belle tonnellerie familiale, elle rejoint Léopold en 2016. Par amour, puis par passion.</p>
    </article>
    <div class="legacy-wide-media"><img src="../assets/img/old-site/fanny_croizet.jpg" alt="Fanny Croizet"></div>
  </div>
</section>
"""
    return layout(path, "Léopold et Fanny | Cognac Esprit Organic", "Léopold et Fanny Croizet portent Cognac Esprit Organic avec une même passion pour la vigne, le Cognac et la transmission.", "Travailler d’une même passion", "Un héritage passionnant mis au profit des générations futures.", "A passionate heritage serving future generations.", body, image="assets/img/old-site/leopold_croizet.jpg", page_class="legacy-page people-page", show_hero=False)


def team_page(path="equipe/index.html"):
    body = """
<section class="team-page-content">
  <h1 class="visually-hidden">Notre équipe</h1>
  <div class="visually-hidden">
    <p>Femmes et hommes engagés pour un Cognac biologique d’exception.</p>
    <p>Cognac Esprit Organic est une maison familiale indépendante engagée dans une viticulture biologique exigeante.</p>
    <ul>
      <li>Léopold Croizet, vigneron, distillateur, gérant.</li>
      <li>Fanny Croizet, coordinatrice production et régie douanes.</li>
      <li>Damien Bertrand, directeur commercial export.</li>
      <li>Thierry Chavagne, chef d’exploitation.</li>
      <li>Sébastien Gaborit, chef d’équipe viticole assistant distillateur.</li>
      <li>Joanna Gaborit, responsable de la mise en bouteille.</li>
      <li>Stéphanie Beaulieu, responsable comptable et administrative.</li>
      <li>Manoé Amrouche, coordinatrice comptable et administrative.</li>
    </ul>
  </div>
  <figure class="team-poster-shell">
    <img src="../assets/img/team/notre-equipe-cognac-esprit-organic.png" alt="Notre équipe Cognac Esprit Organic : Léopold Croizet, Fanny Croizet, Damien Bertrand, Thierry Chavagne, Sébastien Gaborit, Joanna Gaborit, Stéphanie Beaulieu et Manoé Amrouche." width="2526" height="1786">
  </figure>
</section>
"""
    return layout(path, "L’équipe | Cognac Esprit Organic", "Notre équipe Cognac Esprit Organic : femmes et hommes engagés pour un Cognac biologique d’exception.", "Notre équipe", "Femmes et hommes engagés pour un Cognac biologique d’exception.", "Women and men committed to exceptional organic Cognac.", body, image="assets/img/team/notre-equipe-cognac-esprit-organic.png", page_class="legacy-page team-page", show_hero=False)


def importer_page():
    body = f"""
{split('<p class="eyebrow">B2B export</p><h2 data-fr>Une page dédiée aux importateurs, cavistes, CHR, bars, hôtels et réseaux bio.</h2><h2 data-en>A dedicated page for importers, wine merchants, hospitality, bars, hotels and organic retail networks.</h2>', '<p data-fr>Esprit Organic s’adresse aux marchés export formulés ainsi : Europe, USA, Canada. Cette page reste volontairement factuelle : elle présente la gamme, les informations de contact et les documents à préparer, sans inventer de volumes ni de distributeurs.</p><p data-en>Esprit Organic addresses export markets formulated as: Europe, USA, Canada. This page stays factual: it presents the range, contact details and documents to prepare, without inventing volumes or distributors.</p><a class="button" href="contact.html" data-fr>Demander des informations export</a><a class="button" href="contact.html" data-en>Request export information</a>')}
{section('<div class="feature-grid"><article><h2 data-fr>Gamme</h2><h2 data-en>Range</h2><p>VS, VSOP, Napoléon, XO, XXO, Single Cask, Pineau blanc, Pineau rouge.</p></article><article><h2 data-fr>Positionnement</h2><h2 data-en>Positioning</h2><p data-fr>Cognac biologique familial, naturel, premium et indépendant.</p><p data-en>Family, natural, premium and independent organic Cognac.</p></article><article><h2 data-fr>Marchés</h2><h2 data-en>Markets</h2><p>Europe, USA, Canada.</p></article></div>')}
{section('<h2 data-fr>Documents à préparer</h2><h2 data-en>Documents to prepare</h2><ul class="check-list"><li data-fr><a href="fiches-techniques-produits.html">Données produits et documents professionnels en HTML accessible.</a></li><li data-en><a href="fiches-techniques-produits.html">Product data and professional documents in accessible HTML.</a></li><li data-fr>Photos bouteilles et gamme.</li><li data-en>Bottle and range photographs.</li><li data-fr>Informations réglementaires et nutritionnelles en HTML accessible.</li><li data-en>Regulatory and nutritional information in accessible HTML.</li></ul>')}
"""
    return layout("importers.html", "Importateurs cognac bio | Cognac Esprit Organic", "Page export B2B pour les importateurs de Cognac Esprit Organic en Europe, aux USA et au Canada : gamme bio, positionnement et contact.", "Pour les importateurs", "Une page B2B export pour les marchés Europe, USA, Canada.", "A B2B export page for Europe, USA and Canada.", body)


def producer_page():
    location_cards = "<div class=\"feature-grid\"><article><h2>Location</h2><p>30 Rue d'Angoulême, 16200 Triac-Lautrait, France.</p></article><article><h2>Organic focus</h2><p>Family, natural and premium positioning for professional buyers looking for organic Cognac from France.</p></article><article><h2>Export wording</h2><p>Europe, USA, Canada.</p></article></div>"
    body = f"""
{split('<p class="eyebrow">Organic Cognac Producer in France</p><h2>Esprit Organic, organic Cognac from the Cognac region.</h2>', '<p>This page is written in English for international buyers. Esprit Organic is an organic Cognac brand led by Léopold and Fanny Croizet.</p><p>The range includes VS, VSOP, Napoléon, XO, XXO, Single Cask, white Pineau and red Pineau.</p><a class="button" href="importers.html">For Importers</a>')}
{section(location_cards)}
{section('<h2>Useful internal pages</h2><div class="link-list"><a href="produits/transmission-xo.html">Transmission XO</a><a href="production/">Organic approach</a><a href="demarche/">Production</a><a href="contact.html">Contact</a></div>')}
"""
    return layout("organic-cognac-producer-france.html", "Organic Cognac Producer in France | Cognac Esprit Organic", "Cognac Esprit Organic is an organic Cognac brand in France, with a range for Europe, USA and Canada.", "Organic Cognac Producer in France", "Page stratégique en anglais pour les acheteurs internationaux.", "Strategic English page for international buyers.", body)


def organic_proof_schema(page_path="agriculture-biologique.html", name="Certification biologique et preuves", lang="fr", description="Preuves publiques de certification Agriculture biologique Europe pour le Domaine de la Grande Versenne et Maison des Pierres SARL."):
    page = page_url(page_path)
    domaine_url = "https://certificat.ecocert.com/entreprise/08B9DD03-5B47-4067-B539-49D2382DC373"
    maison_url = "https://certificat.ecocert.com/entreprise/26299168-7D42-4646-845F-E0A5429B3227"
    annuaire_bio_url = "https://annuaire.agencebio.org/operateur/70760/domaine-de-la-grande-versenne"
    domaine_id = page + "#domaine-grande-versenne"
    maison_id = page + "#maison-des-pierres"
    domaine_cert_id = page + "#certification-domaine-grande-versenne"
    maison_cert_id = page + "#certification-maison-des-pierres"
    standard_id = page + "#agriculture-biologique-europe"
    ecocert_id = "https://certificat.ecocert.com/#organization"
    return {
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "WebSite",
                "@id": DOMAIN + "/#website",
                "name": "Cognac Esprit Organic",
                "url": DOMAIN + "/",
                "publisher": {"@id": DOMAIN + "/#organization"},
            },
            {
                "@type": "WebPage",
                "@id": page + "#webpage",
                "name": name,
                "alternateName": "Agriculture biologique" if lang == "fr" else "Organic agriculture",
                "url": page,
                "description": description,
                "inLanguage": lang,
                "dateModified": "2026-06-27",
                "isPartOf": {"@id": DOMAIN + "/#website"},
                "publisher": {"@id": DOMAIN + "/#organization"},
                "about": [
                    {"@id": domaine_id},
                    {"@id": maison_id},
                    {"@id": domaine_cert_id},
                    {"@id": maison_cert_id},
                ],
                "citation": [domaine_url, annuaire_bio_url, maison_url],
                "mainEntity": {
                    "@type": "ItemList",
                    "itemListElement": [
                        {"@type": "ListItem", "position": 1, "item": {"@id": domaine_cert_id}},
                        {"@type": "ListItem", "position": 2, "item": {"@id": maison_cert_id}},
                    ],
                },
            },
            {
                "@type": "DefinedTerm",
                "@id": standard_id,
                "name": "Agriculture biologique Europe",
                "termCode": "(EU) 2018/848 [FR]",
                "inDefinedTermSet": {
                    "@type": "DefinedTermSet",
                    "name": "Règlement européen de l'agriculture biologique",
                },
            },
            {
                "@type": "Organization",
                "@id": ecocert_id,
                "name": "Ecocert",
                "url": "https://certificat.ecocert.com/",
            },
            {
                "@type": "Organization",
                "@id": domaine_id,
                "name": "Domaine de la Grande Versenne",
                "url": domaine_url,
                "identifier": "08B9DD03-5B47-4067-B539-49D2382DC373",
                "address": {
                    "@type": "PostalAddress",
                    "streetAddress": "30 rue d'Angoulême",
                    "postalCode": "16200",
                    "addressLocality": "Triac-Lautrait",
                    "addressCountry": "FR",
                },
                "sameAs": [annuaire_bio_url],
                "hasCertification": {"@id": domaine_cert_id},
            },
            {
                "@type": "Certification",
                "@id": domaine_cert_id,
                "name": "Certification Agriculture biologique Europe",
                "url": domaine_url,
                "issuedBy": {"@id": ecocert_id},
                "about": {"@id": standard_id},
                "description": "Domaine de la Grande Versenne certifié Agriculture biologique Europe selon le règlement (UE) 2018/848 [FR]. Activités Ecocert : agriculteur, fabricant / préparateur.",
                "validIn": {"@type": "AdministrativeArea", "name": "Union européenne"},
            },
            {
                "@type": "Organization",
                "@id": maison_id,
                "name": "Maison des Pierres SARL",
                "url": maison_url,
                "identifier": "26299168-7D42-4646-845F-E0A5429B3227",
                "address": {
                    "@type": "PostalAddress",
                    "streetAddress": "30 rue d'Angoulême, Lantin",
                    "postalCode": "16200",
                    "addressLocality": "Triac-Lautrait",
                    "addressCountry": "FR",
                },
                "hasCertification": {"@id": maison_cert_id},
            },
            {
                "@type": "Certification",
                "@id": maison_cert_id,
                "name": "Certification Agriculture biologique Europe",
                "url": maison_url,
                "issuedBy": {"@id": ecocert_id},
                "about": {"@id": standard_id},
                "description": "Maison des Pierres SARL certifiée Agriculture biologique Europe selon le règlement (UE) 2018/848 [FR]. Activités Ecocert : distributeur, fabricant / préparateur, grossiste spécialisé.",
                "validIn": {"@type": "AdministrativeArea", "name": "Union européenne"},
            },
        ],
    }


def organic_proof_page():
    body = """
<section class="organic-proof-intro">
  <div class="section-inner organic-proof-intro-grid">
    <div>
      <p class="eyebrow">Preuves publiques</p>
      <h2>Le bio n’est pas une intention. C’est une traçabilité.</h2>
    </div>
    <div class="organic-proof-lead">
      <p>Cognac Esprit Organic s’appuie sur une production conduite en agriculture biologique au Domaine de la Grande Versenne et sur une structure de commercialisation certifiée, Maison des Pierres SARL.</p>
      <p>Les liens ci-dessous renvoient vers Ecocert et l’Annuaire Bio, organismes et annuaires publics consultés le 27 juin 2026.</p>
    </div>
  </div>
</section>
<section class="organic-proof-cards-section">
  <div class="section-inner">
    <div class="organic-proof-cards">
      <article class="organic-proof-card">
        <div class="organic-proof-card-media"><img src="assets/img/old-site/domaine-scaled.jpg" alt="Domaine de la Grande Versenne à Triac-Lautrait" loading="lazy"></div>
        <div class="organic-proof-card-copy">
          <p class="proof-kicker">Domaine viticole</p>
          <h2>Domaine de la Grande Versenne</h2>
          <ul class="proof-facts"><li><span>Adresse</span><strong>30 rue d’Angoulême, 16200 Triac-Lautrait</strong></li><li><span>Certification</span><strong>Agriculture biologique Europe</strong></li><li><span>Règlement</span><strong>(UE) 2018/848 [FR]</strong></li><li><span>Activités Ecocert</span><strong>Agriculteur, fabricant / préparateur</strong></li></ul>
          <div class="proof-links"><a class="button" href="https://certificat.ecocert.com/entreprise/08B9DD03-5B47-4067-B539-49D2382DC373" target="_blank" rel="noopener">Voir la fiche Ecocert</a><a class="text-link" href="https://annuaire.agencebio.org/operateur/70760/domaine-de-la-grande-versenne" target="_blank" rel="noopener">Voir l’Annuaire Bio</a></div>
        </div>
      </article>
      <article class="organic-proof-card reverse">
        <div class="organic-proof-card-media"><img src="assets/img/products/gamme-esprit-organic.jpg" alt="Gamme Cognac Esprit Organic issue de l'agriculture biologique" loading="lazy"></div>
        <div class="organic-proof-card-copy">
          <p class="proof-kicker">Maison et commercialisation</p>
          <h2>Maison des Pierres SARL</h2>
          <ul class="proof-facts"><li><span>Adresse</span><strong>30 rue d’Angoulême, Lantin, 16200 Triac-Lautrait</strong></li><li><span>Certification</span><strong>Agriculture biologique Europe</strong></li><li><span>Règlement</span><strong>(UE) 2018/848 [FR]</strong></li><li><span>Activités Ecocert</span><strong>Distributeur, fabricant / préparateur, grossiste spécialisé</strong></li></ul>
          <div class="proof-links"><a class="button" href="https://certificat.ecocert.com/entreprise/26299168-7D42-4646-845F-E0A5429B3227" target="_blank" rel="noopener">Voir la fiche Ecocert</a></div>
        </div>
      </article>
    </div>
  </div>
</section>
<section class="organic-certification-band">
  <div class="section-inner organic-certification-grid">
    <div class="organic-ab-mark"><img src="assets/img/logo-bio-home-tight.png" alt="Logo Agriculture biologique" loading="lazy"></div>
    <div><p class="eyebrow">Ce que cela engage</p><h2>De la vigne à la bouteille, une chaîne suivie.</h2><p>L’agriculture biologique encadre la culture de la vigne et les étapes de préparation contrôlées. Pour un cognac, cette exigence se lit dans la conduite du vignoble, la transformation, l’élevage, l’assemblage et la traçabilité administrative.</p><div class="organic-chain"><span>Vignes</span><span>Vin</span><span>Distillation</span><span>Élevage</span><span>Bouteille</span></div></div>
  </div>
</section>
<section class="organic-proof-note">
  <div class="section-inner organic-proof-note-grid">
    <div><h2>Un choix agricole avant d’être un argument.</h2></div>
    <div><p>La page ne cherche pas à promettre plus que ce que les preuves publiques montrent : des opérateurs identifiés, une certification Ecocert, une activité bio déclarée, et une cohérence entre le domaine, la maison et la gamme Cognac Esprit Organic.</p><div class="link-list"><a href="production/">Notre démarche</a><a href="demarche/">La production</a><a href="produits/transmission-xo.html">La gamme</a><a href="contact.html">Contact</a></div></div>
  </div>
</section>
"""
    return layout("agriculture-biologique.html", "Agriculture biologique | Cognac Esprit Organic", "Les preuves publiques de l'engagement bio Cognac Esprit Organic : Domaine de la Grande Versenne et Maison des Pierres certifiés Agriculture biologique Europe par Ecocert.", "Agriculture biologique", "Une démarche contrôlée, documentée, et visible dans les annuaires publics.", "A verified organic approach documented in public directories.", body, schemas=[organic_proof_schema()], image="assets/img/old-site/IMG_4079-scaled.jpg", page_class="organic-proof-page")


def contact_page():
    body = f"""
{split('<p class="eyebrow">Contact</p><h2 data-fr>Contacter Cognac Esprit Organic</h2><h2 data-en>Contact Cognac Esprit Organic</h2>', f'<ul class="meta-list"><li><span>Email</span><strong><a href="mailto:{CONTACT["email"]}">{CONTACT["email"]}</a></strong></li><li><span>Téléphone</span><strong><a href="tel:+33545358810">{CONTACT["phone"]}</a></strong></li><li><span>Adresse</span><strong>{CONTACT["address"]}</strong></li></ul>')}
{section('<h2 data-fr>Visites</h2><h2 data-en>Visits</h2><p data-fr>Horaires actuels : lundi-vendredi, 10h-12h ou 14h-17h. Durée : 1h. Maximum : 10 personnes.</p><p data-en>Current visiting hours: Monday-Friday, 10am-12pm or 2pm-5pm. Duration: 1 hour. Maximum: 10 people.</p>')}
"""
    return layout("contact.html", "Contact | Cognac Esprit Organic", "Contact Cognac Esprit Organic : email, téléphone, adresse à Triac-Lautrait et informations de visite.", "Contact Cognac Esprit Organic", "Email, téléphone, adresse et informations de visite validées.", "Email, phone, address and approved visit information.", body)


def visit_page():
    maps_query = "30%20Rue%20d%27Angouleme%2016200%20Triac-Lautrait%20France"
    body = f"""
<section class="visit-map-section">
  <div class="visit-map-copy">
    <h2 data-fr>Venez sur le territoire des Fins Bois</h2>
    <h2 data-en>Visit the Fins Bois area</h2>
    <p data-fr>Venez découvrir une petite distillerie nichée sur le territoire des Fins Bois. Nous serons heureux de vous accueillir et de vous faire découvrir quelques secrets de production et de nouvelles expériences gustatives.</p>
    <p data-en>Come and discover a small distillery in the Fins Bois area. We will be pleased to welcome you and share a few production secrets and tasting experiences.</p>
    <h3 data-fr>Horaires</h3>
    <h3 data-en>Opening times</h3>
    <p data-fr>Du lundi au vendredi, 10h-12h ou 14h-17h.</p>
    <p data-en>Monday to Friday, 10am-12pm or 2pm-5pm.</p>
    <ul>
      <li data-fr>Durée : 1h.</li>
      <li data-en>Duration: 1 hour.</li>
      <li data-fr>Maximum 10 personnes par visite.</li>
      <li data-en>Maximum 10 people per visit.</li>
      <li>30 Rue d'Angoulême, 16200 Triac-Lautrait.</li>
    </ul>
    <a class="visit-map-link" href="https://www.google.com/maps/search/?api=1&query={maps_query}" target="_blank" rel="noopener" data-fr>Ouvrir dans Google Maps</a>
    <a class="visit-map-link" href="https://www.google.com/maps/search/?api=1&query={maps_query}" target="_blank" rel="noopener" data-en>Open in Google Maps</a>
  </div>
  <div class="visit-map-frame">
    <iframe title="Carte Google Maps - Cognac Esprit Organic, Triac-Lautrait" src="https://www.google.com/maps?q={maps_query}&output=embed" loading="lazy" referrerpolicy="no-referrer-when-downgrade"></iframe>
  </div>
</section>
"""
    return layout("visiter.html", "Visiter | Cognac Esprit Organic", "Informations de visite Cognac Esprit Organic : lundi-vendredi, 10h-12h ou 14h-17h, durée 1h, maximum 10 personnes et carte Google Maps.", "Bienvenue sur nos terres", "Nous vous accueillons toute l’année. Contactez-nous !", "We welcome visitors throughout the year. Contact us!", body, image="assets/img/old-site/distillerie_02.jpg", page_class="visit-page")


def simple_page(path, title, desc, h1, intro_fr, intro_en, body):
    return layout(path, title, desc, h1, intro_fr, intro_en, body)


def faq_page():
    questions = [
        ("Quels produits Cognac Esprit Organic sont disponibles ?", "Les produits disponibles aujourd’hui sont VS, VSOP, Napoléon, XO, XXO, Single Cask, Pineau blanc et Pineau rouge."),
        ("Quels marchés export sont visés ?", "La formulation validée est : Europe, USA, Canada."),
        ("Où se situe Cognac Esprit Organic ?", CONTACT["address"]),
        ("Quels sont les horaires de visite ?", "Les visites sont possibles lundi-vendredi, 10h-12h ou 14h-17h, durée 1h, maximum 10 personnes."),
    ]
    faq_schema = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}}
            for q, a in questions
        ],
    }
    items = "".join(f'<article class="faq-item"><h2>{escape(q)}</h2><p>{escape(a)}</p></article>' for q, a in questions)
    return layout("faq.html", "FAQ | Cognac Esprit Organic", "Questions fréquentes sur Cognac Esprit Organic, la gamme, l'export et les visites.", "FAQ Cognac Esprit Organic", "Questions utiles pour les visiteurs et partenaires.", "Useful questions for visitors and partners.", section(items), schemas=[faq_schema])


def cocktails_page():
    body = """
<section class="old-duo page-duo">
  <div class="old-panel image-panel">
    <img src="assets/img/brand/home-cocktail.jpg" alt="Cocktail Cognac Esprit Organic">
    <span class="panel-copy haut-gauche"><strong data-fr>Accompagner nos Cognacs</strong><strong data-en>Pair our Cognacs</strong><small data-fr>Laisser courir l'inspiration</small><small data-en>Let inspiration flow</small></span>
  </div>
  <div class="old-panel text-panel green">
    <p data-fr>Cette page reprend l'univers cocktail de l'ancien site. Les recettes détaillées seront ajoutées uniquement après validation, afin de ne pas inventer d'accords ou de dosages.</p>
    <p data-en>This page carries over the cocktail universe of the former website. Detailed recipes will be added only after approval, without inventing pairings or measures.</p>
  </div>
</section>
<section class="cream-signature compact">
  <div>
    <p data-fr>À compléter</p>
    <p data-en>To complete</p>
    <span>•••</span>
    <strong data-fr>Prévoir ici les cocktails validés, les ingrédients, les étapes, les visuels et les produits Esprit Organic associés.</strong>
    <strong data-en>Approved cocktails, ingredients, steps, images and associated Esprit Organic products will be added here.</strong>
  </div>
</section>
"""
    return layout("cocktails.html", "Cocktails | Cognac Esprit Organic", "Page cocktails Cognac Esprit Organic : accompagnements et recettes à intégrer après validation.", "Accompagner nos Cognacs", "L'univers cocktail du site, reconstruit sans inventer de recettes.", "The cocktail universe rebuilt without inventing recipes.", body, image="assets/img/brand/home-cocktail.jpg")


def gallery_page():
    files = sorted((ROOT / "assets/img/old-site").glob("*"))
    allowed = {".jpg", ".jpeg", ".png", ".svg"}
    items = []
    for file in files:
        if file.suffix.lower() not in allowed:
            continue
        label = file.stem.replace("_", " ").replace("-", " ")
        items.append(
            f'<figure><img src="assets/img/old-site/{escape(file.name)}" alt="Ancien site Cognac Esprit Organic - {escape(label)}" loading="lazy"><figcaption>{escape(label)}</figcaption></figure>'
        )
    body = f"""
<section>
  <div class="section-inner">
    <p class="eyebrow">Archives visuelles</p>
    <h2 data-fr>Photos et visuels récupérés de l'ancien site</h2>
    <h2 data-en>Images recovered from the former website</h2>
    <p data-fr>Cette galerie rassemble les visuels utiles récupérés depuis l'ancien site WordPress. Elle sert de réserve propre pour reconstruire les pages sans dépendre de WordPress.</p>
    <p data-en>This gallery gathers useful visuals recovered from the former WordPress website. It provides a clean reserve for rebuilding pages without depending on WordPress.</p>
    <div class="legacy-gallery">{''.join(items)}</div>
  </div>
</section>
"""
    return layout("galerie.html", "Galerie | Cognac Esprit Organic", "Galerie des photos et visuels récupérés de l'ancien site Cognac Esprit Organic.", "Galerie Cognac Esprit Organic", "Les photos et visuels récupérés de l'ancien site, regroupés dans une page propre.", "Recovered images from the former website, gathered in a clean page.", body, image="assets/img/brand/hero-old-vine.jpg")


def nutrition_page():
    cards = []
    for product in PRODUCTS:
        if product["slug"] in NUTRITION_VALUES:
            cards.append(
                f"""
      <article class="nutrition-card">
        <h3>{escape(product["name"])}</h3>
        <p>{escape(product["category"])}</p>
{nutrition_table(product["slug"], product["name"])}
      </article>
"""
            )
    body = f"""
<section>
  <div class="section-inner">
    <p class="eyebrow">Nutrition</p>
    <h2 data-fr>Valeurs nutritionnelles par produit</h2>
    <h2 data-en>Nutritional values by product</h2>
    <p data-fr>Les valeurs sont indiquées pour 30 ml et 100 ml, avec l'énergie dans l'ordre réglementaire kJ / kcal.</p>
    <p data-en>Values are shown per 30 ml and per 100 ml, with energy displayed in the regulatory kJ / kcal order.</p>
    <div class="nutrition-list">{''.join(cards)}</div>
  </div>
</section>
"""
    return layout("valeurs-nutritionnelles.html", "Valeurs nutritionnelles | Cognac Esprit Organic", "Valeurs nutritionnelles Cognac Esprit Organic par produit, pour 30 ml et 100 ml.", "Valeurs nutritionnelles", "Les tableaux nutritionnels Esprit Organic avec l'énergie en kJ / kcal.", "Cognac Esprit Organic nutritional tables with energy shown in kJ / kcal.", body, image="assets/img/brand/hero-old-vine.jpg")


def technical_product_rows(product, lang="fr"):
    extra = PRODUCT_EXTRAS.get(product["slug"], {})
    if lang == "en":
        rows = [
            ("Brand", "Cognac Esprit Organic"),
            ("Product", product["name"]),
            ("Category", english_category(product)),
            ("Origin", "France"),
            ("Short profile", product["en_short"]),
            ("Bottle size", product["volume"]),
            ("Alcohol by volume", english_abv(product["abv"])),
            ("Grape varieties", product["grapes"]),
        ]
        rows.extend(EN_SENSORY.get(product["slug"], {}).items())
        return rows
    rows = [
        ("Marque", "Cognac Esprit Organic"),
        ("Produit", product["name"]),
        ("Catégorie", product["category"]),
        ("Origine", "France"),
        ("Profil court", product["short"]),
        ("Contenance", product["volume"]),
        ("Titre alcoométrique", product["abv"]),
        ("Cépages", product["grapes"]),
    ]
    rows.extend(extra.get("sensory", {}).items())
    return rows


def english_category(product):
    category_map = {
        "Pineau des Charentes blanc": "White Pineau des Charentes",
        "Pineau des Charentes rouge": "Red Pineau des Charentes",
    }
    return category_map.get(product["category"], product["category"])


def english_abv(value):
    return value.replace(",", ".").replace(" %", "%")


def technical_award_name(award, lang):
    return award.get("en_name" if lang == "en" else "name", award["name"])


def technical_award_proof_label(award, lang):
    return award.get("en_proof_label" if lang == "en" else "proof_label", award["proof_label"])


def documented_award(product):
    return DOCUMENTED_AWARDS.get(product["slug"])


def technical_product_item(product, lang="fr"):
    excluded = {"Brand", "Product", "Category", "Short profile"} if lang == "en" else {"Marque", "Produit", "Catégorie", "Profil court"}
    properties = [
        property_value(label, value)
        for label, value in technical_product_rows(product, lang)
        if label not in excluded
    ]
    award = documented_award(product)
    if award:
        properties.append(property_value("Documented award" if lang == "en" else "Récompense documentée", technical_award_proof_label(award, lang)))
    url_prefix = "en/" if lang == "en" else ""
    item = {
        "@type": "Product",
        "name": product["name"],
        "url": page_url(f"{url_prefix}produits/{product['slug']}.html"),
        "brand": {"@type": "Brand", "name": "Cognac Esprit Organic", "@id": DOMAIN + "/#brand"},
        "manufacturer": {"@id": DOMAIN + "/#organization"},
        "category": english_category(product) if lang == "en" else product["category"],
        "image": DOMAIN + "/" + product["image"],
        "description": product["en_short"] if lang == "en" else product["short"],
        "size": product["volume"],
        "additionalProperty": properties,
    }
    if award:
        item["award"] = technical_award_name(award, lang)
    return item


def technical_alternate_links(path):
    first_segment = path.split("/", 1)[0]
    base_path = path.split("/", 1)[1] if first_segment in {"en", "da", "no", "sv"} else path
    localized_paths = {
        "fr": base_path,
        "en": f"en/{base_path}",
        "da": f"da/{base_path}",
        "no": f"no/{base_path}",
        "sv": f"sv/{base_path}",
    }
    return "\n  ".join([
        '<!-- Locale alternates -->',
        *(f'<link rel="alternate" hreflang="{lang}" href="{page_url(localized_path)}">' for lang, localized_path in localized_paths.items()),
        f'<link rel="alternate" hreflang="x-default" href="{page_url(base_path)}">',
        '<!-- /Locale alternates -->',
    ])


def technical_product_cards(lang="fr"):
    asset_prefix = "../" if lang == "en" else ""
    product_link_prefix = "produits/"
    award_label = "Documented award" if lang == "en" else "Récompense documentée"
    product_link_text = "View product page" if lang == "en" else "Voir la fiche produit"
    caption_prefix = "Product data" if lang == "en" else "Données produit"
    index_links = "".join(
        f'<a href="#{escape(product["slug"])}">{escape(product["name"])}</a>'
        for product in PRODUCTS
    )
    cards = []
    for product in PRODUCTS:
        award = documented_award(product)
        rows = "".join(
            f'<tr><th scope="row">{escape(label)}</th><td>{escape(value)}</td></tr>'
            for label, value in technical_product_rows(product, lang)
        )
        if award:
            rows += (
                f'<tr class="technical-award-row"><th scope="row">{escape(award_label)}</th>'
                f'<td><span>{escape(technical_award_name(award, lang))}</span> '
                f'<a class="technical-proof-link" href="{escape(award["url"])}" target="_blank" rel="noopener noreferrer">'
                f'{escape(technical_award_proof_label(award, lang))}</a></td></tr>'
            )
        category = english_category(product) if lang == "en" else product["category"]
        short = product["en_short"] if lang == "en" else product["short"]
        answer = (
            f'{escape(product["name"])} is part of the Cognac Esprit Organic range, classified as {escape(category)}. {escape(short)}'
            if lang == "en"
            else f'{escape(product["name"])} est un produit de la gamme Cognac Esprit Organic, classé {escape(category)}. {escape(short)}'
        )
        cards.append(
            f"""
      <article class="technical-product-card" id="{escape(product["slug"])}">
        <header>
          <div>
            <h2>{escape(product["name"])}</h2>
            <p class="tag">{escape(category)}</p>
          </div>
          <a class="text-link" href="{product_link_prefix}{escape(product["slug"])}.html">{escape(product_link_text)}</a>
        </header>
        <p class="technical-answer">{answer}</p>
        <div class="nutrition-table-wrap">
          <table class="nutrition-table">
            <caption>{escape(caption_prefix)} - {escape(product["name"])}</caption>
            <tbody>{rows}</tbody>
          </table>
        </div>
      </article>
"""
        )
    return index_links, "".join(cards), asset_prefix


def technical_item_list(lang="fr"):
    path = "en/fiches-techniques-produits.html" if lang == "en" else "fiches-techniques-produits.html"
    item_list = {
        "@context": "https://schema.org",
        "@type": "ItemList",
        "name": "Cognac Esprit Organic product data and professional documents" if lang == "en" else "Données produits et documents professionnels Cognac Esprit Organic",
        "itemListElement": [
            {"@type": "ListItem", "position": index + 1, "item": technical_product_item(product, lang)}
            for index, product in enumerate(PRODUCTS)
        ],
        "@id": page_url(path) + "#products",
    }
    return item_list


def technical_product_facts_page():
    index_links, cards_html, asset_prefix = technical_product_cards("fr")
    item_list = technical_item_list("fr")
    body = f"""
<section class="product-data-intro">
  <div class="section-inner">
    <p class="eyebrow">Données produit</p>
    <h2>Données produits et documents professionnels</h2>
    <p>Cette page regroupe les faits stables des produits Cognac Esprit Organic dans un format clair, consultable et réutilisable par les partenaires professionnels. Elle ne remplace pas les fiches commerciales ; elle sert de page de référence documentaire.</p>
    <p>Les tableaux ci-dessous n'ajoutent pas de prix, de stock, d'avis client, de certification non affichée, ni de récompense sans preuve consultable.</p>
    <figure class="technical-hero-image">
      <img src="{asset_prefix}assets/img/products/gamme-esprit-organic.jpg" alt="Gamme Cognac Esprit Organic : Fondation VS, Conviction VSOP, Cohesion Napoléon et Transmission XO" width="1800" height="1130" loading="lazy">
      <figcaption>Gamme Cognac Esprit Organic : fiches commerciales et données techniques reliées dans une même source publique.</figcaption>
    </figure>
    <nav class="technical-index" aria-label="Accès rapide aux données produit">{index_links}</nav>
    <p class="technical-note">Référence professionnelle : cette page centralise les informations stables de la gamme et les relie aux pages produit.</p>
  </div>
</section>
<section>
  <div class="section-inner">
    <div class="technical-product-list">{cards_html}</div>
  </div>
</section>
"""
    return layout(
        "fiches-techniques-produits.html",
        "Données produits et documents professionnels | Cognac Esprit Organic",
        "Données factuelles des produits Cognac Esprit Organic pour partenaires professionnels : catégories, contenances, titres alcoométriques, cépages, notes et preuves.",
        "Données produits et documents professionnels",
        "Une page de référence factuelle, séparée des fiches commerciales.",
        "A factual reference page, separate from commercial product pages.",
        body,
        schemas=[item_list],
        image="assets/img/brand/hero-old-vine.jpg",
        page_class="product-data-page",
        head_extra=technical_alternate_links("fiches-techniques-produits.html"),
    )


def technical_product_facts_page_en():
    index_links, cards_html, asset_prefix = technical_product_cards("en")
    path = "en/fiches-techniques-produits.html"
    canonical = page_url(path)
    item_list = technical_item_list("en")
    schema_items = [
        organization_schema(),
        {
            "@context": "https://schema.org",
            "@type": "BreadcrumbList",
            "itemListElement": [
                {"@type": "ListItem", "position": 1, "name": "Home", "item": DOMAIN + "/en/"},
                {"@type": "ListItem", "position": 2, "name": "Product data and professional documents", "item": canonical},
            ],
            "@id": canonical + "#breadcrumb",
        },
        item_list,
    ]
    product_menu_links = "".join(
        f'<a href="produits/{escape(product["slug"])}.html">{escape(product["name"])}</a>'
        for product in PRODUCTS
    )
    body = f"""
<section class="product-data-intro">
  <div class="section-inner">
    <p class="eyebrow">Product data</p>
    <h2>Product data and professional documents</h2>
    <p>This page brings together stable facts about Cognac Esprit Organic products in a clear, consultable format for professional partners. It does not replace the commercial product pages; it is a documentary reference page.</p>
    <p>The tables below do not add prices, stock, customer reviews, undisplayed certification, or awards without a consultable proof source.</p>
    <figure class="technical-hero-image">
      <img src="{asset_prefix}assets/img/products/gamme-esprit-organic.jpg" alt="Cognac Esprit Organic range: Fondation VS, Conviction VSOP, Cohesion Napoléon and Transmission XO" width="1800" height="1130" loading="lazy">
      <figcaption>Cognac Esprit Organic range: commercial pages and technical product data connected in one public source.</figcaption>
    </figure>
    <nav class="technical-index" aria-label="Quick access to product data">{index_links}</nav>
    <p class="technical-note">Professional reference: this page centralises stable range information and links it to the product pages.</p>
  </div>
</section>
<section>
  <div class="section-inner">
    <div class="technical-product-list">{cards_html}</div>
  </div>
</section>
"""
    return f"""<!doctype html>
<html lang="en" data-default-lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Product data and professional documents | Cognac Esprit Organic</title>
  <meta name="description" content="Factual product data for Cognac Esprit Organic professional partners: categories, bottle sizes, alcohol by volume, grape varieties, tasting notes and proof links.">
  <meta name="robots" content="index,follow">
  <link rel="canonical" href="{canonical}">
  {technical_alternate_links(path)}
  <meta property="og:title" content="Product data and professional documents | Cognac Esprit Organic">
  <meta property="og:description" content="Factual product data for Cognac Esprit Organic professional partners: categories, bottle sizes, alcohol by volume, grape varieties, tasting notes and proof links.">
  <meta property="og:type" content="website">
  <meta property="og:image" content="{DOMAIN}/assets/img/brand/hero-old-vine.jpg">
  <link rel="icon" href="../assets/img/fav_organic.png">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@300;400;500;600;700;800;900&family=Raleway:wght@200;300;400;500;600;700;800;900&family=Roboto+Slab:wght@200;300;400;500;600;700;800&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="../assets/css/styles.css?v=20260627-technical-facts01">
  {json_ld(schema_items)}
</head>
<body data-lang="en" class="product-data-page">
  <a class="skip-link" href="#contenu">Skip to content</a>
  <header class="site-header">
    <nav class="nav" aria-label="Primary navigation">
      <a class="brand" href="/en/" aria-label="Cognac Esprit Organic">
        <img src="../assets/img/logo-esprit-organic-brown.svg" alt="Cognac Esprit Organic">
      </a>
      <button class="nav-toggle" type="button" data-nav-toggle aria-expanded="false" aria-label="Open menu">Menu</button>
      <div class="nav-links" data-nav-links>
<div class="nav-dropdown">
  <a href="produits/transmission-xo.html"><span data-fr>The range</span><span data-en>The range</span></a>
  <div class="dropdown-menu" role="menu">{product_menu_links}</div>
</div>
<div class="nav-dropdown">
  <a href="production/"><span data-fr>The house</span><span data-en>The house</span></a>
  <div class="dropdown-menu" role="menu"><a href="production/"><span data-fr>Our approach</span><span data-en>Our approach</span></a><a href="demarche/"><span data-fr>Production</span><span data-en>Production</span></a><a href="leopold-et-fanny/"><span data-fr>Léopold and Fanny</span><span data-en>Léopold and Fanny</span></a><a href="equipe/"><span data-fr>The team</span><span data-en>The team</span></a></div>
</div>
<a href="visiter.html"><span data-fr>Visit</span><span data-en>Visit</span></a>
<div class="lang-menu" data-lang-menu><button class="lang-toggle" type="button" data-lang-toggle aria-haspopup="true" aria-expanded="false">EN</button><div class="lang-menu-panel" role="menu" aria-label="Choose language"><button type="button" class="lang-option" data-lang-option="fr" role="menuitem">FR</button><button type="button" class="lang-option" data-lang-option="en" role="menuitem">EN</button><button type="button" class="lang-option" data-lang-option="da" role="menuitem">DA</button><button type="button" class="lang-option" data-lang-option="no" role="menuitem">NO</button><button type="button" class="lang-option" data-lang-option="sv" role="menuitem">SV</button></div></div><a class="header-bio-link" href="agriculture-biologique.html" aria-label="Organic agriculture"><img class="header-bio" src="../assets/img/logo-bio-home-tight.png" alt="Organic agriculture"></a></div>
    </nav>
  </header>
  <main id="contenu">
    <section class="page-hero" style="--hero-image: url('/assets/img/brand/hero-old-vine.jpg')">
      <div class="section-inner narrow">
        <p class="eyebrow">Cognac Esprit Organic</p>
        <h1>Product data and professional documents</h1>
        <p class="lead" data-fr>A factual reference page, separate from commercial product pages.</p>
        <p class="lead" data-en>A factual reference page, separate from commercial product pages.</p>
      </div>
    </section>
    {body}
  </main>
  <footer class="site-footer">
    <div class="footer-grid">
      <div>
        <img class="footer-logo" src="../assets/img/logo-esprit-organic-white.svg" alt="Cognac Esprit Organic">
        <p class="small">Alcohol abuse is dangerous for your health. Consume in moderation.</p>
      </div>
      <div class="footer-links">
        <a href="produits/transmission-xo.html">Range</a>
        <a href="faq.html">FAQ</a>
        <a href="cocktails.html">Cocktails</a>
      </div>
    </div>
  </footer>
  <script src="../assets/js/main.js?v=20260629-faq01"></script>
</body>
</html>
"""


def legal_page():
    body = f"""
<section>
  <div class="section-inner split">
    <div>
      <p class="eyebrow">Informations légales</p>
      <h2 data-fr>Brouillon à confirmer</h2>
      <h2 data-en>Draft to confirm</h2>
      <p data-fr>Les informations confirmées sont limitées aux coordonnées affichées ci-contre. Les mentions légales complètes restent à valider ; cette page est donc en noindex temporaire.</p>
      <p data-en>Only the contact details shown here are confirmed. The complete legal notice still needs validation, so this page uses a temporary noindex.</p>
    </div>
    <div>
      <ul class="meta-list">
        <li><span>Site</span><strong>{DOMAIN}</strong></li>
        <li><span>Marque</span><strong>Cognac Esprit Organic</strong></li>
        <li><span>Email</span><strong>{CONTACT['email']}</strong></li>
        <li><span>Téléphone</span><strong>{CONTACT['phone']}</strong></li>
        <li><span>Adresse</span><strong>{CONTACT['address']}</strong></li>
        <li><span>Éditeur du site</span><strong>à confirmer</strong></li>
        <li><span>Forme juridique</span><strong>à confirmer</strong></li>
        <li><span>Numéro d'immatriculation</span><strong>à confirmer</strong></li>
        <li><span>TVA intracommunautaire</span><strong>à confirmer</strong></li>
        <li><span>Responsable de publication</span><strong>à confirmer</strong></li>
        <li><span>Hébergeur</span><strong>à confirmer</strong></li>
      </ul>
    </div>
  </div>
</section>
"""
    return layout("mentions-legales.html", "Mentions légales | Cognac Esprit Organic", "Mentions légales Cognac Esprit Organic : informations connues et champs à confirmer.", "Mentions légales", "Informations connues et champs à confirmer avant publication.", "Known information and fields to confirm before publication.", body, image="assets/img/brand/hero-old-vine.jpg", robots="noindex,nofollow")


def write_css():
    css = r''':root {
  --ink: #17130f;
  --muted: #6b5d50;
  --paper: #ece8dc;
  --cream: #fbf8ee;
  --panel: #ded6c4;
  --line: rgba(94, 61, 35, .22);
  --brand: #704019;
  --brand-dark: #3b2113;
  --leaf: #63a55a;
  --green-dark: #2f4a2b;
  --gold: #b78a43;
  --white: #ffffff;
  --shadow: 0 26px 70px rgba(23, 19, 15, .18);
  --radius: 8px;
  font-family: Montserrat, Arial, sans-serif;
}
* { box-sizing: border-box; }
html { scroll-behavior: smooth; }
body { margin: 0; color: var(--ink); background: var(--paper); font-family: Montserrat, Arial, sans-serif; line-height: 1.62; }
body[data-lang="fr"] [data-en],
body[data-lang="en"] [data-fr],
body[data-lang="da"] [data-en],
body[data-lang="no"] [data-en],
body[data-lang="sv"] [data-en] { display: none !important; }
a { color: inherit; }
img { display: block; max-width: 100%; height: auto; }
.skip-link { position: absolute; left: 16px; top: -60px; z-index: 50; background: var(--ink); color: var(--white); padding: 10px 14px; }
.skip-link:focus { top: 16px; }
.site-header { position: sticky; top: 0; z-index: 20; border-bottom: 1px solid rgba(94, 61, 35, .18); background: rgba(236, 232, 220, .92); backdrop-filter: blur(14px); }
.home-page .site-header { position: fixed; left: 0; right: 0; background: rgba(0,0,0,.35); border-bottom-color: rgba(255,255,255,.08); }
.nav { width: min(1240px, calc(100% - 40px)); min-height: 86px; margin: 0 auto; display: flex; align-items: center; gap: 22px; }
.home-page .nav { min-height: 100px; }
.brand img { width: 168px; }
.home-page .brand img { width: 200px; filter: brightness(0) invert(1); }
.nav-toggle, .lang-toggle { border: 1px solid var(--line); background: var(--cream); color: var(--ink); min-height: 42px; border-radius: var(--radius); font-weight: 800; cursor: pointer; }
.nav-toggle { display: none; margin-left: auto; padding: 0 12px; }
.lang-toggle { min-width: 46px; }
.lang-menu { position: relative; display: inline-flex; }
.lang-menu-panel {
  position: absolute;
  right: 0;
  top: calc(100% + 8px);
  z-index: 35;
  min-width: 84px;
  padding: 8px;
  border: 1px solid rgba(94, 61, 35, .18);
  background: var(--cream);
  box-shadow: 0 16px 34px rgba(23,19,15,.16);
  opacity: 0;
  visibility: hidden;
  transform: translateY(8px);
  transition: opacity .18s ease, transform .18s ease, visibility .18s ease;
}
.lang-menu.is-open .lang-menu-panel,
.lang-menu:hover .lang-menu-panel,
.lang-menu:focus-within .lang-menu-panel { opacity: 1; visibility: visible; transform: translateY(0); }
.lang-option {
  display: block;
  width: 100%;
  min-height: 34px;
  border: 0;
  background: transparent;
  color: var(--brand);
  font-family: Montserrat, Arial, sans-serif;
  font-size: .78rem;
  font-weight: 800;
  text-align: left;
  cursor: pointer;
}
.lang-option:hover,
.lang-option:focus-visible,
.lang-option[aria-current="true"] { background: rgba(94, 61, 35, .08); }
.header-bio-link {
  display: block;
  width: 88px;
  align-self: center;
  margin-left: 4px;
  line-height: 0;
  border-radius: 6px;
  outline-offset: 4px;
}
.header-bio {
  display: block;
  width: 100%;
  height: auto;
  object-fit: contain;
  padding: 0;
  background: transparent;
}
.home-page .header-bio-link {
  width: 112px;
}
.nav-links { display: flex; align-items: center; gap: 14px; margin-left: auto; font-size: .94rem; }
.nav-links a { text-decoration: none; color: var(--muted); padding: 10px 2px; white-space: nowrap; text-transform: uppercase; letter-spacing: .06em; font-size: .78rem; font-weight: 800; }
.nav-dropdown { position: relative; padding: 18px 0; }
.dropdown-menu {
  position: absolute;
  left: 50%;
  top: calc(100% - 4px);
  z-index: 30;
  min-width: 178px;
  padding: 16px 0;
  background: #6fa663;
  box-shadow: 0 16px 34px rgba(23,19,15,.18);
  opacity: 0;
  visibility: hidden;
  transform: translate(-50%, 8px);
  transition: opacity .18s ease, transform .18s ease, visibility .18s ease;
}
.nav-dropdown:hover .dropdown-menu,
.nav-dropdown:focus-within .dropdown-menu {
  opacity: 1;
  visibility: visible;
  transform: translate(-50%, 0);
}
.nav-links .dropdown-menu a,
.home-page .nav-links .dropdown-menu a {
  display: block;
  padding: 8px 22px;
  color: #fff;
  font-size: .72rem;
  letter-spacing: .02em;
  text-transform: uppercase;
  white-space: nowrap;
}
.nav-links .dropdown-menu a:hover,
.nav-links .dropdown-menu a:focus-visible {
  background: rgba(255,255,255,.13);
  color: #fff;
}
.home-page .nav-links a { color: rgba(255,255,255,.9); }
.home-page .lang-toggle {
  border: 0;
  background: transparent;
  color: #fff;
  font-family: "Roboto Slab", Georgia, serif;
  font-size: .95rem;
  min-width: auto;
}
.nav-links a[aria-current="page"], .nav-links a:hover { color: var(--green-dark); }
.home-page .nav-links a[aria-current="page"], .home-page .nav-links a:hover { color: var(--white); }
.page-hero { min-height: 66vh; padding: 150px 0 82px; display: grid; align-items: end; color: var(--cream); background: linear-gradient(90deg, rgba(23,19,15,.82), rgba(23,19,15,.38), rgba(23,19,15,.08)), var(--hero-image) center / cover; border-bottom: 1px solid var(--line); }
.home-page .page-hero { background: linear-gradient(90deg, rgba(23,19,15,.78), rgba(23,19,15,.28), rgba(23,19,15,.02)), var(--hero-image) center / cover; }
.home-page .page-hero { min-height: 100svh; padding-top: 170px; }
.home-page .page-hero::after { content: ""; position: absolute; z-index: 1; left: 0; right: 0; bottom: 0; height: 110px; background: linear-gradient(0deg, var(--paper), rgba(236,232,220,0)); pointer-events: none; }
.page-hero { position: relative; }
.video-hero {
  overflow: hidden;
  background: #21170f;
}
.video-hero::before {
  content: "";
  position: absolute;
  inset: 0;
  z-index: 1;
  background: linear-gradient(90deg, rgba(23,19,15,.72), rgba(23,19,15,.34), rgba(23,19,15,.18));
}
.video-hero .section-inner {
  position: relative;
  z-index: 2;
}
.hero-bg-video {
  position: absolute;
  inset: 0;
  width: 100%;
  height: 100%;
  object-fit: cover;
  object-position: center;
}
.section-inner { width: min(1240px, calc(100% - 40px)); margin: 0 auto; }
.narrow { max-width: 920px; }
section { padding: 74px 0; }
.soft { background: #e2dccd; }
.eyebrow { margin: 0 0 14px; color: var(--gold); text-transform: uppercase; letter-spacing: .22em; font-size: .74rem; font-weight: 900; }
h1, h2, h3 { font-family: Georgia, "Times New Roman", serif; line-height: 1.08; margin: 0; font-weight: 500; letter-spacing: 0; }
h1 { max-width: 900px; font-size: clamp(3.4rem, 8vw, 7.8rem); text-wrap: balance; }
h2 { font-size: clamp(2.05rem, 4vw, 4.2rem); text-wrap: balance; }
h3 { font-size: 1.38rem; }
.subhead { margin-top: 34px; font-size: clamp(1.45rem, 2vw, 2rem); }
p { margin: 18px 0 0; }
.lead { max-width: 760px; margin-top: 20px; font-size: clamp(1.08rem, 2vw, 1.35rem); color: rgba(255,255,255,.86); }
.actions { display: flex; flex-wrap: wrap; gap: 12px; margin-top: 28px; }
.button { display: inline-flex; align-items: center; justify-content: center; min-height: 48px; padding: 13px 20px; border: 1px solid var(--brand); border-radius: 0; background: var(--brand); color: var(--white); text-decoration: none; font-weight: 900; text-transform: uppercase; letter-spacing: .08em; font-size: .78rem; }
.button.secondary { background: transparent; color: inherit; border-color: currentColor; }
.text-link { display: inline-block; margin-top: 18px; color: var(--brand-dark); font-weight: 900; text-transform: uppercase; letter-spacing: .08em; font-size: .8rem; }
.split { display: grid; grid-template-columns: minmax(0, 1fr) minmax(280px, 430px); gap: 62px; align-items: start; }
.split.wide { grid-template-columns: minmax(0, .8fr) minmax(320px, 1fr); }
.editorial-intro { padding-top: 96px; background: var(--paper); }
.range-showcase { background: var(--cream); }
.section-heading { display: flex; align-items: end; justify-content: space-between; gap: 24px; margin-bottom: 30px; }
.section-heading h2 { max-width: 760px; }
.product-grid { display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); gap: 2px; margin-top: 28px; }
.product-grid.compact { grid-template-columns: repeat(3, minmax(0, 1fr)); }
.card, .feature-grid article, .media-steps article { padding: 28px; border: 1px solid var(--line); border-radius: var(--radius); background: var(--cream); box-shadow: 0 8px 24px rgba(27, 23, 18, .06); }
.product-card { position: relative; display: flex; flex-direction: column; gap: 12px; min-height: 100%; padding: 24px; text-decoration: none; color: var(--cream); background: radial-gradient(circle at 50% 22%, rgba(255,255,255,.18), transparent 34%), linear-gradient(160deg, #704019, #2a1a12); overflow: hidden; transition: transform .45s ease, box-shadow .45s ease; }
.product-card:nth-child(even) { background: radial-gradient(circle at 50% 22%, rgba(255,255,255,.18), transparent 34%), linear-gradient(160deg, #5e3d23, #263a24); }
.product-card:hover { transform: translateY(-8px); box-shadow: var(--shadow); }
.product-card img { aspect-ratio: 4 / 5; width: 100%; object-fit: contain; filter: drop-shadow(0 26px 28px rgba(0,0,0,.34)); transform: scale(.94); transition: transform .45s ease; }
.product-card:hover img { transform: scale(1); }
.product-card p { color: rgba(255,255,255,.82); font-size: .94rem; }
.tag { align-self: flex-start; padding: 4px 0; border-bottom: 1px solid rgba(255,255,255,.4); color: var(--leaf); font-size: .76rem; font-weight: 900; text-transform: uppercase; letter-spacing: .1em; }
.product-card .tag { color: #d4c29c; }
.feature-grid { display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 18px; }
.media-steps { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 22px; }
.media-steps img { aspect-ratio: 16 / 10; width: 100%; object-fit: cover; border-radius: var(--radius); margin-bottom: 18px; }
.image-band { min-height: 68vh; display: grid; align-items: end; color: var(--cream); background: linear-gradient(90deg, rgba(23,19,15,.84), rgba(23,19,15,.24)), var(--band-image) center / cover; }
.image-band h2 { max-width: 820px; margin-bottom: 26px; }
.product-detail { background: linear-gradient(90deg, var(--paper) 0 50%, var(--brand-dark) 50%); }
.product-layout { display: grid; grid-template-columns: minmax(280px, 48%) minmax(0, 1fr); gap: 2px; align-items: stretch; }
.product-image-panel { min-height: 680px; display: grid; place-items: center; padding: 42px; background: radial-gradient(circle at 50% 22%, #fff8e6, #d8cfbd 56%, #c7baa3); border: 1px solid var(--line); }
.product-image-panel img { width: 100%; max-height: 640px; object-fit: contain; filter: drop-shadow(0 32px 34px rgba(0,0,0,.28)); }
.product-layout > div:last-child { padding: clamp(34px, 6vw, 76px); background: var(--brand-dark); color: var(--cream); }
.product-layout > div:last-child p { color: rgba(255,255,255,.82); }
.meta-list { padding: 0; margin: 24px 0 0; list-style: none; border-top: 1px solid var(--line); }
.meta-list li { display: flex; justify-content: space-between; gap: 20px; padding: 13px 0; border-bottom: 1px solid var(--line); }
.meta-list span { color: var(--muted); }
.dark-list { border-color: rgba(255,255,255,.24); }
.dark-list li { border-color: rgba(255,255,255,.24); }
.dark-list span { color: rgba(255,255,255,.62); }
.visit-page .page-hero {
  min-height: 48vh;
  padding: 150px 0 78px;
  text-align: center;
  align-items: center;
  background-image: linear-gradient(rgba(20,15,10,.42), rgba(20,15,10,.42)), var(--hero-image);
}
.visit-page .page-hero .narrow {
  margin-inline: auto;
}
.visit-map-section {
  display: grid;
  grid-template-columns: minmax(280px, 32%) minmax(0, 1fr);
  gap: 0;
  padding: 0;
  border-top: 2px solid var(--paper);
  border-bottom: 2px solid var(--paper);
}
.visit-map-copy {
  display: grid;
  align-content: center;
  min-height: 520px;
  padding: clamp(34px, 5vw, 78px);
  background: #522E03;
  color: var(--paper);
  text-align: center;
}
.visit-map-copy h2,
.visit-map-copy h3 {
  margin: 0 0 18px;
  color: inherit;
  font-family: "Roboto Slab", Georgia, serif;
  line-height: 1.08;
}
.visit-map-copy h2 { font-size: clamp(1.45rem, 2.25vw, 2.2rem); }
.visit-map-copy h3 { margin-top: 24px; font-size: clamp(1.25rem, 1.9vw, 1.75rem); }
.visit-map-copy p {
  max-width: 440px;
  margin: 0 auto;
  color: rgba(255,255,255,.9);
  font-size: clamp(.88rem, 1vw, 1rem);
  line-height: 1.55;
}
.visit-map-copy p + p { margin-top: 10px; }
.visit-map-copy ul {
  max-width: 440px;
  margin: 16px auto 0;
  padding: 0;
  list-style: none;
  color: rgba(255,255,255,.9);
  font-size: clamp(.86rem, .95vw, .98rem);
  line-height: 1.55;
}
.visit-map-link {
  width: fit-content;
  margin: 22px auto 0;
  color: #fff;
  font-size: .86rem;
  font-weight: 800;
}
.visit-map-frame {
  min-height: 520px;
  background: #ded8c8;
}
.visit-map-frame iframe {
  display: block;
  width: 100%;
  height: 100%;
  min-height: 520px;
  border: 0;
}
.pill-list, .check-list { padding-left: 20px; }
.pill-list li { margin: 8px 0; }
.note { margin-top: 24px; padding: 16px 18px; border-left: 4px solid var(--leaf); background: rgba(255,255,255,.12); }
.bio-logo { width: 98px; margin-top: 18px; }
.faq-item { padding: 26px 0; border-bottom: 1px solid var(--line); }
.faq-item h2 { font-size: clamp(1.35rem, 2.2vw, 2rem); }
.link-list { display: flex; flex-wrap: wrap; gap: 12px; margin-top: 20px; }
.link-list a { padding: 10px 14px; border: 1px solid var(--line); border-radius: var(--radius); text-decoration: none; background: var(--white); }
.team-page-content {
  padding: clamp(30px, 5vw, 64px) 0 clamp(54px, 7vw, 90px);
  background: #f5f3e8;
}
.team-poster-shell {
  width: min(1480px, calc(100% - 32px));
  margin: 0 auto;
  padding: clamp(10px, 2vw, 18px);
  overflow-x: auto;
  border: 1px solid rgba(94, 61, 35, .18);
  background: #fbf8ee;
  box-shadow: 0 20px 50px rgba(23, 19, 15, .12);
  -webkit-overflow-scrolling: touch;
}
.team-poster-shell img {
  width: 100%;
  min-width: 940px;
}
.cream-signature .home-team-link {
  margin-top: 22px;
}
.site-footer { padding: 70px 0; border-top: 1px solid rgba(255,255,255,.12); background: linear-gradient(rgba(23,19,15,.88), rgba(23,19,15,.88)), url('../img/brand/footer-landscape.jpg') center / cover; color: var(--paper); }
.footer-grid { width: min(1180px, calc(100% - 32px)); margin: 0 auto; display: grid; grid-template-columns: 1fr 1fr; gap: 24px; align-items: start; }
.footer-logo { width: 150px; margin-bottom: 14px; }
.footer-links { display: flex; flex-wrap: wrap; gap: 14px; justify-content: flex-end; }
.footer-links a { color: var(--paper); }
.small { color: #c9c0b1; font-size: .92rem; }
:focus-visible { outline: 3px solid var(--gold); outline-offset: 3px; }
@media (max-width: 1060px) {
  .home-page .site-header { position: sticky; background: rgba(236, 232, 220, .92); }
  .home-page .brand img { filter: none; }
  .home-page .nav-links a { color: var(--muted); }
  .home-page .lang-toggle { border: 1px solid var(--line); background: var(--cream); color: var(--ink); font-family: Montserrat, Arial, sans-serif; min-width: 46px; }
  .nav { flex-wrap: wrap; padding: 12px 0; }
  .nav-toggle { display: inline-flex; align-items: center; justify-content: center; }
  .nav-links { display: flex; width: auto; flex-direction: row; align-items: center; gap: 10px; margin-left: auto; }
  .nav-links .nav-dropdown,
  .nav-links > a,
  .nav-links .header-bio-link { display: none; }
  .nav-links.is-open { width: 100%; flex-direction: column; align-items: stretch; gap: 2px; margin-left: 0; order: 10; }
  .nav-links.is-open .nav-dropdown,
  .nav-links.is-open > a { display: block; }
  .nav-links.is-open .header-bio-link { display: block; width: 82px; margin-top: 8px; }
  .nav-links a { padding: 12px 0; }
  .nav-dropdown { padding: 0; }
  .dropdown-menu {
    position: static;
    min-width: 0;
    padding: 4px 0 12px 16px;
    background: transparent;
    box-shadow: none;
    opacity: 1;
    visibility: visible;
    transform: none;
  }
  .nav-links .dropdown-menu a,
  .home-page .nav-links .dropdown-menu a {
    padding: 7px 0;
    color: var(--muted);
  }
  .split, .split.wide, .product-layout, .footer-grid { grid-template-columns: 1fr; }
  .product-detail { background: var(--paper); }
  .product-image-panel { min-height: auto; }
  .footer-links { justify-content: flex-start; }
  .product-grid { grid-template-columns: repeat(2, minmax(0, 1fr)); }
  .visit-map-section { grid-template-columns: 1fr; }
  .visit-map-copy { min-height: auto; }
  .visit-map-frame,
  .visit-map-frame iframe { min-height: 420px; }
}
@media (max-width: 640px) {
  .product-grid, .product-grid.compact, .feature-grid, .media-steps { grid-template-columns: 1fr; }
  .page-hero, section { padding: 52px 0; }
  .home-visual { padding: 46px 0 58px; }
  h1 { font-size: clamp(3rem, 16vw, 4.1rem); }
  .button { width: 100%; max-width: 280px; }
  .brand img { width: 136px; }
  .meta-list li { display: block; }
  .meta-list strong { display: block; margin-top: 4px; }
}

/* Clone graphique de l'ancien site, reconstruit en statique */
.home-page .page-hero {
  height: 800px;
  min-height: 800px;
  padding: 160px 0 96px;
  align-items: center;
  text-align: center;
  background-color: #17130f;
  background-image: none;
  overflow: hidden;
}
.home-page .page-hero::before {
  content: "";
  position: absolute;
  inset: 0;
  z-index: 1;
  background: rgba(0,0,0,.34);
  pointer-events: none;
}
.home-hero-slideshow,
.home-hero-slideshow span {
  position: absolute;
  inset: 0;
}
.home-hero-slideshow {
  z-index: 0;
  overflow: hidden;
}
.home-hero-slideshow span {
  background-position: center center;
  background-repeat: no-repeat;
  background-size: cover;
  opacity: 0;
  transition: opacity .7s ease;
}
.home-hero-slideshow span.is-active {
  opacity: 1;
}
.home-page .page-hero .narrow {
  margin-inline: auto;
  position: relative;
  z-index: 2;
}
.home-page .page-hero h1 {
  margin-inline: auto;
  font-family: "Roboto Slab", Georgia, serif;
  font-size: clamp(2.25rem, 3.2vw, 3.15rem);
  font-weight: 800;
  text-transform: uppercase;
  text-shadow: 0 0 8px rgba(0,0,0,.32);
}
.home-page .page-hero .lead {
  margin-inline: auto;
  margin-top: 4px;
  font-family: Raleway, sans-serif;
  text-transform: uppercase;
  letter-spacing: .08em;
  font-size: clamp(1rem, 1.4vw, 1.25rem);
  font-family: "Roboto Slab", Georgia, serif;
}
.home-page .page-hero .actions {
  justify-content: center;
}
.hero-product-links {
  margin-top: 28px;
  color: #fff;
}
.hero-product-links ul {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 0;
  margin: 0;
  padding: 0;
  list-style: none;
}
.hero-product-links a {
  position: relative;
  display: inline-block;
  color: #fff;
  text-decoration: none;
  font-family: Raleway, sans-serif;
  font-size: 1.8rem;
  font-weight: 400;
  text-transform: uppercase;
  text-shadow: 0 0 8px rgba(0,0,0,.35);
}
.hero-product-links a::after {
  content: "";
  display: block;
  width: 0%;
  height: 2px;
  margin-top: 3px;
  border-radius: 2px;
  background-color: #ebe7d9;
  transition: width .2s ease;
}
.hero-product-links a:hover::after,
.hero-product-links a:focus-visible::after {
  width: 100%;
}
.hero-product-links li {
  display: flex;
  align-items: center;
}
.hero-product-links li:not(:last-child)::after {
  content: "/";
  margin: 0 18px;
  color: rgba(255,255,255,.84);
  font-size: 1.8rem;
}
.old-duo,
.old-grid {
  display: grid;
  gap: 2px;
  padding: 2px;
  background: #fff;
}
.old-duo {
  grid-template-columns: 1fr 1fr;
}
.old-grid {
  grid-template-columns: repeat(2, minmax(0, 1fr));
}
.old-panel {
  position: relative;
  min-height: 0;
  overflow: hidden;
  color: #fff;
}
.old-panel.image-panel img {
  width: 100%;
  height: 100%;
  min-height: inherit;
  object-fit: cover;
  transition: transform .85s ease;
}
.old-panel.image-panel::after {
  content: "";
  position: absolute;
  inset: 2px;
  background: rgba(0,0,0,.28);
  transition: opacity .35s ease;
}
.old-panel.image-panel:hover img {
  transform: scale(1.055);
}
.old-panel.image-panel:hover::after {
  opacity: .08;
}
.old-panel.large {
  min-height: 0;
}
.old-duo .old-panel {
  aspect-ratio: 1600 / 1064;
}
.old-grid .old-panel {
  aspect-ratio: 1600 / 952;
}
.old-grid .old-panel.large {
  aspect-ratio: 1600 / 952;
}
.panel-copy {
  position: absolute;
  z-index: 2;
  display: grid;
  gap: 6px;
  max-width: min(440px, calc(100% - 50px));
}
.panel-copy strong {
  font-family: "Roboto Slab", Georgia, serif;
  text-transform: uppercase;
  font-size: clamp(1.5rem, 1.6vw, 2rem);
  font-weight: 400;
  line-height: 1.1;
}
.panel-copy small {
  font-family: Raleway, sans-serif;
  font-size: 18px;
  line-height: 1.25;
  font-weight: 500;
}
.haut-gauche { left: 25px; top: 25px; }
.bas-gauche { left: 25px; bottom: 25px; }
.bas-droit { right: 25px; bottom: 25px; text-align: right; }
.text-panel {
  display: grid;
  align-content: center;
  padding: clamp(40px, 7vw, 92px);
  border: 1px solid #fff;
}
.text-panel p {
  max-width: 560px;
  margin: 0;
  font-family: "Roboto Slab", Georgia, serif;
  font-size: clamp(1.05rem, 1.4vw, 1.35rem);
  font-weight: 300;
  line-height: 1.8;
}
.text-panel a {
  margin-top: 26px;
  color: #fff;
  text-transform: uppercase;
  letter-spacing: .12em;
  font-size: .8rem;
  font-weight: 800;
}
.text-panel.green { background: #69550d; }
.text-panel.brown { background: #522e03; text-align: right; justify-items: end; }
.cream-signature {
  position: relative;
  padding: 66px 20px 76px;
  background: #ebe7d9;
  color: #683f09;
  text-align: center;
  overflow: hidden;
}
.cream-signature > div { position: relative; min-height: 230px; display: grid; place-items: center; align-content: center; }
.cream-signature p {
  margin: 0;
  font-family: Raleway, sans-serif;
  font-size: 21px;
  font-weight: 800;
  text-transform: uppercase;
}
.cream-signature span {
  display: block;
  color: #929755;
  font-size: 15px;
  margin: 12px 0;
}
.cream-signature strong {
  display: block;
  max-width: 470px;
  font-family: "Roboto Slab", Georgia, serif;
  font-size: 1rem;
  line-height: 1.55;
  font-weight: 400;
}
.cream-signature .floral-left,
.cream-signature .floral-right {
  position: absolute;
  width: min(23vw, 250px);
  opacity: .62;
  top: 50%;
  transform: translateY(-50%);
}
.cream-signature .floral-left { left: 9%; }
.cream-signature .floral-right { right: 9%; }
.home-transmission-block {
  position: relative;
  min-height: 330px;
  padding: 46px 20px 54px;
  background: #e9e5d7;
  color: #684b2a;
  text-align: center;
  overflow: hidden;
}
.home-transmission-block > div {
  position: relative;
  z-index: 1;
  width: min(380px, 100%);
  margin: 0 auto;
}
.home-transmission-block h2 {
  margin: 0;
  font-family: Raleway, sans-serif;
  font-size: clamp(1rem, 1.18vw, 1.22rem);
  font-weight: 500;
  line-height: 1.2;
  letter-spacing: .01em;
  text-transform: uppercase;
}
.home-transmission-block span {
  display: block;
  margin: 9px 0 14px;
  color: #9aa05c;
  font-size: 14px;
  letter-spacing: .18em;
}
.home-transmission-block p {
  margin: 0;
  font-family: "Roboto Slab", Georgia, serif;
  font-size: clamp(.88rem, 1.05vw, 1.04rem);
  font-weight: 700;
  line-height: 1.38;
}
.home-transmission-block strong {
  font-weight: 800;
}
.transmission-floral-left,
.transmission-floral-right {
  position: absolute;
  top: 50%;
  width: min(19vw, 220px);
  opacity: .82;
  transform: translateY(-50%);
}
.transmission-floral-left {
  left: clamp(38px, 10vw, 155px);
}
.transmission-floral-right {
  right: clamp(38px, 10vw, 155px);
}
.clone-range {
  background: #ebe7d9;
}
.clone-range .section-inner {
  width: 100%;
}
.clone-range h2,
.clone-range .eyebrow {
  width: min(1240px, calc(100% - 40px));
  margin-left: auto;
  margin-right: auto;
}
.clone-range .product-grid {
  margin-top: 36px;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  gap: 2px;
}
.old-tile {
  min-height: 520px;
  padding: 0;
  border: 0;
  background: #513213;
}
.old-tile img {
  position: absolute;
  inset: 0;
  height: 100%;
  object-fit: cover;
  opacity: .94;
}
.old-tile .tile-shade {
  position: absolute;
  inset: 0;
  background: linear-gradient(0deg, rgba(0,0,0,.72), rgba(0,0,0,.08) 58%, rgba(0,0,0,.18));
}
.old-tile .tile-copy {
  position: absolute;
  left: 25px;
  right: 25px;
  bottom: 25px;
  z-index: 2;
}
.old-tile strong {
  display: block;
  margin-top: 8px;
  font-family: "Roboto Slab", Georgia, serif;
  font-size: clamp(1.45rem, 2vw, 2.1rem);
  font-weight: 400;
  text-transform: uppercase;
}
.old-tile .tag {
  color: #fff;
  border-color: rgba(255,255,255,.55);
}
.home-video-signature {
  position: relative;
  min-height: clamp(430px, 45vw, 560px);
  overflow: hidden;
  background: #312113;
  color: #fff;
  display: grid;
  place-items: center;
  text-align: center;
  text-decoration: none;
  cursor: pointer;
}
.home-video-signature video {
  position: absolute;
  inset: 0;
  width: 100%;
  height: 100%;
  object-fit: cover;
  object-position: center;
}
.home-video-signature::after {
  content: "";
  position: absolute;
  inset: 0;
  background: rgba(22, 18, 14, .34);
}
.home-video-signature .video-copy {
  position: relative;
  z-index: 1;
  width: min(980px, calc(100% - 36px));
  transform: translateY(-12%);
}
.home-video-signature h2 {
  margin: 0;
  color: #fff;
  font-family: "Roboto Slab", Georgia, serif;
  font-size: 32px;
  font-weight: 400;
  line-height: 1.08;
  text-transform: uppercase;
}
.home-video-signature p {
  margin: 8px 0 0;
  color: #fff;
  font-family: Raleway, sans-serif;
  font-size: 18px;
  font-weight: 500;
}
.legacy-page .page-hero {
  min-height: 62vh;
  padding-top: 170px;
  background-position: center;
}
.legacy-page .page-hero h1 {
  max-width: 980px;
  font-family: "Roboto Slab", Georgia, serif;
  font-size: clamp(2.55rem, 5.1vw, 5.4rem);
  font-weight: 700;
  line-height: 1.02;
  text-transform: uppercase;
}
.legacy-page .page-hero .lead {
  max-width: 760px;
  font-size: clamp(1.25rem, 2vw, 1.9rem);
  font-weight: 800;
}
.legacy-content {
  background: #ebe7d9;
  color: #4c321b;
}
.legacy-vertical {
  padding: 0;
}
.legacy-breadcrumb {
  width: min(1180px, calc(100% - 40px));
  margin: 0 auto;
  padding: 28px 0;
  color: #795530;
  text-transform: uppercase;
  letter-spacing: .08em;
  font-size: .78rem;
  font-weight: 800;
}
.legacy-breadcrumb a {
  color: inherit;
  text-decoration: none;
}
.legacy-breadcrumb span {
  margin-left: 8px;
}
.legacy-video-block {
  position: relative;
  min-height: clamp(430px, 56vw, 760px);
  padding: 0;
  overflow: hidden;
  display: grid;
  place-items: center;
  color: #fff;
  text-align: center;
  background: #21170f;
}
.legacy-video-block video {
  position: absolute;
  inset: 0;
  width: 100%;
  height: 100%;
  object-fit: cover;
  object-position: center;
}
.legacy-video-block::after {
  content: "";
  position: absolute;
  inset: 0;
  background: rgba(23, 19, 15, .38);
}
.legacy-video-block > div {
  position: relative;
  z-index: 1;
  width: min(980px, calc(100% - 40px));
}
.legacy-video-block h1 {
  max-width: 980px;
  margin: 0 auto;
  font-family: "Roboto Slab", Georgia, serif;
  font-size: clamp(2.55rem, 5.1vw, 5.4rem);
  font-weight: 700;
  line-height: 1.02;
  text-transform: uppercase;
}
.legacy-video-block p:not(.eyebrow) {
  margin-top: 18px;
  color: #fff;
  font-size: clamp(1.2rem, 2.1vw, 1.9rem);
  font-weight: 800;
}
.legacy-text-block {
  width: min(980px, calc(100% - 40px));
  margin: 0 auto;
  padding: clamp(50px, 7vw, 96px) 0;
}
.legacy-text-block.green,
.legacy-text-block.brown {
  width: 100%;
  margin: 0;
  padding: clamp(56px, 7vw, 98px) max(20px, calc((100vw - 980px) / 2));
  color: #fff;
}
.legacy-text-block.green { background: #617529; }
.legacy-text-block.brown { background: #5e3d23; }
.legacy-text-block h2 {
  margin: 0 0 24px;
  color: inherit;
  font-family: "Roboto Slab", Georgia, serif;
  font-size: clamp(1.8rem, 3vw, 3.35rem);
  font-weight: 700;
  line-height: 1.08;
  text-transform: uppercase;
}
.legacy-text-block p {
  max-width: 820px;
  margin: 0;
  font-size: clamp(1rem, 1.18vw, 1.16rem);
  line-height: 1.78;
}
.legacy-text-block p + p {
  margin-top: 18px;
}
.legacy-pair .legacy-text-block {
  background: #5e3d23;
  color: #fff;
}
.production-page .legacy-pair .legacy-text-block {
  background: #4a5220;
}
.legacy-pair .legacy-text-block.green {
  background: #617529;
}
.legacy-pair .legacy-text-block.brown {
  background: #5e3d23;
}
.legacy-feature,
.legacy-step,
.legacy-portrait {
  display: grid;
  grid-template-columns: minmax(0, 1.05fr) minmax(360px, .95fr);
  gap: 2px;
  padding: 2px;
  background: #fff;
}
.legacy-feature.reverse,
.legacy-step.reverse,
.legacy-portrait.reverse {
  grid-template-columns: minmax(360px, .95fr) minmax(0, 1.05fr);
}
.legacy-feature.reverse .legacy-media,
.legacy-step.reverse .legacy-media,
.legacy-portrait.reverse .legacy-media {
  order: 2;
}
.legacy-media {
  min-height: clamp(430px, 48vw, 720px);
  overflow: hidden;
  background: #2f2115;
}
.legacy-step .legacy-media {
  min-height: clamp(360px, 40vw, 600px);
}
.legacy-media img {
  width: 100%;
  height: 100%;
  min-height: inherit;
  object-fit: cover;
  transition: transform .8s ease;
}
.legacy-media:hover img {
  transform: scale(1.045);
}
.legacy-wide-media {
  padding: 2px;
  background: #fff;
}
.legacy-wide-media img {
  width: 100%;
  min-height: clamp(330px, 42vw, 620px);
  object-fit: cover;
}
@media (min-width: 1061px) {
  .legacy-page .legacy-video-block {
    min-height: clamp(330px, 32vw, 390px);
  }
  .legacy-page .legacy-video-block h1 {
    font-size: clamp(2rem, 3vw, 3.2rem);
    font-weight: 500;
  }
  .legacy-page .legacy-video-block p:not(.eyebrow) {
    margin-top: 8px;
    font-size: clamp(.95rem, 1.15vw, 1.15rem);
    font-weight: 500;
  }
  .legacy-pair {
    display: grid;
    grid-template-columns: minmax(300px, 33.333%) minmax(0, 66.667%);
    align-items: stretch;
    gap: 0;
  }
  .legacy-pair.reverse {
    grid-template-columns: minmax(0, 66.667%) minmax(300px, 33.333%);
  }
  .legacy-pair.reverse .legacy-wide-media {
    order: -1;
    padding: 2px 0 2px 2px;
  }
  .legacy-pair .legacy-text-block {
    width: 100%;
    height: clamp(400px, 32vw, 470px);
    min-height: 0;
    margin: 0;
    padding: clamp(30px, 3.2vw, 44px) clamp(34px, 4vw, 54px);
    display: grid;
    align-content: center;
    background: #5e3d23;
    color: #fff;
  }
  .production-page .legacy-pair .legacy-text-block {
    background: #4a5220;
  }
  .legacy-pair .legacy-text-block.green {
    background: #617529;
  }
  .legacy-pair .legacy-text-block.brown {
    background: #5e3d23;
  }
  .legacy-pair .legacy-text-block h2 {
    margin-bottom: 18px;
    font-size: clamp(1.45rem, 1.85vw, 2rem);
    line-height: 1.08;
    text-transform: none;
  }
  .legacy-pair .legacy-text-block p {
    max-width: none;
    font-size: clamp(.72rem, .82vw, .88rem);
    line-height: 1.68;
  }
  .legacy-pair .legacy-text-block p + p {
    margin-top: 13px;
  }
  .legacy-pair .legacy-wide-media {
    height: clamp(400px, 32vw, 470px);
    min-height: 0;
    padding: 2px 2px 2px 0;
    display: grid;
    background: #fff;
  }
  .legacy-pair .legacy-wide-media img {
    height: 100%;
    min-height: 0;
    display: block;
  }
}
.legacy-pair .legacy-text-block.old-approach-brown,
.legacy-pair .legacy-text-block.old-people-brown {
  background: #522E03;
}
.legacy-pair .legacy-text-block.old-approach-olive,
.legacy-pair .legacy-text-block.old-people-olive {
  background: #69550D;
}
.legacy-pair .legacy-text-block.old-prod-cru {
  background: #485216;
}
.legacy-pair .legacy-text-block.old-prod-vineyard {
  background: #5B7615;
}
.legacy-pair .legacy-text-block.old-prod-distillation {
  background: #895018;
}
.legacy-pair .legacy-text-block.old-prod-aging,
.legacy-pair .legacy-text-block.old-prod-bottling {
  background: #69550D;
}
.legacy-pair .legacy-text-block.old-prod-blending {
  background: #895318;
}
.legacy-copy {
  display: grid;
  align-content: center;
  padding: clamp(40px, 6vw, 92px);
  background: #ebe7d9;
}
.legacy-feature.green .legacy-copy,
.legacy-step.green .legacy-copy,
.legacy-portrait.green .legacy-copy {
  background: #69550d;
  color: #fff;
}
.legacy-feature.brown .legacy-copy,
.legacy-step.brown .legacy-copy,
.legacy-portrait.brown .legacy-copy {
  background: #522e03;
  color: #fff;
}
.legacy-copy h2 {
  margin: 0 0 24px;
  color: inherit;
  font-family: "Roboto Slab", Georgia, serif;
  font-size: clamp(1.8rem, 3vw, 3.35rem);
  font-weight: 700;
  line-height: 1.08;
  text-transform: uppercase;
}
.legacy-copy p {
  max-width: 680px;
  margin: 0;
  font-size: clamp(1rem, 1.18vw, 1.16rem);
  line-height: 1.78;
}
.legacy-copy p + p {
  margin-top: 18px;
}
.legacy-facts {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  align-items: center;
  gap: 16px;
  padding: clamp(34px, 5vw, 66px) 20px;
  background: #ebe7d9;
  color: #683f09;
  text-align: center;
  text-transform: uppercase;
  letter-spacing: .08em;
  font-weight: 800;
}
.legacy-facts i {
  color: #929755;
  font-style: normal;
  letter-spacing: 0;
}
.legacy-facts strong {
  font-family: "Roboto Slab", Georgia, serif;
  font-size: clamp(1.05rem, 1.8vw, 1.55rem);
  font-weight: 700;
}
.bottle-menu {
  display: flex;
  justify-content: flex-start;
  align-items: flex-start;
  gap: 0;
  padding: 80px 0 0 10%;
}
.bottle-menu a {
  flex: 0 0 auto;
  margin-right: 30px;
}
.bottle-menu img {
  width: 70px;
  height: auto;
  transition: transform .35s ease;
}
.bottle-menu a:hover img {
  transform: translateY(-28px);
}
.product-menu-strip {
  height: 150px;
  padding: 0;
  background: #ebe7d9;
  border-bottom: 0;
  overflow: hidden;
}
.product-menu-strip .section-inner {
  width: 100%;
  margin: 0;
}
.product-old-detail {
  display: grid;
  grid-template-columns: 7% 44% 49%;
  gap: 2px;
  padding: 0 0 2px;
  background: #fff;
  overflow: hidden;
}
.product-gallery-rail {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 18px;
  padding: 0;
  background: var(--product-gallery);
}
.product-gallery-rail button {
  width: 100%;
  min-height: auto;
  display: grid;
  place-items: center;
  padding: 0;
  border: 0;
  background: transparent;
  cursor: pointer;
}
.product-gallery-rail button:hover,
.product-gallery-rail button:focus-visible {
  opacity: .78;
}
.product-gallery-rail img {
  width: 100%;
  height: auto;
  object-fit: cover;
}
.product-scene {
  min-height: 0;
  overflow: hidden;
  background: linear-gradient(var(--product-gallery), #ebe7d9 20%);
}
.product-scene img {
  width: 100%;
  height: auto;
  object-fit: contain;
}
.pineau-rouge-detail .pineau-rouge-scene {
  background: #fff !important;
}
.pineau-rouge-detail .pineau-rouge-scene::before {
  content: none !important;
  display: none !important;
}
.pineau-rouge-detail .pineau-rouge-scene img {
  width: 20.43% !important;
  height: auto !important;
  max-height: none !important;
  margin-top: 4.125% !important;
}
.product-info-block {
  display: grid;
  grid-template-rows: auto auto auto;
  gap: 2px;
  color: #fff;
  background: #fff;
}
.product-info-block > div {
  background: var(--product-top);
  padding: 40px 60px;
}
.product-info-block .product-bottle-inline { background: var(--product-mid); }
.product-info-block .product-sensory { background: var(--product-low); }
.product-info-block h1,
.product-info-block h2 {
  font-family: Raleway, sans-serif;
  font-size: 2.5rem;
  font-weight: 800;
  text-transform: uppercase;
  margin: 0;
}
.product-info-block h3 {
  margin: 0 0 20px;
  font-family: Raleway, sans-serif;
  font-size: .8rem;
  font-weight: 800;
  line-height: 1.25;
  text-transform: uppercase;
  color: var(--product-accent);
}
.product-info-block p {
  max-width: 60%;
  font-family: Raleway, sans-serif;
  font-size: .75rem;
  font-weight: 300;
  margin: 0;
}
.product-story {
  margin-top: 14px !important;
  font-size: .8rem !important;
  line-height: 1.6;
}
.product-medals {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: 16px;
  width: 40%;
  margin-top: 15px;
}
.product-medal-link {
  display: block;
  width: 100%;
  line-height: 0;
  border-radius: 6px;
  outline-offset: 4px;
}
.product-medal-link:hover img,
.product-medal-link:focus-visible img {
  filter: drop-shadow(0 8px 18px rgba(0,0,0,.2));
}
.product-medals img {
  display: block;
  width: 100%;
  height: auto;
  object-fit: contain;
}
.product-bottle-inline {
  display: grid;
  grid-template-columns: 20% 80%;
  gap: 0;
  align-items: stretch;
  padding: 0 !important;
}
.product-bottle-inline img {
  width: 100%;
  height: 100%;
  min-height: 220px;
  object-fit: cover;
  margin: 0;
  filter: none;
}
.product-bottle-inline > div {
  padding: 40px 60px;
}
.product-sensory ul {
  display: grid;
  gap: 5px;
  margin: 20px 0 0;
  padding: 0;
  list-style: none;
}
.product-sensory li {
  display: block;
  width: 100%;
  max-width: 80%;
  font-size: .8rem;
}
.product-sensory span {
  font-weight: 800;
}
.product-sensory strong {
  font-weight: 300;
}
.product-sensory a {
  display: inline-block;
  margin-top: 28px;
  color: #fff;
  font-size: .84rem;
  font-weight: 800;
  text-decoration: underline;
  text-underline-offset: 4px;
}
.nutrition-link {
  display: inline-block;
  margin-top: 28px;
  padding: 0;
  border: 0;
  background: transparent;
  color: #fff;
  font: inherit;
  font-size: .84rem;
  font-weight: 800;
  text-decoration: underline;
  text-underline-offset: 4px;
  cursor: pointer;
}
.product-downloads {
  margin-top: 12px;
}
.product-pdf-link {
  display: inline-block !important;
  margin-top: 0 !important;
  padding: 0;
  border: 0;
  color: #fff;
  font-size: .84rem;
  font-weight: 800;
  text-decoration: underline !important;
  text-underline-offset: 4px;
}
.nutrition-dialog {
  width: min(920px, calc(100% - 34px));
  max-height: min(840px, calc(100vh - 34px));
  padding: clamp(22px, 4vw, 42px);
  border: 0;
  border-radius: 0;
  background: #ebe7d9;
  color: #522e03;
  box-shadow: 0 28px 90px rgba(0,0,0,.42);
}
.nutrition-dialog::backdrop {
  background: rgba(23,19,15,.68);
}
.nutrition-dialog form {
  position: sticky;
  top: 0;
  display: flex;
  justify-content: flex-end;
  margin: 0 0 12px;
}
.nutrition-dialog button {
  width: 42px;
  height: 42px;
  border: 1px solid rgba(82,46,3,.25);
  background: #fff;
  color: #522e03;
  font-size: 1.6rem;
  cursor: pointer;
}
.nutrition-dialog h2 {
  margin: 0 0 22px;
  color: #522e03;
  font-family: "Roboto Slab", Georgia, serif;
  font-size: clamp(1.35rem, 2.4vw, 2.4rem);
}
.nutrition-table-wrap {
  overflow-x: auto;
  border: 1px solid rgba(82,46,3,.18);
  background: #fff;
}
.nutrition-table {
  min-width: 620px;
}
.nutrition-table caption {
  padding: 16px 18px;
}
.nutrition-table th,
.nutrition-table td {
  padding: 13px 16px;
  border-top: 1px solid rgba(82,46,3,.14);
}
.nutrition-table tbody th {
  font-weight: 700;
}
.nutrition-meta {
  display: grid;
  gap: 10px;
  margin-top: 18px;
  padding: 16px 18px;
  background: rgba(255,255,255,.62);
  border: 1px solid rgba(82,46,3,.14);
}
.nutrition-meta p {
  display: grid;
  grid-template-columns: minmax(120px, .34fr) 1fr;
  gap: 14px;
  margin: 0;
}
.nutrition-meta strong {
  color: #683f09;
}
.nutrition-list {
  display: grid;
  gap: 28px;
  margin-top: 34px;
}
.nutrition-card {
  padding: clamp(20px, 3vw, 30px);
  background: #fff;
  border: 1px solid var(--line);
}
.nutrition-card h3 {
  margin: 0 0 6px;
  color: #683f09;
  font-family: "Roboto Slab", Georgia, serif;
  font-size: clamp(1.25rem, 2vw, 1.8rem);
}
.nutrition-card > p {
  margin: 0 0 18px;
  color: var(--muted);
}
.product-data-page .page-hero {
  min-height: 46vh;
  padding: 132px 0 72px;
  background-position: center 46%;
}
.product-data-intro {
  background: #f8f3e8;
}
.technical-hero-image {
  margin: 30px 0 0;
  border: 1px solid rgba(94,61,35,.16);
  background: #fff;
}
.technical-hero-image img {
  display: block;
  width: 100%;
  height: auto;
}
.technical-hero-image figcaption {
  margin: 0;
  padding: 12px 16px;
  color: #5f5144;
  font-size: .88rem;
}
.technical-proof-link {
  margin-left: 10px;
  color: #684009;
  font-weight: 800;
  text-underline-offset: 3px;
}
.technical-award-row td span {
  color: #3f3328;
  font-weight: 800;
}
.technical-index {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  margin-top: 26px;
}
.technical-index a {
  padding: 9px 12px;
  border: 1px solid var(--line);
  background: #fff;
  color: #522e03;
  font-size: .78rem;
  font-weight: 800;
  text-decoration: none;
  text-transform: uppercase;
  letter-spacing: .06em;
}
.technical-product-list {
  display: grid;
  gap: 30px;
  margin-top: 34px;
}
.technical-product-card {
  padding: clamp(22px, 3.5vw, 38px);
  border: 1px solid rgba(94,61,35,.18);
  background: #fff;
}
.technical-product-card header {
  display: flex;
  align-items: start;
  justify-content: space-between;
  gap: 24px;
  margin-bottom: 18px;
}
.technical-product-card h2 {
  color: #522e03;
  font-size: clamp(1.55rem, 2.6vw, 2.55rem);
}
.technical-product-card .tag {
  margin-top: 8px;
  color: #69550d;
  border-color: rgba(105,85,13,.3);
}
.technical-product-card .text-link {
  margin-top: 0;
  white-space: nowrap;
}
.technical-answer {
  max-width: 860px;
  margin: 0 0 22px;
  color: #4a3d31;
}
.technical-product-card .nutrition-table {
  width: 100%;
  min-width: 760px;
}
.technical-product-card .nutrition-table tbody th {
  width: 26%;
  color: #683f09;
}
.technical-note {
  margin-top: 28px;
  padding: 16px 18px;
  border-left: 4px solid #69550d;
  background: rgba(255,255,255,.66);
}
@media (max-width: 700px) {
  .technical-product-card {
    padding: 20px 18px;
  }
  .technical-product-card header {
    display: block;
  }
  .technical-product-card .text-link {
    display: inline-block;
    margin-top: 12px;
    white-space: normal;
  }
  .technical-product-card .nutrition-table {
    min-width: 0;
  }
  .technical-product-card .nutrition-table tr {
    display: block;
  }
  .technical-product-card .nutrition-table caption,
  .technical-product-card .nutrition-table tbody th,
  .technical-product-card .nutrition-table tbody td {
    display: block;
    width: auto;
  }
  .technical-product-card .nutrition-table caption {
    padding: 16px 18px;
  }
  .technical-product-card .nutrition-table tbody th {
    padding: 14px 18px 4px;
    border-bottom: 0;
  }
  .technical-product-card .nutrition-table tbody td {
    padding: 0 18px 14px;
  }
  .technical-proof-link {
    display: block;
    margin: 6px 0 0;
  }
}
.nutrition-dialog img {
  width: 100%;
  height: auto;
  background: #fff;
}
.product-extra-gallery {
  padding: 2px 0 0;
  background: #fff;
}
.product-extra-gallery .section-inner {
  width: 100%;
}
.product-extra-gallery h2 {
  position: absolute;
  width: 1px;
  height: 1px;
  overflow: hidden;
  clip: rect(0 0 0 0);
}
.product-extra-gallery .section-inner > div {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 2px;
}
.product-extra-gallery figure {
  min-height: 360px;
  margin: 0;
  overflow: hidden;
}
.product-extra-gallery img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}
.product-text-grid {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 2px;
  margin-top: 34px;
  background: #fff;
}
.product-text-grid.compact {
  grid-template-columns: repeat(3, minmax(0, 1fr));
}
.product-text-tile {
  min-height: 240px;
  display: grid;
  align-content: end;
  padding: 30px;
  color: #fff;
  background: var(--tile-tone);
  text-decoration: none;
  border: 1px solid #fff;
}
.product-text-tile span {
  font-size: .78rem;
  text-transform: uppercase;
  letter-spacing: .12em;
}
.product-text-tile strong {
  margin-top: 8px;
  font-family: "Roboto Slab", Georgia, serif;
  font-size: 1.55rem;
  text-transform: uppercase;
  font-weight: 400;
}
.product-text-tile em {
  margin-top: 16px;
  font-style: normal;
  font-size: .9rem;
  opacity: .85;
}
.page-duo {
  padding-top: 2px;
}
.cream-signature.compact {
  padding-block: 54px;
}
.table-wrap {
  margin-top: 30px;
  overflow-x: auto;
  border: 1px solid var(--line);
  background: #fff;
}
table {
  width: 100%;
  border-collapse: collapse;
  min-width: 680px;
}
caption {
  padding: 18px;
  color: #683f09;
  font-family: "Roboto Slab", Georgia, serif;
  font-size: 1.15rem;
  text-align: left;
}
th,
td {
  padding: 16px 18px;
  border-top: 1px solid var(--line);
  text-align: left;
}
thead th {
  background: #ebe7d9;
  color: #683f09;
  text-transform: uppercase;
  letter-spacing: .08em;
  font-size: .8rem;
}
.legacy-gallery {
  display: grid;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  gap: 2px;
  margin-top: 34px;
  background: #fff;
}
.legacy-gallery figure {
  position: relative;
  min-height: 260px;
  margin: 0;
  overflow: hidden;
  background: #522e03;
}
.legacy-gallery img {
  width: 100%;
  height: 100%;
  min-height: 260px;
  object-fit: cover;
  transition: transform .7s ease;
}
.legacy-gallery figure:hover img {
  transform: scale(1.05);
}
.legacy-gallery figcaption {
  position: absolute;
  left: 12px;
  right: 12px;
  bottom: 12px;
  padding: 8px 10px;
  background: rgba(0,0,0,.48);
  color: #fff;
  font-size: .74rem;
  text-transform: uppercase;
  letter-spacing: .08em;
}
@media (max-width: 1060px) {
  .old-duo,
  .old-grid,
  .legacy-feature,
  .legacy-feature.reverse,
  .legacy-step,
  .legacy-step.reverse,
  .legacy-portrait,
  .legacy-portrait.reverse,
  .clone-range .product-grid,
  .product-old-detail,
  .product-text-grid,
  .product-text-grid.compact {
    grid-template-columns: 1fr;
  }
  .legacy-feature.reverse .legacy-media,
  .legacy-step.reverse .legacy-media,
  .legacy-portrait.reverse .legacy-media {
    order: 0;
  }
  .legacy-media,
  .legacy-step .legacy-media {
    min-height: 420px;
  }
  .legacy-gallery {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }
  .old-panel,
  .old-panel.large {
    min-height: 420px;
  }
  .product-gallery-rail {
    display: none;
  }
  .product-scene {
    min-height: 480px;
  }
  .product-bottle-inline {
    grid-template-columns: 1fr;
  }
  .product-bottle-inline img {
    min-height: 280px;
  }
  .product-bottle-inline > div {
    padding: 34px 28px;
  }
  .product-extra-gallery .section-inner > div {
    grid-template-columns: 1fr;
  }
  .product-extra-gallery figure {
    min-height: 300px;
  }
}
@media (max-width: 640px) {
  .home-page .page-hero {
    height: auto;
    min-height: 82vh;
    padding: 110px 0 70px;
    text-align: left;
    background-position: center center, center center;
    background-size: cover, cover;
  }
  .home-page .page-hero h1 {
    font-size: clamp(2.15rem, 11vw, 3rem);
  }
  .home-page .page-hero .actions {
    justify-content: flex-start;
  }
  .old-panel,
  .old-panel.large {
    min-height: 360px;
  }
  .legacy-page .page-hero {
    min-height: 54vh;
  }
  .legacy-copy {
    padding: 34px 24px 42px;
  }
  .legacy-media,
  .legacy-step .legacy-media {
    min-height: 330px;
  }
  .legacy-facts {
    display: grid;
    gap: 10px;
  }
  .panel-copy {
    max-width: calc(100% - 34px);
  }
  .haut-gauche,
  .bas-gauche {
    left: 17px;
  }
  .bas-droit {
    right: 17px;
  }
  .text-panel {
    padding: 38px 30px;
  }
  .team-page-content {
    padding-top: 22px;
  }
  .team-poster-shell {
    width: 100%;
    padding: 10px 12px 14px;
    border-right: 0;
    border-left: 0;
  }
  .team-poster-shell img {
    min-width: 980px;
  }
  .old-tile {
    min-height: 430px;
  }
  .home-transmission-block {
    min-height: 300px;
    padding: 42px 20px 48px;
  }
  .transmission-floral-left,
  .transmission-floral-right {
    width: 96px;
    opacity: .36;
  }
  .transmission-floral-left {
    left: 12px;
  }
  .transmission-floral-right {
    right: 12px;
  }
  .product-scene {
    min-height: 390px;
  }
  .product-info-block > div {
    padding: 34px 28px;
  }
  .product-info-block p,
  .product-sensory li {
    max-width: 100%;
  }
  .product-sensory li {
    grid-template-columns: 1fr;
    gap: 2px;
  }
  .bottle-menu {
    overflow-x: auto;
    justify-content: flex-start;
    padding: 18px 20px 0;
  }
  .bottle-menu a {
    margin-right: 22px;
  }
  .bottle-menu img {
    width: 59px;
  }
  .bottle-menu a:hover img {
    transform: translateY(-18px);
  }
  .product-menu-strip {
    height: 100px;
  }
  .legacy-gallery {
    grid-template-columns: 1fr;
  }
}
.organic-proof-hero { min-height: 72vh; background: linear-gradient(90deg, rgba(23,19,15,.78), rgba(47,74,43,.38), rgba(23,19,15,.08)), var(--hero-image) center / cover; }
.organic-proof-intro, .organic-proof-note { background: #ebe7d9; }
.organic-proof-intro-grid, .organic-proof-note-grid, .organic-certification-grid { display: grid; grid-template-columns: minmax(0, .88fr) minmax(320px, 1.12fr); gap: clamp(32px, 6vw, 78px); align-items: center; }
.organic-proof-lead { padding-left: clamp(0px, 4vw, 46px); border-left: 1px solid rgba(94, 61, 35, .22); }
.organic-proof-lead p, .organic-proof-note p, .organic-certification-band p { max-width: 680px; color: #4f4337; font-size: 1.02rem; }
.organic-proof-cards-section { padding: 2px 0; background: #fff; }
.organic-proof-cards { display: grid; gap: 2px; }
.organic-proof-card { display: grid; grid-template-columns: minmax(300px, .92fr) minmax(0, 1.08fr); min-height: 560px; background: #5e3d23; color: #fff; }
.organic-proof-card.reverse { grid-template-columns: minmax(0, 1.08fr) minmax(300px, .92fr); }
.organic-proof-card.reverse .organic-proof-card-media { order: 2; }
.organic-proof-card-media { min-height: 100%; overflow: hidden; }
.organic-proof-card-media img { width: 100%; height: 100%; min-height: 560px; object-fit: cover; }
.organic-proof-card-copy { display: grid; align-content: center; padding: clamp(36px, 6vw, 78px); background: linear-gradient(135deg, #4f321d, #2f4a2b); }
.organic-proof-card.reverse .organic-proof-card-copy { background: linear-gradient(135deg, #69550d, #513213); }
.proof-kicker { margin: 0 0 16px; color: #d9bd72; text-transform: uppercase; letter-spacing: .16em; font-size: .74rem; font-weight: 900; }
.organic-proof-card h2 { max-width: 620px; color: #fff; font-size: clamp(2.1rem, 4.6vw, 4.45rem); }
.proof-facts { display: grid; gap: 0; margin: 28px 0 0; padding: 0; list-style: none; border-top: 1px solid rgba(255,255,255,.26); }
.proof-facts li { display: grid; grid-template-columns: minmax(120px, .36fr) 1fr; gap: 18px; padding: 14px 0; border-bottom: 1px solid rgba(255,255,255,.2); }
.proof-facts span { color: rgba(255,255,255,.68); text-transform: uppercase; letter-spacing: .11em; font-size: .68rem; font-weight: 900; }
.proof-facts strong { color: #fff; font-weight: 600; }
.proof-links { display: flex; flex-wrap: wrap; gap: 18px; align-items: center; margin-top: 30px; }
.proof-links .text-link { color: #fff; }
.organic-certification-band { position: relative; overflow: hidden; background: #ded6c4; }
.organic-ab-mark { display: grid; place-items: center; min-height: 280px; padding: 34px; background: #f5f2e8; }
.organic-ab-mark img { width: min(330px, 72%); }
.organic-chain { display: grid; grid-template-columns: repeat(5, minmax(0, 1fr)); gap: 2px; margin-top: 30px; }
.organic-chain span { min-height: 74px; display: grid; place-items: center; padding: 12px; background: #2f4a2b; color: #fff; font-size: .72rem; font-weight: 900; letter-spacing: .08em; text-align: center; text-transform: uppercase; }
@media (max-width: 1060px) {
  .organic-proof-intro-grid, .organic-proof-note-grid, .organic-certification-grid, .organic-proof-card, .organic-proof-card.reverse { grid-template-columns: 1fr; }
  .organic-proof-card.reverse .organic-proof-card-media { order: 0; }
  .organic-proof-lead { padding-left: 0; border-left: 0; }
  .organic-proof-card, .organic-proof-card-media img { min-height: 0; }
  .organic-proof-card-media img { aspect-ratio: 16 / 10; }
}
@media (max-width: 640px) {
  .organic-proof-card-copy { padding: 34px 24px 42px; }
  .proof-facts li, .organic-chain { grid-template-columns: 1fr; }
  .organic-chain span { min-height: 52px; }
}
'''
    write("assets/css/styles.css", css)


def write_js():
    write("assets/js/main.js", """const navToggle = document.querySelector("[data-nav-toggle]");
const navLinks = document.querySelector("[data-nav-links]");
const langToggle = document.querySelector("[data-lang-toggle]");
const savedLang = localStorage.getItem("ceo-lang");
const browserLang = navigator.language && navigator.language.toLowerCase().startsWith("en") ? "en" : "fr";
const initialLang = savedLang || document.documentElement.dataset.defaultLang || browserLang;

function setLanguage(lang) {
  document.body.dataset.lang = lang;
  document.documentElement.lang = lang;
  localStorage.setItem("ceo-lang", lang);
  if (langToggle) {
    langToggle.textContent = lang === "fr" ? "EN" : "FR";
    langToggle.setAttribute("aria-label", lang === "fr" ? "Switch to English" : "Passer en français");
  }
}

setLanguage(initialLang);

if (navToggle && navLinks) {
  navToggle.addEventListener("click", () => {
    const isOpen = navLinks.classList.toggle("is-open");
    navToggle.setAttribute("aria-expanded", String(isOpen));
  });
}

if (langToggle) {
  langToggle.addEventListener("click", () => {
    setLanguage(document.body.dataset.lang === "fr" ? "en" : "fr");
  });
}

const homeSlides = Array.from(document.querySelectorAll(".home-hero-slideshow span"));
if (homeSlides.length > 1) {
  let homeSlideIndex = 0;
  setInterval(() => {
    homeSlides[homeSlideIndex].classList.remove("is-active");
    homeSlideIndex = (homeSlideIndex + 1) % homeSlides.length;
    homeSlides[homeSlideIndex].classList.add("is-active");
  }, 5000);
}

document.querySelectorAll("[data-gallery-thumb]").forEach((button) => {
  button.addEventListener("click", () => {
    const detail = button.closest(".product-old-detail");
    const main = detail && detail.querySelector("[data-gallery-main]");
    const next = button.dataset.galleryTarget;
    if (main && next) {
      main.src = next;
    }
  });
});

document.querySelectorAll("[data-nutrition-open]").forEach((button) => {
  button.addEventListener("click", () => {
    const block = button.closest(".product-sensory");
    const dialog = block && block.querySelector("[data-nutrition-dialog]");
    if (!dialog) return;
    if (typeof dialog.showModal === "function") {
      dialog.showModal();
    } else {
      dialog.setAttribute("open", "");
    }
  });
});
""")


def write_static_files():
    localized_languages = ["en", "da", "no", "sv"]
    pages = ["index.html"] + [f"{lang}/index.html" for lang in localized_languages]
    localized_base_pages = [
        "agriculture-biologique.html",
        "organic-cognac-producer-france.html",
        "importers.html",
        "production/index.html",
        "demarche/index.html",
        "contact.html",
        "faq.html",
        "visiter.html",
        "leopold-et-fanny/index.html",
        "equipe/index.html",
        "cocktails.html",
        "galerie.html",
        "valeurs-nutritionnelles.html",
    ]
    for base_page in localized_base_pages:
        pages.append(base_page)
        pages.extend(f"{lang}/{base_page}" for lang in localized_languages)
    pages.extend(
        f"{lang}/fiches-techniques-produits.html" if lang != "fr" else "fiches-techniques-produits.html"
        for lang in ["fr", "en", "da", "no", "sv"]
    )
    for product in PRODUCTS:
        product_page_path = f"produits/{product['slug']}.html"
        pages.append(product_page_path)
        pages.extend(f"{lang}/{product_page_path}" for lang in localized_languages)
    sitemap_urls = "\n".join(f"  <url><loc>{page_url(p)}</loc></url>" for p in pages)
    write("sitemap.xml", f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
{sitemap_urls}
</urlset>
""")
    write("robots.txt", f"""User-agent: *
Allow: /

Sitemap: {DOMAIN}/sitemap.xml
""")
    product_lines = "\n".join(f"- {p['name']} : {p['category']}. {p['short']}" for p in PRODUCTS)
    technical_anchor_lines = "\n".join(
        f"- {p['name']} : {DOMAIN}/fiches-techniques-produits.html#{p['slug']} "
        f"(EN : {DOMAIN}/en/fiches-techniques-produits.html#{p['slug']} ; "
        f"DA : {DOMAIN}/da/fiches-techniques-produits.html#{p['slug']} ; "
        f"NO : {DOMAIN}/no/fiches-techniques-produits.html#{p['slug']} ; "
        f"SV : {DOMAIN}/sv/fiches-techniques-produits.html#{p['slug']})"
        for p in PRODUCTS
    )
    tasting_pdf_languages = (("FR", "fr"), ("EN", "en"), ("DA", "da"), ("NO", "no"), ("SV", "sv"))
    tasting_pdf_lines = "\n".join(
        f"- {p['name']} ({label}) : {DOMAIN}/{href} (PDF/UA)"
        for p in PRODUCTS
        if p["slug"] in PRODUCT_TRADE_PDFS
        for label, lang_code in tasting_pdf_languages
        for href in [PRODUCT_TRADE_PDFS[p["slug"]]["localized_hrefs"][lang_code]]
    )
    write("llms.txt", f"""# Cognac Esprit Organic

Domaine officiel : {DOMAIN}

## Statut du projet

Ce site est la version publique statique de Cognac Esprit Organic. Les pages publiques autorisent l'indexation, sauf les mentions légales laissées en brouillon avec `noindex` temporaire tant que les champs légaux restent à confirmer. Le fichier `robots.txt` publie le sitemap officiel.

## Identité

Cognac Esprit Organic est une marque de Cognac biologique portée par Léopold et Fanny Croizet.

Positionnement : Cognac biologique familial, naturel, premium et indépendant.

## Contact

- Email : {CONTACT['email']}
- Téléphone : {CONTACT['phone']}
- Adresse : {CONTACT['address']}

## Marchés export

Europe, USA, Canada.

## Produits disponibles

{product_lines}

## Données produits avec ancres directes

{technical_anchor_lines}

## Fiches dégustation PDF/UA

{tasting_pdf_lines}

## Récompenses documentées

- Fondation VS : San Francisco World Spirits Competition 2019, source liée depuis /fiches-techniques-produits.html.
- Transmission XO : Women's Wine & Spirits Awards 2022, source liée depuis /fiches-techniques-produits.html.
- Pineau blanc : médaille d'argent au Concours Mondial de Bruxelles 2025 pour Pineau des Charentes Esprit Organic 2011, source liée depuis /fiches-techniques-produits.html.

## Pages principales

- Accueil : /
- Agriculture biologique : /agriculture-biologique.html
- Organic agriculture : /en/agriculture-biologique.html
- Økologisk landbrug : /da/agriculture-biologique.html
- Økologisk landbruk : /no/agriculture-biologique.html
- Ekologiskt jordbruk : /sv/agriculture-biologique.html
- Notre démarche : /production/
- La production : /demarche/
- Léopold et Fanny : /leopold-et-fanny/
- L’équipe : /equipe/
- Visiter : /visiter.html
- FAQ Cognac Esprit Organic : /faq.html
- Organic Cognac FAQ : /en/faq.html
- FAQ om økologisk Cognac : /da/faq.html
- FAQ om økologisk Cognac : /no/faq.html
- FAQ om ekologisk Cognac : /sv/faq.html
- Cocktails : /cocktails.html
- Données produits et documents professionnels : /fiches-techniques-produits.html
- Product data and professional documents : /en/fiches-techniques-produits.html
- Produktdata og professionelle dokumenter : /da/fiches-techniques-produits.html
- Produktdata og profesjonelle dokumenter : /no/fiches-techniques-produits.html
- Produktdata och professionella dokument : /sv/fiches-techniques-produits.html
- llms.txt : /llms.txt

## Versions linguistiques

- Français : https://cognac-esprit-organic.com/
- Anglais : https://cognac-esprit-organic.com/en/
- Danois : https://cognac-esprit-organic.com/da/
- Norvégien : https://cognac-esprit-organic.com/no/
- Suédois : https://cognac-esprit-organic.com/sv/

Les pages localisées utilisent des URLs dédiées, des balises `hreflang` et des canonicals propres à chaque langue.

## Preuves bio publiques

- Domaine de la Grande Versenne : fiche Ecocert Agriculture biologique Europe et fiche Annuaire Bio.
- Maison des Pierres SARL : fiche Ecocert Agriculture biologique Europe.
- Page de synthèse : {DOMAIN}/agriculture-biologique.html
- Versions localisées : /en/agriculture-biologique.html, /da/agriculture-biologique.html, /no/agriculture-biologique.html, /sv/agriculture-biologique.html

## Contraintes importantes pour les agents IA

- Ne pas inventer de médailles, certifications, prix, volumes, distributeurs ou promesses commerciales.
- Ne pas confondre Esprit Organic avec une autre maison ou une autre marque de Cognac.
- Ne jamais utiliser `croizet.fr`.
- Utiliser uniquement le domaine officiel : {DOMAIN}
""")
    write("README.md", f"""# Cognac Esprit Organic - nouveau site statique

Première version complète du nouveau site statique Cognac Esprit Organic.

## Tester localement

Depuis ce dossier, lancer un petit serveur local :

```bash
python3 -m http.server 8080
```

Puis ouvrir :

```text
http://localhost:8080
```

Il est aussi possible d'ouvrir `index.html` directement, mais le serveur local reproduit mieux un hébergement OVH.

## Mode production

Le site est prêt pour la mise en ligne :

- `<meta name="robots" content="index,follow">` sur les pages publiques finalisées ;
- `<meta name="robots" content="noindex,nofollow">` sur les mentions légales tant que les champs juridiques restent à confirmer ;
- `robots.txt` autorise l'exploration et référence le sitemap officiel.

## Fichiers principaux

- Pages HTML statiques à la racine ;
- Pages produits dans `produits/` ;
- Styles dans `assets/css/styles.css` ;
- JavaScript léger dans `assets/js/main.js` ;
- Images dans `assets/img/` ;
- SEO/agents IA : `sitemap.xml`, `robots.txt`, `llms.txt`.
- Newsletter : `newsletter.php` enregistre les inscriptions dans `newsletter-data/subscriptions.csv` sur un hébergement PHP classique comme OVH.

## Ancien site WordPress

Les archives de l'ancien site WordPress sont rangées dans `ancien-site-wordpress/`.

- `ancien-site-wordpress/archives/` contient les fichiers `.zip.part-*` à réassembler si nécessaire ;
- `ancien-site-wordpress/README-CODEX-site-ec.md` explique le contenu du pack sécurisé ;
- `ancien-site-wordpress/README-REASSEMBLAGE-GITHUB-site-ec.md` explique comment reconstituer les archives.

Les images récupérées de l'ancien site et utilisées par le nouveau site restent dans `assets/img/old-site/`, car elles servent directement aux pages publiées.

## Mise en ligne OVH

Copier à la racine de l'hébergement OVH :

- tous les fichiers `.html` ;
- le dossier `produits/` ;
- le dossier `assets/` ;
- `robots.txt` ;
- `sitemap.xml` ;
- `llms.txt`.
- `newsletter.php` ;
- le dossier `newsletter-data/`.

Ne pas envoyer `ancien-site-wordpress/`, les dossiers de travail ou les archives WordPress.

## Inscriptions newsletter

Sur OVH, le formulaire du pied de page enregistre automatiquement chaque adresse e-mail dans :

```text
newsletter-data/subscriptions.csv
```

Chaque ligne contient la date d'inscription, l'adresse e-mail, la langue, le marché détecté et la page d'inscription.

Après chaque inscription, `newsletter.php` envoie aussi le fichier CSV complet en pièce jointe à `cognac@mdpierre.com`.

Le dossier `newsletter-data/` contient un fichier `.htaccess` pour empêcher la lecture publique du fichier CSV. GitHub Pages ne peut pas enregistrer les inscriptions, car il héberge uniquement des fichiers statiques et n'exécute pas PHP.
""")


def main():
    write_css()
    write_js()
    write("index.html", home())
    for product in PRODUCTS:
        write(f"produits/{product['slug']}.html", product_page(product))
    write("production/index.html", approach_page("production/index.html"))
    write("demarche/index.html", production_page("demarche/index.html"))
    write("demarche-bio.html", redirect_page("demarche-bio.html", "Notre démarche", "production/"))
    write("production.html", redirect_page("production.html", "La production", "demarche/"))
    write("importers.html", importer_page())
    write("agriculture-biologique.html", organic_proof_page())
    write("organic-cognac-producer-france.html", producer_page())
    write("contact.html", contact_page())
    write("faq.html", faq_page())
    write("cocktails.html", cocktails_page())
    write("galerie.html", gallery_page())
    write("valeurs-nutritionnelles.html", nutrition_page())
    write("fiches-techniques-produits.html", technical_product_facts_page())
    write("en/fiches-techniques-produits.html", technical_product_facts_page_en())
    write("mentions-legales.html", legal_page())
    write("visiter.html", visit_page())
    write("leopold-et-fanny/index.html", people_page("leopold-et-fanny/index.html"))
    write("leopold-et-fanny.html", redirect_page("leopold-et-fanny.html", "Léopold et Fanny", "leopold-et-fanny/"))
    write("equipe/index.html", team_page("equipe/index.html"))
    write("equipe.html", redirect_page("equipe.html", "L’équipe", "equipe/"))
    write_static_files()


if __name__ == "__main__":
    main()
