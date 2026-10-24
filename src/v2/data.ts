// Storefront v2 content for the town this build is for (PUBLIC_TOWN).
// Shared constants live in ./shared.ts; each town's places, pairs, copy and catalog rules in ./towns/<slug>.ts.
import { townSlug } from '../config/site.config';
import type { TownContent, Place } from './shared';
import { hattiesburg } from './towns/hattiesburg';

export * from './shared';

const TOWNS: Record<string, TownContent> = { hattiesburg };
export const TOWN: TownContent = TOWNS[townSlug];
if (!TOWN) throw new Error(`[v2] No storefront v2 content for town "${townSlug}" (add src/v2/towns/${townSlug}.ts)`);

export const {
  PLACES, FALLBACK_PLACE, HIDE_EMPTY_PLACES, HELD_PREFIXES, SINGLE_COLOR, TYPE_OVERRIDE, blankFor,
  START_HERE, AUTO_START, NOTE_BY_PREFIX, DESC_OVERRIDE, PAIRS, FAMILIES, MEMBER_LABEL, TITLE_OVERRIDE, FRAME_SIZE, FAQ,
  PRODUCT_IMAGES, PLACE_DIR, ADD_ONS, MATE_FALLBACK, TYPE_IMG, COPY,
} = TOWN;

// Near-duplicates kept in the store but left out of grids (their pages still work). Brad has the final call.
import hiddenList from './hidden.json';
export const HIDDEN_FROM_GRID = new Set<string>(hiddenList);

// Places that have something to sell. Towns with HIDE_EMPTY_PLACES drop the rest from grids, nav and routes,
// so a place whose products aren't in the store yet never shows an empty grid.
export function livePlaces(products: { lead: boolean; place: Place | null }[]): Place[] {
  if (!HIDE_EMPTY_PLACES) return PLACES;
  return PLACES.filter((pl) => products.some((p) => p.lead && p.place?.slug === pl.slug));
}
// Story count for headings ("Seven Hattiesburg stories"): the catch-all "Around <town>" place doesn't count.
export const storyCount = (places: Place[]) => places.filter((p) => !p.catchAll).length;
// A place's story, plus the paragraphs that wait on a product being in the store.
export function placeStory(pl: Place, handles: string[]): string[] {
  return pl.story.concat((pl.storyIf || []).filter((s) => handles.some((h) => h.startsWith(s.prefix))).map((s) => s.text));
}
export function placeSources(pl: Place, handles: string[]) {
  return pl.sources.concat((pl.storyIf || []).filter((s) => s.source && handles.some((h) => h.startsWith(s.prefix))).map((s) => s.source!));
}
