"""UT Austin GeoAI Talk — Core scenes S01–S04 (Isaac Corley)"""

import random

import numpy as np
from manim import (
    DOWN,
    LEFT,
    RIGHT,
    UP,
    Arrow,
    DashedLine,
    FadeIn,
    Line,
    Rectangle,
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
    format_card,
    mini_grid,
    panel,
    sans,
    scene_tag,
    stat_chip,
)

random.seed(7)
np.random.seed(7)


class S01_CloudNativeStack(PacedScene):
    def construct(self):
        self.camera.background_color = BG  # ty: ignore[invalid-assignment]
        tag = scene_tag("the data stack", accent=PERI)
        self.play(FadeIn(tag), run_time=0.6)

        base = panel(11.0, 0.9, fill=PANEL2)
        base_lbl = sans("Object Storage", size=22, color=PERI)
        base_sub = caption("S3 / GCS / Azure Blob", size=14)
        base_lbl.move_to(base.get_center() + UP * 0.12)
        base_sub.next_to(base_lbl, DOWN, buff=0.08)
        base_grp = VGroup(base, base_lbl, base_sub)
        base_grp.to_edge(DOWN, buff=0.55)
        self.play(FadeIn(base_grp), run_time=0.7)
        self.wait(0.4)

        cog_icon = mini_grid(3, 4, 0.11, PERI, fill_color=PERI, fill_opacity=0.12)
        cog = format_card("COG", "Cloud-Optimized GeoTIFF", cog_icon, PERI, w=2.45, h=1.4)

        gp_cols = VGroup()
        for i in range(4):
            col = Rectangle(width=0.1, height=0.42, color=EARTH, stroke_width=0.8)
            col.set_fill(EARTH, opacity=0.15 + i * 0.07)
            gp_cols.add(col)
        gp_cols.arrange(RIGHT, buff=0.06)
        gpq = format_card("GeoParquet", "Columnar vectors", gp_cols, PERI, w=2.45, h=1.4)

        zarr_grid = mini_grid(2, 2, 0.18, AMBER, fill_color=AMBER, fill_opacity=0.12)
        depth = VGroup()
        for sq in zarr_grid[:2]:
            corner = sq.get_corner(UP + RIGHT)
            l1 = Line(corner, corner + RIGHT * 0.08 + UP * 0.08, color=AMBER, stroke_width=0.7)
            depth.add(l1)
        zarr_icon = VGroup(zarr_grid, depth)
        zarr = format_card("Zarr", "N-D arrays / chunks", zarr_icon, PERI, w=2.45, h=1.4)

        cards = VGroup(cog, gpq, zarr).arrange(RIGHT, buff=0.45)
        cards.next_to(base_grp, UP, buff=0.42)

        for card in [cog, gpq, zarr]:
            self.play(FadeIn(card, shift=UP * 0.3), run_time=0.55)
            self.wait(0.2)

        stac_panel = panel(8.5, 0.8, fill=SURFACE)
        stac_lbl = sans("STAC", size=22, color=PERI)
        stac_sub = caption("metadata catalog", size=13)
        stac_lbl.move_to(stac_panel.get_center() + UP * 0.1)
        stac_sub.next_to(stac_lbl, DOWN, buff=0.06)
        stac_grp = VGroup(stac_panel, stac_lbl, stac_sub)
        stac_grp.next_to(cards, UP, buff=0.35)
        self.play(FadeIn(stac_grp, shift=UP * 0.25), run_time=0.6)

        dashes = VGroup()
        for card in [cog, gpq, zarr]:
            d = DashedLine(
                stac_panel.get_bottom(),
                card[0].get_top(),
                color=DIM,
                stroke_width=1.0,
                dash_length=0.08,
            )
            dashes.add(d)
        self.play(FadeIn(dashes), run_time=0.5)
        self.wait(0.4)

        pm_icon = mini_grid(2, 3, 0.09, PERI, fill_color=PERI, fill_opacity=0.1)
        pm = format_card("PMTiles", "Tile serving", pm_icon, PERI, w=2.3, h=1.4)
        pm.next_to(cards, RIGHT, buff=0.55).align_to(cards, DOWN)
        self.play(FadeIn(pm, shift=RIGHT * 0.3), run_time=0.5)
        self.wait(0.3)

        arrows = VGroup()
        for t in [cog, gpq, zarr, pm]:
            start = base_grp[0].get_top()
            end = t[0].get_bottom()
            sx = np.array([end[0], start[1], 0.0])
            a = Arrow(
                sx,
                end,
                color=PERI,
                stroke_width=1.8,
                buff=0.08,
                max_tip_length_to_length_ratio=0.15,
            )
            arrows.add(a)
        self.play(FadeIn(arrows, shift=UP * 0.15), run_time=0.7)

        range_lbl = caption("HTTP range requests", size=14, color=PERI)
        range_lbl.next_to(arrows, LEFT, buff=0.3)
        range_lbl.shift(LEFT * 0.55)
        range_lbl.align_to(cards, DOWN)
        self.play(FadeIn(range_lbl), run_time=0.4)
        self.wait(0.6)

        chip = stat_chip(
            "No servers needed", "stream directly from object storage", PERI, width=5.5
        )
        chip.next_to(stac_grp, UP, buff=0.25)
        self.play(FadeIn(chip, shift=DOWN * 0.2), run_time=0.6)

        cleanup(self, hold=1.5)
