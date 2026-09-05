# Lucian Vrînceanu — portfolio

A single-page, build-free cinematic site. Open `index.html` from any static
host (or `npx http-server portfolio`) — there is no framework and no build step.

```
index.html        the whole site: markup, styles and behaviour
vendor/           GSAP + ScrollTrigger, Lenis, Three.js (self-hosted, pinned)
fonts/            Archivo + Newsreader, self-hosted woff2 (latin + latin-ext)
assets/           optional local copies of the three cinematic clips
```

## Fonts

Archivo and Newsreader are self-hosted from `fonts/` — no third-party request,
and the page renders correctly offline. Both include latin-ext, which the `î`
and `â` in Vrînceanu need.

To load them from Google Fonts instead, replace the stylesheet link in the head
with:

```html
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Archivo:ital,wdth,wght@0,62..125,400..900;1,62..125,400..900&family=Newsreader:ital,opsz,wght@0,6..72,200..500;1,6..72,200..500&display=swap" />
```

Keep the `wdth` axis in that URL — the display type relies on widths between
70% and 88%, and a static build renders it wrong.

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
CDN copy is used; if neither loads, a procedural fallback film renders so no
slot is ever a black rectangle.

## Making the hero scrub smooth (important)

The hero is scrubbed frame by frame from scroll position, and that places an
unusual demand on the file. A normal MP4 stores a keyframe only every one or
two seconds and rebuilds the frames between them from differences. Playing
forward, that is efficient. **Seeking** to an arbitrary time is not: the
browser has to find the previous keyframe and decode forward to reach the
frame you asked for. Ask it to do that on every scroll frame, over the
network, and the scrub stutters or looks frozen — the clip appears not to
respond to scrolling at all.

Two things fix it, and both are needed:

1. **Re-encode all-intra.** Every frame becomes a keyframe, so any frame can
   be presented immediately. `prepare-assets.sh` does this — it downloads the
   three clips and encodes the hero with `-g 1 -keyint_min 1 -sc_threshold 0`
   plus `-movflags +faststart`. Edit the three filenames in it first, then:

   ```bash
   bash prepare-assets.sh
   ```

2. **Serve them locally.** Set `USE_LOCAL_ASSETS = true` in `index.html`. A
   seek that has to make a network round trip can never feel immediate, no
   matter how the file is encoded.

The all-intra hero file is several times larger than the original. That is the
trade: size for seekability. The two ambient clips only ever play forward, so
they get a normal encode and stay small.

The player already avoids the other common cause of stutter — it waits for the
decoder to finish each seek before requesting the next one, instead of writing
`currentTime` on every frame and making the browser abort a seek it had
already started.

## Contact details

`CONTACT` at the top of the script block holds the email, LinkedIn and company
URLs used by the footer and the primary call to action.
