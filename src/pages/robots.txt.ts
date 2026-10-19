import type { APIRoute } from 'astro';
import { town } from '../config/site.config';

// Launched towns are crawlable; a town still in private preview is not.
export const GET: APIRoute = () => {
  const body = town.launched
    ? `User-agent: *\nAllow: /\nSitemap: ${town.siteUrl}/sitemap-index.xml\n`
    : `User-agent: *\nDisallow: /\n`;
  return new Response(body, { headers: { 'Content-Type': 'text/plain; charset=utf-8' } });
};
