#!/usr/bin/env python3
"""Redraw the contact QR in index.html.

The page builds the .vcf download in the browser, so that file always matches
CONTACT. The QR cannot: it is a picture, baked into the HTML. Run this whenever
CONTACT changes — above all when the phone number is filled in — or the code
will keep handing out yesterday's details.

    pip install segno && python3 make-qr.py

What the QR carries is deliberately leaner than the downloaded file: name,
title, phone, e-mail and the LinkedIn address, and not the tagline. Every
character costs modules, and modules cost millimetres. Dropping one line of
marketing takes the symbol from version 14 down to 11, which is 0.49 mm per
module on a 30 mm business card instead of 0.41 — the difference between a
card that scans on the first try and one that does not.
"""

import io
import re
import sys

try:
    import segno
except ImportError:                                    # pragma: no cover
    sys.exit("segno is missing.  pip install segno")

# Keep these in step with CONTACT in index.html.
NAME_GIVEN = "Lucian"
NAME_FAMILY = "Vrînceanu"
ROLE = "Consultant energetic"
EMAIL = "vrinceanulucian.vl@gmail.com"
PHONE = ""  # e.g. "+40712345678"
SITE = "https://lucianvrinceanu.com"
LINKEDIN = "https://www.linkedin.com/in/lucian-vr%C3%AEnceanu-7913a8173/"

HTML = "index.html"
BEGIN, END = "<!-- QR:BEGIN -->", "<!-- QR:END -->"


def payload() -> str:
    lines = [
        "BEGIN:VCARD",
        "VERSION:3.0",
        f"N:{NAME_FAMILY};{NAME_GIVEN};;;",
        f"FN:{NAME_GIVEN} {NAME_FAMILY}",
        f"TITLE:{ROLE}",
    ]
    if PHONE:
        lines.append(f"TEL;TYPE=CELL:{PHONE}")
    lines += [f"EMAIL:{EMAIL}", f"URL:{SITE}", f"URL:{LINKEDIN}", "END:VCARD"]
    return "\r\n".join(lines) + "\r\n"


def svg(qr) -> str:
    """One <path> of horizontal runs, on a cream tile.

    The tile is always light and the modules always dark, in both themes: a
    scanner wants dark-on-light, and an inverted symbol is a coin toss on
    anything but the newest phones.
    """
    matrix = [list(row) for row in qr.matrix]
    n = len(matrix)
    quiet = 4                       # the standard four-module margin
    size = n + quiet * 2
    runs = []
    for y, row in enumerate(matrix):
        x = 0
        while x < n:
            if row[x]:
                start = x
                while x < n and row[x]:
                    x += 1
                runs.append(f"M{start + quiet} {y + quiet}h{x - start}v1h-{x - start}z")
            else:
                x += 1
    out = io.StringIO()
    out.write(
        f'<svg class="qr" viewBox="0 0 {size} {size}" role="img" '
        f'aria-label="{NAME_GIVEN} {NAME_FAMILY}" shape-rendering="crispEdges" '
        f'xmlns="http://www.w3.org/2000/svg">'
    )
    out.write(f'<rect width="{size}" height="{size}" fill="#EFE9DD"/>')
    out.write(f'<path fill="#041014" d="{"".join(runs)}"/>')
    out.write("</svg>")
    return out.getvalue()


def main() -> None:
    data = payload()
    qr = segno.make(data, error="m")
    markup = svg(qr)

    html = io.open(HTML, encoding="utf-8").read()
    pattern = re.compile(re.escape(BEGIN) + r".*?" + re.escape(END), re.S)
    if not pattern.search(html):
        sys.exit(f"{BEGIN} … {END} not found in {HTML}")
    io.open(HTML, "w", encoding="utf-8").write(
        pattern.sub(BEGIN + markup + END, html, count=1)
    )

    modules = qr.symbol_size(border=0)[0]
    print(f"{len(data.encode())} octets  ->  version {qr.version}, {modules}x{modules} modules")
    print(f"printed at 30 mm that is {30 / (modules + 8):.2f} mm per module")
    if not PHONE:
        print("no phone number set — fill in PHONE and run this again")


if __name__ == "__main__":
    main()
