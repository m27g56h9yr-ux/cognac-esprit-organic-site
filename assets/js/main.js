const navToggle = document.querySelector("[data-nav-toggle]");
const navLinks = document.querySelector("[data-nav-links]");
const langToggle = document.querySelector("[data-lang-toggle]");
const langMenu = document.querySelector("[data-lang-menu]");
const langOptions = Array.from(document.querySelectorAll("[data-lang-option]"));
const savedLang = localStorage.getItem("ceo-lang");
const supportedLangs = ["fr", "en", "da", "no", "sv"];
const languageAliases = { nb: "no", nn: "no" };
const countryLanguages = {
  DK: "da",
  NO: "no",
  SJ: "no",
  SE: "sv",
  FR: "fr",
  MC: "fr",
  BE: "fr",
  CH: "fr",
  LU: "fr"
};
function detectVisitorLanguage() {
  const locales = navigator.languages && navigator.languages.length ? navigator.languages : [navigator.language];
  for (const locale of locales.filter(Boolean)) {
    const parts = locale.replace("_", "-").split("-");
    const country = parts.length > 1 ? parts[parts.length - 1].toUpperCase() : "";
    if (countryLanguages[country]) return countryLanguages[country];
    const language = (parts[0] || "").toLowerCase();
    const normalized = languageAliases[language] || language;
    if (supportedLangs.includes(normalized)) return normalized;
  }
  return "en";
}
function detectVisitorMarket() {
  const locales = navigator.languages && navigator.languages.length ? navigator.languages : [navigator.language];
  const hasFrenchCanadaLocale = locales.filter(Boolean).some((locale) => {
    const parts = locale.replace("_", "-").split("-");
    const language = (parts[0] || "").toLowerCase();
    const country = parts.length > 1 ? parts[parts.length - 1].toUpperCase() : "";
    return language === "fr" && country === "CA";
  });
  return hasFrenchCanadaLocale ? "qc" : "";
}
const initialLang = savedLang || detectVisitorLanguage();
const visitorMarket = detectVisitorMarket();
const langNames = {
  fr: "Français",
  en: "English",
  da: "Dansk",
  no: "Norsk",
  sv: "Svenska"
};

const footerNewsletterCopy = {
  fr: {
    title: "Je souhaite recevoir de vos nouvelles de temps en temps.",
    consentStart: "En renseignant votre adresse e-mail, vous acceptez de recevoir nos dernières actualités sur nos produits et vous prenez connaissance de nos ",
    consentLink: "mentions légales",
    consentEnd: ".",
    placeholder: "Laissez-nous votre e-mail",
    submit: "S'inscrire",
    instagram: "Instagram",
    invalid: "Merci d’indiquer une adresse e-mail valide.",
    loading: "Enregistrement en cours...",
    success: "Merci, votre adresse est enregistrée.",
    error: "L’enregistrement automatique sera actif après mise en ligne sur OVH."
  },
  en: {
    title: "I would like to hear from you from time to time.",
    consentStart: "By entering your e-mail address, you agree to receive occasional news about our products and acknowledge our ",
    consentLink: "legal notice",
    consentEnd: ".",
    placeholder: "Leave us your e-mail",
    submit: "Subscribe",
    instagram: "Instagram",
    invalid: "Please enter a valid e-mail address.",
    loading: "Saving...",
    success: "Thank you, your e-mail address has been saved.",
    error: "Automatic registration will be active after the OVH upload."
  },
  da: {
    title: "Jeg vil gerne høre fra jer fra tid til anden.",
    consentStart: "Ved at angive din e-mailadresse accepterer du at modtage nyheder om vores produkter og bekræfter vores ",
    consentLink: "juridiske oplysninger",
    consentEnd: ".",
    placeholder: "Skriv din e-mail",
    submit: "Tilmeld",
    instagram: "Instagram",
    invalid: "Indtast venligst en gyldig e-mailadresse.",
    loading: "Gemmer...",
    success: "Tak, din e-mailadresse er gemt.",
    error: "Automatisk registrering bliver aktiv efter upload til OVH."
  },
  no: {
    title: "Jeg vil gjerne høre fra dere fra tid til annen.",
    consentStart: "Ved å skrive inn e-postadressen din samtykker du til å motta nyheter om produktene våre og bekrefter våre ",
    consentLink: "juridiske opplysninger",
    consentEnd: ".",
    placeholder: "Skriv inn e-postadressen din",
    submit: "Meld meg på",
    instagram: "Instagram",
    invalid: "Skriv inn en gyldig e-postadresse.",
    loading: "Lagrer...",
    success: "Takk, e-postadressen din er lagret.",
    error: "Automatisk registrering blir aktiv etter opplasting til OVH."
  },
  sv: {
    title: "Jag vill gärna höra från er då och då.",
    consentStart: "Genom att ange din e-postadress godkänner du att få nyheter om våra produkter och bekräftar vår ",
    consentLink: "juridiska information",
    consentEnd: ".",
    placeholder: "Ange din e-postadress",
    submit: "Prenumerera",
    instagram: "Instagram",
    invalid: "Ange en giltig e-postadress.",
    loading: "Sparar...",
    success: "Tack, din e-postadress har sparats.",
    error: "Automatisk registrering blir aktiv efter uppladdning till OVH."
  }
};

function getSiteRootUrl() {
  const script = document.querySelector('script[src*="assets/js/main.js"]');
  if (!script) return new URL("./", window.location.href).href;
  const scriptUrl = new URL(script.getAttribute("src"), window.location.href).href;
  return scriptUrl.split("/assets/js/")[0] + "/";
}

function renderFooterEnhancements(lang) {
  const footer = document.querySelector(".site-footer");
  const footerGrid = footer && footer.querySelector(".footer-grid");
  if (!footerGrid) return;
  const copy = footerNewsletterCopy[lang] || footerNewsletterCopy.en;
  const rootUrl = getSiteRootUrl();
  let instagramLink = footer.querySelector("[data-footer-instagram]");
  const footerLinks = footer.querySelector(".footer-links");
  if (!instagramLink && footerLinks) {
    instagramLink = document.createElement("a");
    instagramLink.href = "https://www.instagram.com/cognac_esprit_organic/";
    instagramLink.target = "_blank";
    instagramLink.rel = "noopener";
    instagramLink.className = "footer-social-link";
    instagramLink.dataset.footerInstagram = "true";
    footerLinks.appendChild(instagramLink);
  }
  if (instagramLink) {
    instagramLink.innerHTML = `
      <svg aria-hidden="true" viewBox="0 0 24 24" focusable="false">
        <rect x="3.5" y="3.5" width="17" height="17" rx="5"></rect>
        <circle cx="12" cy="12" r="4"></circle>
        <circle cx="17.2" cy="6.8" r="1"></circle>
      </svg>
      <span></span>
    `;
    instagramLink.querySelector("span").textContent = copy.instagram;
    instagramLink.setAttribute("aria-label", copy.instagram);
  }

  let newsletter = footer.querySelector("[data-footer-newsletter]");
  if (!newsletter) {
    newsletter = document.createElement("section");
    newsletter.className = "footer-newsletter";
    newsletter.dataset.footerNewsletter = "true";
    newsletter.innerHTML = `
      <h2></h2>
      <p class="footer-newsletter-consent"><span data-consent-start></span><a data-consent-link></a><span data-consent-end></span></p>
      <form class="footer-newsletter-form" data-newsletter-form>
        <label class="visually-hidden" for="newsletter-email">Adresse e-mail</label>
        <input id="newsletter-email" name="email" type="email" autocomplete="email" required>
        <button type="submit" aria-label="Envoyer">→</button>
      </form>
      <p class="footer-newsletter-status" data-newsletter-status aria-live="polite"></p>
    `;
    footerGrid.appendChild(newsletter);
    const form = newsletter.querySelector("[data-newsletter-form]");
    form.addEventListener("submit", async (event) => {
      event.preventDefault();
      const status = newsletter.querySelector("[data-newsletter-status]");
      const input = form.querySelector('input[type="email"]');
      const button = form.querySelector('button[type="submit"]');
      const email = input.value.trim();
      const activeCopy = footerNewsletterCopy[document.body.dataset.lang] || footerNewsletterCopy.en;
      if (!input.checkValidity()) {
        status.textContent = activeCopy.invalid;
        input.focus();
        return;
      }
      status.textContent = activeCopy.loading;
      button.disabled = true;
      try {
        const response = await fetch(`${getSiteRootUrl()}newsletter.php`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            email,
            language: document.body.dataset.lang || "fr",
            market: document.body.dataset.market || "",
            page: window.location.href
          })
        });
        const result = await response.json().catch(() => ({}));
        if (!response.ok || result.ok !== true) throw new Error("newsletter");
        input.value = "";
        status.textContent = activeCopy.success;
      } catch (error) {
        status.textContent = activeCopy.error;
      } finally {
        button.disabled = false;
      }
    });
  }
  newsletter.querySelector("h2").textContent = copy.title;
  newsletter.querySelector("[data-consent-start]").textContent = copy.consentStart;
  newsletter.querySelector("[data-consent-link]").textContent = copy.consentLink;
  newsletter.querySelector("[data-consent-link]").href = `${rootUrl}mentions-legales.html`;
  newsletter.querySelector("[data-consent-end]").textContent = copy.consentEnd;
  newsletter.querySelector('input[type="email"]').placeholder = copy.placeholder;
  newsletter.querySelector('button[type="submit"]').textContent = copy.submit;
}

const translations = {
  en: {
    "Accueil": "Home",
    "Aller au contenu": "Skip to content",
    "La gamme": "The range",
    "Gamme": "Range",
    "La maison": "The house",
    "Notre démarche": "Our approach",
    "La production": "Production",
    "Léopold et Fanny": "Léopold and Fanny",
    "Visiter": "Visit",
    "Menu": "Menu",
    "Cocktails": "Cocktails",
    "Contact": "Contact",
    "Mentions légales": "Legal notice",
    "Valeurs nutritionnelles": "Nutritional values",
    "Toute la nature de nos Cognacs": "All the nature of our Cognacs",
    "Organique et sans complexe": "Organic and uncomplicated",
    "Accompagner nos Cognacs": "Pair our Cognacs",
    "Laisser courir l'inspiration": "Let inspiration flow",
    "Laisser courir l’inspiration avec des recettes fraîches, naturelles et faciles à servir.": "Let inspiration flow with fresh, natural recipes that are easy to serve.",
    "Bienvenue sur nos terres": "Welcome to our land",
    "Depuis 20 ans, Léopold Croizet conduit son vignoble en agriculture biologique. Il distille, élève et met en bouteille sa production à la propriété.": "For 20 years, Léopold Croizet has managed his vineyard organically. He distils, ages and bottles production at the estate.",
    "Le cycle naturel": "The natural cycle",
    "Travailler dans la durabilité": "Working sustainably",
    "L'esprit organic": "The Organic spirit",
    "Notre histoire": "Our story",
    "Maîtriser & laisser faire": "Mastering & letting nature work",
    "Travailler dans le bon sens": "Working in the right direction",
    "Cultiver pour transmettre": "Cultivating to transmit",
    "est né d’une volonté": "was born from a desire",
    "de transmission dans laquelle": "to transmit, carried by",
    "mettent tout leur cœur,": "with all their heart,",
    "leur énergie": "energy",
    "et leur passion.": "and passion.",
    "L'abus d'alcool est dangereux pour la santé. A consommer avec modération.": "Alcohol abuse is dangerous for your health. Drink responsibly.",
    "Cognac biologique familial, naturel et premium.": "Family, natural and premium organic Cognac.",
    "Cognac biologique familial, naturel, premium et indépendant.": "Family, natural, premium and independent organic Cognac.",
    "Une page B2B export pour les marchés Europe, USA, Canada.": "A B2B export page for Europe, USA and Canada.",
    "Une page dédiée aux importateurs, cavistes, CHR, bars, hôtels et réseaux bio.": "A dedicated page for importers, wine merchants, hospitality, bars, hotels and organic retail networks.",
    "Demander des informations export": "Request export information",
    "Documents à préparer": "Documents to prepare",
    "Fiches produits professionnelles.": "Professional product sheets.",
    "Photos bouteilles et gamme.": "Bottle and range photographs.",
    "Informations réglementaires et nutritionnelles en HTML accessible.": "Regulatory and nutritional information in accessible HTML.",
    "Venez sur le territoire des Fins Bois": "Visit the Fins Bois area",
    "Venez découvrir une petite distillerie nichée sur le territoire des Fins Bois. Nous serons heureux de vous accueillir et de vous faire découvrir quelques secrets de production et de nouvelles expériences gustatives.": "Come and discover a small distillery in the Fins Bois area. We will be pleased to welcome you and share a few production secrets and tasting experiences.",
    "Horaires": "Opening times",
    "Du lundi au vendredi, 10h-12h ou 14h-17h.": "Monday to Friday, 10am-12pm or 2pm-5pm.",
    "Durée : 1h.": "Duration: 1 hour.",
    "Maximum 10 personnes par visite.": "Maximum 10 people per visit.",
    "Ouvrir dans Google Maps": "Open in Google Maps",
    "Email, téléphone, adresse et informations de visite validées.": "Email, phone, address and approved visit information.",
    "Contacter Cognac Esprit Organic": "Contact Cognac Esprit Organic",
    "Téléphone": "Phone",
    "Adresse": "Address",
    "Visites": "Visits",
    "Horaires actuels : lundi-vendredi, 10h-12h ou 14h-17h. Durée : 1h. Maximum : 10 personnes.": "Current visiting hours: Monday-Friday, 10am-12pm or 2pm-5pm. Duration: 1 hour. Maximum: 10 people.",
    "Questions utiles pour Google, les visiteurs et les agents IA.": "Useful questions for Google, visitors and AI agents.",
    "Quels produits Cognac Esprit Organic sont disponibles ?": "Which Cognac Esprit Organic products are available?",
    "Les produits disponibles aujourd’hui sont VS, VSOP, Napoléon, XO, XXO, Single Cask, Pineau blanc et Pineau rouge.": "The range includes VS, VSOP, Napoléon, XO, XXO, Single Cask, white Pineau and red Pineau.",
    "Quels sont les horaires de visite ?": "What are the visiting hours?",
    "Les visites sont possibles lundi-vendredi, 10h-12h ou 14h-17h, durée 1h, maximum 10 personnes.": "Visits are available Monday to Friday, 10am-12pm or 2pm-5pm, duration 1 hour, maximum 10 people.",
    "Quels marchés export sont visés ?": "Which export markets are targeted?",
    "La formulation validée est : Europe, USA, Canada.": "The approved wording is: Europe, USA, Canada.",
    "Où se situe Cognac Esprit Organic ?": "Where is Cognac Esprit Organic located?",
    "Le site est-il indexable pendant la préproduction ?": "Is the site indexable during pre-production?",
    "Non. La première version contient temporairement noindex,nofollow.": "No. The first version temporarily contains noindex,nofollow.",
    "Tableaux accessibles à compléter": "Accessible tables to complete",
    "Valeurs nutritionnelles à compléter par produit": "Nutritional values to complete by product",
    "Statut": "Status",
    "À intégrer depuis les données validées.": "To be added from approved data.",
    "Photos et visuels récupérés de l'ancien site": "Images recovered from the former website",
    "Cette galerie rassemble les visuels utiles récupérés depuis l'ancien site WordPress. Elle sert de réserve propre pour reconstruire les pages sans dépendre de WordPress.": "This gallery gathers useful visuals recovered from the former WordPress website. It provides a clean reserve for rebuilding pages without depending on WordPress.",
    "Recettes cocktails": "Cocktail recipes",
    "Trois créations fraîches autour du Cognac et du Pineau Esprit Organic.": "Three fresh creations around Cognac and Pineau Esprit Organic.",
    "Une page pensée comme un carnet d’inspiration : les fiches visuelles ouvrent l’appétit, les recettes donnent l’essentiel, sans surcharger l’expérience.": "A page designed like an inspiration notebook: the visuals create desire, the recipes give the essentials without overloading the experience.",
    "L’heure dorée": "The Golden Hour",
    "Fraîcheur et élégance du Bio.": "Freshness and organic elegance.",
    "Un cocktail fruité et végétal, aux notes douces de melon charentais, rehaussé par le Cognac Esprit Organic. Très désaltérant, faible en alcool, parfait pour l’été.": "A fruity, vegetal cocktail with gentle Charentais melon notes, lifted by Cognac Esprit Organic. Very refreshing, low in alcohol, perfect for summer.",
    "Ingrédients": "Ingredients",
    "Préparation": "Preparation",
    "Style de dégustation": "Tasting style",
    "Désaltérant": "Refreshing",
    "Frais": "Fresh",
    "Fruité": "Fruity",
    "Pétillant": "Sparkling",
    "Tonique": "Tonic",
    "Épicé": "Spicy",
    "Quelques glaçons": "A few ice cubes",
    "1 rondelle de citron vert": "1 lime slice",
    "1 trait de citron vert": "1 dash of lime",
    "1,5 cl jus de citron vert frais": "1.5 cl fresh lime juice",
    "4 rondelles de concombre": "4 cucumber slices",
    "6 feuilles de menthe fraîche": "6 fresh mint leaves",
    "Eau pétillante": "Sparkling water",
    "Placer tous les ingrédients dans un blender avec quelques glaçons.": "Place all ingredients in a blender with a few ice cubes.",
    "Mixer 15 secondes.": "Blend for 15 seconds.",
    "Servir immédiatement dans un verre rempli de glaçons. Décorer d’une feuille de menthe.": "Serve immediately in a glass filled with ice. Garnish with a mint leaf.",
    "Remplir une timbale cuivrée de glaçons.": "Fill a copper mug with ice.",
    "Verser le Cognac Foundation VS.": "Pour in the Cognac Foundation VS.",
    "Ajouter le jus de citron vert.": "Add the fresh lime juice.",
    "Compléter avec la Ginger Beer.": "Top up with Ginger Beer.",
    "Mélanger délicatement.": "Stir gently.",
    "Décorer d’une rondelle de citron vert.": "Garnish with a lime slice.",
    "Mixer le melon charentais avec le Pineau blanc, le Pineau rouge et le Cognac VSOP.": "Blend the Charentais melon with the white Pineau, red Pineau and Cognac VSOP.",
    "Verser dans un verre rempli de glaçons.": "Pour into a glass filled with ice.",
    "Compléter avec de l’eau pétillante.": "Top up with sparkling water.",
    "Mélanger délicatement et déguster aussitôt.": "Stir gently and enjoy immediately.",
    "La fraîcheur du citron vert rencontre les notes épicées du gingembre et le caractère fruité du Cognac Esprit Organic Foundation VS.": "Fresh lime meets spicy ginger notes and the fruity character of Cognac Esprit Organic Foundation VS.",
    "Naturellement rafraîchissant.": "Naturally refreshing.",
    "L’alliance fruitée et pétillante de nos Pineaux et du Cognac VSOP, rehaussée par la douceur du melon charentais. Frais, léger et irrésistiblement estival.": "The fruity, sparkling alliance of our Pineaux and Cognac VSOP, lifted by the sweetness of Charentais melon. Fresh, light and irresistibly summery.",
    "L’apéritif tendance.": "The contemporary aperitif.",
    "Cognac biologique jeune, fruité et expressif, pensé pour une lecture directe du fruit.": "A young, fruity and expressive organic Cognac with a direct fruit-forward profile.",
    "Cognac biologique rond et gourmand, avec une expression souple des fruits confits, du bois et des épices.": "A rounded and generous organic Cognac, expressing candied fruit, warm oak and spice.",
    "Cognac biologique équilibré, long et poivré, autour des fruits secs et d'une finale mentholée.": "A balanced organic Cognac with length, peppery notes, dried fruit and a fresh finish.",
    "Cognac biologique structuré et généreux, marqué par la cerise noire, les fleurs séchées et le rancio.": "A structured and generous organic Cognac with black cherry, dried flowers and rancio notes.",
    "Premier XXO en agriculture biologique, doux, structuré et très fruité.": "Presented as the first XXO in organic agriculture, soft, structured and fruit-forward.",
    "Édition limitée, 51 %, sélectionnée par Fanny.": "Limited edition, 51%, selected by Fanny.",
    "Pineau des Charentes biologique élaboré avec Colombard et Ugni Blanc, sans sulfites ajoutés.": "Organic Pineau des Charentes made with Colombard and Ugni Blanc, with no added sulphites.",
    "Dégustation": "Tasting",
    "Notes sensorielles": "Sensory notes",
    "Bouche :": "Mouth:",
    "Couleur :": "Colour:",
    "Nez :": "Nose:",
    "Palais :": "Palate:",
    "Finale :": "Finish:",
    "Prendre conscience, mieux produire": "Becoming aware, producing better",
    "Pour mieux consommer, préserver et transmettre.": "To consume better, preserve and pass on.",
    "Déjà 20 ans de production durable": "Already 20 years of sustainable production",
    "Une gamme biologique": "An organic range",
    "Un savoir-faire générationnel": "Generational know-how",
    "Il est là, depuis plus de 20 ans.": "It has been here for more than 20 years.",
    "Un Cru, les Fins Bois": "A cru: Fins Bois",
    "Respect de nos terres et culture de la vigne": "Respect for our land and vine growing",
    "Distillation": "Distillation",
    "Élevage soigné et suivi": "Careful, attentive ageing",
    "L’art subtil de l’assemblage": "The subtle art of blending",
    "La mise en bouteille": "Bottling",
    "Travailler d’une même passion": "Working with the same passion",
    "Un héritage passionnant mis au profit des générations futures.": "A passionate heritage serving future generations."
  },
  da: {
    "Accueil": "Forside",
    "Aller au contenu": "Gå til indhold",
    "La gamme": "Sortimentet",
    "Gamme": "Sortiment",
    "La maison": "Huset",
    "Notre démarche": "Vores tilgang",
    "La production": "Produktionen",
    "Léopold et Fanny": "Léopold og Fanny",
    "Visiter": "Besøg",
    "Menu": "Menu",
    "Cocktails": "Cocktails",
    "Contact": "Kontakt",
    "Mentions légales": "Juridiske oplysninger",
    "Valeurs nutritionnelles": "Næringsværdier",
    "Toute la nature de nos Cognacs": "Hele naturen i vores Cognac",
    "Organique et sans complexe": "Økologisk og ukompliceret",
    "Accompagner nos Cognacs": "Nyd vores Cognacs i cocktails",
    "Laisser courir l'inspiration": "Lad inspirationen flyde",
    "Laisser courir l’inspiration avec des recettes fraîches, naturelles et faciles à servir.": "Lad inspirationen flyde med friske, naturlige opskrifter, der er lette at servere.",
    "Bienvenue sur nos terres": "Velkommen til vores jord",
    "Depuis 20 ans, Léopold Croizet conduit son vignoble en agriculture biologique. Il distille, élève et met en bouteille sa production à la propriété.": "I 20 år har Léopold Croizet dyrket sin vingård økologisk. Han destillerer, lagrer og aftapper produktionen på ejendommen.",
    "Le cycle naturel": "Den naturlige cyklus",
    "Travailler dans la durabilité": "Arbejde bæredygtigt",
    "L'esprit organic": "Den organiske ånd",
    "Notre histoire": "Vores historie",
    "Maîtriser & laisser faire": "Mestre og lade naturen gøre sit",
    "Travailler dans le bon sens": "Arbejde i den rigtige retning",
    "Cultiver pour transmettre": "Dyrke for at give videre",
    "est né d’une volonté": "blev født af et ønske",
    "de transmission dans laquelle": "om at give videre, hvor",
    "mettent tout leur cœur,": "lægger hele deres hjerte,",
    "leur énergie": "deres energi",
    "et leur passion.": "og deres passion.",
    "L'abus d'alcool est dangereux pour la santé. A consommer avec modération.": "Alkoholmisbrug er sundhedsskadeligt. Nydes med måde.",
    "Cognac biologique familial, naturel et premium.": "Familiedrevet, naturlig og premium økologisk Cognac.",
    "Cognac biologique familial, naturel, premium et indépendant.": "Familiedrevet, naturlig, premium og uafhængig økologisk Cognac.",
    "Une page B2B export pour les marchés Europe, USA, Canada.": "En B2B-eksportside for markederne Europa, USA og Canada.",
    "Une page dédiée aux importateurs, cavistes, CHR, bars, hôtels et réseaux bio.": "En side for importører, vinhandlere, restaurationsbranchen, barer, hoteller og økologiske netværk.",
    "Demander des informations export": "Bed om eksportinformation",
    "Documents à préparer": "Dokumenter der skal forberedes",
    "Fiches produits professionnelles.": "Professionelle produktark.",
    "Photos bouteilles et gamme.": "Fotos af flasker og sortiment.",
    "Informations réglementaires et nutritionnelles en HTML accessible.": "Regulatoriske oplysninger og næringsoplysninger i tilgængelig HTML.",
    "Venez sur le territoire des Fins Bois": "Besøg Fins Bois-området",
    "Venez découvrir une petite distillerie nichée sur le territoire des Fins Bois. Nous serons heureux de vous accueillir et de vous faire découvrir quelques secrets de production et de nouvelles expériences gustatives.": "Kom og oplev et lille destilleri i Fins Bois-området. Vi glæder os til at byde dig velkommen og dele nogle produktionshemmeligheder og smagsoplevelser.",
    "Horaires": "Åbningstider",
    "Du lundi au vendredi, 10h-12h ou 14h-17h.": "Mandag til fredag, 10-12 eller 14-17.",
    "Durée : 1h.": "Varighed: 1 time.",
    "Maximum 10 personnes par visite.": "Maksimalt 10 personer pr. besøg.",
    "Ouvrir dans Google Maps": "Åbn i Google Maps",
    "Email, téléphone, adresse et informations de visite validées.": "E-mail, telefon, adresse og godkendte besøgsoplysninger.",
    "Contacter Cognac Esprit Organic": "Kontakt Cognac Esprit Organic",
    "Téléphone": "Telefon",
    "Adresse": "Adresse",
    "Visites": "Besøg",
    "Horaires actuels : lundi-vendredi, 10h-12h ou 14h-17h. Durée : 1h. Maximum : 10 personnes.": "Aktuelle besøgstider: mandag-fredag, 10-12 eller 14-17. Varighed: 1 time. Maksimum: 10 personer.",
    "Questions utiles pour Google, les visiteurs et les agents IA.": "Nyttige spørgsmål for Google, besøgende og AI-agenter.",
    "Quels produits Cognac Esprit Organic sont disponibles ?": "Hvilke Cognac Esprit Organic-produkter er tilgængelige?",
    "Les produits disponibles aujourd’hui sont VS, VSOP, Napoléon, XO, XXO, Single Cask, Pineau blanc et Pineau rouge.": "De tilgængelige produkter er VS, VSOP, Napoléon, XO, XXO, Single Cask, hvid Pineau og rød Pineau.",
    "Quels sont les horaires de visite ?": "Hvad er besøgstiderne?",
    "Les visites sont possibles lundi-vendredi, 10h-12h ou 14h-17h, durée 1h, maximum 10 personnes.": "Besøg er mulige mandag til fredag, 10-12 eller 14-17, varighed 1 time, maksimum 10 personer.",
    "Quels marchés export sont visés ?": "Hvilke eksportmarkeder er målrettet?",
    "La formulation validée est : Europe, USA, Canada.": "Den godkendte formulering er: Europa, USA, Canada.",
    "Où se situe Cognac Esprit Organic ?": "Hvor ligger Cognac Esprit Organic?",
    "Le site est-il indexable pendant la préproduction ?": "Kan siden indekseres under præproduktion?",
    "Non. La première version contient temporairement noindex,nofollow.": "Nej. Den første version indeholder midlertidigt noindex,nofollow.",
    "Tableaux accessibles à compléter": "Tilgængelige tabeller der skal udfyldes",
    "Valeurs nutritionnelles à compléter par produit": "Næringsværdier der skal udfyldes pr. produkt",
    "Statut": "Status",
    "À intégrer depuis les données validées.": "Tilføjes fra godkendte data.",
    "Photos et visuels récupérés de l'ancien site": "Fotos og visuelle elementer fra det tidligere site",
    "Cette galerie rassemble les visuels utiles récupérés depuis l'ancien site WordPress. Elle sert de réserve propre pour reconstruire les pages sans dépendre de WordPress.": "Dette galleri samler nyttige visuelle elementer fra det tidligere WordPress-site. Det fungerer som en ren ressource til at genopbygge siderne uden WordPress.",
    "Recettes cocktails": "Cocktailopskrifter",
    "Trois créations fraîches autour du Cognac et du Pineau Esprit Organic.": "Tre friske kreationer med Cognac og Pineau Esprit Organic.",
    "Une page pensée comme un carnet d’inspiration : les fiches visuelles ouvrent l’appétit, les recettes donnent l’essentiel, sans surcharger l’expérience.": "En side tænkt som en inspirationsbog: de visuelle kort vækker lysten, opskrifterne giver det væsentlige uden at overbelaste oplevelsen.",
    "L’heure dorée": "Den gyldne time",
    "Fraîcheur et élégance du Bio.": "Friskhed og økologisk elegance.",
    "Un cocktail fruité et végétal, aux notes douces de melon charentais, rehaussé par le Cognac Esprit Organic. Très désaltérant, faible en alcool, parfait pour l’été.": "En frugtig og grøn cocktail med bløde noter af Charentais-melon, løftet af Cognac Esprit Organic. Meget forfriskende, lav på alkohol og perfekt til sommeren.",
    "Ingrédients": "Ingredienser",
    "Préparation": "Tilberedning",
    "Style de dégustation": "Smagsstil",
    "Désaltérant": "Forfriskende",
    "Frais": "Frisk",
    "Fruité": "Frugtig",
    "Pétillant": "Mousserende",
    "Tonique": "Tonic",
    "Épicé": "Krydret",
    "Quelques glaçons": "Nogle isterninger",
    "1 rondelle de citron vert": "1 skive lime",
    "1 trait de citron vert": "1 stænk lime",
    "1,5 cl jus de citron vert frais": "1,5 cl frisk limesaft",
    "4 rondelles de concombre": "4 skiver agurk",
    "6 feuilles de menthe fraîche": "6 friske mynteblade",
    "Eau pétillante": "Danskvand",
    "Placer tous les ingrédients dans un blender avec quelques glaçons.": "Kom alle ingredienser i en blender med nogle isterninger.",
    "Mixer 15 secondes.": "Blend i 15 sekunder.",
    "Servir immédiatement dans un verre rempli de glaçons. Décorer d’une feuille de menthe.": "Server straks i et glas fyldt med is. Pynt med et mynteblad.",
    "Remplir une timbale cuivrée de glaçons.": "Fyld et kobberkrus med is.",
    "Verser le Cognac Foundation VS.": "Hæld Cognac Foundation VS i.",
    "Ajouter le jus de citron vert.": "Tilsæt frisk limesaft.",
    "Compléter avec la Ginger Beer.": "Top op med Ginger Beer.",
    "Mélanger délicatement.": "Rør forsigtigt.",
    "Décorer d’une rondelle de citron vert.": "Pynt med en skive lime.",
    "Mixer le melon charentais avec le Pineau blanc, le Pineau rouge et le Cognac VSOP.": "Blend Charentais-melonen med hvid Pineau, rød Pineau og Cognac VSOP.",
    "Verser dans un verre rempli de glaçons.": "Hæld i et glas fyldt med is.",
    "Compléter avec de l’eau pétillante.": "Top op med danskvand.",
    "Mélanger délicatement et déguster aussitôt.": "Rør forsigtigt og nyd med det samme.",
    "La fraîcheur du citron vert rencontre les notes épicées du gingembre et le caractère fruité du Cognac Esprit Organic Foundation VS.": "Frisk lime møder ingefærens krydrede noter og den frugtige karakter i Cognac Esprit Organic Foundation VS.",
    "Naturellement rafraîchissant.": "Naturligt forfriskende.",
    "L’alliance fruitée et pétillante de nos Pineaux et du Cognac VSOP, rehaussée par la douceur du melon charentais. Frais, léger et irrésistiblement estival.": "Den frugtige og perlende forening af vores Pineaux og Cognac VSOP, løftet af Charentais-melonens sødme. Frisk, let og uimodståeligt sommerlig.",
    "L’apéritif tendance.": "Den moderne aperitif.",
    "Cognac biologique jeune, fruité et expressif, pensé pour une lecture directe du fruit.": "En ung, frugtig og udtryksfuld økologisk Cognac med en direkte frugtprofil.",
    "Cognac biologique rond et gourmand, avec une expression souple des fruits confits, du bois et des épices.": "En rund og generøs økologisk Cognac med bløde udtryk af kandiseret frugt, træ og krydderier.",
    "Cognac biologique équilibré, long et poivré, autour des fruits secs et d'une finale mentholée.": "En afbalanceret økologisk Cognac med længde, pebrede noter, tørret frugt og en mentholfrisk afslutning.",
    "Cognac biologique structuré et généreux, marqué par la cerise noire, les fleurs séchées et le rancio.": "En struktureret og generøs økologisk Cognac præget af sort kirsebær, tørrede blomster og rancio.",
    "Premier XXO en agriculture biologique, doux, structuré et très fruité.": "Præsenteret som den første XXO i økologisk landbrug, blød, struktureret og meget frugtig.",
    "Édition limitée, 51 %, sélectionnée par Fanny.": "Begrænset udgave, 51 %, udvalgt af Fanny.",
    "Pineau des Charentes biologique élaboré avec Colombard et Ugni Blanc, sans sulfites ajoutés.": "Økologisk Pineau des Charentes lavet med Colombard og Ugni Blanc, uden tilsatte sulfitter.",
    "Dégustation": "Smagning",
    "Notes sensorielles": "Sensoriske noter",
    "Bouche :": "Mund:",
    "Couleur :": "Farve:",
    "Nez :": "Næse:",
    "Palais :": "Gane:",
    "Finale :": "Afslutning:",
    "Prendre conscience, mieux produire": "Blive bevidst, producere bedre",
    "Pour mieux consommer, préserver et transmettre.": "For at forbruge bedre, bevare og give videre.",
    "Déjà 20 ans de production durable": "Allerede 20 år med bæredygtig produktion",
    "Une gamme biologique": "Et økologisk sortiment",
    "Un savoir-faire générationnel": "Generationers knowhow",
    "Un Cru, les Fins Bois": "En cru: Fins Bois",
    "Respect de nos terres et culture de la vigne": "Respekt for jorden og dyrkning af vinstokken",
    "Distillation": "Destillation",
    "Élevage soigné et suivi": "Omhyggelig og fulgt lagring",
    "L’art subtil de l’assemblage": "Den subtile kunst at blende",
    "La mise en bouteille": "Aftapning",
    "Travailler d’une même passion": "At arbejde med samme passion",
    "Un héritage passionnant mis au profit des générations futures.": "En passioneret arv til gavn for fremtidige generationer."
  },
  no: {
    "Accueil": "Hjem",
    "Aller au contenu": "Gå til innhold",
    "La gamme": "Sortimentet",
    "Gamme": "Sortiment",
    "La maison": "Huset",
    "Notre démarche": "Vår tilnærming",
    "La production": "Produksjonen",
    "Léopold et Fanny": "Léopold og Fanny",
    "Visiter": "Besøk",
    "Menu": "Meny",
    "Cocktails": "Cocktailer",
    "Contact": "Kontakt",
    "Mentions légales": "Juridisk informasjon",
    "Valeurs nutritionnelles": "Næringsverdier",
    "Toute la nature de nos Cognacs": "Hele naturen i vår Cognac",
    "Organique et sans complexe": "Økologisk og ukomplisert",
    "Accompagner nos Cognacs": "Server våre Cognacer i cocktails",
    "Laisser courir l'inspiration": "La inspirasjonen flyte",
    "Laisser courir l’inspiration avec des recettes fraîches, naturelles et faciles à servir.": "La inspirasjonen flyte med friske, naturlige oppskrifter som er enkle å servere.",
    "Bienvenue sur nos terres": "Velkommen til våre marker",
    "Depuis 20 ans, Léopold Croizet conduit son vignoble en agriculture biologique. Il distille, élève et met en bouteille sa production à la propriété.": "I 20 år har Léopold Croizet dyrket vinmarken sin økologisk. Han destillerer, lagrer og tapper produksjonen på eiendommen.",
    "Le cycle naturel": "Den naturlige syklusen",
    "Travailler dans la durabilité": "Arbeide bærekraftig",
    "L'esprit organic": "Den organiske ånden",
    "Notre histoire": "Vår historie",
    "Maîtriser & laisser faire": "Mestre og la naturen virke",
    "Travailler dans le bon sens": "Arbeide i riktig retning",
    "Cultiver pour transmettre": "Dyrke for å føre videre",
    "est né d’une volonté": "ble født av et ønske",
    "de transmission dans laquelle": "om å føre videre, der",
    "mettent tout leur cœur,": "legger hele sitt hjerte,",
    "leur énergie": "sin energi",
    "et leur passion.": "og sin lidenskap.",
    "L'abus d'alcool est dangereux pour la santé. A consommer avec modération.": "Alkoholmisbruk er skadelig for helsen. Nyt med måte.",
    "Cognac biologique familial, naturel et premium.": "Familiedrevet, naturlig og premium økologisk Cognac.",
    "Cognac biologique familial, naturel, premium et indépendant.": "Familiedrevet, naturlig, premium og uavhengig økologisk Cognac.",
    "Une page B2B export pour les marchés Europe, USA, Canada.": "En B2B-eksportside for markedene Europa, USA og Canada.",
    "Une page dédiée aux importateurs, cavistes, CHR, bars, hôtels et réseaux bio.": "En side for importører, vinhandlere, serveringsbransjen, barer, hoteller og økologiske nettverk.",
    "Demander des informations export": "Be om eksportinformasjon",
    "Documents à préparer": "Dokumenter som skal forberedes",
    "Fiches produits professionnelles.": "Profesjonelle produktark.",
    "Photos bouteilles et gamme.": "Bilder av flasker og sortiment.",
    "Informations réglementaires et nutritionnelles en HTML accessible.": "Regulatorisk og ernæringsmessig informasjon i tilgjengelig HTML.",
    "Venez sur le territoire des Fins Bois": "Besøk Fins Bois-området",
    "Venez découvrir une petite distillerie nichée sur le territoire des Fins Bois. Nous serons heureux de vous accueillir et de vous faire découvrir quelques secrets de production et de nouvelles expériences gustatives.": "Kom og oppdag et lite destilleri i Fins Bois-området. Vi tar gjerne imot deg og deler noen produksjonshemmeligheter og smaksopplevelser.",
    "Horaires": "Åpningstider",
    "Du lundi au vendredi, 10h-12h ou 14h-17h.": "Mandag til fredag, 10-12 eller 14-17.",
    "Durée : 1h.": "Varighet: 1 time.",
    "Maximum 10 personnes par visite.": "Maksimalt 10 personer per besøk.",
    "Ouvrir dans Google Maps": "Åpne i Google Maps",
    "Email, téléphone, adresse et informations de visite validées.": "E-post, telefon, adresse og godkjent besøksinformasjon.",
    "Contacter Cognac Esprit Organic": "Kontakt Cognac Esprit Organic",
    "Téléphone": "Telefon",
    "Adresse": "Adresse",
    "Visites": "Besøk",
    "Horaires actuels : lundi-vendredi, 10h-12h ou 14h-17h. Durée : 1h. Maximum : 10 personnes.": "Gjeldende besøkstider: mandag-fredag, 10-12 eller 14-17. Varighet: 1 time. Maksimum: 10 personer.",
    "Questions utiles pour Google, les visiteurs et les agents IA.": "Nyttige spørsmål for Google, besøkende og AI-agenter.",
    "Quels produits Cognac Esprit Organic sont disponibles ?": "Hvilke Cognac Esprit Organic-produkter er tilgjengelige?",
    "Les produits disponibles aujourd’hui sont VS, VSOP, Napoléon, XO, XXO, Single Cask, Pineau blanc et Pineau rouge.": "Tilgjengelige produkter er VS, VSOP, Napoléon, XO, XXO, Single Cask, hvit Pineau og rød Pineau.",
    "Quels sont les horaires de visite ?": "Hva er besøkstidene?",
    "Les visites sont possibles lundi-vendredi, 10h-12h ou 14h-17h, durée 1h, maximum 10 personnes.": "Besøk er mulig mandag til fredag, 10-12 eller 14-17, varighet 1 time, maksimum 10 personer.",
    "Quels marchés export sont visés ?": "Hvilke eksportmarkeder er målrettet?",
    "La formulation validée est : Europe, USA, Canada.": "Den godkjente formuleringen er: Europa, USA, Canada.",
    "Où se situe Cognac Esprit Organic ?": "Hvor ligger Cognac Esprit Organic?",
    "Le site est-il indexable pendant la préproduction ?": "Kan nettstedet indekseres under preproduksjon?",
    "Non. La première version contient temporairement noindex,nofollow.": "Nei. Den første versjonen inneholder midlertidig noindex,nofollow.",
    "Tableaux accessibles à compléter": "Tilgjengelige tabeller som skal fylles ut",
    "Valeurs nutritionnelles à compléter par produit": "Næringsverdier som skal fylles ut per produkt",
    "Statut": "Status",
    "À intégrer depuis les données validées.": "Legges til fra godkjente data.",
    "Photos et visuels récupérés de l'ancien site": "Bilder og visuelle elementer fra det tidligere nettstedet",
    "Cette galerie rassemble les visuels utiles récupérés depuis l'ancien site WordPress. Elle sert de réserve propre pour reconstruire les pages sans dépendre de WordPress.": "Dette galleriet samler nyttige visuelle elementer fra det tidligere WordPress-nettstedet. Det fungerer som en ren ressurs for å gjenoppbygge sidene uten WordPress.",
    "Recettes cocktails": "Cocktailoppskrifter",
    "Trois créations fraîches autour du Cognac et du Pineau Esprit Organic.": "Tre friske kreasjoner med Cognac og Pineau Esprit Organic.",
    "Une page pensée comme un carnet d’inspiration : les fiches visuelles ouvrent l’appétit, les recettes donnent l’essentiel, sans surcharger l’expérience.": "En side tenkt som en inspirasjonsbok: de visuelle kortene vekker lysten, oppskriftene gir det viktigste uten å overbelaste opplevelsen.",
    "L’heure dorée": "Den gylne timen",
    "Fraîcheur et élégance du Bio.": "Friskhet og økologisk eleganse.",
    "Un cocktail fruité et végétal, aux notes douces de melon charentais, rehaussé par le Cognac Esprit Organic. Très désaltérant, faible en alcool, parfait pour l’été.": "En fruktig og grønn cocktail med milde toner av Charentais-melon, løftet av Cognac Esprit Organic. Svært forfriskende, lav på alkohol og perfekt for sommeren.",
    "Ingrédients": "Ingredienser",
    "Préparation": "Tilberedning",
    "Style de dégustation": "Smaksstil",
    "Désaltérant": "Forfriskende",
    "Frais": "Frisk",
    "Fruité": "Fruktig",
    "Pétillant": "Sprudlende",
    "Tonique": "Tonic",
    "Épicé": "Krydret",
    "Quelques glaçons": "Noen isbiter",
    "1 rondelle de citron vert": "1 skive lime",
    "1 trait de citron vert": "1 dash lime",
    "1,5 cl jus de citron vert frais": "1,5 cl fersk limesaft",
    "4 rondelles de concombre": "4 skiver agurk",
    "6 feuilles de menthe fraîche": "6 friske mynteblader",
    "Eau pétillante": "Kullsyrevann",
    "Placer tous les ingrédients dans un blender avec quelques glaçons.": "Ha alle ingrediensene i en blender med noen isbiter.",
    "Mixer 15 secondes.": "Blend i 15 sekunder.",
    "Servir immédiatement dans un verre rempli de glaçons. Décorer d’une feuille de menthe.": "Server straks i et glass fylt med is. Pynt med et mynteblad.",
    "Remplir une timbale cuivrée de glaçons.": "Fyll et kobberkrus med is.",
    "Verser le Cognac Foundation VS.": "Hell i Cognac Foundation VS.",
    "Ajouter le jus de citron vert.": "Tilsett fersk limesaft.",
    "Compléter avec la Ginger Beer.": "Topp med Ginger Beer.",
    "Mélanger délicatement.": "Rør forsiktig.",
    "Décorer d’une rondelle de citron vert.": "Pynt med en skive lime.",
    "Mixer le melon charentais avec le Pineau blanc, le Pineau rouge et le Cognac VSOP.": "Blend Charentais-melonen med hvit Pineau, rød Pineau og Cognac VSOP.",
    "Verser dans un verre rempli de glaçons.": "Hell i et glass fylt med is.",
    "Compléter avec de l’eau pétillante.": "Topp med kullsyrevann.",
    "Mélanger délicatement et déguster aussitôt.": "Rør forsiktig og nyt med det samme.",
    "La fraîcheur du citron vert rencontre les notes épicées du gingembre et le caractère fruité du Cognac Esprit Organic Foundation VS.": "Frisk lime møter ingefærens krydrede toner og den fruktige karakteren til Cognac Esprit Organic Foundation VS.",
    "Naturellement rafraîchissant.": "Naturlig forfriskende.",
    "L’alliance fruitée et pétillante de nos Pineaux et du Cognac VSOP, rehaussée par la douceur du melon charentais. Frais, léger et irrésistiblement estival.": "Den fruktige og perlende kombinasjonen av våre Pineaux og Cognac VSOP, løftet av sødmen fra Charentais-melon. Frisk, lett og uimotståelig sommerlig.",
    "L’apéritif tendance.": "Den moderne aperitiffen.",
    "Cognac biologique jeune, fruité et expressif, pensé pour une lecture directe du fruit.": "En ung, fruktig og uttrykksfull økologisk Cognac med en direkte fruktprofil.",
    "Cognac biologique rond et gourmand, avec une expression souple des fruits confits, du bois et des épices.": "En rund og generøs økologisk Cognac med myke uttrykk av kandisert frukt, tre og krydder.",
    "Cognac biologique équilibré, long et poivré, autour des fruits secs et d'une finale mentholée.": "En balansert økologisk Cognac med lengde, peppertoner, tørket frukt og en mentolfrisk avslutning.",
    "Cognac biologique structuré et généreux, marqué par la cerise noire, les fleurs séchées et le rancio.": "En strukturert og generøs økologisk Cognac preget av sort kirsebær, tørkede blomster og rancio.",
    "Premier XXO en agriculture biologique, doux, structuré et très fruité.": "Presentert som den første XXO i økologisk landbruk, myk, strukturert og svært fruktig.",
    "Édition limitée, 51 %, sélectionnée par Fanny.": "Begrenset utgave, 51 %, valgt ut av Fanny.",
    "Pineau des Charentes biologique élaboré avec Colombard et Ugni Blanc, sans sulfites ajoutés.": "Økologisk Pineau des Charentes laget med Colombard og Ugni Blanc, uten tilsatte sulfitter.",
    "Dégustation": "Smaking",
    "Notes sensorielles": "Sensoriske noter",
    "Bouche :": "Munn:",
    "Couleur :": "Farge:",
    "Nez :": "Nese:",
    "Palais :": "Gane:",
    "Finale :": "Avslutning:",
    "Prendre conscience, mieux produire": "Bli bevisst, produsere bedre",
    "Pour mieux consommer, préserver et transmettre.": "For å konsumere bedre, bevare og føre videre.",
    "Déjà 20 ans de production durable": "Allerede 20 år med bærekraftig produksjon",
    "Une gamme biologique": "Et økologisk sortiment",
    "Un savoir-faire générationnel": "Generasjoners fagkunnskap",
    "Un Cru, les Fins Bois": "En cru: Fins Bois",
    "Respect de nos terres et culture de la vigne": "Respekt for jorden og dyrking av vinrankene",
    "Distillation": "Destillasjon",
    "Élevage soigné et suivi": "Omhyggelig og fulgt lagring",
    "L’art subtil de l’assemblage": "Den subtile kunsten å blende",
    "La mise en bouteille": "Tapping",
    "Travailler d’une même passion": "Å arbeide med samme lidenskap",
    "Un héritage passionnant mis au profit des générations futures.": "En lidenskapelig arv til nytte for kommende generasjoner."
  },
  sv: {
    "Accueil": "Startsida",
    "Aller au contenu": "Gå till innehåll",
    "La gamme": "Sortimentet",
    "Gamme": "Sortiment",
    "La maison": "Huset",
    "Notre démarche": "Vårt arbetssätt",
    "La production": "Produktionen",
    "Léopold et Fanny": "Léopold och Fanny",
    "Visiter": "Besök",
    "Menu": "Meny",
    "Cocktails": "Cocktails",
    "Contact": "Kontakt",
    "Mentions légales": "Juridisk information",
    "Valeurs nutritionnelles": "Näringsvärden",
    "Toute la nature de nos Cognacs": "All natur i våra Cognacer",
    "Organique et sans complexe": "Ekologiskt och okomplicerat",
    "Accompagner nos Cognacs": "Servera våra Cognacer i cocktails",
    "Laisser courir l'inspiration": "Låt inspirationen flöda",
    "Laisser courir l’inspiration avec des recettes fraîches, naturelles et faciles à servir.": "Låt inspirationen flöda med fräscha, naturliga recept som är enkla att servera.",
    "Bienvenue sur nos terres": "Välkommen till våra marker",
    "Depuis 20 ans, Léopold Croizet conduit son vignoble en agriculture biologique. Il distille, élève et met en bouteille sa production à la propriété.": "I 20 år har Léopold Croizet odlat sin vingård ekologiskt. Han destillerar, lagrar och buteljerar produktionen på gården.",
    "Le cycle naturel": "Den naturliga cykeln",
    "Travailler dans la durabilité": "Arbeta hållbart",
    "L'esprit organic": "Den ekologiska andan",
    "Notre histoire": "Vår historia",
    "Maîtriser & laisser faire": "Bemästra och låta naturen verka",
    "Travailler dans le bon sens": "Arbeta i rätt riktning",
    "Cultiver pour transmettre": "Odla för att föra vidare",
    "est né d’une volonté": "föddes ur en vilja",
    "de transmission dans laquelle": "att föra vidare, där",
    "mettent tout leur cœur,": "lägger hela sitt hjärta,",
    "leur énergie": "sin energi",
    "et leur passion.": "och sin passion.",
    "L'abus d'alcool est dangereux pour la santé. A consommer avec modération.": "Alkoholmissbruk är skadligt för hälsan. Njut med måtta.",
    "Cognac biologique familial, naturel et premium.": "Familjedriven, naturlig och premium ekologisk Cognac.",
    "Cognac biologique familial, naturel, premium et indépendant.": "Familjedriven, naturlig, premium och oberoende ekologisk Cognac.",
    "Une page B2B export pour les marchés Europe, USA, Canada.": "En B2B-exportsida för marknaderna Europa, USA och Kanada.",
    "Une page dédiée aux importateurs, cavistes, CHR, bars, hôtels et réseaux bio.": "En sida för importörer, vinhandlare, restaurangbranschen, barer, hotell och ekologiska nätverk.",
    "Demander des informations export": "Begär exportinformation",
    "Documents à préparer": "Dokument att förbereda",
    "Fiches produits professionnelles.": "Professionella produktblad.",
    "Photos bouteilles et gamme.": "Bilder på flaskor och sortiment.",
    "Informations réglementaires et nutritionnelles en HTML accessible.": "Regulatorisk information och näringsinformation i tillgänglig HTML.",
    "Venez sur le territoire des Fins Bois": "Besök Fins Bois-området",
    "Venez découvrir une petite distillerie nichée sur le territoire des Fins Bois. Nous serons heureux de vous accueillir et de vous faire découvrir quelques secrets de production et de nouvelles expériences gustatives.": "Kom och upptäck ett litet destilleri i Fins Bois-området. Vi tar gärna emot dig och delar några produktionshemligheter och smakupplevelser.",
    "Horaires": "Öppettider",
    "Du lundi au vendredi, 10h-12h ou 14h-17h.": "Måndag till fredag, 10-12 eller 14-17.",
    "Durée : 1h.": "Längd: 1 timme.",
    "Maximum 10 personnes par visite.": "Högst 10 personer per besök.",
    "Ouvrir dans Google Maps": "Öppna i Google Maps",
    "Email, téléphone, adresse et informations de visite validées.": "E-post, telefon, adress och godkänd besöksinformation.",
    "Contacter Cognac Esprit Organic": "Kontakta Cognac Esprit Organic",
    "Téléphone": "Telefon",
    "Adresse": "Adress",
    "Visites": "Besök",
    "Horaires actuels : lundi-vendredi, 10h-12h ou 14h-17h. Durée : 1h. Maximum : 10 personnes.": "Aktuella besökstider: måndag-fredag, 10-12 eller 14-17. Längd: 1 timme. Max: 10 personer.",
    "Questions utiles pour Google, les visiteurs et les agents IA.": "Nyttiga frågor för Google, besökare och AI-agenter.",
    "Quels produits Cognac Esprit Organic sont disponibles ?": "Vilka Cognac Esprit Organic-produkter finns tillgängliga?",
    "Les produits disponibles aujourd’hui sont VS, VSOP, Napoléon, XO, XXO, Single Cask, Pineau blanc et Pineau rouge.": "Tillgängliga produkter är VS, VSOP, Napoléon, XO, XXO, Single Cask, vit Pineau och röd Pineau.",
    "Quels sont les horaires de visite ?": "Vilka är besökstiderna?",
    "Les visites sont possibles lundi-vendredi, 10h-12h ou 14h-17h, durée 1h, maximum 10 personnes.": "Besök är möjliga måndag till fredag, 10-12 eller 14-17, längd 1 timme, högst 10 personer.",
    "Quels marchés export sont visés ?": "Vilka exportmarknader är målgruppen?",
    "La formulation validée est : Europe, USA, Canada.": "Den godkända formuleringen är: Europa, USA, Kanada.",
    "Où se situe Cognac Esprit Organic ?": "Var ligger Cognac Esprit Organic?",
    "Le site est-il indexable pendant la préproduction ?": "Kan webbplatsen indexeras under förproduktionen?",
    "Non. La première version contient temporairement noindex,nofollow.": "Nej. Den första versionen innehåller tillfälligt noindex,nofollow.",
    "Tableaux accessibles à compléter": "Tillgängliga tabeller att komplettera",
    "Valeurs nutritionnelles à compléter par produit": "Näringsvärden att komplettera per produkt",
    "Statut": "Status",
    "À intégrer depuis les données validées.": "Läggs till från godkända data.",
    "Photos et visuels récupérés de l'ancien site": "Bilder och visuellt material från den tidigare webbplatsen",
    "Cette galerie rassemble les visuels utiles récupérés depuis l'ancien site WordPress. Elle sert de réserve propre pour reconstruire les pages sans dépendre de WordPress.": "Detta galleri samlar användbart visuellt material från den tidigare WordPress-webbplatsen. Det fungerar som en ren resurs för att bygga om sidorna utan WordPress.",
    "Recettes cocktails": "Cocktailrecept",
    "Trois créations fraîches autour du Cognac et du Pineau Esprit Organic.": "Tre fräscha skapelser med Cognac och Pineau Esprit Organic.",
    "Une page pensée comme un carnet d’inspiration : les fiches visuelles ouvrent l’appétit, les recettes donnent l’essentiel, sans surcharger l’expérience.": "En sida tänkt som en inspirationsbok: de visuella korten väcker lusten, recepten ger det väsentliga utan att överbelasta upplevelsen.",
    "L’heure dorée": "Den gyllene timmen",
    "Fraîcheur et élégance du Bio.": "Fräschör och ekologisk elegans.",
    "Un cocktail fruité et végétal, aux notes douces de melon charentais, rehaussé par le Cognac Esprit Organic. Très désaltérant, faible en alcool, parfait pour l’été.": "En fruktig och grön cocktail med mjuka toner av Charentais-melon, lyft av Cognac Esprit Organic. Mycket uppfriskande, låg alkoholhalt och perfekt för sommaren.",
    "Ingrédients": "Ingredienser",
    "Préparation": "Tillredning",
    "Style de dégustation": "Smakstil",
    "Désaltérant": "Uppfriskande",
    "Frais": "Fräsch",
    "Fruité": "Fruktig",
    "Pétillant": "Mousserande",
    "Tonique": "Tonic",
    "Épicé": "Kryddig",
    "Quelques glaçons": "Några isbitar",
    "1 rondelle de citron vert": "1 skiva lime",
    "1 trait de citron vert": "1 skvätt lime",
    "1,5 cl jus de citron vert frais": "1,5 cl färsk limejuice",
    "4 rondelles de concombre": "4 skivor gurka",
    "6 feuilles de menthe fraîche": "6 färska myntablad",
    "Eau pétillante": "Kolsyrat vatten",
    "Placer tous les ingrédients dans un blender avec quelques glaçons.": "Lägg alla ingredienser i en blender med några isbitar.",
    "Mixer 15 secondes.": "Mixa i 15 sekunder.",
    "Servir immédiatement dans un verre rempli de glaçons. Décorer d’une feuille de menthe.": "Servera direkt i ett glas fyllt med is. Garnera med ett myntablad.",
    "Remplir une timbale cuivrée de glaçons.": "Fyll en kopparmugg med is.",
    "Verser le Cognac Foundation VS.": "Häll i Cognac Foundation VS.",
    "Ajouter le jus de citron vert.": "Tillsätt färsk limejuice.",
    "Compléter avec la Ginger Beer.": "Toppa med Ginger Beer.",
    "Mélanger délicatement.": "Rör försiktigt.",
    "Décorer d’une rondelle de citron vert.": "Garnera med en skiva lime.",
    "Mixer le melon charentais avec le Pineau blanc, le Pineau rouge et le Cognac VSOP.": "Mixa Charentais-melonen med vit Pineau, röd Pineau och Cognac VSOP.",
    "Verser dans un verre rempli de glaçons.": "Häll i ett glas fyllt med is.",
    "Compléter avec de l’eau pétillante.": "Toppa med kolsyrat vatten.",
    "Mélanger délicatement et déguster aussitôt.": "Rör försiktigt och njut direkt.",
    "La fraîcheur du citron vert rencontre les notes épicées du gingembre et le caractère fruité du Cognac Esprit Organic Foundation VS.": "Frisk lime möter ingefärans kryddiga toner och den fruktiga karaktären hos Cognac Esprit Organic Foundation VS.",
    "Naturellement rafraîchissant.": "Naturligt uppfriskande.",
    "L’alliance fruitée et pétillante de nos Pineaux et du Cognac VSOP, rehaussée par la douceur du melon charentais. Frais, léger et irrésistiblement estival.": "Den fruktiga och bubblande föreningen av våra Pineaux och Cognac VSOP, lyft av sötman från Charentais-melon. Fräsch, lätt och oemotståndligt somrig.",
    "L’apéritif tendance.": "Den moderna aperitifen.",
    "Cognac biologique jeune, fruité et expressif, pensé pour une lecture directe du fruit.": "En ung, fruktig och uttrycksfull ekologisk Cognac med en direkt fruktprofil.",
    "Cognac biologique rond et gourmand, avec une expression souple des fruits confits, du bois et des épices.": "En rund och generös ekologisk Cognac med mjuka uttryck av kanderad frukt, trä och kryddor.",
    "Cognac biologique équilibré, long et poivré, autour des fruits secs et d'une finale mentholée.": "En balanserad ekologisk Cognac med längd, peppriga toner, torkad frukt och en mentolfrisk avslutning.",
    "Cognac biologique structuré et généreux, marqué par la cerise noire, les fleurs séchées et le rancio.": "En strukturerad och generös ekologisk Cognac präglad av svart körsbär, torkade blommor och rancio.",
    "Premier XXO en agriculture biologique, doux, structuré et très fruité.": "Presenterad som den första XXO inom ekologiskt jordbruk, mjuk, strukturerad och mycket fruktig.",
    "Édition limitée, 51 %, sélectionnée par Fanny.": "Begränsad upplaga, 51 %, utvald av Fanny.",
    "Pineau des Charentes biologique élaboré avec Colombard et Ugni Blanc, sans sulfites ajoutés.": "Ekologisk Pineau des Charentes gjord med Colombard och Ugni Blanc, utan tillsatta sulfiter.",
    "Dégustation": "Provning",
    "Notes sensorielles": "Sensoriska noter",
    "Bouche :": "Mun:",
    "Couleur :": "Färg:",
    "Nez :": "Doft:",
    "Palais :": "Gom:",
    "Finale :": "Avslutning:",
    "Prendre conscience, mieux produire": "Bli medveten, producera bättre",
    "Pour mieux consommer, préserver et transmettre.": "För att konsumera bättre, bevara och föra vidare.",
    "Déjà 20 ans de production durable": "Redan 20 år av hållbar produktion",
    "Une gamme biologique": "Ett ekologiskt sortiment",
    "Un savoir-faire générationnel": "Generationers kunnande",
    "Un Cru, les Fins Bois": "En cru: Fins Bois",
    "Respect de nos terres et culture de la vigne": "Respekt för jorden och odlingen av vinrankan",
    "Distillation": "Destillation",
    "Élevage soigné et suivi": "Omsorgsfull och följd lagring",
    "L’art subtil de l’assemblage": "Den subtila konsten att blenda",
    "La mise en bouteille": "Buteljering",
    "Travailler d’une même passion": "Att arbeta med samma passion",
    "Un héritage passionnant mis au profit des générations futures.": "Ett passionerat arv till gagn för kommande generationer."
  }
};

const legacyPageTranslations = {
  en: {
    "La Production": "Production",
    "Je dédie FONDATION à ma grand-mère Germaine, pionnière de la famille, qui me répétait sans cesse : Ce patrimoine est solide car il est sain, la terre n’a pas besoin d’autre chose que le travail de l’homme et ses connaissances. Les produits chimiques ne sont pas nécessaires pour que la vigne pousse et produise. C’est ce discours impactant qui m’a poussé à crée cette marque.": "I dedicate FONDATION to my grandmother Germaine, a pioneer in the family, who kept telling me: this heritage is strong because it is healthy; the land needs nothing more than human work and knowledge. Chemicals are not necessary for vines to grow and produce. This powerful belief inspired me to create this brand.",
    "FONDATION se caractérise par une belle fraîcheur en bouche des notes fruitées de poire et de pêche ou encore de fleur de vigne. Les premiers tannins du bois révèlent des arômes briochés. Idéal pour réaliser des cocktails ou être consommé sur glace.": "FONDATION is marked by a fresh palate with fruity notes of pear, peach and vine flower. The first wood tannins reveal brioche aromas. Ideal for cocktails or served over ice.",
    "Fanny et moi-même sommes convaincus qu’un « mieux produire » est la meilleure solution pour préserver notre vignoble et nous permettre de continuer à travailler de manière passionnée dans le respect de la terre. CONVICTION c’est un hommage à notre vision d’une vie saine, d’un bon sens paysan mais aussi à notre alliance dans le travail et dans la vie.": "Fanny and I are convinced that producing better is the best way to preserve our vineyard and to keep working with passion while respecting the land. CONVICTION pays tribute to our vision of a healthy life, rural common sense and our partnership in work and in life.",
    "CONVICTION est un cognac rond et gourmand. Les premières années en fûts lui confèrent des notes de fruits confits et de vanille. On y trouve en bouche des notes de fruits secs, de bois chaud et d’épices. CONVICTION offre une finale fraîche de clou de girofle.": "CONVICTION is a rounded, generous Cognac. Its first years in cask bring notes of candied fruit and vanilla. The palate reveals dried fruit, warm oak and spice. CONVICTION finishes with a fresh clove note.",
    "La réussite de cette gamme tient aussi dans la force dont chacun d’entre nous a su faire preuve. Mon grand-père Marc et son frère Roger, ma grand-mère Germaine et mes parents Pierre et Eliane ont largement contribué à l’aboutissement de cet engagement dans l’agriculture biologique. C’est un travail d’équipe qui remonte à plusieurs générations. COHESION leur rend hommage.": "The success of this range also lies in the strength shown by each of us. My grandfather Marc and his brother Roger, my grandmother Germaine and my parents Pierre and Eliane all contributed greatly to this commitment to organic agriculture. It is teamwork rooted in several generations. COHESION pays tribute to them.",
    "Une finale masculine, équilibrée, légèrement poivrée et mentholée": "A structured, balanced finish, lightly peppery and mentholated",
    "Un vieillissement généreux en barriques lui confère de belles notes de fruits secs (cacahuète, amande, noisette) et de bois chaud et d’épices. Finale longue et poivrée.": "Generous ageing in barrels gives it fine notes of dried fruit, including peanut, almond and hazelnut, with warm oak and spice. Long, peppery finish.",
    "Le respect de l’environnement doit être un des engagements majeurs des générations futures. Quelle terre allons-nous laisser à nos enfants demain ? J’aimerai dédier ce cognac aux générations à venir et à mes enfants plus particulièrement. La transmission symbolise pour moi le fruit d’un travail soigné et consciencieux d’une génération prête à passer le relai à la suivante. Nous ne sommes que des passeurs.": "Respect for the environment must be one of the major commitments of future generations. What land will we leave our children tomorrow? I would like to dedicate this Cognac to generations to come, and especially to my children. Transmission symbolizes the fruit of careful, conscientious work by one generation ready to pass the baton to the next. We are only guardians passing it on.",
    "Structurée avec une belle rondeur en bouche": "Structured with beautiful roundness on the palate",
    "De nombreuses années de vieillissement ont été nécessaires pour élaborer TRANSMISSION. On y trouve en bouche des notes fruitées (cerise noire) et fleuries (fleurs séchées). Les premières notes du rancio apparaissent en finale.": "Many years of ageing were needed to create TRANSMISSION. The palate reveals fruity notes of black cherry and floral notes of dried flowers. The first rancio notes appear on the finish.",
    "Nous sommes très fiers de présenter le Premier XXO en agriculture Biologique. Ce cognac est issu d’un assemblage d’eaux de vie dont la plus jeune à 14 ans. C’est un cognac structuré, très fruité. Les eaux de vie qui composent ce XXO ont vieilli dans des barriques neuves de chêne de gros grains type Limousin.": "We are very proud to present the first XXO in organic agriculture. This Cognac is made from a blend of eaux-de-vie, the youngest of which is 14 years old. It is structured and very fruity. The eaux-de-vie in this XXO aged in new Limousin-type, wide-grain oak barrels.",
    "Rondeur, douceur et délicatesse": "Roundness, softness and delicacy",
    "Après une extraction tannique de quelques années, elles ont terminé de vieillir dans des barriques rousses, dans les chais humides du domaine familial. Ce type d’environnement offre aux eaux de vie de la rondeur et de la douceur. C’est cette douceur qui nous a permis conserver son titre à 43,5% plutôt que 40%. Nous évitons ainsi toutes dilution excessive des arômes délicats qui le composent. Léopold CROIZET": "After several years of tannic extraction, they completed their ageing in older red barrels in the humid cellars of the family estate. This environment gives the eaux-de-vie roundness and softness. That softness allowed us to keep it at 43.5% rather than 40%, avoiding excessive dilution of its delicate aromas. Léopold CROIZET",
    "Proposé en édition limitée ce brut de fût a été sélectionné par Fanny notre maitre de chai pour ses qualités propres et son fort potentiel aromatique. Les eaux de vie de ce millésime exceptionnel ont débuté leur vieillissement en barriques neuves de chêne français sur un mix de grains. Elles ont ensuite fini de se « patiner » dans nos vieilles barriques rousses afin que le temps œuvre et que la magie de l’oxydation et de l’évaporation opère. Cet échange, obtenu après de longues années de vieillissement offre un résultat exceptionnel : une palette aromatique fondue, harmonieuse et riche !": "Offered as a limited edition, this cask strength Cognac was selected by Fanny, our cellar master, for its intrinsic qualities and strong aromatic potential. The eaux-de-vie from this exceptional vintage began ageing in new French oak barrels with mixed grain. They then finished developing in our old red barrels, allowing time, oxidation and evaporation to work their magic. After long years of ageing, this exchange gives an exceptional result: a melted, harmonious and rich aromatic palette.",
    "Naturellement boisé": "Naturally woody",
    "Une seule barrique a été retenue pour l’incroyable richesse aromatique qu’elle dégageait et pour la douceur de ses parfums. Elle n’a subi aucune adjonction de boisé ni de sucre et a subi une réduction douce et régulière d’eau distillée afin d’amener le cognac à un vieillissement final de 52%. Ce premier Single Cask est déjà une belle réussite, titrant à 51%.": "A single barrel was chosen for its incredible aromatic richness and the softness of its aromas. No wood extract or sugar was added. It was gently and gradually reduced with distilled water to bring the Cognac to a final ageing strength of 52%. This first Single Cask is already a fine success, bottled at 51%.",
    "Ce pineau des Charentes est élaboré à partir d’un assemblage d'eaux-de-vie de cognac et de moût de raisins issus de nos cépages de Colombard et d'Ugni Blanc. Il a vieilli pendant de nombreuses années en fûts de chêne, ce qui lui donne sa couleur ambrée et brillante. On retrouve en bouche des notes de fruits confits et de vanille. C’est un pineau riche et gourmand, bien structuré avec des notes intenses et harmonieuses.": "This Pineau des Charentes is made from a blend of Cognac eaux-de-vie and grape must from our Colombard and Ugni Blanc varieties. It aged for many years in oak casks, giving it its bright amber colour. The palate shows notes of candied fruit and vanilla. It is a rich, generous Pineau, well structured with intense and harmonious notes.",
    "Bois de chêne, brioche, fleur de vigne, pêche, poire, vanille": "Oak, brioche, vine flower, peach, pear, vanilla",
    "Jaune or, jaune paille": "Golden yellow, straw yellow",
    "Arômes de fruits frais tels que poire, pêche et fruits compotés (pommes au four et raisins secs dorés)": "Fresh fruit aromas such as pear and peach, with stewed fruit notes, baked apple and golden raisins",
    "Subtil mélange de fraîcheur et de fruité suivi par la rondeur de notes briochées et vanillées": "Subtle mix of freshness and fruit, followed by round brioche and vanilla notes",
    "Fraîcheur fruitée de raisin frais et de poire": "Fruity freshness of fresh grape and pear",
    "Abricot sec, clou de girofle, prune, rose, vanille": "Dried apricot, clove, plum, rose, vanilla",
    "Jaune doré": "Golden yellow",
    "Équilibré et rond : bois de chêne et de vanille. Subtile touche de fruits compotés (pruneau, abricot).": "Balanced and rounded: oak and vanilla. Subtle touch of stewed fruit, prune and apricot.",
    "Riche et ample avec un beau caractère fruité typique du cru Fins Bois": "Rich and broad with a fine fruity character typical of the Fins Bois cru",
    "Fraîche, clou de girofle": "Fresh, clove",
    "Amande, bois chaud légèrement vanillé, cacahouète, noisette, poire, toffee": "Almond, warm lightly vanilla oak, peanut, hazelnut, pear, toffee",
    "Jaune orangé": "Orange-yellow",
    "Un vieillissement en barrique laissant apparaitre les premières notes boisées et vanillées.": "Barrel ageing reveals the first woody and vanilla notes.",
    "De fins tanins de chêne se lient aux notes de fruits secs : amande, noisette et noix": "Fine oak tannins combine with dried-fruit notes: almond, hazelnut and walnut",
    "Masculine, équilibrée, légèrement poivrée et mentholée": "Structured, balanced, lightly peppery and mentholated",
    "Bois, cannelle, gingembre confit, pruneau, tabac, vanille": "Wood, cinnamon, candied ginger, prune, tobacco, vanilla",
    "Ambre doré": "Golden amber",
    "Complexe de fruits (cerise noire) accompagné de notes fleuries (fleurs sauvages) et de quelques épices chaudes. Avec le temps, les arômes évoluent vers des notes de fruits confits et d'épices et de vieux bois": "Complex fruit, black cherry, with floral notes of wild flowers and warm spices. Over time the aromas evolve toward candied fruit, spices and old wood",
    "Explosion de saveurs et d'arômes épicés": "An explosion of spicy flavours and aromas",
    "Épicée de noix de muscade et de cannelle. Le rancio apparait en finale et mentholée": "Spiced with nutmeg and cinnamon. Rancio appears on the fresh mentholated finish",
    "Cannelle, tabac et fleurs séchées, fruits confits": "Cinnamon, tobacco, dried flowers, candied fruit",
    "Ambrée, aux reflets dorés": "Amber with golden highlights",
    "Notes explosives de fruits confits et compotées, d’épices douces de cannelle": "Expressive notes of candied and stewed fruit, with gentle cinnamon spice",
    "C’est un cognac rond et riche, structuré": "A round, rich and structured Cognac",
    "Finale fraiche, notes de réglisse": "Fresh finish with liquorice notes",
    "Tabac et fleurs séchées, fruits confits": "Tobacco and dried flowers, candied fruit",
    "Ambre foncée, aux reflets rouges": "Dark amber with red highlights",
    "Notes intense d’orange confite et de gingembre, de pruneaux. On y retrouve également des notes de clou de girofle": "Intense notes of candied orange, ginger and prune, with clove notes",
    "C’est un cognac fort, épicé, les fruits confits sont très présents": "A powerful, spicy Cognac with very present candied fruit",
    "Finale fraiche de clou de girofle": "Fresh clove finish",
    "Brioche, jus de raisin frais, poire, pruneau, vanille": "Brioche, fresh grape juice, pear, prune, vanilla",
    "Jaune or, jaune paille, brillant": "Golden yellow, straw yellow, bright",
    "Élaboré, équilibré. Belle association de notes fruitées (raisins frais, poire) et vanillées": "Elaborate and balanced. Fine combination of fruity notes, fresh grape and pear, with vanilla",
    "Riche, gourmand, complexe": "Rich, generous, complex",
    "Fruité, intense, gourmand": "Fruity, intense, generous",
    "Nous sommes fiers d’être implantés dans le cru des Fins Bois, cru que nous revendiquons haut et fort. Il ne faut pas oublier que c’est le cru majoritaire de notre région, il coule dans les veines de nombreuses bouteilles de cognac.": "We are proud to be established in the Fins Bois cru, a cru we proudly claim. It is the major cru of our region and runs through many bottles of Cognac.",
    "Notre domaine se situe à proximité de Jarnac et bénéficie des terres calcaires de champagne et des terres argilocalcaires et de « groies » des Fins Bois. Cette diversité apporte à nos eaux-de-vie une belle complexité aromatique.": "Our estate is located near Jarnac and benefits from chalky Champagne soils as well as clay-limestone and groies soils from Fins Bois. This diversity brings fine aromatic complexity to our eaux-de-vie.",
    "Nous respectons les sols en cultivant la vigne sans produits chimiques ni pesticides. Trèfle et fèverole habitent nos vignes et favorisent la régénération des sols. La conduite des vignes est étudiée en fonction du type de sol et des parcelles.": "We respect the soils by growing vines without chemical products or pesticides. Clover and fava bean grow among our vines and help regenerate the soils. Vine management is adapted to each soil type and plot.",
    "Le but est d’obtenir des raisins sains de la meilleure qualité possible. Nous cultivons la diversité : le domaine se compose de 3 cépages de vins blancs : l’Ugni Blanc, le Colombard et la Folle Blanche.": "The aim is to obtain healthy grapes of the best possible quality. We cultivate diversity: the estate includes three white wine grape varieties, Ugni Blanc, Colombard and Folle Blanche.",
    "C’est une technique propre à notre maison, que je tiens de mon père, qu’il tenait lui-même de sa mère. Elle souligne la rondeur des eaux-de-vie et développe l’intensité des parfums de notre cru.": "This is a technique specific to our house, passed to me by my father, who inherited it from his mother. It highlights the roundness of the eaux-de-vie and develops the intensity of the aromas of our cru.",
    "Nous distillons dans 2 alambics en cuivre de 16 hl et 20 hl pour souligner cette complexité aromatique que l’on chérit tant.": "We distil in two copper stills of 16 hl and 20 hl to express the aromatic complexity we value so deeply.",
    "Fanny s’occupe passionnément d’élever nos eaux-de-vie, elle prend son temps et laisse s’opérer cette étape magique. Elle sélectionne avec soin ses barriques, en fonction des grains du bois, des chauffes et des contenances.": "Fanny passionately oversees the ageing of our eaux-de-vie. She takes her time and lets this magical stage unfold. She carefully selects her barrels according to wood grain, toast and capacity.",
    "Elle mise sur la diversité pour acquérir de la complexité. Les potentiels tanniques du bois de chêne sont aussi riches et variés que les caractéristiques organoleptiques des cépages utilisés.": "She relies on diversity to build complexity. The tannic potential of oak is as rich and varied as the organoleptic characteristics of the grape varieties used.",
    "C’est la partie complexe qui fait appel à tous nos sens car il s’agit ici d’obtenir un cognac équilibré, rond, aromatique et surtout agréable à consommer.": "This complex stage calls on all our senses, because the goal is to create a balanced, rounded, aromatic Cognac that is above all enjoyable to drink.",
    "Francis, le père de Fanny, n’est jamais loin pour déguster avec nous. C’est important pour moi de partager, d’écouter. On prend tellement de plaisir à le faire ce cognac. Le partage, c’est la moitié du travail.": "Francis, Fanny’s father, is never far away to taste with us. Sharing and listening matter to me. We take so much pleasure in making this Cognac. Sharing is half the work.",
    "Comme toutes les étapes d’élaboration de ce cognac, la mise en bouteille s’effectue également sur la propriété. Elle est faite à la main comme autrefois.": "Like every stage in making this Cognac, bottling also takes place on the estate. It is done by hand, as it used to be.",
    "Nous portons un soin particulier à l’habillage de nos bouteilles.": "We take particular care with the dressing of our bottles.",
    "Esprit Organic est une marque de cognac familiale, dont la production est issue de l’agriculture biologique depuis plus de 20 ans. C’est un cognac de producteur implanté dans le cru des Fins Bois, au domaine de la Grande Versenne, à Triac-Lautrait et géré avec passion par Léopold et Fanny Croizet.": "Esprit Organic is a family Cognac brand whose production has come from organic agriculture for more than 20 years. It is a producer Cognac established in the Fins Bois cru, at the Domaine de la Grande Versenne in Triac-Lautrait, and passionately managed by Léopold and Fanny Croizet.",
    "On ne décide pas de faire du cognac « bio » par hasard. C’est une démarche personnelle mais aussi collective. C’est une bonne parole que l’on prêche et que l’on partage avec plaisir, comme un verre de cognac.": "Choosing to make organic Cognac is not accidental. It is both a personal and collective approach, a belief we share with pleasure, like a glass of Cognac.",
    "Esprit Organic, c’est un état d’esprit dont le nom est un hommage à notre démarche.": "Esprit Organic is a state of mind, and its name pays tribute to our approach.",
    "Un choix qui permet de suivre une évolution intéressante et qui fait la place libre à l’expression du terroir, au retour du « bon sens » paysan : une dynamique de travail que nous voulons remettre en avant.": "A choice that allows an interesting evolution and gives room to the expression of terroir and the return of rural common sense: a working dynamic we want to bring back to the fore.",
    "Chaque produit raconte une histoire, celle d’une lignée de vignerons passionnés, implantés depuis plusieurs générations à Triac Lautrait, qui à force de travail, de conviction et de passion a pu transmettre cet héritage de la cuture de la vigne et du cognac et façonner la vision qui transpire aujourd’hui à travers ESPRIT ORGANIC.": "Each product tells a story: that of a line of passionate winegrowers established for several generations in Triac Lautrait, who through work, conviction and passion have passed on this heritage of vine growing and Cognac, shaping the vision expressed today through ESPRIT ORGANIC.",
    "est issu d’une longue lignée de vignerons. 10e génération de la famille à travailler la vigne, en Algérie du côté maternel, en Charente du côté paternel. L’expérience et le savoir-faire coulent dans ses veines.": "comes from a long line of winegrowers. He is the 10th generation of the family to work the vine, in Algeria on his mother’s side and in Charente on his father’s side. Experience and know-how run in his veins.",
    "Études de commerce international et MBA en poche, il est armé pour reprendre et développer la propriété familiale. Il commence par convertir son vignoble en AB.": "With studies in international business and an MBA, he was ready to take over and develop the family estate. He began by converting the vineyard to organic agriculture.",
    "Pour lui, l’avenir se trouve dans la préservation de son patrimoine et la conviction profonde que la notion de « bon sens paysan » doit reprendre sa place dans le travail de la terre.": "For him, the future lies in preserving this heritage and in the deep conviction that rural common sense must regain its place in working the land.",
    "est passionnée depuis petite par les métiers de la vigne en observant son grand-père récolter et distiller les fruits de ses vendanges. Son père, dégustateur dans une grande maison de négoce, lui a très vite transmis la sensibilité aux multiples saveurs du cognac.": "has been passionate about vine-related crafts since childhood, watching her grandfather harvest and distil the fruit of his vines. Her father, a taster in a major trading house, quickly passed on to her a sensitivity to the many flavours of Cognac.",
    "Ce qui au départ n’était qu’un simple jeu sensitif a débouché sur un master de commerce international des vins et spiritueux avec une prédominance pour la dégustation des eaux-de-vie.": "What began as a simple sensory game led to a master’s degree in international wine and spirits business, with a strong focus on tasting eaux-de-vie.",
    "Après quelques années à parfaire son nez et ses connaissances du vieillissement des eaux-de-vie dans une belle tonnellerie familiale, elle rejoint Léopold en 2016. Par amour, puis par passion.": "After several years refining her nose and her knowledge of eau-de-vie ageing in a fine family cooperage, she joined Léopold in 2016. First for love, then for passion."
  }
};

const nordicLegacyTerms = {
  da: {
    "La Production": "Produktionen",
    "Je dédie FONDATION à ma grand-mère Germaine, pionnière de la famille, qui me répétait sans cesse : Ce patrimoine est solide car il est sain, la terre n’a pas besoin d’autre chose que le travail de l’homme et ses connaissances. Les produits chimiques ne sont pas nécessaires pour que la vigne pousse et produise. C’est ce discours impactant qui m’a poussé à crée cette marque.": "Jeg tilegner FONDATION til min bedstemor Germaine, familiens pioner, som ofte sagde til mig: denne arv er stærk, fordi den er sund. Jorden behøver ikke andet end menneskets arbejde og viden. Kemiske produkter er ikke nødvendige for, at vinstokken kan vokse og bære frugt. Det stærke budskab fik mig til at skabe dette mærke.",
    "FONDATION se caractérise par une belle fraîcheur en bouche des notes fruitées de poire et de pêche ou encore de fleur de vigne. Les premiers tannins du bois révèlent des arômes briochés. Idéal pour réaliser des cocktails ou être consommé sur glace.": "FONDATION kendetegnes af en fin friskhed i munden med frugtige noter af pære, fersken og vinblomst. De første tanniner fra træet afslører brioche-aromaer. Ideel til cocktails eller serveret over is.",
    "Fanny et moi-même sommes convaincus qu’un « mieux produire » est la meilleure solution pour préserver notre vignoble et nous permettre de continuer à travailler de manière passionnée dans le respect de la terre. CONVICTION c’est un hommage à notre vision d’une vie saine, d’un bon sens paysan mais aussi à notre alliance dans le travail et dans la vie.": "Fanny og jeg er overbeviste om, at det at producere bedre er den bedste måde at bevare vores vingård på og fortsætte arbejdet med passion og respekt for jorden. CONVICTION hylder vores syn på et sundt liv, landlig sund fornuft og vores fællesskab i arbejde og liv.",
    "CONVICTION est un cognac rond et gourmand. Les premières années en fûts lui confèrent des notes de fruits confits et de vanille. On y trouve en bouche des notes de fruits secs, de bois chaud et d’épices. CONVICTION offre une finale fraîche de clou de girofle.": "CONVICTION er en rund og fyldig Cognac. De første år på fade giver noter af kandiseret frugt og vanilje. I munden findes noter af tørret frugt, varmt træ og krydderier. CONVICTION har en frisk afslutning med nellike.",
    "La réussite de cette gamme tient aussi dans la force dont chacun d’entre nous a su faire preuve. Mon grand-père Marc et son frère Roger, ma grand-mère Germaine et mes parents Pierre et Eliane ont largement contribué à l’aboutissement de cet engagement dans l’agriculture biologique. C’est un travail d’équipe qui remonte à plusieurs générations. COHESION leur rend hommage.": "Sortimentets succes bygger også på den styrke, hver af os har vist. Min bedstefar Marc og hans bror Roger, min bedstemor Germaine og mine forældre Pierre og Eliane har alle bidraget stærkt til dette engagement i økologisk landbrug. Det er et fælles arbejde gennem flere generationer. COHESION hylder dem.",
    "Une finale masculine, équilibrée, légèrement poivrée et mentholée": "En struktureret, balanceret afslutning, let pebret og mentoleret",
    "Un vieillissement généreux en barriques lui confère de belles notes de fruits secs (cacahuète, amande, noisette) et de bois chaud et d’épices. Finale longue et poivrée.": "Generøs fadlagring giver fine noter af tørret frugt, jordnød, mandel og hasselnød samt varmt træ og krydderier. Lang og pebret afslutning.",
    "Le respect de l’environnement doit être un des engagements majeurs des générations futures. Quelle terre allons-nous laisser à nos enfants demain ? J’aimerai dédier ce cognac aux générations à venir et à mes enfants plus particulièrement. La transmission symbolise pour moi le fruit d’un travail soigné et consciencieux d’une génération prête à passer le relai à la suivante. Nous ne sommes que des passeurs.": "Respekt for miljøet skal være et af de vigtigste løfter for kommende generationer. Hvilken jord efterlader vi til vores børn i morgen? Jeg vil tilegne denne Cognac til de kommende generationer, især mine børn. Transmission symboliserer for mig frugten af et omhyggeligt og samvittighedsfuldt arbejde fra en generation, der er klar til at give stafetten videre. Vi er kun dem, der fører arven videre.",
    "Structurée avec une belle rondeur en bouche": "Struktureret med smuk rundhed i munden",
    "De nombreuses années de vieillissement ont été nécessaires pour élaborer TRANSMISSION. On y trouve en bouche des notes fruitées (cerise noire) et fleuries (fleurs séchées). Les premières notes du rancio apparaissent en finale.": "Mange års lagring var nødvendige for at skabe TRANSMISSION. I munden findes frugtige noter af sort kirsebær og blomstrede noter af tørrede blomster. De første rancio-noter viser sig i afslutningen.",
    "Nous sommes très fiers de présenter le Premier XXO en agriculture Biologique. Ce cognac est issu d’un assemblage d’eaux de vie dont la plus jeune à 14 ans. C’est un cognac structuré, très fruité. Les eaux de vie qui composent ce XXO ont vieilli dans des barriques neuves de chêne de gros grains type Limousin.": "Vi er meget stolte af at præsentere den første XXO i økologisk landbrug. Denne Cognac er lavet af en blanding af eaux-de-vie, hvor den yngste er 14 år. Den er struktureret og meget frugtig. Eaux-de-vie’erne i denne XXO er lagret på nye Limousin-type egetræsfade med grove årer.",
    "Rondeur, douceur et délicatesse": "Rundhed, blødhed og finesse",
    "Proposé en édition limitée ce brut de fût a été sélectionné par Fanny notre maitre de chai pour ses qualités propres et son fort potentiel aromatique. Les eaux de vie de ce millésime exceptionnel ont débuté leur vieillissement en barriques neuves de chêne français sur un mix de grains. Elles ont ensuite fini de se « patiner » dans nos vieilles barriques rousses afin que le temps œuvre et que la magie de l’oxydation et de l’évaporation opère. Cet échange, obtenu après de longues années de vieillissement offre un résultat exceptionnel : une palette aromatique fondue, harmonieuse et riche !": "Denne fadstyrke Cognac tilbydes i begrænset udgave og er udvalgt af Fanny, vores kældermester, for sine egne kvaliteter og sit stærke aromatiske potentiale. Eaux-de-vie fra denne særlige årgang begyndte lagringen på nye franske egetræsfade med blandede årer. Derefter modnede de videre i vores gamle røde fade, hvor tid, oxidation og fordampning kunne gøre deres arbejde. Efter mange års lagring giver denne udveksling et enestående resultat: en smeltet, harmonisk og rig aromatisk palette.",
    "Naturellement boisé": "Naturligt træpræget",
    "Ce pineau des Charentes est élaboré à partir d’un assemblage d'eaux-de-vie de cognac et de moût de raisins issus de nos cépages de Colombard et d'Ugni Blanc. Il a vieilli pendant de nombreuses années en fûts de chêne, ce qui lui donne sa couleur ambrée et brillante. On retrouve en bouche des notes de fruits confits et de vanille. C’est un pineau riche et gourmand, bien structuré avec des notes intenses et harmonieuses.": "Denne Pineau des Charentes fremstilles af en blanding af Cognac eaux-de-vie og druemost fra vores Colombard- og Ugni Blanc-druer. Den har lagret i mange år på egetræsfade, hvilket giver den sin klare ravfarve. I munden findes noter af kandiseret frugt og vanilje. Det er en rig, fyldig og velstruktureret Pineau med intense og harmoniske noter.",
    "Nous sommes fiers d’être implantés dans le cru des Fins Bois, cru que nous revendiquons haut et fort. Il ne faut pas oublier que c’est le cru majoritaire de notre région, il coule dans les veines de nombreuses bouteilles de cognac.": "Vi er stolte af at være forankret i Fins Bois-cruet, som vi tydeligt står ved. Det er det største cru i vores region og løber gennem mange flasker Cognac.",
    "Notre domaine se situe à proximité de Jarnac et bénéficie des terres calcaires de champagne et des terres argilocalcaires et de « groies » des Fins Bois. Cette diversité apporte à nos eaux-de-vie une belle complexité aromatique.": "Vores ejendom ligger tæt på Jarnac og nyder godt af kalkholdige champagnejorde samt ler-kalkholdige groies-jorde fra Fins Bois. Denne mangfoldighed giver vores eaux-de-vie en smuk aromatisk kompleksitet.",
    "Esprit Organic est une marque de cognac familiale, dont la production est issue de l’agriculture biologique depuis plus de 20 ans. C’est un cognac de producteur implanté dans le cru des Fins Bois, au domaine de la Grande Versenne, à Triac-Lautrait et géré avec passion par Léopold et Fanny Croizet.": "Esprit Organic er et familiedrevet Cognac-mærke, hvor produktionen har været baseret på økologisk landbrug i mere end 20 år. Det er en producent-Cognac fra Fins Bois-cruet, på Domaine de la Grande Versenne i Triac-Lautrait, drevet med passion af Léopold og Fanny Croizet.",
    "On ne décide pas de faire du cognac « bio » par hasard. C’est une démarche personnelle mais aussi collective. C’est une bonne parole que l’on prêche et que l’on partage avec plaisir, comme un verre de cognac.": "Man beslutter ikke tilfældigt at lave økologisk Cognac. Det er både en personlig og fælles tilgang, en overbevisning vi deler med glæde, som et glas Cognac.",
    "Chaque produit raconte une histoire, celle d’une lignée de vignerons passionnés, implantés depuis plusieurs générations à Triac Lautrait, qui à force de travail, de conviction et de passion a pu transmettre cet héritage de la cuture de la vigne et du cognac et façonner la vision qui transpire aujourd’hui à travers ESPRIT ORGANIC.": "Hvert produkt fortæller en historie: historien om en slægt af passionerede vinbønder, der i flere generationer har været forankret i Triac Lautrait, og som gennem arbejde, overbevisning og passion har videreført arven fra vinmarken og Cognac og formet den vision, der i dag udtrykkes gennem ESPRIT ORGANIC.",
    "est issu d’une longue lignée de vignerons. 10e génération de la famille à travailler la vigne, en Algérie du côté maternel, en Charente du côté paternel. L’expérience et le savoir-faire coulent dans ses veines.": "kommer fra en lang linje af vinbønder. Han er 10. generation i familien, der arbejder med vinstokken, i Algeriet på moderens side og i Charente på faderens side. Erfaring og knowhow løber i hans årer.",
    "est passionnée depuis petite par les métiers de la vigne en observant son grand-père récolter et distiller les fruits de ses vendanges. Son père, dégustateur dans une grande maison de négoce, lui a très vite transmis la sensibilité aux multiples saveurs du cognac.": "har siden barndommen været passioneret af vinens håndværk, mens hun så sin bedstefar høste og destillere frugten af sine druer. Hendes far, smager i et stort handelshus, gav hende tidligt sansen for Cognacs mange smage."
  }
};

Object.assign(nordicLegacyTerms.no = {}, nordicLegacyTerms.da);
Object.assign(nordicLegacyTerms.sv = {}, nordicLegacyTerms.da);
Object.assign(nordicLegacyTerms.no, {
  "La Production": "Produksjonen",
  "Je dédie FONDATION à ma grand-mère Germaine, pionnière de la famille, qui me répétait sans cesse : Ce patrimoine est solide car il est sain, la terre n’a pas besoin d’autre chose que le travail de l’homme et ses connaissances. Les produits chimiques ne sont pas nécessaires pour que la vigne pousse et produise. C’est ce discours impactant qui m’a poussé à crée cette marque.": "Jeg tilegner FONDATION til min bestemor Germaine, familiens pioner, som stadig sa til meg: denne arven er sterk fordi den er sunn. Jorden trenger ikke annet enn menneskets arbeid og kunnskap. Kjemiske produkter er ikke nødvendige for at vinrankene skal vokse og gi frukt. Dette sterke budskapet inspirerte meg til å skape dette merket.",
  "FONDATION se caractérise par une belle fraîcheur en bouche des notes fruitées de poire et de pêche ou encore de fleur de vigne. Les premiers tannins du bois révèlent des arômes briochés. Idéal pour réaliser des cocktails ou être consommé sur glace.": "FONDATION kjennetegnes av en fin friskhet i munnen med fruktige noter av pære, fersken og vinblomst. De første tanninene fra treverket viser aromaer av brioche. Ideell til cocktails eller servert over is.",
  "Fanny et moi-même sommes convaincus qu’un « mieux produire » est la meilleure solution pour préserver notre vignoble et nous permettre de continuer à travailler de manière passionnée dans le respect de la terre. CONVICTION c’est un hommage à notre vision d’une vie saine, d’un bon sens paysan mais aussi à notre alliance dans le travail et dans la vie.": "Fanny og jeg er overbevist om at det å produsere bedre er den beste måten å bevare vinmarken vår på og fortsette å arbeide med lidenskap og respekt for jorden. CONVICTION er en hyllest til vår visjon om et sunt liv, bondens sunne fornuft og vårt fellesskap i arbeid og liv.",
  "CONVICTION est un cognac rond et gourmand. Les premières années en fûts lui confèrent des notes de fruits confits et de vanille. On y trouve en bouche des notes de fruits secs, de bois chaud et d’épices. CONVICTION offre une finale fraîche de clou de girofle.": "CONVICTION er en rund og fyldig Cognac. De første årene på fat gir noter av kandisert frukt og vanilje. I munnen finner man noter av tørket frukt, varmt treverk og krydder. CONVICTION har en frisk avslutning med nellik.",
  "La réussite de cette gamme tient aussi dans la force dont chacun d’entre nous a su faire preuve. Mon grand-père Marc et son frère Roger, ma grand-mère Germaine et mes parents Pierre et Eliane ont largement contribué à l’aboutissement de cet engagement dans l’agriculture biologique. C’est un travail d’équipe qui remonte à plusieurs générations. COHESION leur rend hommage.": "Suksessen til denne serien bygger også på styrken hver av oss har vist. Min bestefar Marc og hans bror Roger, min bestemor Germaine og mine foreldre Pierre og Eliane har alle bidratt sterkt til dette engasjementet for økologisk landbruk. Det er et lagarbeid gjennom flere generasjoner. COHESION hyller dem.",
  "Une finale masculine, équilibrée, légèrement poivrée et mentholée": "En strukturert, balansert avslutning, lett pepret og mentolpreget",
  "Un vieillissement généreux en barriques lui confère de belles notes de fruits secs (cacahuète, amande, noisette) et de bois chaud et d’épices. Finale longue et poivrée.": "Generøs fatlagring gir fine noter av tørket frukt, peanøtt, mandel og hasselnøtt, samt varmt treverk og krydder. Lang og pepret avslutning.",
  "Le respect de l’environnement doit être un des engagements majeurs des générations futures. Quelle terre allons-nous laisser à nos enfants demain ? J’aimerai dédier ce cognac aux générations à venir et à mes enfants plus particulièrement. La transmission symbolise pour moi le fruit d’un travail soigné et consciencieux d’une génération prête à passer le relai à la suivante. Nous ne sommes que des passeurs.": "Respekt for miljøet må være et av de viktigste løftene for kommende generasjoner. Hvilken jord skal vi etterlate barna våre i morgen? Jeg vil tilegne denne Cognacen til generasjonene som kommer, og særlig til mine barn. Transmission symboliserer for meg frukten av et omhyggelig og samvittighetsfullt arbeid fra en generasjon som er klar til å gi stafetten videre. Vi er bare forvaltere.",
  "Structurée avec une belle rondeur en bouche": "Strukturert med vakker rundhet i munnen",
  "De nombreuses années de vieillissement ont été nécessaires pour élaborer TRANSMISSION. On y trouve en bouche des notes fruitées (cerise noire) et fleuries (fleurs séchées). Les premières notes du rancio apparaissent en finale.": "Mange års lagring var nødvendig for å skape TRANSMISSION. I munnen finner man fruktige noter av svart kirsebær og blomsterpreg av tørkede blomster. De første rancio-notene kommer frem i avslutningen.",
  "Nous sommes très fiers de présenter le Premier XXO en agriculture Biologique. Ce cognac est issu d’un assemblage d’eaux de vie dont la plus jeune à 14 ans. C’est un cognac structuré, très fruité. Les eaux de vie qui composent ce XXO ont vieilli dans des barriques neuves de chêne de gros grains type Limousin.": "Vi er svært stolte av å presentere den første XXO i økologisk landbruk. Denne Cognacen er laget av en blanding av eaux-de-vie, der den yngste er 14 år. Det er en strukturert og svært fruktig Cognac. Eaux-de-vie-ene i denne XXO-en er lagret på nye Limousin-type eikefat med grove årer.",
  "Rondeur, douceur et délicatesse": "Rundhet, mykhet og finesse",
  "Proposé en édition limitée ce brut de fût a été sélectionné par Fanny notre maitre de chai pour ses qualités propres et son fort potentiel aromatique. Les eaux de vie de ce millésime exceptionnel ont débuté leur vieillissement en barriques neuves de chêne français sur un mix de grains. Elles ont ensuite fini de se « patiner » dans nos vieilles barriques rousses afin que le temps œuvre et que la magie de l’oxydation et de l’évaporation opère. Cet échange, obtenu après de longues années de vieillissement offre un résultat exceptionnel : une palette aromatique fondue, harmonieuse et riche !": "Denne fatstyrke Cognacen tilbys i begrenset utgave og er valgt ut av Fanny, vår kjellermester, for sine egne kvaliteter og sitt sterke aromatiske potensial. Eaux-de-vie fra denne eksepsjonelle årgangen begynte lagringen på nye franske eikefat med blandede årer. Deretter modnet de videre i våre gamle røde fat, slik at tid, oksidasjon og fordampning kunne gjøre sitt. Etter mange års lagring gir dette et eksepsjonelt resultat: en smeltet, harmonisk og rik aromatisk palett.",
  "Naturellement boisé": "Naturlig trepreget",
  "Ce pineau des Charentes est élaboré à partir d’un assemblage d'eaux-de-vie de cognac et de moût de raisins issus de nos cépages de Colombard et d'Ugni Blanc. Il a vieilli pendant de nombreuses années en fûts de chêne, ce qui lui donne sa couleur ambrée et brillante. On retrouve en bouche des notes de fruits confits et de vanille. C’est un pineau riche et gourmand, bien structuré avec des notes intenses et harmonieuses.": "Denne Pineau des Charentes er laget av en blanding av Cognac eaux-de-vie og druemost fra våre Colombard- og Ugni Blanc-druer. Den har lagret i mange år på eikefat, noe som gir den en klar ravfarge. I munnen finner man noter av kandisert frukt og vanilje. Det er en rik, fyldig og velstrukturert Pineau med intense og harmoniske noter.",
  "Esprit Organic est une marque de cognac familiale, dont la production est issue de l’agriculture biologique depuis plus de 20 ans. C’est un cognac de producteur implanté dans le cru des Fins Bois, au domaine de la Grande Versenne, à Triac-Lautrait et géré avec passion par Léopold et Fanny Croizet.": "Esprit Organic er et familieeid Cognac-merke der produksjonen har vært basert på økologisk landbruk i mer enn 20 år. Det er en produsent-Cognac fra Fins Bois-cruet, på Domaine de la Grande Versenne i Triac-Lautrait, drevet med lidenskap av Léopold og Fanny Croizet.",
  "On ne décide pas de faire du cognac « bio » par hasard. C’est une démarche personnelle mais aussi collective. C’est une bonne parole que l’on prêche et que l’on partage avec plaisir, comme un verre de cognac.": "Man bestemmer seg ikke tilfeldig for å lage økologisk Cognac. Det er både en personlig og kollektiv tilnærming, en overbevisning vi deler med glede, som et glass Cognac.",
  "Esprit Organic, c’est un état d’esprit dont le nom est un hommage à notre démarche.": "Esprit Organic er en sinnstilstand, og navnet er en hyllest til vår tilnærming.",
  "Chaque produit raconte une histoire, celle d’une lignée de vignerons passionnés, implantés depuis plusieurs générations à Triac Lautrait, qui à force de travail, de conviction et de passion a pu transmettre cet héritage de la cuture de la vigne et du cognac et façonner la vision qui transpire aujourd’hui à travers ESPRIT ORGANIC.": "Hvert produkt forteller en historie: historien om en slekt av lidenskapelige vinbønder, forankret i flere generasjoner i Triac Lautrait, som gjennom arbeid, overbevisning og lidenskap har ført videre arven fra vinmarken og Cognac og formet visjonen som i dag uttrykkes gjennom ESPRIT ORGANIC.",
  "est issu d’une longue lignée de vignerons. 10e génération de la famille à travailler la vigne, en Algérie du côté maternel, en Charente du côté paternel. L’expérience et le savoir-faire coulent dans ses veines.": "kommer fra en lang linje av vinbønder. Han er 10. generasjon i familien som arbeider med vinstokken, i Algerie på morssiden og i Charente på farssiden. Erfaring og kunnskap ligger i blodet.",
  "est passionnée depuis petite par les métiers de la vigne en observant son grand-père récolter et distiller les fruits de ses vendanges. Son père, dégustateur dans une grande maison de négoce, lui a très vite transmis la sensibilité aux multiples saveurs du cognac.": "har siden barndommen vært lidenskapelig opptatt av vinens håndverk, da hun så bestefaren høste og destillere frukten fra innhøstingen. Faren hennes, smaker i et stort handelshus, ga henne tidlig sansen for Cognacens mange smaker."
});
Object.assign(nordicLegacyTerms.sv, {
  "La Production": "Produktionen",
  "Je dédie FONDATION à ma grand-mère Germaine, pionnière de la famille, qui me répétait sans cesse : Ce patrimoine est solide car il est sain, la terre n’a pas besoin d’autre chose que le travail de l’homme et ses connaissances. Les produits chimiques ne sont pas nécessaires pour que la vigne pousse et produise. C’est ce discours impactant qui m’a poussé à crée cette marque.": "Jag tillägnar FONDATION min farmor Germaine, familjens pionjär, som ofta sade till mig: detta arv är starkt därför att det är sunt. Jorden behöver inget annat än människans arbete och kunskap. Kemiska produkter behövs inte för att vinrankan ska växa och bära frukt. Det starka budskapet inspirerade mig att skapa detta varumärke.",
  "FONDATION se caractérise par une belle fraîcheur en bouche des notes fruitées de poire et de pêche ou encore de fleur de vigne. Les premiers tannins du bois révèlent des arômes briochés. Idéal pour réaliser des cocktails ou être consommé sur glace.": "FONDATION kännetecknas av fin friskhet i munnen med fruktiga toner av päron, persika och vinblomma. De första tanninerna från träet avslöjar briochearomer. Idealisk i cocktails eller serverad över is.",
  "Fanny et moi-même sommes convaincus qu’un « mieux produire » est la meilleure solution pour préserver notre vignoble et nous permettre de continuer à travailler de manière passionnée dans le respect de la terre. CONVICTION c’est un hommage à notre vision d’une vie saine, d’un bon sens paysan mais aussi à notre alliance dans le travail et dans la vie.": "Fanny och jag är övertygade om att producera bättre är det bästa sättet att bevara vår vingård och fortsätta arbeta passionerat med respekt för jorden. CONVICTION är en hyllning till vår syn på ett sunt liv, bondens sunda förnuft och vår gemenskap i arbete och liv.",
  "CONVICTION est un cognac rond et gourmand. Les premières années en fûts lui confèrent des notes de fruits confits et de vanille. On y trouve en bouche des notes de fruits secs, de bois chaud et d’épices. CONVICTION offre une finale fraîche de clou de girofle.": "CONVICTION är en rund och generös Cognac. De första åren på fat ger toner av kanderad frukt och vanilj. I munnen finns toner av torkad frukt, varmt trä och kryddor. CONVICTION avslutas friskt med kryddnejlika.",
  "La réussite de cette gamme tient aussi dans la force dont chacun d’entre nous a su faire preuve. Mon grand-père Marc et son frère Roger, ma grand-mère Germaine et mes parents Pierre et Eliane ont largement contribué à l’aboutissement de cet engagement dans l’agriculture biologique. C’est un travail d’équipe qui remonte à plusieurs générations. COHESION leur rend hommage.": "Sortimentets framgång bygger också på den styrka som var och en av oss har visat. Min farfar Marc och hans bror Roger, min farmor Germaine och mina föräldrar Pierre och Eliane har alla bidragit starkt till detta engagemang för ekologiskt jordbruk. Det är ett lagarbete över flera generationer. COHESION hyllar dem.",
  "Une finale masculine, équilibrée, légèrement poivrée et mentholée": "En strukturerad, balanserad avslutning, lätt pepprig och mentolfrisk",
  "Un vieillissement généreux en barriques lui confère de belles notes de fruits secs (cacahuète, amande, noisette) et de bois chaud et d’épices. Finale longue et poivrée.": "Generös fatlagring ger fina toner av torkad frukt, jordnöt, mandel och hasselnöt samt varmt trä och kryddor. Lång och pepprig avslutning.",
  "Le respect de l’environnement doit être un des engagements majeurs des générations futures. Quelle terre allons-nous laisser à nos enfants demain ? J’aimerai dédier ce cognac aux générations à venir et à mes enfants plus particulièrement. La transmission symbolise pour moi le fruit d’un travail soigné et consciencieux d’une génération prête à passer le relai à la suivante. Nous ne sommes que des passeurs.": "Respekten för miljön måste vara ett av de viktigaste åtagandena för kommande generationer. Vilken jord lämnar vi till våra barn i morgon? Jag vill tillägna denna Cognac kommande generationer, särskilt mina barn. Transmission symboliserar för mig frukten av ett noggrant och samvetsgrant arbete från en generation som är redo att lämna över till nästa. Vi är bara förvaltare.",
  "Structurée avec une belle rondeur en bouche": "Strukturerad med vacker rundhet i munnen",
  "De nombreuses années de vieillissement ont été nécessaires pour élaborer TRANSMISSION. On y trouve en bouche des notes fruitées (cerise noire) et fleuries (fleurs séchées). Les premières notes du rancio apparaissent en finale.": "Många års lagring krävdes för att skapa TRANSMISSION. I munnen finns fruktiga toner av svart körsbär och blommiga toner av torkade blommor. De första rancio-tonerna framträder i avslutningen.",
  "Nous sommes très fiers de présenter le Premier XXO en agriculture Biologique. Ce cognac est issu d’un assemblage d’eaux de vie dont la plus jeune à 14 ans. C’est un cognac structuré, très fruité. Les eaux de vie qui composent ce XXO ont vieilli dans des barriques neuves de chêne de gros grains type Limousin.": "Vi är mycket stolta över att presentera den första XXO i ekologiskt jordbruk. Denna Cognac är gjord av en blandning av eaux-de-vie där den yngsta är 14 år. Det är en strukturerad och mycket fruktig Cognac. Eaux-de-vie i denna XXO har lagrats på nya Limousin-typ ekfat med grov ådring.",
  "Rondeur, douceur et délicatesse": "Rundhet, mjukhet och finess",
  "Proposé en édition limitée ce brut de fût a été sélectionné par Fanny notre maitre de chai pour ses qualités propres et son fort potentiel aromatique. Les eaux de vie de ce millésime exceptionnel ont débuté leur vieillissement en barriques neuves de chêne français sur un mix de grains. Elles ont ensuite fini de se « patiner » dans nos vieilles barriques rousses afin que le temps œuvre et que la magie de l’oxydation et de l’évaporation opère. Cet échange, obtenu après de longues années de vieillissement offre un résultat exceptionnel : une palette aromatique fondue, harmonieuse et riche !": "Denna fatstyrka erbjuds i begränsad upplaga och har valts ut av Fanny, vår källarmästare, för sina egna kvaliteter och sin starka aromatiska potential. Eaux-de-vie från denna exceptionella årgång började lagras på nya franska ekfat med blandad ådring. Därefter mognade de vidare i våra gamla röda fat, där tid, oxidation och avdunstning kunde verka. Efter många års lagring ger detta ett exceptionellt resultat: en sammansmält, harmonisk och rik aromatisk palett.",
  "Naturellement boisé": "Naturligt träpräglad",
  "Ce pineau des Charentes est élaboré à partir d’un assemblage d'eaux-de-vie de cognac et de moût de raisins issus de nos cépages de Colombard et d'Ugni Blanc. Il a vieilli pendant de nombreuses années en fûts de chêne, ce qui lui donne sa couleur ambrée et brillante. On retrouve en bouche des notes de fruits confits et de vanille. C’est un pineau riche et gourmand, bien structuré avec des notes intenses et harmonieuses.": "Denna Pineau des Charentes framställs av en blandning av Cognac eaux-de-vie och druvmust från våra Colombard- och Ugni Blanc-druvor. Den har lagrats i många år på ekfat, vilket ger den sin klara bärnstensfärg. I munnen finns toner av kanderad frukt och vanilj. Det är en rik, generös och välstrukturerad Pineau med intensiva och harmoniska toner.",
  "Esprit Organic est une marque de cognac familiale, dont la production est issue de l’agriculture biologique depuis plus de 20 ans. C’est un cognac de producteur implanté dans le cru des Fins Bois, au domaine de la Grande Versenne, à Triac-Lautrait et géré avec passion par Léopold et Fanny Croizet.": "Esprit Organic är ett familjeägt Cognac-varumärke vars produktion har byggt på ekologiskt jordbruk i mer än 20 år. Det är en producent-Cognac från Fins Bois-crut, på Domaine de la Grande Versenne i Triac-Lautrait, driven med passion av Léopold och Fanny Croizet.",
  "On ne décide pas de faire du cognac « bio » par hasard. C’est une démarche personnelle mais aussi collective. C’est une bonne parole que l’on prêche et que l’on partage avec plaisir, comme un verre de cognac.": "Man väljer inte att göra ekologisk Cognac av en slump. Det är både ett personligt och kollektivt förhållningssätt, en övertygelse som vi gärna delar, som ett glas Cognac.",
  "Esprit Organic, c’est un état d’esprit dont le nom est un hommage à notre démarche.": "Esprit Organic är ett sinnestillstånd, och namnet är en hyllning till vårt arbetssätt.",
  "Chaque produit raconte une histoire, celle d’une lignée de vignerons passionnés, implantés depuis plusieurs générations à Triac Lautrait, qui à force de travail, de conviction et de passion a pu transmettre cet héritage de la cuture de la vigne et du cognac et façonner la vision qui transpire aujourd’hui à travers ESPRIT ORGANIC.": "Varje produkt berättar en historia: historien om en släkt passionerade vinodlare, förankrade i flera generationer i Triac Lautrait, som genom arbete, övertygelse och passion har fört vidare arvet från vinodlingen och Cognac och format den vision som i dag uttrycks genom ESPRIT ORGANIC.",
  "est issu d’une longue lignée de vignerons. 10e génération de la famille à travailler la vigne, en Algérie du côté maternel, en Charente du côté paternel. L’expérience et le savoir-faire coulent dans ses veines.": "kommer från en lång linje av vinodlare. Han är 10:e generationen i familjen som arbetar med vinrankan, i Algeriet på moderns sida och i Charente på faderns sida. Erfarenhet och kunnande finns i hans ådror.",
  "est passionnée depuis petite par les métiers de la vigne en observant son grand-père récolter et distiller les fruits de ses vendanges. Son père, dégustateur dans une grande maison de négoce, lui a très vite transmis la sensibilité aux multiples saveurs du cognac.": "har sedan barndomen varit passionerad av vinets hantverk, när hon såg sin farfar skörda och destillera frukten från sina vinstockar. Hennes far, provare i ett stort handelshus, gav henne tidigt känslan för Cognacs många smaker."
});
Object.assign(translations.en, legacyPageTranslations.en);
Object.assign(translations.da, nordicLegacyTerms.da);
Object.assign(translations.no, nordicLegacyTerms.no);
Object.assign(translations.sv, nordicLegacyTerms.sv);

const pineauProductTranslations = {
  en: {
    "Pineau blanc": "White Pineau",
    "Pineau rouge": "Red Pineau",
    "Pineau blanc des Charentes biologique élaboré avec Colombard et Ugni Blanc, sans sulfites ajoutés.": "Organic white Pineau des Charentes made with Colombard and Ugni Blanc, with no added sulphites.",
    "Ce pineau blanc des Charentes est élaboré à partir d’un assemblage d'eaux-de-vie de cognac et de moût de raisins issus de nos cépages de Colombard et d'Ugni Blanc. Il a vieilli pendant de nombreuses années en fûts de chêne, ce qui lui donne sa couleur ambrée et brillante. On retrouve en bouche des notes de fruits confits et de vanille. C’est un pineau riche et gourmand, bien structuré avec des notes intenses et harmonieuses.": "This white Pineau des Charentes is made from a blend of Cognac eaux-de-vie and grape must from our Colombard and Ugni Blanc varieties. It has aged for many years in oak casks, giving it its bright amber colour. The palate shows candied fruit and vanilla notes. It is a rich, generous Pineau, well structured with intense and harmonious notes.",
    "Pineau des Charentes rouge issu de Merlot et d'Ugni Blanc, avec une expression fruitée, souple et gourmande.": "Red Pineau des Charentes made with Merlot and Ugni Blanc, with a supple, generous fruit expression.",
    "Ce Pineau rouge prolonge l'esprit de la gamme Esprit Organic dans un registre plus coloré : une bouche ronde, fraîche et fruitée, pensée pour l'apéritif, les desserts aux fruits ou un service légèrement rafraîchi.": "This red Pineau extends the Esprit Organic range in a more colourful register: a round, fresh and fruity palate, suited to aperitifs, fruit desserts or lightly chilled service.",
    "Ce Pineau rouge des Charentes est élaboré à partir de Merlot et d'Ugni Blanc. Il présente une robe rouge profonde et brillante. Le nez évoque les fruits rouges mûrs, la cerise et une touche de prune. La bouche est souple, ample et gourmande, avec une finale fruitée et légèrement épicée.": "This red Pineau des Charentes is made with Merlot and Ugni Blanc. It shows a deep, bright red colour. The nose suggests ripe red fruit, cherry and a touch of plum. The palate is supple, broad and generous, with a fruity, lightly spicy finish.",
    "Fruits rouges mûrs, cerise, prune, douceur du raisin": "Ripe red fruit, cherry, plum, grape sweetness",
    "Rouge profond, reflets rubis, brillant": "Deep red, ruby highlights, bright",
    "Fruité et gourmand, autour de la cerise, de la mûre et des fruits rouges confits": "Fruity and generous, with cherry, blackberry and candied red fruit",
    "Souple, rond, fruité, avec une belle fraîcheur": "Supple, round and fruity, with fine freshness",
    "Gourmande, fruitée, légèrement épicée": "Generous, fruity and lightly spicy",
    "Valeurs nutritionnelles à ajouter dès réception de la fiche produit Pineau rouge.": "Nutritional values to add once the official red Pineau product sheet is available.",
    "Valeurs nutritionnelles - Pineau blanc": "Nutritional values - White Pineau",
    "Valeurs nutritionnelles - Pineau rouge": "Nutritional values - Red Pineau"
  },
  da: {
    "Pineau blanc": "Hvid Pineau",
    "Pineau rouge": "Rød Pineau",
    "Pineau blanc des Charentes biologique élaboré avec Colombard et Ugni Blanc, sans sulfites ajoutés.": "Økologisk hvid Pineau des Charentes lavet med Colombard og Ugni Blanc, uden tilsatte sulfitter.",
    "Ce pineau blanc des Charentes est élaboré à partir d’un assemblage d'eaux-de-vie de cognac et de moût de raisins issus de nos cépages de Colombard et d'Ugni Blanc. Il a vieilli pendant de nombreuses années en fûts de chêne, ce qui lui donne sa couleur ambrée et brillante. On retrouve en bouche des notes de fruits confits et de vanille. C’est un pineau riche et gourmand, bien structuré avec des notes intenses et harmonieuses.": "Denne hvide Pineau des Charentes fremstilles af en blanding af Cognac eaux-de-vie og druemost fra vores Colombard- og Ugni Blanc-druer. Den har lagret i mange år på egetræsfade, hvilket giver den sin klare ravfarve. I munden findes noter af kandiseret frugt og vanilje. Det er en rig, fyldig Pineau med struktur og harmoniske noter.",
    "Pineau des Charentes rouge issu de Merlot et d'Ugni Blanc, avec une expression fruitée, souple et gourmande.": "Rød Pineau des Charentes lavet med Merlot og Ugni Blanc, med et smidigt, frugtigt og generøst udtryk.",
    "Ce Pineau rouge prolonge l'esprit de la gamme Esprit Organic dans un registre plus coloré : une bouche ronde, fraîche et fruitée, pensée pour l'apéritif, les desserts aux fruits ou un service légèrement rafraîchi.": "Denne røde Pineau fører Esprit Organic-sortimentet videre i en mere farverig stil: rund, frisk og frugtig i munden, velegnet til aperitif, frugtdesserter eller let afkølet servering.",
    "Ce Pineau rouge des Charentes est élaboré à partir de Merlot et d'Ugni Blanc. Il présente une robe rouge profonde et brillante. Le nez évoque les fruits rouges mûrs, la cerise et une touche de prune. La bouche est souple, ample et gourmande, avec une finale fruitée et légèrement épicée.": "Denne røde Pineau des Charentes er lavet med Merlot og Ugni Blanc. Farven er dyb rød og blank. Duften leder tankerne mod modne røde frugter, kirsebær og et strejf af blomme. Smagen er smidig, fyldig og generøs med en frugtig, let krydret afslutning.",
    "Fruits rouges mûrs, cerise, prune, douceur du raisin": "Modne røde frugter, kirsebær, blomme, druesødme",
    "Rouge profond, reflets rubis, brillant": "Dyb rød, rubinreflekser, blank",
    "Fruité et gourmand, autour de la cerise, de la mûre et des fruits rouges confits": "Frugtig og generøs med kirsebær, brombær og kandiserede røde frugter",
    "Souple, rond, fruité, avec une belle fraîcheur": "Smidig, rund og frugtig med fin friskhed",
    "Gourmande, fruitée, légèrement épicée": "Generøs, frugtig og let krydret",
    "Valeurs nutritionnelles à ajouter dès réception de la fiche produit Pineau rouge.": "Næringsværdier tilføjes, når den officielle produktfiche for rød Pineau er klar.",
    "Valeurs nutritionnelles - Pineau blanc": "Næringsværdier - Hvid Pineau",
    "Valeurs nutritionnelles - Pineau rouge": "Næringsværdier - Rød Pineau"
  },
  no: {
    "Pineau blanc": "Hvit Pineau",
    "Pineau rouge": "Rød Pineau",
    "Pineau blanc des Charentes biologique élaboré avec Colombard et Ugni Blanc, sans sulfites ajoutés.": "Økologisk hvit Pineau des Charentes laget med Colombard og Ugni Blanc, uten tilsatte sulfitter.",
    "Ce pineau blanc des Charentes est élaboré à partir d’un assemblage d'eaux-de-vie de cognac et de moût de raisins issus de nos cépages de Colombard et d'Ugni Blanc. Il a vieilli pendant de nombreuses années en fûts de chêne, ce qui lui donne sa couleur ambrée et brillante. On retrouve en bouche des notes de fruits confits et de vanille. C’est un pineau riche et gourmand, bien structuré avec des notes intenses et harmonieuses.": "Denne hvite Pineau des Charentes er laget av en blanding av Cognac eaux-de-vie og druemost fra Colombard- og Ugni Blanc-druene våre. Den har lagret i mange år på eikefat, noe som gir den en klar ravfarge. I munnen finner man noter av kandisert frukt og vanilje. Det er en rik, fyldig Pineau med struktur og harmoniske noter.",
    "Pineau des Charentes rouge issu de Merlot et d'Ugni Blanc, avec une expression fruitée, souple et gourmande.": "Rød Pineau des Charentes laget med Merlot og Ugni Blanc, med et fruktig, mykt og fyldig uttrykk.",
    "Ce Pineau rouge prolonge l'esprit de la gamme Esprit Organic dans un registre plus coloré : une bouche ronde, fraîche et fruitée, pensée pour l'apéritif, les desserts aux fruits ou un service légèrement rafraîchi.": "Denne røde Pineauen viderefører Esprit Organic-serien i en mer fargerik stil: rund, frisk og fruktig i munnen, godt egnet som aperitiff, til fruktdesserter eller lett avkjølt servering.",
    "Ce Pineau rouge des Charentes est élaboré à partir de Merlot et d'Ugni Blanc. Il présente une robe rouge profonde et brillante. Le nez évoque les fruits rouges mûrs, la cerise et une touche de prune. La bouche est souple, ample et gourmande, avec une finale fruitée et légèrement épicée.": "Denne røde Pineau des Charentes er laget med Merlot og Ugni Blanc. Fargen er dyp rød og klar. Duften minner om modne røde frukter, kirsebær og et hint av plomme. Smaken er myk, fyldig og generøs med en fruktig, lett krydret avslutning.",
    "Fruits rouges mûrs, cerise, prune, douceur du raisin": "Modne røde frukter, kirsebær, plomme, druesødme",
    "Rouge profond, reflets rubis, brillant": "Dyp rød, rubinreflekser, klar",
    "Fruité et gourmand, autour de la cerise, de la mûre et des fruits rouges confits": "Fruktig og fyldig med kirsebær, bjørnebær og kandiserte røde frukter",
    "Souple, rond, fruité, avec une belle fraîcheur": "Myk, rund og fruktig med fin friskhet",
    "Gourmande, fruitée, légèrement épicée": "Fyldig, fruktig og lett krydret",
    "Valeurs nutritionnelles à ajouter dès réception de la fiche produit Pineau rouge.": "Næringsverdier legges til når den offisielle produktfiche for rød Pineau er klar.",
    "Valeurs nutritionnelles - Pineau blanc": "Næringsverdier - Hvit Pineau",
    "Valeurs nutritionnelles - Pineau rouge": "Næringsverdier - Rød Pineau"
  },
  sv: {
    "Pineau blanc": "Vit Pineau",
    "Pineau rouge": "Röd Pineau",
    "Pineau blanc des Charentes biologique élaboré avec Colombard et Ugni Blanc, sans sulfites ajoutés.": "Ekologisk vit Pineau des Charentes gjord med Colombard och Ugni Blanc, utan tillsatta sulfiter.",
    "Ce pineau blanc des Charentes est élaboré à partir d’un assemblage d'eaux-de-vie de cognac et de moût de raisins issus de nos cépages de Colombard et d'Ugni Blanc. Il a vieilli pendant de nombreuses années en fûts de chêne, ce qui lui donne sa couleur ambrée et brillante. On retrouve en bouche des notes de fruits confits et de vanille. C’est un pineau riche et gourmand, bien structuré avec des notes intenses et harmonieuses.": "Denna vita Pineau des Charentes framställs av en blandning av Cognac eaux-de-vie och druvmust från våra Colombard- och Ugni Blanc-druvor. Den har lagrats i många år på ekfat, vilket ger den sin klara bärnstensfärg. I munnen finns toner av kanderad frukt och vanilj. Det är en rik, generös Pineau med struktur och harmoniska toner.",
    "Pineau des Charentes rouge issu de Merlot et d'Ugni Blanc, avec une expression fruitée, souple et gourmande.": "Röd Pineau des Charentes gjord med Merlot och Ugni Blanc, med ett fruktigt, mjukt och generöst uttryck.",
    "Ce Pineau rouge prolonge l'esprit de la gamme Esprit Organic dans un registre plus coloré : une bouche ronde, fraîche et fruitée, pensée pour l'apéritif, les desserts aux fruits ou un service légèrement rafraîchi.": "Denna röda Pineau för vidare Esprit Organic-sortimentet i en mer färgstark stil: rund, frisk och fruktig i munnen, lämpad som aperitif, till fruktdesserter eller lätt kyld servering.",
    "Ce Pineau rouge des Charentes est élaboré à partir de Merlot et d'Ugni Blanc. Il présente une robe rouge profonde et brillante. Le nez évoque les fruits rouges mûrs, la cerise et une touche de prune. La bouche est souple, ample et gourmande, avec une finale fruitée et légèrement épicée.": "Denna röda Pineau des Charentes görs med Merlot och Ugni Blanc. Färgen är djupt röd och klar. Doften påminner om mogna röda frukter, körsbär och en ton av plommon. Smaken är mjuk, fyllig och generös med en fruktig, lätt kryddig avslutning.",
    "Fruits rouges mûrs, cerise, prune, douceur du raisin": "Mogna röda frukter, körsbär, plommon, druvsötma",
    "Rouge profond, reflets rubis, brillant": "Djup röd, rubinreflexer, klar",
    "Fruité et gourmand, autour de la cerise, de la mûre et des fruits rouges confits": "Fruktig och generös med körsbär, björnbär och kanderade röda frukter",
    "Souple, rond, fruité, avec une belle fraîcheur": "Mjuk, rund och fruktig med fin friskhet",
    "Gourmande, fruitée, légèrement épicée": "Generös, fruktig och lätt kryddig",
    "Valeurs nutritionnelles à ajouter dès réception de la fiche produit Pineau rouge.": "Näringsvärden läggs till när den officiella produktinformationen för röd Pineau finns klar.",
    "Valeurs nutritionnelles - Pineau blanc": "Näringsvärden - Vit Pineau",
    "Valeurs nutritionnelles - Pineau rouge": "Näringsvärden - Röd Pineau"
  }
};

Object.entries(pineauProductTranslations).forEach(([lang, dictionary]) => {
  Object.assign(translations[lang], dictionary);
});

function applyTextTranslations(lang) {
  const treeWalker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT, {
    acceptNode(node) {
      const parent = node.parentElement;
      if (!parent || ["SCRIPT", "STYLE", "NOSCRIPT"].includes(parent.tagName)) {
        return NodeFilter.FILTER_REJECT;
      }
      return node.nodeValue.trim() ? NodeFilter.FILTER_ACCEPT : NodeFilter.FILTER_REJECT;
    }
  });
  const dictionary = translations[lang] || {};
  const nodes = [];
  while (treeWalker.nextNode()) nodes.push(treeWalker.currentNode);
  nodes.forEach((node) => {
    if (!node._ceoOriginalText) node._ceoOriginalText = node.nodeValue;
    const original = node._ceoOriginalText;
    const trimmed = original.trim();
    if (!trimmed) return;
    const translated = lang === "fr" ? trimmed : dictionary[trimmed];
    if (!translated) {
      node.nodeValue = original;
      return;
    }
    node.nodeValue = original.replace(trimmed, translated);
  });
}

function setLanguage(lang) {
  if (!supportedLangs.includes(lang)) lang = "fr";
  document.body.dataset.lang = lang;
  document.body.dataset.market = visitorMarket;
  document.documentElement.lang = lang;
  localStorage.setItem("ceo-lang", lang);
  applyTextTranslations(lang);
  renderFooterEnhancements(lang);
  if (langToggle) {
    langToggle.textContent = lang.toUpperCase();
    langToggle.setAttribute("aria-label", `Changer de langue. Langue actuelle : ${langNames[lang]}`);
    langToggle.setAttribute("title", "FR / EN / DA / NO / SV");
    langToggle.setAttribute("aria-expanded", "false");
  }
  if (langMenu) langMenu.classList.remove("is-open");
  langOptions.forEach((option) => {
    option.setAttribute("aria-current", String(option.dataset.langOption === lang));
  });
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
    const isOpen = langMenu && langMenu.classList.toggle("is-open");
    langToggle.setAttribute("aria-expanded", String(Boolean(isOpen)));
  });
}

langOptions.forEach((option) => {
  option.addEventListener("click", () => {
    setLanguage(option.dataset.langOption || "fr");
  });
});

document.addEventListener("click", (event) => {
  if (!langMenu || langMenu.contains(event.target)) return;
  langMenu.classList.remove("is-open");
  if (langToggle) langToggle.setAttribute("aria-expanded", "false");
});

document.addEventListener("keydown", (event) => {
  if (event.key !== "Escape" || !langMenu) return;
  langMenu.classList.remove("is-open");
  if (langToggle) langToggle.setAttribute("aria-expanded", "false");
});

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
