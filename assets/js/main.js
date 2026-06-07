const navToggle = document.querySelector("[data-nav-toggle]");
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
