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
)

random.seed(7)
np.random.seed(7)


class S03_TorchGeoSampling(PacedScene):
    def construct(self):
        self.camera.background_color = BG  # ty: ignore[invalid-assignment]
        tag = scene_tag("torchgeo geosampling", accent=AMBER)
        self.play(FadeIn(tag), run_time=0.6)

        img_rect = Rectangle(width=4.0, height=2.8, color=PERI, stroke_width=1.5)
        img_rect.set_fill(PERI, opacity=0.08)
        img_lbl = caption("Sentinel-2 Imagery", size=14, color=PERI)
        img_lbl.next_to(img_rect, UP, buff=0.08)

        lbl_rect = Rectangle(width=3.6, height=2.4, color=EARTH, stroke_width=1.5)
        lbl_rect.set_fill(EARTH, opacity=0.08)
        lbl_lbl = caption("Land Cover Labels", size=14, color=EARTH)
        lbl_lbl.next_to(lbl_rect, DOWN, buff=0.08)

        img_grp = VGroup(img_rect, img_lbl).shift(LEFT * 0.3 + UP * 0.15)
        lbl_grp = VGroup(lbl_rect, lbl_lbl).shift(RIGHT * 0.3 + DOWN * 0.15)
        VGroup(img_grp, lbl_grp).to_edge(LEFT, buff=1.0)

        self.play(FadeIn(img_grp), run_time=0.6)
        self.play(FadeIn(lbl_grp), run_time=0.6)
        self.wait(0.4)

        overlap = Rectangle(width=3.0, height=2.0, color=AMBER, stroke_width=2.0)
        overlap.set_fill(AMBER, opacity=0.12)
        overlap.move_to((img_rect.get_center() + lbl_rect.get_center()) / 2)
        ov_lbl = caption("intersection", size=12, color=AMBER)
        ov_lbl.next_to(overlap, UP, buff=0.06)
        self.play(FadeIn(overlap), FadeIn(ov_lbl), run_time=0.6)

        code = mono("dataset = imagery & labels", size=16, color=AMBER)
        code.next_to(VGroup(img_grp, lbl_grp), DOWN, buff=0.5)
        self.play(FadeIn(code), run_time=0.5)
        self.wait(0.5)

        rng = np.random.RandomState(7)
        patches = VGroup()
        for _ in range(4):
            px, py = rng.uniform(-1.2, 1.2), rng.uniform(-0.7, 0.7)
            patch = Square(side_length=0.5, color=AMBER, stroke_width=1.8)
            patch.set_fill(AMBER, opacity=0.18)
            patch.move_to(overlap.get_center() + RIGHT * px + UP * py)
            patches.add(patch)

        for p in patches:
            self.play(FadeIn(p), run_time=0.35)
        self.wait(0.3)

        loader_box = panel(2.2, 2.0, fill=SURFACE)
        loader_lbl = sans("DataLoader", size=18, color=AMBER)
        batch_lbl = caption("batch_size=16", size=12)
        loader_lbl.move_to(loader_box.get_center() + UP * 0.3)
        batch_lbl.next_to(loader_lbl, DOWN, buff=0.1)
        loader_all = VGroup(loader_box, loader_lbl, batch_lbl)
        loader_all.to_edge(RIGHT, buff=1.0)

        arr = Arrow(
            overlap.get_right(),
            loader_box.get_left(),
            color=AMBER,
            stroke_width=1.8,
            buff=0.15,
            max_tip_length_to_length_ratio=0.1,
        )
        self.play(FadeIn(loader_all), FadeIn(arr), run_time=0.6)
        self.wait(0.3)

        from manim import FadeOut

        self.play(
            *[p.animate.move_to(loader_box.get_center()) for p in patches],
            run_time=0.7,
        )
        self.play(*[FadeOut(p) for p in patches], run_time=0.3)

        train_box = panel(1.8, 1.0, fill=SURFACE)
        train_lbl = sans("Train", size=18, color=EARTH)
        train_lbl.move_to(train_box)
        train_grp = VGroup(train_box, train_lbl)
        train_grp.next_to(loader_all, DOWN, buff=0.4)
        arr2 = Arrow(
            loader_box.get_bottom(),
            train_box.get_top(),
            color=EARTH,
            stroke_width=1.8,
            buff=0.08,
            max_tip_length_to_length_ratio=0.12,
        )
        self.play(FadeIn(train_grp), FadeIn(arr2), run_time=0.5)
        self.wait(0.5)

        insight = caption("CRS + resolution + alignment = automatic", size=15, color=AMBER)
        insight.to_edge(DOWN, buff=0.45)
        self.play(FadeIn(insight), run_time=0.5)

        cleanup(self, hold=1.5)
