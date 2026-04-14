"""UT Austin GeoAI Talk — Extended scenes S05–S17 (Isaac Corley)"""

from manim import (
    DOWN,
    LEFT,
    RIGHT,
    UP,
    Create,
    Dot,
    FadeIn,
    Line,
    VGroup,
)

from _theme import (
    AMBER,
    BG,
    BORDER,
    CORAL,
    DIM,
    EARTH,
    PERI,
    SURFACE,
    PacedScene,
    caption,
    cleanup,
    mono,
    panel,
    sans,
    scene_tag,
    stat_chip,
)


class S14_CNGTimeline(PacedScene):
    """Horizontal timeline showing the evolution of CNG formats 2015-2025."""

    def construct(self):
        self.camera.background_color = BG  # ty: ignore[invalid-assignment]
        tag = scene_tag("cloud-native timeline", accent=PERI)
        self.play(FadeIn(tag), run_time=0.6)

        # Timeline data: (year, title, detail, accent, above)
        data = [
            ("2015", "Landsat on AWS", "COG concept", PERI, True),
            ("2017", "STAC sprint", "Radiant Earth", PERI, False),
            ("2021", "STAC 1.0", "PMTiles · COPC", EARTH, True),
            ("2022", "Overture Maps", "Zarr v2 OGC", AMBER, False),
            ("2023", "GeoParquet 1.0", "COG OGC · CNG", CORAL, True),
            ("2024", "Overture GA", "STAC 1.1", EARTH, False),
            ("2025", "Zarr-Py 3.0", "Native Parquet geo", PERI, True),
        ]

        # Main line
        line = Line(LEFT * 5.8, RIGHT * 5.8, color=BORDER, stroke_width=2)
        line.shift(DOWN * 0.2)
        self.play(Create(line), run_time=0.6)

        n = len(data)
        x_start = -5.4
        x_end = 5.4
        spacing = (x_end - x_start) / (n - 1)

        for i, (year, title, detail, accent, above) in enumerate(data):
            x = x_start + i * spacing
            dot = Dot(point=(x, line.get_y(), 0), radius=0.06, color=accent)
            yr = mono(year, size=14, color=DIM)
            yr.next_to(dot, DOWN * 0.8 if above else UP * 0.8, buff=0.15)

            card_bg = panel(1.4, 0.85, fill=SURFACE)
            t = sans(title, size=13, color=accent)
            if t.width > card_bg.width - 0.15:
                t.scale((card_bg.width - 0.15) / t.width)
            d = caption(detail, size=10)
            if d.width > card_bg.width - 0.15:
                d.scale((card_bg.width - 0.15) / d.width)
            t.move_to(card_bg.get_center() + UP * 0.15)
            d.move_to(card_bg.get_center() + DOWN * 0.2)
            card = VGroup(card_bg, t, d)

            if above:
                card.next_to(dot, UP, buff=0.35)
                shift_dir = DOWN * 0.3
            else:
                card.next_to(dot, DOWN, buff=0.35)
                shift_dir = UP * 0.3

            # Small connector line
            connector = Line(
                dot.get_center(),
                card_bg.get_edge_center(DOWN if above else UP),
                color=BORDER,
                stroke_width=1,
            )

            self.play(
                FadeIn(dot),
                FadeIn(yr),
                FadeIn(connector),
                FadeIn(card, shift=shift_dir),
                run_time=0.45,
            )

        self.wait(0.5)

        chip = stat_chip("2015 → 2025", "a decade of cloud-native geo", CORAL, width=5)
        chip.to_edge(DOWN, buff=0.35)
        self.play(FadeIn(chip, shift=UP * 0.15), run_time=0.6)
        cleanup(self, hold=2.0)
