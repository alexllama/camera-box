# Modular box camera — assembly

Samsung S24 Ultra (in its case) as the capture device, ~90 × 90 mm box, PLA on
a Bambu Lab A1. All dimensions in mm, all parts in `parts/`, print files in
`exports/`.

Coordinate system: x = width, y = height (bottom −45, top +45), z = optical
axis, z = 0 at the front plate's outer face.

## Printed parts

| Part | File | Size | Notes |
|---|---|---|---|
| `FrontPlate` | `camera_front_body.FCStd` | 92.7 × 92.0 × 15.5 | Ø59.05 lens bore, outer cap/skirt (friction-fit over tube) |
| `FrontTube` | `camera_front_body.FCStd` | 90 × 90 × 105 | 18 focus slots at z = 25…93, stop slot at z = 17 |
| `RearBody` | `camera_rear_body.FCStd` | 90 × 90 × 122 | Ø22 aperture, foam recess, 4 pilots |
| `FrontLid` | `camera_lids.FCStd` | 86.7 × 3.9 × 110 | pocket-free, ridge underneath |
| `RearLid` | `camera_lids.FCStd` | 86.7 × 3.9 × 115 | pocket-free, ridge underneath |
| `PhoneCap` | `camera_phone_cap.FCStd` | 240 × 115.8 × 27.4 | sliding C-channel, friction collar, no screws |
| `CarrierFrame` (legacy) | `camera_carrier.FCStd` | 191.4 × 102.1 × 16 | optional bolt-on alternative, 4 × M3 + M5 pusher |
| `CarrierJaw` (legacy) | `camera_carrier.FCStd` | 5.2 × 82.5 × 13.9 | optional, slides in the right rail |
| `SheetFrameFront` | `camera_screen.FCStd` | 85.5 × 78.9 × 1.15 | sheet pocket + 4 pins |
| `SheetFrameBack` | `camera_screen.FCStd` | 85.5 × 78.9 × 1.15 | 4 press-fit sockets |
| `Stop 1–6` | `camera_stops.FCStd` | 85.5 × 78.9 × 2.3 each | drop-in aperture sliders, see below |

**The rear body must be the version with the full-width seat over the rear
wall** (rebuilt together with the lids); an earlier print lacks it and the rear
lid will not sit down.

Print orientation — everything is support-free:

- `FrontPlate`: spigot up, flange on the bed. Print with a brim only if first layer adhesion is sketchy on your cleaned/shifted plate.
- `FrontTube` / `RearBody`: cavity up, as modelled.
- Both lids: under-face down, ridges pointing up, chamfer at the top.
- `PhoneCap`: as modelled, z up; rails and lips point up, collar hangs down.
  240 mm long — shift it off the bed's labels if needed.
- `CarrierFrame` (legacy): **front face down** (z = 236 on the bed), so the lips
  and countersinks are supported.
- `CarrierJaw` (legacy): lip down.
- Both screen halves: flat, pocket/pins up.
- All six stop sliders: flat on the thin web, slot pads up.

## Fasteners and consumables

- 4 × M3 × 20 countersunk (DIN 7991) + 2 mm hex key — **legacy carrier only**
- 1 × M5 × 16–20 bolt + 1 standard M5 nut (8 mm AF) — **legacy carrier only**
- 3 mm closed-cell foam, ring Ø34 OD / Ø24 ID (trim the OD to ~33.5)
- Focusing sheet ≤ 0.45 mm thick, cut to about **72 × 64**
- Black vinyl/gaffer tape

## Assembly

1. **Lens into the plate.** Press the lens into its printed ring, then press the
   ring's Ø59.05 spigot into the plate from the front face. Nothing else goes
   into the plate: the stop is a slider that drops into its own slot later (step
   4a), which is what replaced the old tape-retained discs. 2. **Plate onto the tube.** Slide the cap/skirt over the front of the tube until
   the plate flange butts the tube face at z = 5. The outer collar (90.3 mm ID,
   0.15 mm clearance) is a friction fit — square it up as you go on. No glue; it
   holds the plate in place and helps retain the front lid.
3. **Rear body into the tube.** Its 12 mm spigot laps into the tube's rear end;
   outer faces flush at z = 110. It is a hollow ring, so it does not block the
   light path.
4. **Seal the two body joints.** Both are sliding fits and will leak: tape the
   outside at z = 110 (and at z = 5 only if you want extra insurance; the skirt
   already covers that joint). Only glue once you are happy — you may still want
   to pull them apart to swap the lens.
4a. **Stop slider into the slot at z = 17.** Lids off, lower it in from the top
   until the pads land on the cavity floor, and let it sit. That slot sits
   between the plate and the first focus slot, which is where an aperture stop
   does the most good. Pull it out by its tab with two fingers; no tape,
   nothing to lose.
5. **Foam ring** into the Ø34 × 0.6 recess in the rear wall's outer face. It
   should stand ~2.4 mm proud.
6. **Phone cap.** Push the collar over the rear end of the body — 12 mm lap,
   90.4 mm ID over the 90 mm body, friction fit, no glue. The rails overhang to
   x = −60…180, so leave room beside the camera when setting it down.
7. **Phone.** Screen away from the camera, volume buttons up: slide the cased
   phone in from the right along the channel until the chosen rear lens sits
   over the Ø22 aperture. Inner width −65.05…+18.15 gives 0.15 mm a side.
   Friction holds it wherever you stop; the tick on the top lip marks x = 0,
   the main-lens position. Both ends are open, so it can also be loaded from
   the left if that suits your setup.
8. **Screen frame.** Cut the sheet, drop it into the front half's pocket, press
   the back half on (4 pins, light press fit — drill the sockets 2.5 mm if
   tight). Hold the sandwich vertical, aligned with the chosen slot pair, and
   lower it in; it lands on the cavity floor at y = −40.9.
9. **Lids.** Lower the front lid first (butts the plate at z = 5), then the rear
   lid. The 10 mm stepped lap closes at z = 105 on top and z = 115 underneath.
   Lift them with a fingernail in the 0.8 mm chamfer groove.

## Sliding phone cap

`PhoneCap` replaces the bolt-on carrier: the collar grips the rear body and the
two long rails hold the phone by its screen-side edges and long sides. No M3 or
M5 hardware is involved, and nothing covers the foam ring.

- **Channel:** 3.5 mm thick rails, inner width y = −65.05…+18.15 (0.15 mm a
  side on the cased phone; the volume buttons at y = 18.0 just clear). Lips
  overlap the screen edge by 2.2 mm and sit 0.2 mm above the screen surface.
- **Travel:** the rails run x = −60…180, about 75 mm of lens selection. Both
  ends are open; load from the right in normal use. There are no detents, so
  you can stop at any point and friction holds the phone.
- **Repeatability:** the notch in the top lip marks x = 0 (main lens centred).
  Once you know where your other lenses land, pencil marks on that lip are
  enough to find them again.
- **Tuning:** if the phone creeps, reduce `PHONE_RAIL_CLR` in `params.py` from
  0.15 toward 0.10 and reprint; if it binds, raise it toward 0.20. Do not go
  below 0.08 — the case is soft and you will fight insertion.
- The foam ring still sits in the rear wall and compresses to 1.7 mm; the cap
  webs stay 0.2 mm below the phone's back (or above the rear wall face), so the
  light seal is unchanged.
- The old `CarrierFrame`/`CarrierJaw` files are kept as a fallback if you ever
  want a hard-stop instead of a sliding fit, but they need the M3 and M5 parts.

## Focusing

- **18 slot pairs**, centres at z = 25 + 4k → 25, 29 … 93. All 18 are clear of
  the tube, the rear body and the lids (checked as solids, not by eye). A 19th
  pair at **z = 17**, out in front of the first focus slot, holds the aperture
  stop; it is not a focusing position.
- The slots exist only in the front tube, on purpose. The film plane must stay
  in front of the rear body's spigot (front face at z = 98); behind that starts
  the phone chamber, and slots there would cut through the Ø22 aperture, the
  foam recess and the M3 pilots.
- With f ≈ 64 the plane lands at **z ≈ 66–76** (the glass sits 6–10 mm inside
  the 13 mm plate), i.e. slots 65–77, two thirds of the way along the travel.
  The 68 mm of travel brackets f ≈ 17–87, so the 64 mm estimate would have to
  be wrong by more than +35 % before the range runs out.
- The far end doubles as close-focus travel: +20 mm ≈ 0.25 m subject distance,
  so keeping the plane at ~70 costs nothing.
- Start at **z = 65** and move one slot at a time in either direction. Judge on
  the live preview: check the sharpness of the far subject, not the screen
  texture. The image is upside down and mirrored — normal.
- 4 mm steps can leave you up to 2 mm off the true plane. Two ways to fine-tune
  with no new parts:
  - **Shim the lens ring.** Moving the lens δ along the axis moves the image
    plane δ (1:1). A card washer behind the ring's flange moves the plane
    forward; sanding the flange's rear face moves it back. This is the precise
    route, and 1–2 mm of shim still leaves the spigot well inside the bore.
  - **Stop down.** The sliders in the z = 17 slot fix this directly; see
    *Aperture stops* below. In short, Ø3.6 (≈ f/15) gives ±1.5 mm of depth of
    focus, so a whole 4 mm slot step is sharp.
- Only if the true plane falls past slot 93 (a much longer lens than 64 mm):
  shorten `REAR_SPIGOT` and raise `SLOT_FIRST_Z`, then rebuild the tube and rear
  body. `build_1a.py` refuses to build if the last slot fouls the spigot.

## Aperture stops (test set)

Six sliders, one per hole. Each drops into the **stop slot at z = 17** from the
top and lands on the cavity floor — the same motion as the screen frame. No
tape, no loose discs, nothing to lose inside the box, and the slot centres the
hole on the axis for free (which is the one thing a stop must get right).

Why they get their own slot, right behind the plate: a stop only works in front
of the sheet, and the further back it sits the less it does. Seen from the
sheet, the f-number is

    N = (sheet z − stop z) / hole

so the same Ø2.5 hole is f/21 at z = 17 and f/18 in the first focus slot (25) —
a quarter of a stop, not dramatic, but it also means the stop never competes
with the focusing frame for a slot, and can never end up behind the sheet, where
it would crop the picture instead of stopping the lens.

| Slider | Index dots | Hole | f/# (stop at 17, sheet at 70) | Depth of focus (± at 0.1 mm blur) |
|---|---|---|---|---|
| 1 | 1 | Ø10.0 | f/5.3 | ±0.5 mm |
| 2 | 2 | Ø7.0 | f/7.6 | ±0.8 mm |
| 3 | 3 | Ø5.0 | f/10.6 | ±1.1 mm |
| 4 | 4 | Ø3.6 | f/14.7 | ±1.5 mm |
| 5 | 5 | Ø2.5 | f/21.2 | ±2.1 mm |
| 6 | 6 | Ø1.8 | f/29.4 | ±2.9 mm |

No slider at all is the wide-open reference: the bare Ø59 bore, f/1.1, very
bright and very soft.

- **Print all six as one plate** (`aperture_stops.3mf`, 174 × 243 mm, ~29 g,
  or `stop_1_d10mm.stl` … `stop_6_d1.8mm.stl` one at a time). Flat on the web,
  pads up, no supports. **Use black or dark filament if you have it** — a white
  slider's lens-side face scatters light into the image.
- **Identify by counting the dots** in the pull tab. The two smallest holes may
  print slightly undersized; check against a bright light and ream with a
  needle if one closes up. A tenth of a millimetre is under 5 % of the
  f-number, so do not chase it.
- **Swapping:** lids off, pinch the tab, lift the slider out, drop the next one
  in. Ten seconds, no tools. The pull tab stays above the light cone, so it
  cannot leak light onto the sheet.
- **They also fit any focus slot**, which is the fallback if your tube was
  printed before the z = 17 slot existed: use slot 25. Same parts, a quarter
  stop weaker (f/4.5 … f/25 instead of f/5.3 … f/29), nothing else changes.
- **Reading the result:** f/10–f/15 (sliders 3–4) is the sane range for a single
  element — start there. Wider is brighter but the edges will smear; narrower
  is cleaner but the sheet goes dim (f/29 is 30× dimmer than f/5.3, so the
  phone needs a long exposure and the sheet gets hard to focus on).
- Pick the stop that makes your 4 mm slot steps stop mattering — slider 6
  (±2.9 mm) covers a whole step — or the widest one you can still focus
  comfortably. Then just leave it in the slot; there is no reason to glue it,
  and its dot count is what you write in your log.
- The f-numbers above are approximate: they assume f = 64 and a sheet at z = 70.
  If your real plane ends up at 77, every f-number in the table rises by 7/53
  (one sixth of a stop). Good enough to compare sliders, not a calibration.


## Phone fit (the one thing with real tolerance)

Design values come from measurements taken with the case on: 165 × 82.5,
buttons +0.4, lens 17.6 from the button-side edge and 34.33 from the opposite
short edge. The footprint is therefore x = −34.33…+130.67, y = −64.9…+17.6.

If those two lens offsets were measured to the bare phone's edges instead of
the case's, the lens sits up to ~1.75 mm off the optical axis. That still sits
inside the Ø22 aperture and inside the Ø24 foam ID, so it is harmless — but the
framing shifts, and you will see it in the preview.

Depth: the phone's front is held at z = 233.2 by the two end lips, which puts
the case's back at 221.7 and compresses the 3 mm foam to 1.7 mm. Both the camera
bump (12.47) and the kickstand (12.99) clear the wall face by ~0.2 mm.

## Rubber-band variant (legacy carrier only)

No screw needed: loop a ~200 mm silicone cord through the buttonhole at x = −38
in the top rail, around the notch in the jaw's end, and back through the same
hole. Repeat on the bottom rail. Both runs stay outside the phone's footprint,
so nothing crosses the screen.

## Light leaks

Every sliding joint leaks a little. The lids and the frame are L-shaped
labyrinths rather than straight gaps, but for the first tests tape:

- the plate/tube ring at z = 5
- the tube/rear-body ring at z = 110
- the lid seams (side chamfer grooves and the z ≈ 105/115 joint)

If an image is fogged, suspect the lid seams first, then the body rings.
