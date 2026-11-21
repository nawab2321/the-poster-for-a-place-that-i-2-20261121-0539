"""Set the Vespera poster's lettering and print it as a self-contained PNG."""

import argparse
from math import ceil, floor
from pathlib import Path
from struct import pack, unpack_from
import zlib


SIZE = 1024
MARGIN = 14
MAX_BYTES = 1_048_576
PLATE = Path(__file__).resolve().parent / "assets" / "vespera-plate.png"
PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"
PAPER = (232, 216, 185)


def png_chunk(kind, data):
    return pack(">I", len(data)) + kind + data + pack(">I", zlib.crc32(kind + data))


def read_plate():
    """Read the RGB illustration plate, whose rows use the PNG Sub predictor."""
    source = PLATE.read_bytes()
    width, height, depth, mode, compression, predictor, interlace = unpack_from(
        ">IIBBBBB", source, 16
    )
    expected = SIZE - 2 * MARGIN
    if source[:8] != PNG_SIGNATURE or (width, height) != (expected, expected):
        raise ValueError("Unexpected illustration plate dimensions or format")
    if (depth, mode, compression, predictor, interlace) != (8, 2, 0, 0, 0):
        raise ValueError("The illustration plate must be non-interlaced 8-bit RGB")

    compressed = bytearray()
    offset = 8
    while offset < len(source):
        length, kind = unpack_from(">I4s", source, offset)
        if kind == b"IDAT":
            compressed.extend(source[offset + 8:offset + 8 + length])
        offset += 12 + length

    scanlines = zlib.decompress(compressed)
    stride = 3 * width
    if len(scanlines) != height * (stride + 1):
        raise ValueError("Incomplete illustration plate")

    for offset in range(0, len(scanlines), stride + 1):
        filter_type = scanlines[offset]
        row = bytearray(scanlines[offset + 1:offset + 1 + stride])
        if filter_type == 1:
            for channel in range(3, stride):
                row[channel] = (row[channel] + row[channel - 3]) & 255
        elif filter_type != 0:
            raise ValueError("Export the illustration plate with the Sub predictor")
        yield row


def outline(items):
    """Expand cubic curves in a letter's outline into short edges."""
    points = [items[0]]
    for item in items[1:]:
        if len(item) == 2:
            points.append(item)
            continue
        ox, oy = points[-1]
        ax, ay, bx, by, x, y = item
        for step in range(1, 25):
            t = step / 24
            u = 1 - t
            points.append((
                u**3 * ox + 3 * u*u*t * ax + 3 * u*t*t * bx + t**3 * x,
                u**3 * oy + 3 * u*u*t * ay + 3 * u*t*t * by + t**3 * y,
            ))
    return points


# High-contrast display capitals drawn to a 100-unit cap height.
# Two inner contours reuse the copper observatory's arched-window shape.
BOWL = [(18, 8), (30, 8), (46, 8, 52, 16, 52, 28),
        (52, 41, 45, 49, 30, 49), (18, 49)]
GLYPHS = {
    "V": (81, [[(0, 0), (32, 0), (32, 3), (22, 8), (47, 77), (72, 8),
               (62, 3), (62, 0), (81, 0), (81, 4), (76, 10), (43, 102),
               (39, 102), (7, 10), (0, 4)]]),
    "E": (61, [[(0, 0), (57, 0), (57, 17), (54, 17), (49, 8), (18, 8),
               (18, 45), (40, 45), (45, 38), (48, 38), (48, 59), (45, 59),
               (40, 52), (18, 52), (18, 92), (52, 92), (58, 81), (61, 81),
               (61, 100), (0, 100), (0, 97), (5, 92), (5, 8), (0, 3)]]),
    "S": (64, [[(59, 4), (59, 25), (55, 25), (53, 14, 45, 6, 33, 6),
               (22, 6, 15, 12, 15, 22), (15, 32, 24, 36, 39, 43),
               (57, 51, 64, 60, 64, 73), (64, 91, 50, 102, 29, 102),
               (18, 102, 9, 99, 2, 95), (2, 73), (6, 73),
               (9, 88, 17, 95, 30, 95), (43, 95, 51, 88, 51, 77),
               (51, 66, 43, 62, 29, 55), (10, 46, 3, 38, 3, 26),
               (3, 10, 16, -2, 34, -2), (44, -2, 53, 0, 59, 4)]]),
    "P": (66, [[(0, 0), (32, 0), (54, 0, 66, 10, 66, 27),
               (66, 45, 53, 56, 32, 56), (18, 56), (18, 92), (26, 97),
               (26, 100), (0, 100), (0, 97), (5, 92), (5, 8), (0, 3)], BOWL]),
    "R": (76, [[(0, 0), (32, 0), (54, 0, 66, 10, 66, 27),
               (66, 40, 59, 49, 45, 53), (69, 88), (76, 97), (76, 100),
               (58, 100), (29, 56), (18, 56), (18, 92), (25, 97), (25, 100),
               (0, 100), (0, 97), (5, 92), (5, 8), (0, 3)], BOWL]),
    "A": (84, [[(0, 100), (0, 97), (8, 91), (42, -2), (46, -2), (78, 91),
               (84, 97), (84, 100), (55, 100), (55, 97), (63, 92), (56, 72),
               (22, 72), (15, 92), (22, 97), (22, 100)],
               [(25, 65), (54, 65), (40, 24)]]),
}


def ink(canvas, contours, color_at):
    """Rasterize closed contours with even-odd fills and 4× edge sampling."""
    samples = 4
    edges = [(p, q) for contour in contours
             for p, q in zip(contour, (*contour[1:], contour[0])) if p[1] != q[1]]
    left = floor(min(x for contour in contours for x, _ in contour))
    right = ceil(max(x for contour in contours for x, _ in contour))
    top = floor(min(y for contour in contours for _, y in contour))
    bottom = ceil(max(y for contour in contours for _, y in contour))

    for y in range(top, bottom):
        coverage = [0] * (right - left)
        for sub_y in range(samples):
            scan_y = y + (sub_y + 0.5) / samples
            crossings = sorted(
                ax + (scan_y - ay) * (bx - ax) / (by - ay)
                for (ax, ay), (bx, by) in edges if min(ay, by) <= scan_y < max(ay, by)
            )
            for begin, end in zip(crossings[::2], crossings[1::2]):
                first = ceil((begin - left) * samples - 0.5)
                last = ceil((end - left) * samples - 0.5)
                for sub_x in range(first, last):
                    coverage[sub_x // samples] += 1

        color = color_at(y)
        for index, weight in enumerate(coverage):
            if weight:
                pixel = 3 * (y * SIZE + left + index)
                for channel, value in enumerate(color):
                    original = canvas[pixel + channel]
                    canvas[pixel + channel] = (
                        original * (16 - weight) + value * weight + 8
                    ) // 16


def set_title(canvas):
    name = "VESPERA"
    tracking = 20
    scale = 1.22
    title_top = 88
    advance = sum(GLYPHS[letter][0] for letter in name) + tracking * (len(name) - 1)
    cursor = (SIZE - scale * advance) / 2

    def letterpress(y):
        tone = max(0, min(100, y - title_top))
        return (246 - tone // 10, 226 - tone // 6, 188 - tone // 4)

    for letter in name:
        width, shapes = GLYPHS[letter]
        contours = [[(cursor + scale * x, title_top + scale * y) for x, y in outline(shape)]
                    for shape in shapes]
        ink(canvas, contours, letterpress)
        cursor += (width + tracking) * scale

    # The copper compass echoes the observatory's radial window below.
    def copper(_):
        return (185, 136, 83)

    ink(canvas, [[(512, 38), (515, 50), (527, 53), (515, 56), (512, 68),
                  (509, 56), (497, 53), (509, 50)]], copper)
    ink(canvas, [[(444, 53), (484, 52.25), (484, 53.75)],
                 [(580, 53), (540, 52.25), (540, 53.75)]], copper)


def render(channel_steps):
    # Compress the painted plate by rounding nearby ink tones. Set the vector
    # title afterward so the type keeps its original antialiased edges.
    tables = [bytes(min(255, (value + step // 2) // step * step)
                    for value in range(256)) for step in channel_steps]
    canvas = bytearray(bytes(PAPER) * SIZE * SIZE)
    for y, row in enumerate(read_plate(), MARGIN):
        for channel, table in enumerate(tables):
            row[channel::3] = row[channel::3].translate(table)
        start = (y * SIZE + MARGIN) * 3
        canvas[start:start + len(row)] = row
    set_title(canvas)
    return canvas


def encode_png(canvas):
    stride = 3 * SIZE
    scanlines = bytearray()
    for start in range(0, len(canvas), stride):
        row = canvas[start:start + stride]
        scanlines.extend(b"\x01" + row[:3])
        scanlines.extend((value - left) & 255 for value, left in zip(row[3:], row))

    header = pack(">IIBBBBB", SIZE, SIZE, 8, 2, 0, 0, 0)
    return (PNG_SIGNATURE + png_chunk(b"IHDR", header)
            + png_chunk(b"sRGB", b"\x00")
            + png_chunk(b"IDAT", zlib.compress(scanlines, 9)) + png_chunk(b"IEND", b""))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path, default=Path("/output"))
    directory = parser.parse_args().output_dir
    image = encode_png(render((4, 2, 3)))
    if len(image) > MAX_BYTES:
        image = encode_png(render((4, 2, 4)))
    if len(image) > MAX_BYTES:
        raise ValueError("The composed poster exceeds the make.fun image size cap")
    directory.mkdir(parents=True, exist_ok=True)
    (directory / "entry.png").write_bytes(image)


if __name__ == "__main__":
    main()
