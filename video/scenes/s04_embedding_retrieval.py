"""UT Austin GeoAI Talk — Core scenes S01–S04 (Isaac Corley)"""

import random

import numpy as np
from manim import (
    DOWN,
    LEFT,
    RIGHT,
    UP,
    Arrow,
    Dot,
    FadeIn,
    Line,
    VGroup,
)

from _theme import (
    AMBER,
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
    mini_grid,
    mono,
    panel,
    sans,
    scene_tag,
    stat_chip,
)

random.seed(7)
np.random.seed(7)


class S04_EmbeddingRetrieval(PacedScene):
    def construct(self):
        self.camera.background_color = BG  # ty: ignore[invalid-assignment]
        tag = scene_tag("embedding retrieval", accent=CORAL)
        self.play(FadeIn(tag), run_time=0.6)

        q_tile = panel(1.4, 1.4, fill=PANEL2)
        q_grid = mini_grid(3, 3, 0.32, DIM, fill_color=PERI, fill_opacity=0.08)
        q_grid.move_to(q_tile)
        q_lbl = caption("query tile", size=13)
        q_lbl.next_to(q_tile, DOWN, buff=0.1)
        q_grp = VGroup(q_tile, q_grid, q_lbl).to_edge(LEFT, buff=0.8).shift(UP * 0.4)
        self.play(FadeIn(q_grp), run_time=0.6)
        self.wait(0.3)

        enc_box = panel(1.8, 1.2, fill=SURFACE)
        enc_lbl = sans("Encoder", size=18, color=CORAL)
        enc_sub = caption("foundation model", size=11)
        enc_lbl.move_to(enc_box.get_center() + UP * 0.15)
        enc_sub.next_to(enc_lbl, DOWN, buff=0.06)
        enc_grp = VGroup(enc_box, enc_lbl, enc_sub).next_to(q_grp, RIGHT, buff=0.6)

        arr1 = Arrow(
            q_tile.get_right(),
            enc_box.get_left(),
            color=CORAL,
            stroke_width=1.8,
            buff=0.1,
            max_tip_length_to_length_ratio=0.12,
        )
        self.play(FadeIn(enc_grp), FadeIn(arr1), run_time=0.6)
        self.wait(0.3)

        emb_row = mono("1 0 1 1 0 0 1 0 1 1", size=16, color=CORAL)
        emb_row.next_to(enc_box, RIGHT, buff=0.5)
        arr2 = Arrow(
            enc_box.get_right(),
            emb_row.get_left(),
            color=CORAL,
            stroke_width=1.8,
            buff=0.1,
            max_tip_length_to_length_ratio=0.12,
        )
        self.play(FadeIn(arr2), FadeIn(emb_row), run_time=0.6)
        self.wait(0.4)

        space_panel = panel(4.5, 2.8, fill=PANEL2)
        space_panel.to_edge(RIGHT, buff=0.5).shift(DOWN * 0.5)
        sp_lbl = caption("embedding space", size=13, color=DIM)
        sp_lbl.next_to(space_panel, UP, buff=0.08)

        rng = np.random.RandomState(42)
        colors_list = [EARTH, PERI, AMBER, DIM]
        dots = VGroup()
        for _ in range(30):
            dx, dy = rng.uniform(-1.8, 1.8), rng.uniform(-1.1, 1.1)
            c = colors_list[rng.randint(0, 4)]
            dot = Dot(space_panel.get_center() + RIGHT * dx + UP * dy, radius=0.06, color=c)
            dot.set_fill(c, opacity=0.7)
            dots.add(dot)

        self.play(FadeIn(space_panel), FadeIn(sp_lbl), FadeIn(dots), run_time=0.7)
        self.wait(0.4)

        q_dot = Dot(space_panel.get_center() + LEFT * 0.3 + UP * 0.2, radius=0.1, color=CORAL)
        q_dot.set_fill(CORAL, opacity=0.9)
        q_tag = caption("query", size=11, color=CORAL)
        q_tag.next_to(q_dot, UP, buff=0.08)
        self.play(FadeIn(q_dot), FadeIn(q_tag), run_time=0.5)
        self.wait(0.3)

        dists = sorted(
            (np.linalg.norm(d.get_center() - q_dot.get_center()), i) for i, d in enumerate(dots)
        )
        nn_lines = VGroup()
        for _, idx in dists[:4]:
            line = Line(q_dot.get_center(), dots[idx].get_center(), color=CORAL, stroke_width=1.5)
            nn_lines.add(line)
            dots[idx].set_color(CORAL)
        self.play(FadeIn(nn_lines), run_time=0.6)
        self.wait(0.4)

        res_lbl = caption("top-K matches", size=13, color=CORAL)
        res_tiles = VGroup()
        for _ in range(4):
            t = panel(0.7, 0.7, fill=SURFACE)
            g = mini_grid(2, 2, 0.2, DIM, fill_color=CORAL, fill_opacity=0.1)
            g.move_to(t)
            res_tiles.add(VGroup(t, g))
        res_tiles.arrange(RIGHT, buff=0.15)
        res_lbl.next_to(res_tiles, UP, buff=0.1)
        res_grp = VGroup(res_lbl, res_tiles)
        res_grp.next_to(space_panel, DOWN, buff=0.25)
        if res_grp.get_bottom()[1] < -3.4:
            res_grp.shift(UP * 0.3)
        self.play(FadeIn(res_grp, shift=UP * 0.2), run_time=0.6)
        self.wait(0.4)

        chip = stat_chip("Search billions of embeddings", "in milliseconds", CORAL, width=5.5)
        chip.to_edge(LEFT, buff=0.7).to_edge(DOWN, buff=0.4)
        if chip.get_bottom()[1] < -3.4:
            chip.shift(UP * 0.3)
        self.play(FadeIn(chip, shift=UP * 0.15), run_time=0.6)

        cleanup(self, hold=1.5)
