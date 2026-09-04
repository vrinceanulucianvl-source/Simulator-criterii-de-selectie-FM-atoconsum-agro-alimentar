# Lucian Vrînceanu — portfolio

A single-page, build-free cinematic site. Open `index.html` from any static
host (or `npx http-server portfolio`) — there is no framework and no build step.

```
index.html        the whole site: markup, styles and behaviour
vendor/           GSAP + ScrollTrigger, Lenis, Three.js (self-hosted, pinned)
fonts/            fonts.css for self-hosting Archivo + Newsreader (see below)
assets/           optional local copies of the three cinematic clips
```

## Fonts

The page loads Archivo and Newsreader from Google Fonts. `fonts/fonts.css` is
the self-hosted equivalent, kept here because self-hosting is faster and drops
a third-party request — but the eight `.woff2` binaries could not be committed
through this session's GitHub path, so they are not in the repository.

To self-host: copy the `fonts/*.woff2` files from the delivered archive into
`fonts/`, then in `index.html` replace the two Google Fonts tags with

```html
<link rel="stylesheet" href="fonts/fonts.css" />
```

Both routes render identically; only the source of the files changes.

## The three cinematic clips

Generated with Seedance 2.0 (STD, 1080p, 16:9, silent, ~8s), identity-locked to
five reference portraits so the same person appears in every shot.

| Slot         | Scene                    | Wardrobe                                  |
|--------------|--------------------------|-------------------------------------------|
| `boardroom`  | Hero, scroll-scrubbed    | Black three-piece, white shirt, red tie   |
| `strategist` | Core expertise, ambient  | Charcoal three-piece, white shirt, black tie |
| `execution`  | Finale, ambient          | Black three-piece, white shirt, red tie   |

`MEDIA` at the top of the script block lists candidates per slot, tried in
order. A local file in `assets/` wins if it exists; otherwise the Higgsfield
CDN copy is used; if neither loads, a procedural WebGL-free fallback film
renders so no slot is ever a black rectangle.

**Self-hosting the clips is recommended** — it removes the third-party
dependency and lets the hero scrub seek without network latency. Download the
three CDN URLs listed in `MEDIA` and save them as:

```
assets/01-boardroom.mp4
assets/02-strategist.mp4
assets/03-execution.mp4
```

Then set `USE_LOCAL_ASSETS = true` at the top of the script block. Left false,
the page does not probe for them at all, so no visitor pays a failed request.

## Contact details

`CONTACT` at the top of the script block holds the email, LinkedIn and company
URLs used by the footer and the primary call to action.
