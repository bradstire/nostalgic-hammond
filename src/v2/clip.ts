// Trim text for meta descriptions at a word boundary.
export function clip(s: string, n = 155): string {
  const t = s.replace(/\s+/g, ' ').trim();
  if (t.length <= n) return t;
  const cut = t.slice(0, n - 1); const i = cut.lastIndexOf(' ');
  return (i > n * 0.6 ? cut.slice(0, i) : cut).replace(/[,;:.\s]+$/, '') + '…';
}
