"""UT Austin GeoAI Talk — Extended scenes S05–S17 (Isaac Corley)"""

import numpy as np
from manim import (
    DOWN,
    LEFT,
    RIGHT,
    UP,
    Arrow,
    Dot,
    FadeIn,
    SurroundingRectangle,
    VGroup,
)

from _theme import (
    BG,
    CORAL,
    DIM,
    EARTH,
    PANEL2,
    PERI,
    SURFACE,
    PacedScene,
    caption,
    cleanup,
    panel,
    sans,
    satellite_tile,
    scene_tag,
    stat_chip,
)


class S08_ContrastiveLearning(PacedScene):
    """Contrastive learning: positive pair pulled together, negative repelled."""

    def construct(self):
        self.camera.background_color = BG  # ty: ignore[invalid-assignment]
        tag = scene_tag("contrastive learning", accent=PERI)
        self.play(FadeIn(tag), run_time=0.6)

        # Satellite tiles instead of colored grids
        sat_a = satellite_tile(4, 4, 0.3, seed=42)
        border_a = SurroundingRectangle(sat_a, color=PERI, stroke_width=1.8, buff=0.04)
        lbl_a = caption("tile A", size=13, color=PERI)
        lbl_a.next_to(border_a, DOWN, buff=0.08)
        grp_a = VGroup(sat_a, border_a, lbl_a)

        sat_b = satellite_tile(4, 4, 0.3, seed=99)
        border_b = SurroundingRectangle(sat_b, color=EARTH, stroke_width=1.8, buff=0.04)
        lbl_b = caption("tile B (augmented)", size=13, color=EARTH)
        lbl_b.next_to(border_b, DOWN, buff=0.08)
        grp_b = VGroup(sat_b, border_b, lbl_b)

        VGroup(grp_a, grp_b).arrange(RIGHT, buff=1.5)
        VGroup(grp_a, grp_b).to_edge(UP, buff=1.2).shift(LEFT * 1.5)
        self.play(FadeIn(grp_a), FadeIn(grp_b), run_time=0.6)
        self.wait(0.3)

        enc_a = panel(1.2, 0.8, fill=SURFACE)
        enc_a_lbl = sans("f(·)", size=18, color=PERI)
        enc_a_lbl.move_to(enc_a)

        enc_b = panel(1.2, 0.8, fill=SURFACE)
        enc_b_lbl = sans("f(·)", size=18, color=EARTH)
        enc_b_lbl.move_to(enc_b)

        VGroup(enc_a, enc_a_lbl).next_to(grp_a, DOWN, buff=0.4)
        VGroup(enc_b, enc_b_lbl).next_to(grp_b, DOWN, buff=0.4)

        arr_a = Arrow(
            border_a.get_bottom(),
            enc_a.get_top(),
            color=PERI,
            stroke_width=1.5,
            buff=0.08,
            max_tip_length_to_length_ratio=0.12,
        )
        arr_b = Arrow(
            border_b.get_bottom(),
            enc_b.get_top(),
            color=EARTH,
            stroke_width=1.5,
            buff=0.08,
            max_tip_length_to_length_ratio=0.12,
        )
        self.play(
            FadeIn(enc_a),
            FadeIn(enc_a_lbl),
            FadeIn(enc_b),
            FadeIn(enc_b_lbl),
            FadeIn(arr_a),
            FadeIn(arr_b),
            run_time=0.6,
        )
        self.wait(0.3)

        space = panel(4.0, 3.5, fill=PANEL2)
        space.to_edge(RIGHT, buff=0.5).shift(DOWN * 0.2)
        sp_lbl = caption("embedding space", size=14, color=DIM)
        sp_lbl.next_to(space, UP, buff=0.08)
        self.play(FadeIn(space), FadeIn(sp_lbl), run_time=0.5)

        rng = np.random.RandomState(42)
        bg_dots = VGroup()
        for _ in range(20):
            dx, dy = rng.uniform(-1.6, 1.6), rng.uniform(-1.4, 1.4)
            dot = Dot(space.get_center() + RIGHT * dx + UP * dy, radius=0.05, color=DIM)
            dot.set_fill(DIM, opacity=0.3)
            bg_dots.add(dot)
        self.play(FadeIn(bg_dots), run_time=0.4)

        dot_a = Dot(space.get_center() + LEFT * 1.2 + UP * 0.8, radius=0.1, color=PERI)
        dot_a.set_fill(PERI, opacity=0.9)
        tag_a = caption("z_A", size=12, color=PERI)
        tag_a.next_to(dot_a, UP, buff=0.06)

        dot_b = Dot(space.get_center() + RIGHT * 1.0 + DOWN * 0.6, radius=0.1, color=EARTH)
        dot_b.set_fill(EARTH, opacity=0.9)
        tag_b = caption("z_B", size=12, color=EARTH)
        tag_b.next_to(dot_b, DOWN, buff=0.06)

        self.play(FadeIn(dot_a), FadeIn(tag_a), FadeIn(dot_b), FadeIn(tag_b), run_time=0.5)
        self.wait(0.4)

        target = space.get_center() + UP * 0.1
        self.play(
            dot_a.animate.move_to(target + LEFT * 0.15),
            tag_a.animate.move_to(target + LEFT * 0.15 + UP * 0.2),
            dot_b.animate.move_to(target + RIGHT * 0.15),
            tag_b.animate.move_to(target + RIGHT * 0.15 + DOWN * 0.2),
            run_time=1.0,
        )
        self.wait(0.3)

        pull_lbl = sans("attract", size=18, color=EARTH)
        pull_lbl.next_to(VGroup(dot_a, dot_b), DOWN, buff=0.3)
        self.play(FadeIn(pull_lbl), run_time=0.4)
        self.wait(0.3)

        neg_dot = bg_dots[5]
        neg_dot.set_color(CORAL)
        neg_lbl = caption("negative", size=12, color=CORAL)
        neg_lbl.next_to(neg_dot, RIGHT, buff=0.08)
        self.play(FadeIn(neg_lbl), neg_dot.animate.shift(RIGHT * 0.6 + DOWN * 0.4), run_time=0.7)

        repel_lbl = sans("repel", size=18, color=CORAL)
        repel_lbl.next_to(neg_dot, DOWN, buff=0.15)
        self.play(FadeIn(repel_lbl), run_time=0.4)
        self.wait(0.4)

        chip = stat_chip(
            "Learn by comparison", "similar tiles close, different tiles far", PERI, width=5.5
        )
        chip.to_edge(DOWN, buff=0.35).to_edge(LEFT, buff=0.6)
        self.play(FadeIn(chip, shift=UP * 0.15), run_time=0.6)
        cleanup(self, hold=1.5)
