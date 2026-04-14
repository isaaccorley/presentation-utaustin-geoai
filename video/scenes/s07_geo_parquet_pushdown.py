"""UT Austin GeoAI Talk — Extended scenes S05–S17 (Isaac Corley)"""

from manim import (
    DOWN,
    LEFT,
    ORIGIN,
    RIGHT,
    UP,
    Arrow,
    Create,
    FadeIn,
    Rectangle,
    SurroundingRectangle,
    Text,
    VGroup,
)

from _theme import (
    AMBER,
    BG,
    CORAL,
    DIM,
    EARTH,
    PANEL2,
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


class S07_GeoParquetPushdown(PacedScene):
    """GeoParquet predicate pushdown: 2.6B rows → spatial filter → handful."""

    def construct(self):
        self.camera.background_color = BG  # ty: ignore[invalid-assignment]
        tag = scene_tag("geoparquet at scale", accent=EARTH)
        self.play(FadeIn(tag), run_time=0.6)

        big_box = panel(3.5, 3.15, fill=PANEL2)

        row_groups = VGroup()
        for _ in range(6):
            rg = Rectangle(width=2.75, height=0.27, color=DIM, stroke_width=0.8)
            rg.set_fill(DIM, opacity=0.06)
            row_groups.add(rg)
        row_groups.arrange(DOWN, buff=0.04)
        row_groups.move_to(big_box.get_center() + UP * 0.02)
        rg_lbl = caption("row groups", size=10, color=DIM)
        rg_lbl.next_to(row_groups, DOWN, buff=0.04)

        big_lbl = sans("2.6B buildings", size=20, color=EARTH)
        big_sub = caption("Overture Maps on S3", size=13)
        big_lbl.next_to(big_box, DOWN, buff=0.22)
        big_sub.next_to(big_lbl, DOWN, buff=0.08)

        big_grp = VGroup(big_box, row_groups, rg_lbl, big_lbl, big_sub)
        big_grp.to_edge(LEFT, buff=0.6)
        self.play(FadeIn(big_grp), run_time=0.7)
        self.wait(0.4)

        filter_box = panel(2.4, 1.6, fill=SURFACE)
        f_title = sans("Spatial Filter", size=18, color=AMBER)
        f_code = mono("bbox ∩ Austin", size=14, color=AMBER)
        f_title.move_to(filter_box.get_center() + UP * 0.2)
        f_code.next_to(f_title, DOWN, buff=0.12)
        filter_grp = VGroup(filter_box, f_title, f_code).move_to(ORIGIN)

        arr1 = Arrow(
            big_box.get_right(),
            filter_box.get_left(),
            color=EARTH,
            stroke_width=2.0,
            buff=0.12,
            max_tip_length_to_length_ratio=0.1,
        )
        self.play(FadeIn(filter_grp), FadeIn(arr1), run_time=0.6)
        self.wait(0.3)

        skipped = VGroup()
        for i, rg in enumerate(row_groups):
            if i != 2:
                x = Text("✕", font_size=14, color=CORAL)
                x.move_to(rg.get_right() + RIGHT * 0.2)
                skipped.add(x)
        kept = SurroundingRectangle(row_groups[2], color=EARTH, stroke_width=2.0, buff=0.04)
        self.play(FadeIn(skipped), Create(kept), run_time=0.6)
        self.wait(0.4)

        result_box = panel(2.2, 1.8, fill=SURFACE)
        result_box.to_edge(RIGHT, buff=0.8)
        r_title = sans("Result", size=18, color=EARTH)
        r_count = mono("847 buildings", size=16, color=EARTH)
        r_title.move_to(result_box.get_center() + UP * 0.25)
        r_count.next_to(r_title, DOWN, buff=0.15)
        result_grp = VGroup(result_box, r_title, r_count)

        arr2 = Arrow(
            filter_box.get_right(),
            result_box.get_left(),
            color=EARTH,
            stroke_width=2.0,
            buff=0.12,
            max_tip_length_to_length_ratio=0.1,
        )
        self.play(FadeIn(result_grp), FadeIn(arr2), run_time=0.6)
        self.wait(0.4)

        chip = stat_chip(
            "Predicate pushdown", "skip row groups → read only matching data", EARTH, width=5.5
        )
        chip.to_edge(DOWN, buff=0.35)
        self.play(FadeIn(chip, shift=UP * 0.15), run_time=0.6)
        cleanup(self, hold=1.5)
