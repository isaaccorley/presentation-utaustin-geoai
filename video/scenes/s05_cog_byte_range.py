"""UT Austin GeoAI Talk — Extended scenes S05–S17 (Isaac Corley)"""

from manim import (
    DOWN,
    LEFT,
    RIGHT,
    UP,
    Arrow,
    FadeIn,
    Rectangle,
    VGroup,
)

from _theme import (
    BG,
    CORAL,
    DIM,
    PANEL2,
    PERI,
    SURFACE,
    PacedScene,
    caption,
    cleanup,
    mini_grid,
    mono,
    panel,
    sans,
    scene_tag,
    stat_chip,
)


class S05_COGByteRange(PacedScene):
    """HTTP range requests pulling just the tiles you need from a COG."""

    def construct(self):
        self.camera.background_color = BG  # ty: ignore[invalid-assignment]
        tag = scene_tag("cloud-optimized geotiff", accent=PERI)
        self.play(FadeIn(tag), run_time=0.6)

        full = panel(4.0, 3.0, fill=PANEL2)
        full_lbl = sans("COG on S3", size=20, color=PERI)
        full_lbl.next_to(full, UP, buff=0.12)
        grid = mini_grid(6, 8, 0.38, DIM, fill_color=PERI, fill_opacity=0.04)
        grid.move_to(full)
        full_grp = VGroup(full, full_lbl, grid).to_edge(LEFT, buff=0.8)
        self.play(FadeIn(full_grp), run_time=0.7)
        self.wait(0.4)

        pyr_lbls = ["Full res", "1/2", "1/4", "1/8"]
        pyr_rects = VGroup()
        for i, lbl in enumerate(pyr_lbls):
            w = 3.2 - i * 0.7
            r = Rectangle(width=w, height=0.4, color=PERI, stroke_width=1.2)
            r.set_fill(PERI, opacity=0.06 + i * 0.04)
            t = caption(lbl, size=11, color=PERI)
            t.move_to(r)
            pyr_rects.add(VGroup(r, t))
        pyr_rects.arrange(DOWN, buff=0.08)
        pyr_rects.next_to(full_grp, RIGHT, buff=1.2)
        pyr_title = caption("overview levels", size=14, color=DIM)
        pyr_title.next_to(pyr_rects, UP, buff=0.15)
        self.play(FadeIn(pyr_title), run_time=0.3)
        for pr in pyr_rects:
            self.play(FadeIn(pr, shift=DOWN * 0.15), run_time=0.35)
        self.wait(0.4)

        req_box = panel(2.8, 1.6, fill=SURFACE)
        req_box.to_edge(RIGHT, buff=0.6).shift(UP * 0.8)
        req_title = sans("Range Request", size=18, color=CORAL)
        req_code = mono("bytes=4096-8192", size=14, color=CORAL)
        req_title.move_to(req_box.get_center() + UP * 0.25)
        req_code.move_to(req_box.get_center() + DOWN * 0.2)
        req_grp = VGroup(req_box, req_title, req_code)

        highlight = Rectangle(width=0.76, height=0.76, color=CORAL, stroke_width=2.5)
        highlight.set_fill(CORAL, opacity=0.15)
        highlight.move_to(grid[20].get_center())

        arr = Arrow(
            req_box.get_left(),
            highlight.get_right() + RIGHT * 0.3,
            color=CORAL,
            stroke_width=2.0,
            buff=0.1,
            max_tip_length_to_length_ratio=0.1,
        )
        self.play(FadeIn(req_grp), FadeIn(arr), FadeIn(highlight), run_time=0.7)
        self.wait(0.5)

        result = panel(1.2, 1.2, fill=PANEL2)
        result_grid = mini_grid(2, 2, 0.4, PERI, fill_color=PERI, fill_opacity=0.15)
        result_grid.move_to(result)
        res_lbl = caption("2 tiles fetched", size=13, color=PERI)
        res_lbl.next_to(result, DOWN, buff=0.1)
        res_grp = VGroup(result, result_grid, res_lbl)
        res_grp.next_to(req_grp, DOWN, buff=0.5)
        self.play(FadeIn(res_grp, shift=DOWN * 0.2), run_time=0.6)
        self.wait(0.4)

        chip = stat_chip("Read 0.1% of the file", "skip 99.9% — no full download", CORAL, width=5.5)
        chip.to_edge(DOWN, buff=0.4).to_edge(LEFT, buff=0.8)
        self.play(FadeIn(chip, shift=UP * 0.15), run_time=0.6)
        cleanup(self, hold=1.5)
