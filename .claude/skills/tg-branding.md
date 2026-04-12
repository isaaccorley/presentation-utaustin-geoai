---
name: tg-branding
description: Taylor Geospatial brand guide reference — colors, logos, typography, elements, and usage guidelines extracted from the TG Brand Guide.
---

# Taylor Geospatial Brand Guide

Quick reference for all TG brand assets and design tokens. Use this when building or modifying branded materials.

## Color Palette

### Primary Colors

| Name | Hex | RGB | Usage |
|------|-----|-----|-------|
| **Brown** | `#3b1e1c` | 59, 30, 28 | Dark backgrounds, primary text on light bg |
| **Ivory** | `#f4f4eb` | 244, 244, 235 | Light backgrounds, primary text on dark bg |
| **Periwinkle** | `#80a0d8` | 128, 160, 216 | Primary accent, links, interactive elements |

### Secondary Colors

| Name | Hex | RGB | Usage |
|------|-----|-----|-------|
| **Red** | `#ff4f2c` | 255, 79, 44 | Highlight accent, CTAs, emphasis |
| **Light Blue** | `#a7d0dc` | 167, 208, 220 | Secondary accent, supporting elements |
| **Green** | `#cff29e` | 207, 242, 158 | Success states, positive indicators |

### Theme Tokens (slide deck)

**Dark mode** (default):
- Background: `#1a0f0e` (deepened brown)
- Surface: `#261816` / `#33211f`
- Text: `#f4f4eb` (ivory)
- Text secondary: `#c4c4b8`
- Text muted: `#8a8a7e`
- Borders: `#3d2a28` / `#4a3634`

**Light mode**:
- Background: `#f4f4eb` (ivory)
- Surface: `#eaeade` / `#dfdfd4`
- Text: `#3b1e1c` (brown)
- Text secondary: `#5c3d3a`
- Text muted: `#8a6e6b`
- Borders: `#ccc8ba` / `#d9d5c8`

### Brand Gradient

```
linear-gradient(261deg, #ff4f2c 0%, #80a0d8 100%)
```

Light mode variant (higher contrast on ivory):
```
linear-gradient(261deg, #e0401f 0%, #5a7ab8 100%)
```

## Logo Suite

All logos are in `assets/Logos/`. Use the correct variant for the background.

### Primary Logo (stacked, two-line)
- Dark bg: `Logos/Logo without Tagline/Standard Logo/Digital/taylor-geo-logo-ivory-rgb.svg`
- Light bg: `Logos/Logo without Tagline/Standard Logo/Digital/taylor-geo-logo-rgb.svg`

### One-Line Logo (horizontal)
- Dark bg: `Logos/Logo without Tagline/One-Line Logo/Digital/TG-oneline-ivory-rgb.svg`
- Light bg: `Logos/Logo without Tagline/One-Line Logo/Digital/TG-oneline-rgb.svg`

### Brandmark (icon only, no text)
- Dark bg: `Logos/Brandmark/Digital/taylor-geo-brandmark-ivory-rgb.svg`
- Light bg: `Logos/Brandmark/Digital/taylor-geo-brandmark-rgb.svg`

### Logo with Tagline
- Two-line: `Logos/Logo _with_ Tagline/Two-Line Logo with Tagline/Digital/TG-logo-tagline-ivory-rgb.svg`
- One-line: `Logos/Logo _with_ Tagline/One-Line Logo with Tagline/Digital/TG-oneline-tagline-ivory-rgb.svg`

### Secondary Logo
- `Logos/Logo without Tagline/Secondary Logo/Digital/taylor-geo-logo-secondary-rgb.svg`

### Rules
- Always use ivory variants on dark backgrounds, standard on light
- Do not stretch, rotate, or recolor the logo
- Maintain clear space around the logo equal to the height of the brandmark

## Typography

The slide deck uses:
- **Headings & Body:** Space Grotesk (400, 500, 700)
- **Code:** JetBrains Mono (400, 500)

Font files: `public/fonts/`

Font size scale: 14px, 16px, 20px, 24px, 28px, 36px, 48px, 64px, 88px

Heading sizes are responsive — `h1` uses `[7, 8]` (64px/88px), `h2` uses `[6, 7]` (48px/64px) with tight negative letter-spacing for professional density.

## Brand Elements

### Frames (`assets/Elements/Frames/`)
Decorative border elements in four colors (brown, ivory, periwinkle, red) and three styles:
- **Outer frame** — full border
- **Inner frame** — inset border
- **Corner frame** — corner accents only

### Pin Drops (`assets/Elements/Pindrop/`)
Location marker icons in four colors: brown, ivory, periwinkle, red.

### Icons (`assets/Icons/`)
- `impact-icon.svg` — impact/measurement
- `pipelines.svg` — data pipelines
- `scale.svg` — scalability

## Satellite Imagery

Background/hero imagery in `assets/Satellite Imagery/Website Homepage/`:
- Full size: `LandSat1.jpg`, `LandSat2.jpg`, `LandSat3.jpg`
- Brown-tinted: `LandSat_Brown_1.jpg`, `LandSat_Brown_2.jpg`, `LandSat_Brown_3.jpg`
- Cropped halves: `Left 1.jpg`–`Left 3.jpg`, `Right 1.jpg`–`Right 3.jpg`

## Visual Polish Details

### Slide Background
Content slides have subtle depth via two overlays in `Slide.tsx`:
- **Radial gradients** — faint periwinkle glow (upper-right) + faint red warmth (lower-left)
- **Noise texture** — SVG fractalNoise at 0.35 opacity for grain

### Lists
- `ul` uses **accent-colored dash markers** (8px red dashes via `::before`)
- `ol` uses **numbered accent pills** (monospace counter in a circular surface-bg badge)

### Blockquotes
3px accent left border + surface background + padding. Styled as callout containers.

### Tables
Accent-colored header underline, uppercase header text, alternating row striping (`surface` bg on even rows).

### Code Blocks
Gradient accent stripe (periwinkle→red) on the left edge via `::before`. Border uses `subtle` color for visibility.

### Navigation Bar
Glassmorphic: translucent bg + `backdrop-filter: blur(12px)`. Gradient progress bar (periwinkle→red) fills left-to-right across top of nav. Light/dark mode aware backgrounds.

### Columns
Thin 1px vertical separator line (`border` color) between columns.

### Section Slides
Background images render **full-bleed** via `position: fixed` covering the entire viewport. Dark scrim overlay at 50% opacity for text readability. `Slide.tsx` has no `overflow: hidden` to allow this.

## Syntax Highlighting Theme

Code blocks use a custom shiki theme (`theme/syntax.ts`) mapped to TG brand:
- Keywords: `#ff4f2c` (red)
- Functions: `#a7d0dc` (light blue)
- Classes/types: `#80a0d8` (periwinkle)
- Strings: `#cff29e` (green)
- Numbers: `#fbbf24` (warm yellow)
- Comments: `#6a5753` (muted brown, italic)
- Variables: `#f4f4eb` (ivory)
- Operators: `#c4c4b8` (muted)

## File Reference

| File | Purpose |
|------|---------|
| `assets/Brand Guide Lite.pdf` | Official brand guide PDF |
| `theme/colors.ts` | Color tokens (dark + light modes) |
| `theme/fonts.ts` | Font definitions |
| `theme/syntax.ts` | Code syntax highlighting |
| `components/Logo.tsx` | TG brandmark component |
