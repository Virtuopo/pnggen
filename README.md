# pnggen

Generates a sequence of solid black or fully transparent PNG files over a numbered filename range. No dependencies — uses only the Python standard library.

## Requirements

Python 3.6+. No packages to install.

## Usage

```
python pnggen.py <width> <height> <start> <end> [template] [--transparent]
```

| Argument | Description |
|----------|-------------|
| `width` | Image width in pixels |
| `height` | Image height in pixels |
| `start` | First file number (e.g. `0000`) |
| `end` | Last file number (e.g. `0100`) |
| `template` | *(Optional)* Filename template — see below |
| `--transparent` | *(Optional)* Generate fully transparent RGBA PNGs instead of solid black |

The number of images generated is `end - start + 1`.

## Examples

### Basic usage

Generates `0000.png` through `0023.png` — 24 files at 1920×1080:

```bash
python pnggen.py 1920 1080 0000 0023
```

The zero-padding width is inferred from the `start` argument: `0000` → 4 digits.

### Custom filename template

Use a run of `X`s in the template to mark where the number goes. The number of `X`s sets the zero-padding width.

```bash
python pnggen.py 1920 1080 0 99 BlackXXXFrame.png
```

Produces: `Black000Frame.png`, `Black001Frame.png`, … `Black099Frame.png`

```bash
python pnggen.py 3840 2160 1 10 shot_XXXX_comp.png
```

Produces: `shot_0001_comp.png`, `shot_0002_comp.png`, … `shot_0010_comp.png`

### Transparent frames

Add `--transparent` to generate fully transparent RGBA PNGs instead of solid black:

```bash
python pnggen.py 1920 1080 0000 0023 --transparent
```

```bash
python pnggen.py 1920 1080 0000 0023 AlphaXXXXFrame.png --transparent
```

### Single image

```bash
python pnggen.py 512 512 0 0
```

Produces a single `0.png`.

## Notes

- Files are written to the current working directory.
- If a file already exists it will be overwritten without warning.
- The template must contain at least one unbroken run of `X`s. The first such run is used as the number placeholder.
