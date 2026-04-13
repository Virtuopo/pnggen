#!/usr/bin/env python3
"""Generate solid black PNG files over a numbered filename range.

Usage: python pnggen.py <width> <height> <start> <end> [template]

The optional template uses a run of X's to mark where the number goes.
The number of X's sets the zero-padding width.

Examples:
  python pnggen.py 1920 1080 0000 0100
      → 0000.png, 0001.png, … 0100.png

  python pnggen.py 1920 1080 0 100 BlackXXXFrames.png
      → Black000Frames.png, Black001Frames.png, … Black100Frames.png

No external dependencies — uses only the Python standard library.
"""

import re
import sys
import zlib
import struct


def make_black_png(width, height):
    """Build a valid black PNG in memory using only stdlib."""
    def png_chunk(name, data):
        crc = zlib.crc32(name + data) & 0xFFFFFFFF
        return struct.pack(">I", len(data)) + name + data + struct.pack(">I", crc)

    signature = b"\x89PNG\r\n\x1a\n"

    # IHDR: width, height, bit_depth=8, color_type=2 (RGB), compress=0, filter=0, interlace=0
    ihdr = png_chunk(b"IHDR", struct.pack(">IIBBBBB", width, height, 8, 2, 0, 0, 0))

    # Image data: one filter byte (0 = None) + width*3 zero bytes per row
    raw_row = b"\x00" + b"\x00" * (width * 3)
    idat = png_chunk(b"IDAT", zlib.compress(raw_row * height))

    iend = png_chunk(b"IEND", b"")

    return signature + ihdr + idat + iend


def main():
    if len(sys.argv) not in (5, 6):
        print("Usage: python pnggen.py <width> <height> <start> <end> [template]")
        print("Example: python pnggen.py 1920 1080 0000 0100 BlackXXXXFrames.png")
        sys.exit(1)

    width_arg, height_arg, start_arg, end_arg = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]
    template = sys.argv[5] if len(sys.argv) == 6 else None

    try:
        width = int(width_arg)
        height = int(height_arg)
    except ValueError:
        print(f"Error: width and height must be integers, got '{width_arg}' and '{height_arg}'")
        sys.exit(1)

    if width <= 0 or height <= 0:
        print(f"Error: width and height must be positive, got {width} and {height}")
        sys.exit(1)

    try:
        start = int(start_arg)
        end = int(end_arg)
    except ValueError:
        print(f"Error: start and end must be integers, got '{start_arg}' and '{end_arg}'")
        sys.exit(1)

    if end < start:
        print(f"Error: end ({end_arg}) must be >= start ({start_arg})")
        sys.exit(1)

    count = end - start + 1
    png_data = make_black_png(width, height)

    if template:
        match = re.search(r'(X+)', template)
        if not match:
            print("Error: template must contain at least one 'X' to mark the number position")
            print("Example: BlackXXXXFrames.png")
            sys.exit(1)
        pad = len(match.group(1))
        x_placeholder = match.group(1)
    else:
        pad = len(start_arg)
        x_placeholder = None

    for i in range(start, end + 1):
        number = f"{i:0{pad}d}"
        if template:
            filename = template.replace(x_placeholder, number, 1)
        else:
            filename = f"{number}.png"
        with open(filename, "wb") as f:
            f.write(png_data)

    print(f"Generated {count} image{'s' if count != 1 else ''} ({width}x{height}px black PNG).")


if __name__ == "__main__":
    main()
