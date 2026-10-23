// Keep hyphenated compounds (Drive-In, Tri-Stripe) on one line. Returns HTML; use with set:html.
const esc = (s: string) => s.replace(/[&<>"]/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]!));
export function nw(s: string): string {
  return esc(s).replace(/([A-Za-z0-9.'’]+(?:-[A-Za-z0-9.'’]+)+)/g, '<span class="hb-nw">$1</span>');
}
