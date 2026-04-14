# GeoAI & Cloud-Native Geospatial

UT Austin talk deck for Isaac Corley and Taylor Geospatial, built with Next.js, MDX, and Theme UI.

## What's Here

- Main deck: `pages/index.mdx`
- Slide/theme code: `components/`, `theme/`

## Run

```bash
make install
make serve
make check
make build
```

Python tooling

```bash
uv sync --locked --all-groups
uv run pre-commit run --all-files
```

Dev server: `http://localhost:3000`

## Deck Model

- Slides are MDX blocks separated by `---`
- Each deck exports `meta.title`
- Common components: `TitleSlide`, `SectionSlide`, `Columns`, `Embed`, `Diagram`, `SpeakerNotes`
- Navigation: arrows, `Space`, `Enter`; `N` toggles notes; `F` toggles fullscreen

## Deploy

- `main` deploys to GitHub Pages via `.github/workflows/deploy.yml`
- The build uses `PAGES_BASE_PATH=/presentation-utaustin-geoai`
