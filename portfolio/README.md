# Lucian Vrînceanu — portfolio

A single-page, build-free cinematic site. Open `index.html` from any static
host (or `npx http-server portfolio`) — there is no framework and no build step.

```
index.html        the whole site: markup, styles and behaviour
vendor/           GSAP + ScrollTrigger, Lenis, Three.js (self-hosted, pinned)
fonts/            Archivo + Newsreader, self-hosted woff2 (latin + latin-ext)
assets/           optional local copies of the cinematic clips
```

## Language

The page is bilingual, Romanian by default, with a toggle in the nav beside the
theme switch. The choice is stored and applied on the next visit.

Every string exists once, in both languages, in the `I18N` dictionary at the
top of the script block. Elements carry `data-i18n` (plain text) or
`data-i18n-html` (text with inline markup) and are rewritten in place; nothing
is duplicated in the HTML, so the two languages cannot drift apart.

Three pieces need more than a text swap and are handled explicitly:

- the storage chapter's captions come from `BESS_COPY` and re-render on change;
- the closing statement carries inline emphasis, so it is rebuilt from
  `STMT_COPY` and re-split into words, and its reveal tween is rebuilt with it;
- proper nouns stay untranslated in both languages — ANRE, AFIR, Electric Up,
  Fondul pentru Modernizare.

Romanian sets marks above cap height (Â Î Ă) and below the baseline (Ș Ț), so
every rise-up mask opens at both ends with matching negative margins. Without
that the headline diacritics are sheared off.

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

   The server has to answer range requests, or the browser reports the file as
   unseekable and the hero freezes on frame one however well it is encoded.
   `npx http-server` does; Python's `http.server` does not.

The all-intra hero file is several times larger than the original. That is the
trade: size for seekability. The two ambient clips only ever play forward, so
they get a normal encode and stay small.

The player already avoids the other common cause of stutter — it waits for the
decoder to finish each seek before requesting the next one, instead of writing
`currentTime` on every frame and making the browser abort a seek it had
already started.

## The storage chapter

The chapter is a blueprint film, scrubbed frame by frame like the hero: the
plant is drawn, lifted off its site plan and rearranged into a revenue stack,
and the last thing standing is the net column. It replaces a WebGL scene that
assembled the plant component by component — which argued the opposite of the
headline, because a list of equipment is exactly what the chapter says storage
is not.

The scene is still there and still carries the chapter whenever the film does
not load. When the film does load, the render loop keeps driving the captions
and stops doing 3D work nobody can see.

Three things are worth knowing before changing any of it.

**The scroll does not map linearly onto the film.** Ten equal stages of scroll
run over four equal clips, split 4 / 1 / 2 / 3, so the playhead is mapped
piecewise through `MAP` in the chapter's module. A linear map drifts a whole
clip out of step by the end.

**The annotation is SVG, not footage.** Numbered callouts, leaders, dimension
lines and the title block are drawn over the film from `MARKS`, in the film's
own 1600×900 coordinates — so they stay sharp type in the reader's language at
any viewport, and no video model has to render legible text. If the film is
ever regenerated with a different layout, `MARKS` is the one thing to re-tune.

**The vertical cut is a different picture.** A 4:3-tall film on a phone is
cropped left and right, and the caption owns the bottom third, so the vertical
annotation has its own coordinates in `MARKS_TALL`, inside the band that
survives both crops.

Light mode inverts the film rather than washing it: line on near-black becomes
ink on paper, which is what a blueprint wants to be, and the hue rotation keeps
the emerald emerald. Reduced motion parks the film on the resolved drawing with
every callout named.

## Every control does something

No button on the page is allowed to be a dead end. A bare `mailto:` looks like
a working button and does nothing at all on a machine with no mail client
registered — and says nothing either. So the two closing calls to action, and
the email in the footer, open a contact panel instead:

- it composes the message for the track it was opened from (self-consumption
  or investment), with its own subject line, its own prompt and its own
  placeholder;
- **Trimite pe e-mail** fires the `mailto:` with subject and body already
  written, for anyone who does have a client;
- **Copiază mesajul** puts the same text on the clipboard, and the address
  under it copies on click — so the panel still works when the `mailto:` does
  not;
- every action answers with a toast, in the current language;
- the name and contact fields are checked before either action, and the panel
  closes on Escape, on the backdrop, and on its own ×.

`navigator.clipboard` does not exist on `file://` or on any insecure origin,
and this page is meant to be opened straight from disk, so the copy falls back
to a hidden textarea and `execCommand`.

The panel sits above the nav (z-index 940) and stops Lenis while it is open,
which also makes it properly modal: the nav behind it is not clickable.

The rest of the inventory: the nav links and the LV mark scroll, the `Scroll`
cue in the hero is a link to the first section, the ten service rows expand,
and the language and theme toggles persist their choice.

## Contact details

`CONTACT` at the top of the script block holds the name, title, email, phone,
tagline and LinkedIn URL. The footer, the contact panel, the downloadable
contact card and the QR all read from it.

## The contact card and its QR

The footer offers **Save contact**, which writes a vCard 3.0 file in the
browser and hands it over as `lucian-vrinceanu.vcf`. Version 3.0 rather than
4.0: enough address books still refuse 4.0 to make it a bad bet. Lines are
folded at 75 octets on a character boundary and joined with CRLF, as the format
requires — an unfolded long `NOTE` is exactly where parsers give up.

Beside it sits a QR carrying the same contact, so someone reading the page on a
desktop can take it away with their phone, and so the image can go on a printed
business card. It is hidden below 760px, because a phone cannot scan its own
screen and the button already does that job there.

The file is built from `CONTACT` at click time and can never fall out of step.
The QR is a picture and can, so it lives between `<!-- QR:BEGIN -->` and
`<!-- QR:END -->` and is redrawn by:

```bash
pip install segno && python3 make-qr.py
```

**Run it after any change to `CONTACT`** — above all when the phone number is
filled in — or the code keeps handing out the old details. The script mirrors
those fields at the top; edit both.

Two numbers govern the design. The QR deliberately carries less than the file:
name, title, phone, email and LinkedIn, but not the tagline. Every character
costs modules and modules cost millimetres, and dropping one line of marketing
takes the symbol from version 14 to 11 — 0.49mm per module on a 30mm business
card instead of 0.41, which is the difference between a card that scans first
time and one that does not. On screen the code is never smaller than 152px,
because below roughly 150px a decoder stops reading it reliably; that floor
came from screenshotting the rendered code and decoding it back at a range of
sizes, not from taste.
