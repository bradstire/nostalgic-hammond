// Email signup -> the town's Klaviyo list (client subscriptions API, public key only).
// The list id and source label come from src/config/towns.mjs (klaviyoList), replaced at build time (astro.config.mjs).
// Hattiesburg: list "Nostalgic Hattiesburg". Hammond: the newsletter list the original site's popup used (its welcome
// flow sends WELCOME15).
const COMPANY = 'X6vHTB';
const LIST = import.meta.env.PUBLIC_KLAVIYO_LIST;
const CODE = 'WELCOME15';

export function signup(form: HTMLFormElement) {
  const msg = form.querySelector('.hb-form__msg') as HTMLElement;
  form.addEventListener('submit', async (e) => {
    e.preventDefault();
    const input = form.querySelector('input[type=email]') as HTMLInputElement;
    const email = input.value.trim();
    if (!/^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(email)) {
      msg.textContent = 'Please enter a valid email address.';
      input.setAttribute('aria-invalid', 'true'); input.focus(); return;
    }
    input.removeAttribute('aria-invalid');
    const btn = form.querySelector('button') as HTMLButtonElement;
    btn.disabled = true; msg.textContent = 'Signing you up…';
    try {
      const r = await fetch(`https://a.klaviyo.com/client/subscriptions/?company_id=${COMPANY}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/vnd.api+json', revision: '2024-10-15' },
        body: JSON.stringify({ data: { type: 'subscription', attributes: {
          custom_source: import.meta.env.PUBLIC_SIGNUP_SOURCE,
          profile: { data: { type: 'profile', attributes: { email, properties: { town: import.meta.env.PUBLIC_TOWN } } } },
        }, relationships: { list: { data: { type: 'list', id: LIST } } } } }),
      });
      if (!r.ok && r.status !== 202) throw new Error(String(r.status));
      // Keep the live region in place so screen readers announce the result.
      [...form.children].forEach((c) => { if (c !== msg) (c as HTMLElement).hidden = true; });
      msg.innerHTML = `<span class="hb-form__ok"><strong>You're in.</strong> Use code <strong class="hb-code">${CODE}</strong> at checkout for 15% off your first order.</span>`;
      (window as any).nhTrack?.('Lead', { content_name: 'email signup' });
    } catch {
      btn.disabled = false;
      msg.textContent = 'Something went wrong. Please try again in a moment.';
    }
  });
}
