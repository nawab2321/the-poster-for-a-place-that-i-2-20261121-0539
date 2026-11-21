# Vespera

[![make.fun competition](https://make.fun/badge/the-poster-for-a-place-that-i-2-20261121-0539.svg)](https://make.fun/bounty/the-poster-for-a-place-that-i-2-20261121-0539)
[![make.fun rank](https://make.fun/badge/the-poster-for-a-place-that-i-2-20261121-0539/nawab2321/the-poster-for-a-place-that-i-2-20261121-0539/rank.svg)](https://make.fun/bounty/the-poster-for-a-place-that-i-2-20261121-0539)
[![make.fun reward](https://make.fun/badge/the-poster-for-a-place-that-i-2-20261121-0539/nawab2321/the-poster-for-a-place-that-i-2-20261121-0539/reward.svg)](https://make.fun/bounty/the-poster-for-a-place-that-i-2-20261121-0539)

In Vespera the ocean is overhead, and the sun stays at the horizon. A copper tram climbs from a lantern-lit terrace to the Tide Observatory, the largest of the towers hanging beneath the sea.

The poster borrows its palette from maritime travel prints and uses hand-drawn, high-contrast capitals. The compass above the title echoes the observatory's round window. The terrace stairs and tram cable give the eye a route into the city before it reaches the sun.

## Run offline

Run the entry with Python 3.13. It uses only the standard library and the checked-in illustration plate.

```sh
python3 main.py
```

The program writes a 1024 × 1024 RGB PNG to `/output/entry.png`, within the competition's 1,048,576-byte limit. For a local preview, use `python3 main.py --output-dir output` to write `output/entry.png` in the current directory.

## Artwork and rendering

The background illustration was generated for this entry with Codex's built-in image generation tool and resampled to 996 × 996. The checked-in plate is `assets/vespera-plate.png`. The vector contours for each title glyph and the compass live in `main.py`. At runtime it sets the plate inside a paper margin, rounds neighbouring tones on the illustration for compact encoding, draws the title with supersampled edges, and writes the composited image as a PNG.

<details>
<summary>Illustration prompt</summary>

Original illustration plate for a premium collectible travel poster, square 1:1. This is Vespera, an inviting impossible city built into the underside of a horizontal ocean in permanent evening. Draw the finished scene only, with absolutely no letters, text, logos, marks or borders, as an art director will add typesetting above it. The top 25% stays smooth and dark ink-navy across the full width, empty enough for large cream display letters; subtle tonal variation, no bright details. In the middle below that title space, make the impossible geography immediately legible: a wide, thick slab of sapphire ocean stretches in from the top left and right with a clearly visible reflective rippled upper surface and an exposed sharp lower edge. Against the light, an entire elegant golden city is physically attached to and hangs down from the underside of this ocean shelf, like a chandelier. Its unmistakable hero landmark is one substantial central domed tide observatory pointing DOWN, with a large gold circular window in the dome, radiating ribs, and a long delicate downward finial, like a lantern. Arrange lesser upside-down towers attached along the shelf, with a few fine waterfalls spilling off its lip. Keep them grouped in one clean architectural silhouette with open air around and under it. A huge hazy pale coral setting sun low at the right of the scene, around x=75%, y=76%, contrasting with the city and giving the landmark a gorgeous warm rim. Long horizontal amber cloud ribbons at the distant horizon. From a dark foreground cliff terrace in the lower-left corner, one small cream and copper suspended passenger tram with lit windows glides along a graceful rising cable toward the observatory, the tangible way to visit; scale contrast between tram and golden city. A little warm light on the inviting terrace. The place should feel serene, romantic, safe and spectacular. Printed illustration style, 1930s maritime Art Deco expedition poster meets hand-painted architectural gouache, sophisticated graphic simplification, crafted stepped shapes with fine architectural detail at the landmark only, large deliberate silhouette shapes, crisp quiet composition, slate blue and warm midnight indigo with apricot, copper and buttercream illumination. Fine engraved linework in water, subtle matte ink texture. Make the bright eye path terrace to tram to lantern city to the sun. Keep upper quarter dark and quiet, city dominates center, keep lower edge unobtrusive. Original architecture, no recognizable cultural monument, no nebulas, no fantasy clutter, no mirrored reflection pretending to be the city, no lettering at all.

</details>

Entry for [The Poster for a Place That Isn't There](https://make.fun/bounty/the-poster-for-a-place-that-i-2-20261121-0539) on make.fun.
