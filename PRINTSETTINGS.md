# Print settings (Bambu Lab A1, Elegoo black PLA)

## Recommended base profile
Start from **0.20 mm Standard** with a 0.4 mm nozzle. Change only the values below.

| Setting                    | Value                            | Notes                                                             |
| -------                    | -----                            | -----                                                             |
| Layer height               | 0.20 mm                          | 0.24 saves time but coarsens the 4 mm walls and 2.5 mm slot pads. |
| Wall loops                 | 3 (1.26 mm)                      | Main source of stiffness. Don't trade walls for infill.           |
| Top layers / Bottom layers | 4 / 4 (0.8 mm)                   | Light-tight enough for the tube.                                  |
| Sparse infill              | Gyroid 12%                       | Stiff in all directions, efficient for weight/filament.           |
| Wall generator             | Arachne (default)                | Helps with the 0.9 mm webs and 1.15 mm frame halves.              |
| Nozzle temp                | 210 °C (first layer 215 °C)      | Black pigment often wants a touch more than white.                |
| Bed temp                   | 60 °C (first layer), 55 °C after | Use the "Textured PEI Plate" preset.                              |
| Cooling                    | On (default)                     | PLA, thin walls, no enclosure.                                    |
| Supports                   | None                             | Everything was designed flat-bottomed.                            |
| Brim                       | None; 5 mm only if corners lift  | The 90×90 bases are usually fine.                                 |
| Outer wall speed           | ≤ 120 mm/s                       | Cleaner surface, negligible time cost.                            |
| Seam                       | Aligned                          | Lands on a corner.                                                |

## Per-part exceptions

| Part                             | Change                                            | Reason                                                                   |
| ----                             | ------                                            | ------                                                                   |
| FrontPlate                       | Use base profile as-is, spigot up / flange on bed | With cap/skirt ~75–120 g depending on version.                            |
| FrontTube / RearBody             | Use base profile as-is, cavity up                 | 3 walls + 12% gyroid pays off here.                                      |
|                                                                                      | A 1-wall tall box will oil-can and slots can go tight.                   |
| SheetFrameFront / SheetFrameBack | 0.12 mm layers                                    | 1.15 mm thick with a 0.45 mm pocket land on ugly fractions at 0.2.       |
|                                                                                      | 0.12 gives ~0.48 pocket and ~1.20 thickness,                             |
|                                                                                      | keeping the sandwich at ~2.4 mm in a 2.5 mm slot.                        |
| Stop sliders (all six)           | Use base profile as-is                            | 0.9 mm web (4–5 layers), 2.3 mm pads (11–12 layers) are fine at 0.20 mm. |
| PhoneCap                         | As modelled, z up; 4 walls, 15% gyroid            | 240 mm long, shift off the bed's labels; no supports; ~60 g.            |

## Bed discoloration (labels/warnings showing up on black PLA)

The discoloration mapping to the labels/warnings under the plate is usually cosmetic, not a nozzle temp issue.

### Likely causes
1. **Heat tint on the steel sheet** — The magnetic bed's ink changes the local contact, so the underside of the spring-steel sheet can tarnish in the shape of the text after many 60 °C cycles. Lift the plate and check the *underside*. If it's there, it's permanent and won't hurt anything.
2. **First-layer squish pattern** — The ink layer is a few tens of µm thicker, so the first layer over text is squashed slightly differently. On black PLA this reads as dull/grey patches due to gloss differences.

### Troubleshooting checklist
1. **Use the correct preset** — Set to "Textured PEI Plate" (PLA bed 55–60). If it's on "Smooth PEI" or "Cool Plate" (35–45 °C), try again with the correct preset.
2. **Clean both sides** — Wash the plate with dish soap and warm water (not just IPA). Residue on the *underside* can cause patchy heat transfer.
3. **Re-seat the plate** — Make sure it's pushed firmly against the rear stops and nothing is trapped underneath (blobs/filament).
4. **Measure temperature** — With an IR thermometer, soak at 60 °C for 5 minutes and read five points on the plate. ±3–4 °C is normal; >10 °C spread may indicate a bed/thermistor fault worth a support ticket.
5. **Check thickness/gloss** — Print a small 90×90 patch (0.20 mm tall). If the ghost area is only duller/glossier with similar thickness (±0.03 mm), it's a surface/squish/gloss difference. If you want it gone, rotate the part 90° or shift it 10–15 mm so its footprint doesn't sit over the text.

**Notes:** If you see yellow/brown tint or a smell, drop bed temp to 55 °C and re-clean before printing. The bed face of the FrontPlate is its outer lens-side face, so cosmetic discoloration may be visible, but it won't affect fit/function.
