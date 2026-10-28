/* Contact preferences and card counters. No cookies or browser persistence. */
(() => {
  'use strict';
  const pageUrl = new URL(location.href);
  const cardMatch = /^EO([0-9]{1,4})$/i.exec((pageUrl.searchParams.get('carte') || '').trim());
  const cardNumber = cardMatch ? Number(cardMatch[1]) : 0;
  const cardId = cardNumber > 0 ? `EO${String(cardNumber).padStart(2, '0')}` : '';
  const measure = pageUrl.searchParams.get('mesure') !== 'non'
    && navigator.doNotTrack !== '1' && navigator.globalPrivacyControl !== true;
  const noMeasureLink = document.getElementById('nfc-no-measure');
  if (noMeasureLink) {
    const noMeasureUrl = new URL(location.href);
    noMeasureUrl.searchParams.set('mesure', 'non');
    noMeasureUrl.hash = '';
    noMeasureLink.href = noMeasureUrl.href;
    if (!measure) noMeasureLink.textContent = 'La mesure est désactivée pour cette page.';
  }
  if (cardId && measure && document.querySelector('form[data-mode="subscribe"]')) initializeCardCounters();
  function initializeCardCounters() {
    let pageId;
    try {
      pageId = Array.from(crypto.getRandomValues(new Uint8Array(16)), byte => byte.toString(16).padStart(2, '0')).join('');
    } catch (_) { return; }
    const recorded = new Set();
    function record(event) {
      if (recorded.has(event)) return;
      recorded.add(event);
      // Never delay navigation or signup if counting is unavailable.
      fetch(new URL('../api/nfc-event.php', location.href), {
        method: 'POST', credentials: 'omit', cache: 'no-store', keepalive: true,
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ card_id: cardId, event, page_id: pageId })
      }).catch(() => {});
    }
    function recordVisiblePage() {
      if (document.visibilityState === 'visible') record('view');
    }
    recordVisiblePage();
    document.addEventListener('visibilitychange', recordVisiblePage);
    document.getElementById('instagram')?.addEventListener('click', () => record('instagram'));
  }
  const notice = document.getElementById('privacy-notice');
  const privacyOpen = document.getElementById('privacy-open');
  if (notice && typeof notice.showModal === 'function') {
    privacyOpen?.setAttribute('aria-haspopup', 'dialog');
    privacyOpen?.setAttribute('aria-controls', 'privacy-notice');
    privacyOpen?.addEventListener('click', event => {
      event.preventDefault();
      notice.showModal();
    });
    document.getElementById('privacy-close')?.addEventListener('click', () => notice.close());
    if (location.hash === '#privacy-notice') notice.showModal();
  }

  const form = document.getElementById('salon-form');
  if (!form) return;
  const endpoint = form.action;
  const withdraw = form.dataset.mode === 'withdraw';
  const status = form.querySelector('.status');
  const phone = form.elements.phone;
  const email = form.elements.email;
  const sms = form.elements.consent_sms;
  const mail = form.elements.consent_email;
  const submit = form.querySelector('button[type="submit"]');
  const token = withdraw ? location.hash.slice(1) : '';
  const management = document.getElementById('management-state');
  let privateReady = false;
  let busy = false;
  const messages = {
    consent_required: 'Renseignez votre téléphone, votre e-mail, ou les deux pour vous inscrire.',
    channel_required: 'Choisissez les SMS, les e-mails, ou les deux.',
    invalid_sms: 'Vérifiez votre mobile : 06 ou 07 en France, ou le préfixe international (+…).',
    invalid_email: 'Vérifiez votre adresse e-mail, s’il vous plaît.',
    rate_limited: 'Beaucoup de demandes ont été reçues. Réessayez dans quinze minutes.',
    consent_version_changed: 'La page a été mise à jour. Rechargez-la avant de vous inscrire.',
    invalid_token: 'Ce lien privé n’est pas valide. Vous pouvez utiliser le formulaire ci-dessous avec votre coordonnée.',
    expired_challenge: 'Votre session a expiré. Réessayez, s’il vous plaît.',
    challenge_reused: 'Cette demande a déjà été traitée. Vous pouvez réessayer.',
    temporarily_unavailable: 'Impossible de confirmer votre demande pour le moment. Réessayez ou écrivez à cognac@mdpierre.com.'
  };
  function show(message, field, success = false) {
    status.textContent = message;
    status.classList.toggle('success', success);
    if (field) {
      field.setAttribute('aria-invalid', 'true');
      field.setAttribute('aria-describedby', status.id);
      field.focus();
    } else status.focus();
  }
  async function fetchJson(url, options) {
    const controller = new AbortController();
    const timer = setTimeout(() => controller.abort(), 20000);
    try {
      const response = await fetch(url, { ...options, signal: controller.signal });
      const data = await response.json();
      if (!response.ok || !data.ok) throw new Error(data.status || 'temporarily_unavailable');
      return data;
    } finally { clearTimeout(timer); }
  }
  async function request(payload) {
    const challenge = await fetchJson(endpoint, {
      cache: 'no-store', credentials: 'same-origin', headers: { Accept: 'application/json' }
    });
    return fetchJson(endpoint, {
      method: 'POST', cache: 'no-store', credentials: 'same-origin',
      headers: { 'Content-Type': 'application/json', Accept: 'application/json' },
      body: JSON.stringify({ ...payload, challenge: challenge.challenge })
    });
  }
  phone.addEventListener('keydown', event => {
    if (event.key === 'Enter') {
      event.preventDefault();
      email.focus();
    }
  });
  form.addEventListener('submit', async event => {
    event.preventDefault();
    if (busy) return;
    status.textContent = '';
    [phone, email, sms, mail].filter(Boolean).forEach(field => {
      field.removeAttribute('aria-invalid');
      field.removeAttribute('aria-describedby');
    });
    // Read at the user's click so Safari autofill without input events also works.
    const wantsSms = withdraw ? sms.checked && !sms.disabled : Boolean(phone.value.trim());
    const wantsEmail = withdraw ? mail.checked && !mail.disabled : Boolean(email.value.trim());
    if (!wantsSms && !wantsEmail) return show(messages[withdraw ? 'channel_required' : 'consent_required'], withdraw ? (sms.disabled ? mail : sms) : phone);
    if (!privateReady && wantsSms && !phone.value.trim()) return show('Ajoutez le numéro de mobile concerné.', phone);
    if (!privateReady && wantsEmail && (!email.value.trim() || !email.validity.valid)) return show(messages.invalid_email, email);
    const payload = {
      action: withdraw ? 'withdraw' : 'subscribe',
      company_url: form.elements.company_url.value,
      phone: wantsSms && !privateReady ? phone.value.trim() : '',
      email: wantsEmail && !privateReady ? email.value.trim() : ''
    };
    if (withdraw) {
      payload.channels = [wantsSms && 'sms', wantsEmail && 'email'].filter(Boolean);
      if (privateReady) payload.token = token;
    } else Object.assign(payload, {
      consent_sms: wantsSms, consent_email: wantsEmail, card_id: cardId, measure,
      consent_version: form.elements.consent_version.value
    });
    busy = true;
    submit.disabled = true;
    status.textContent = 'Un instant…';
    try {
      const data = await request(payload);
      form.reset();
      show(withdraw
        ? 'Votre demande est prise en compte. Les canaux choisis sont désinscrits des invitations et nouvelles de Cognac Esprit Organic.'
        : `Merci ! Votre inscription par ${wantsSms && wantsEmail ? 'SMS et e-mail' : wantsSms ? 'SMS' : 'e-mail'} est enregistrée.`, null, true);
      if (withdraw && privateReady) {
        // The server has committed the withdrawal: do not obscure success with a second request.
        for (const [channel, field] of [['sms', sms], ['email', mail]]) {
          if (payload.channels.includes(channel)) field.disabled = true;
          field.closest('.consent').hidden = field.disabled;
        }
        submit.hidden = sms.disabled && mail.disabled;
        management.textContent = submit.hidden
          ? 'Votre désinscription est terminée.'
          : 'Vous pouvez aussi arrêter le canal encore actif ci-dessous.';
      } else if (!withdraw && typeof data.manage_url === 'string') {
        const url = new URL(data.manage_url);
        if (url.origin === 'https://cognac-esprit-organic.com' && url.pathname === '/se-retrouver/desinscription/') {
          const link = document.createElement('a');
          link.href = location.hostname === '127.0.0.1' || location.hostname === 'localhost' ? url.pathname + url.hash : url.href;
          link.className = 'success-link';
          link.textContent = 'Gérer mes inscriptions (lien à conserver)';
          link.rel = 'noreferrer';
          status.append(link);
        }
      }
    } catch (error) {
      const field = error.message === 'invalid_sms' ? phone : error.message === 'invalid_email' ? email : null;
      show(messages[error.message] || messages.temporarily_unavailable, field);
    } finally {
      busy = false;
      submit.disabled = false;
    }
  });
  // Enable only once the submit handler prevents ordinary GET/POST navigation.
  submit.disabled = false;
  if (withdraw && token) {
    busy = true;
    submit.disabled = true;
    management.textContent = 'Un instant, nous retrouvons vos choix…';
    request({ action: 'inspect', token }).then(data => {
      const active = data.channels.filter(item => item.state === 'active').map(item => item.channel);
      privateReady = true;
      document.getElementById('contact-fields').hidden = true;
      phone.disabled = email.disabled = true;
      for (const [channel, field] of [['sms', sms], ['email', mail]]) {
        field.disabled = !active.includes(channel);
        field.closest('.consent').hidden = field.disabled;
      }
      management.textContent = active.length
        ? 'Votre lien privé a été reconnu. Choisissez les communications à arrêter.'
        : 'Aucune inscription active n’est associée à ce lien.';
      if (!active.length) form.hidden = true;
    }).catch(error => {
      management.textContent = messages[error.message] || messages.temporarily_unavailable;
    }).finally(() => { busy = false; submit.disabled = false; });
  }
})();
