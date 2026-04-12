# Video Plan — "Are Pretrained Image Matchers Good Enough for SAR–Optical Registration?"

CVPR 2026 Image Matching Workshop — 10-min talk by Isaac Corley (Taylor Geospatial)
Co-authors: Alex Stoken, Gabriele Berton

## Narrative Arc

Hurricane → cloud cover → SAR is the only option → SAR looks *nothing* like optical → can modern matchers bridge the gap with zero cross-modal training? → we evaluate 24 of them → the surprise isn't which matcher wins, it's that **how** you run it matters as much as **which** you run → practical recipe for deployment.

The "aha moment": **RoMa has zero cross-modal training data and still ties for first place** — DINOv2 features alone give emergent modality invariance. And: **protocol choices swing accuracy by 33× for a single matcher**, often exceeding the gap between matchers.

## Visual Language

- **Palette**: deep slate background with dual cyan/amber accents (optical vs SAR) and gold highlights
  - BG `#0E1419`
  - CYAN `#58C4DD` (optical channel)
  - AMBER `#FF9E4A` (SAR channel)
  - GOLD `#FFD93D` (highlights, "aha")
  - GREEN `#83C167` (success, inliers)
  - CORAL `#FF6B6B` (failure, outliers)
  - MUTED `#6B7280` (axes, structure)
- **Typography**: Menlo monospace across all scenes
- **Consistency**: every scene sets `self.camera.background_color = BG`; every transition is a full FadeOut cleanup

## Scene List (targeting ~8–9 min runtime so Isaac can pace live)

### Scene 01 — Title + Hurricane Hook (~45s)
- Stylized hurricane sweep sigil over a coastline icon
- Title card: "Are Pretrained Image Matchers Good Enough for SAR–Optical Satellite Registration?"
- Authors row, venue badge
- Tagline fades in: "Cloud cover wins. SAR takes over. Can pretrained matchers keep up?"

### Scene 02 — Physics Gap (~75s)
- Side-by-side tile panels labeled OPTICAL and SAR
- Optical = smooth gradient tile with grid "buildings"
- SAR = same scene, rendered with speckle noise + layover shift + contrast inversion
- Callouts: "speckle", "layover", "contrast inversion"
- Summary line: "The appearance gap is far larger than day↔night or indoor↔outdoor"

### Scene 03 — Research Question (~45s)
- Bullet cascade: 24 matcher families · zero-shot · no fine-tuning · 3 cross-modal datasets
- Central question types out: "Do they transfer?"

### Scene 04 — The Pipeline (~90s)
- Horizontal 4-stage flow:
  1. Normalize (percentile / CLAHE / z-score)
  2. Tile (768×768, 256 overlap)
  3. Match (pretrained matcher)
  4. Geometric filter (affine-RANSAC → tie-point error)
- Each stage lights up in sequence, then the whole pipe pulses once

### Scene 05 — Tiled Matching in Action (~60s)
- Zoom into a large scene, show overlapping tiles sliding in
- A pair of tiles lifts out, green inlier lines animate between them
- Tiles settle back, aggregated match field hints at the full scene

### Scene 06 — Leaderboard (~90s)
- Animated horizontal bar chart: mean tie-point error (px), top 10 matchers
- Bars grow from right→left (lower is better)
- RoMa + XoFTR light up gold at 3.0 px; MatchAnything-ELoFTR highlighted at 3.4 px
- Chyron: "RoMa ties XoFTR — and RoMa has **zero cross-modal training**"

### Scene 07 — DINOv2 Hypothesis (~60s)
- Diagram: internet-scale images → DINOv2 → frozen features → RoMa regression head
- A feature-space cloud: optical + SAR points start separated, then collapse toward each other when projected through DINOv2
- Caption: "Emergent modality invariance from web-scale pretraining (working hypothesis)"

### Scene 08 — Protocol Sensitivity (~90s)
- Violin-style column per matcher showing mean-error spread under protocol sweeps
- Intra-matcher spread visibly exceeds inter-matcher spacing
- Callout: "Protocol can dominate matcher choice"
- Ends with headline number: "**33×** error swing for a single matcher"

### Scene 09 — Affine vs Homography (~75s)
- Two geometry gizmos: affine (6 DoF) vs homography (8 DoF)
- Show orthorectified scene being warped — affine fits, homography's extra DoF jitters into noise
- Numbers land: "9.74 px affine · 12.34 px homography"

### Scene 10 — Cross-Dataset Transfer (~60s)
- Three dataset cards (SpaceNet9, SRIF, SARptical) arranged horizontally
- Ranking arrows show MINIMA-RoMa consistent across all three
- Caption: "Zero-failure consistency across datasets"

### Scene 11 — Runtime Pareto (~60s)
- Scatter: runtime (s) vs mean error (px)
- RoMa up top (accurate, slow), XFeat bottom (fast, noisy)
- XoFTR pops on the Pareto frontier at ~0.4s, 3.0 px
- Star burst on XoFTR: "Pareto star"

### Scene 12 — Takeaways + Recipe (~60s)
- Three boxed takeaways:
  1. DINOv2 backbones ≈ emergent modality invariance
  2. Protocol tuning ≥ matcher selection
  3. Affine + tiled + percentile norm is the default recipe
- Recipe panel: affine · 768 tile / 128 overlap · percentile · RANSAC ≤10 px · RoMa or MINIMA-RoMa
- End card: repo URL + CVPR IMW 2026 badge

## Animation Rhythm

- Opening (Scenes 1–3): slow, establishing, 2-second holds
- Middle (Scenes 4–8): pipeline builds, faster stagger, quick reveals
- Climax (Scenes 7, 8, 11): slow down on the aha moments, 3-second holds
- Closing (Scene 12): calm, readable, recipe-friendly

## Success Criteria

- Each scene stands alone; Isaac can pause on any of them and talk
- The "aha moments" land visually before they land in text
- Cohesive palette + typography across all 12 scenes
- Total runtime 8–9 minutes so live narration fits in 10
