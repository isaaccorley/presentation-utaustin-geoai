"""UT Austin GeoAI Talk — Extended scenes S05–S17 (Isaac Corley)"""

import numpy as np
from manim import (
    DOWN,
    LEFT,
    RIGHT,
    UP,
    Arrow,
    FadeIn,
    Square,
    SurroundingRectangle,
    Text,
    VGroup,
)

from _theme import (
    AMBER,
    BG,
    BORDER,
    CORAL,
    DIM,
    EARTH,
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


class S09_MAEMaskedModeling(PacedScene):
    """MAE: mask patches, encoder + decoder side-by-side left-to-right."""

    def construct(self):
        self.camera.background_color = BG  # ty: ignore[invalid-assignment]
        tag = scene_tag("masked autoencoder", accent=AMBER)
        self.play(FadeIn(tag), run_time=0.6)

        rows, cols, cell = 6, 6, 0.42
        rng = np.random.RandomState(7)

        # Original satellite tile (far left)
        patches = satellite_tile(rows, cols, cell, seed=7)
        tile_border = SurroundingRectangle(patches, color=BORDER, stroke_width=1.5, buff=0.05)
        tile_lbl = caption("satellite tile", size=14, color=DIM)
        tile_lbl.next_to(tile_border, UP, buff=0.1)
        tile_grp = VGroup(patches, tile_border, tile_lbl)
        tile_grp.to_edge(LEFT, buff=0.55).shift(UP * 0.3)
        self.play(FadeIn(tile_grp), run_time=0.7)
        self.wait(0.4)
        row_y = tile_border.get_center()[1]

        # 75% masking overlay
        mask_indices = rng.choice(rows * cols, size=int(0.75 * rows * cols), replace=False)
        masks = VGroup()
        for idx in mask_indices:
            mask = Square(side_length=cell, color=CORAL, stroke_width=0)
            mask.set_fill(BG, opacity=0.92)
            m_txt = Text("?", font_size=14, color=DIM)
            m_txt.move_to(patches[idx])
            mask.move_to(patches[idx])
            masks.add(VGroup(mask, m_txt))

        mask_lbl = sans("75% masked", size=18, color=CORAL)
        mask_lbl.next_to(tile_border, DOWN, buff=0.2)
        self.play(*[FadeIn(m) for m in masks], FadeIn(mask_lbl), run_time=0.8)
        self.wait(0.5)

        # Encoder box (right of tile)
        enc_box = panel(1.8, 1.3, fill=SURFACE)
        enc_title = sans("Encoder", size=20, color=AMBER)
        enc_sub = caption("visible only", size=12)
        enc_title.move_to(enc_box.get_center() + UP * 0.2)
        enc_sub.next_to(enc_title, DOWN, buff=0.08)
        enc_grp = VGroup(enc_box, enc_title, enc_sub)
        enc_grp.next_to(tile_grp, RIGHT, buff=0.7)
        enc_grp.shift(UP * (row_y - enc_box.get_center()[1]))

        arr1 = Arrow(
            tile_border.get_right(),
            enc_box.get_left(),
            color=AMBER,
            stroke_width=1.8,
            buff=0.12,
            max_tip_length_to_length_ratio=0.1,
        )
        self.play(FadeIn(enc_grp), FadeIn(arr1), run_time=0.6)
        self.wait(0.3)

        # Decoder box (right of encoder)
        dec_box = panel(1.8, 1.3, fill=SURFACE)
        dec_title = sans("Decoder", size=20, color=AMBER)
        dec_sub = caption("reconstruct", size=12)
        dec_title.move_to(dec_box.get_center() + UP * 0.2)
        dec_sub.next_to(dec_title, DOWN, buff=0.08)
        dec_grp = VGroup(dec_box, dec_title, dec_sub)
        dec_grp.next_to(enc_grp, RIGHT, buff=0.7)
        dec_grp.shift(UP * (row_y - dec_box.get_center()[1]))

        arr2 = Arrow(
            enc_box.get_right(),
            dec_box.get_left(),
            color=AMBER,
            stroke_width=1.8,
            buff=0.12,
            max_tip_length_to_length_ratio=0.1,
        )
        self.play(FadeIn(dec_grp), FadeIn(arr2), run_time=0.6)
        self.wait(0.3)

        # Reconstructed tile (far right) — recolor masked patches green
        recon_tile = satellite_tile(rows, cols, cell, seed=7)
        for idx in mask_indices:
            recon_tile[idx].set_fill(EARTH, opacity=0.55)
        recon_border = SurroundingRectangle(recon_tile, color=EARTH, stroke_width=1.5, buff=0.05)
        recon_lbl = caption("reconstructed", size=14, color=EARTH)
        recon_lbl.next_to(recon_border, UP, buff=0.1)
        recon_grp = VGroup(recon_tile, recon_border, recon_lbl)
        recon_grp.next_to(dec_grp, RIGHT, buff=0.7)
        recon_grp.shift(UP * (row_y - recon_border.get_center()[1]))

        arr3 = Arrow(
            dec_box.get_right(),
            recon_border.get_left(),
            color=EARTH,
            stroke_width=1.8,
            buff=0.12,
            max_tip_length_to_length_ratio=0.1,
        )
        self.play(FadeIn(recon_grp, shift=RIGHT * 0.2), FadeIn(arr3), run_time=0.7)
        self.wait(0.4)

        chip = stat_chip(
            "Learn by reconstruction", "no labels needed — self-supervised", AMBER, width=5.5
        )
        chip.to_edge(DOWN, buff=0.35)
        self.play(FadeIn(chip, shift=UP * 0.15), run_time=0.6)
        cleanup(self, hold=1.5)
