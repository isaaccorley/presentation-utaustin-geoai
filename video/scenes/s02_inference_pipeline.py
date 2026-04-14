"""UT Austin GeoAI Talk — Core scenes S01–S04 (Isaac Corley)"""

import random

import numpy as np
from manim import (
    DOWN,
    LEFT,
    RIGHT,
    UP,
    Arrow,
    FadeIn,
    Rectangle,
    Square,
    VGroup,
)

from _theme import (
    AMBER,
    BG,
    DIM,
    EARTH,
    PANEL2,
    PERI,
    SURFACE,
    PacedScene,
    caption,
    cleanup,
    mini_grid,
    panel,
    sans,
    scene_tag,
)

random.seed(7)
np.random.seed(7)


class S02_InferencePipeline(PacedScene):
    def construct(self):
        self.camera.background_color = BG  # ty: ignore[invalid-assignment]
        tag = scene_tag("inference at scale", accent=EARTH)
        self.play(FadeIn(tag), run_time=0.6)

        scene_p = panel(3.5, 3.0, fill=PANEL2)
        grid = mini_grid(8, 8, 0.32, DIM, fill_color=PERI, fill_opacity=0.06)
        grid.move_to(scene_p)
        scene_lbl = caption("10,000 x 10,000 px", size=13)
        scene_lbl.next_to(scene_p, DOWN, buff=0.12)
        cog_lbl = caption("COG on S3", size=12, color=PERI)
        cog_lbl.next_to(scene_lbl, DOWN, buff=0.06)
        scene_grp = VGroup(scene_p, grid, scene_lbl, cog_lbl)
        scene_grp.to_edge(LEFT, buff=0.7).shift(DOWN * 0.15)
        self.play(FadeIn(scene_grp), run_time=0.7)
        self.wait(0.5)

        tile_grid = VGroup()
        for r in range(4):
            for c in range(4):
                sq = Square(side_length=0.62, color=EARTH, stroke_width=1.2)
                sq.set_fill(EARTH, opacity=0.05)
                sq.move_to(
                    scene_p.get_center() + RIGHT * (c - 1.5) * 0.64 + DOWN * (r - 1.5) * 0.64
                )
                tile_grid.add(sq)
        self.play(FadeIn(tile_grid), run_time=0.7)

        overlap = Rectangle(width=0.08, height=0.62, color=AMBER, stroke_width=1.5)
        overlap.set_fill(AMBER, opacity=0.25)
        overlap.move_to(tile_grid[1].get_left())
        ov_lbl = caption("overlap", size=10, color=AMBER)
        ov_lbl.next_to(overlap, UP, buff=0.08)
        self.play(FadeIn(overlap), FadeIn(ov_lbl), run_time=0.5)
        self.wait(0.5)

        sample_tiles = VGroup()
        for _ in range(3):
            t = Square(side_length=0.55, color=EARTH, stroke_width=1.2)
            t.set_fill(EARTH, opacity=0.08)
            sample_tiles.add(t)
        sample_tiles.arrange(DOWN, buff=0.15).move_to(RIGHT * 0.8)
        tile_lbl = caption("256 px tiles", size=12)
        tile_lbl.next_to(sample_tiles, DOWN, buff=0.1)

        self.play(
            *[FadeIn(t, shift=RIGHT * 0.4) for t in sample_tiles],
            FadeIn(tile_lbl),
            run_time=0.7,
        )
        self.wait(0.4)

        model_box = panel(1.8, 1.6, fill=SURFACE)
        m_lbl = sans("Model", size=20, color=EARTH)
        nn_bars = VGroup()
        for w in [0.8, 0.5, 0.8]:
            bar = Rectangle(width=w, height=0.18, color=EARTH, stroke_width=1.0)
            bar.set_fill(EARTH, opacity=0.12)
            nn_bars.add(bar)
        nn_bars.arrange(DOWN, buff=0.1)
        m_lbl.next_to(nn_bars, UP, buff=0.12)
        VGroup(m_lbl, nn_bars).move_to(model_box)
        model_all = VGroup(model_box, m_lbl, nn_bars).move_to(RIGHT * 3.0)

        arr_in = Arrow(
            sample_tiles.get_right(),
            model_box.get_left(),
            color=EARTH,
            stroke_width=1.8,
            buff=0.1,
            max_tip_length_to_length_ratio=0.12,
        )
        self.play(FadeIn(model_all), FadeIn(arr_in), run_time=0.6)
        self.wait(0.4)

        pred_tiles = VGroup()
        for _ in range(3):
            t = Square(side_length=0.55, color=EARTH, stroke_width=1.2)
            t.set_fill(EARTH, opacity=0.3)
            pred_tiles.add(t)
        pred_tiles.arrange(DOWN, buff=0.15).move_to(RIGHT * 5.2)

        arr_out = Arrow(
            model_box.get_right(),
            pred_tiles.get_left(),
            color=EARTH,
            stroke_width=1.8,
            buff=0.1,
            max_tip_length_to_length_ratio=0.12,
        )
        self.play(FadeIn(arr_out), FadeIn(pred_tiles, shift=RIGHT * 0.3), run_time=0.6)
        self.wait(0.4)

        out_lbl = caption("COG / GeoParquet", size=13, color=EARTH)
        out_lbl.next_to(pred_tiles, DOWN, buff=0.15)
        self.play(FadeIn(out_lbl), run_time=0.4)

        note = caption("tiles reassemble into mosaic", size=14, color=DIM)
        note.to_edge(DOWN, buff=0.4)
        self.play(FadeIn(note), run_time=0.5)

        cleanup(self, hold=1.5)
