"""UT Austin GeoAI Talk — Extended scenes S05–S17 (Isaac Corley)"""
import numpy as np
from manim import (
    BOLD,
    DOWN,
    LEFT,
    ORIGIN,
    RIGHT,
    UP,
    ArcBetweenPoints,
    Arrow,
    Create,
    CurvedArrow,
    DashedLine,
    Dot,
    FadeIn,
    FadeOut,
    Line,
    Rectangle,
    ScaleInPlace,
    Square,
    SurroundingRectangle,
    Text,
    VGroup,
)
from _theme import (
    BG, SURFACE, PANEL2, BORDER, MOON, DIM, EARTH, CORAL, AMBER, PERI,
    mono, sans, caption, panel, scene_tag, stat_chip, cleanup,
    mini_grid, satellite_tile, PacedScene,
)


class S05_COGByteRange(PacedScene):
    """HTTP range requests pulling just the tiles you need from a COG."""

    def construct(self):
        self.camera.background_color = BG
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

        arr = Arrow(req_box.get_left(), highlight.get_right() + RIGHT * 0.3,
                    color=CORAL, stroke_width=2.0, buff=0.1,
                    max_tip_length_to_length_ratio=0.1)
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

        chip = stat_chip("Read 0.1% of the file",
                         "skip 99.9% — no full download", CORAL, width=5.5)
        chip.to_edge(DOWN, buff=0.4).to_edge(LEFT, buff=0.8)
        self.play(FadeIn(chip, shift=UP * 0.15), run_time=0.6)
        cleanup(self, hold=1.5)


class S06_STACSearchFanout(PacedScene):
    """STAC search fanning across catalogs, results streaming back."""

    def construct(self):
        self.camera.background_color = BG
        tag = scene_tag("stac search", accent=PERI)
        self.play(FadeIn(tag), run_time=0.6)

        q_box = panel(3.0, 2.0, fill=SURFACE)
        q_title = sans("Search", size=22, color=PERI)
        q_lines = VGroup(
            mono("bbox: Austin, TX", size=14, color=MOON),
            mono("date: 2024-01-06", size=14, color=MOON),
            mono("cloud < 20%", size=14, color=MOON),
        )
        q_lines.arrange(DOWN, buff=0.1, aligned_edge=LEFT)
        q_title.next_to(q_lines, UP, buff=0.2)
        VGroup(q_title, q_lines).move_to(q_box)
        q_grp = VGroup(q_box, q_title, q_lines).to_edge(LEFT, buff=0.6)
        self.play(FadeIn(q_grp), run_time=0.6)
        self.wait(0.3)

        catalogs = [
            ("Planetary\nComputer", PERI),
            ("Earth\nSearch", EARTH),
            ("USGS\nLandsatLook", AMBER),
        ]
        cat_grps = VGroup()
        for name, color in catalogs:
            box = panel(2.2, 1.4, fill=PANEL2)
            lbl = sans(name, size=16, color=color)
            lbl.move_to(box)
            cat_grps.add(VGroup(box, lbl))
        cat_grps.arrange(DOWN, buff=0.3).move_to(RIGHT * 1.5)

        arrows_out = VGroup()
        for cg in cat_grps:
            a = Arrow(q_box.get_right(), cg[0].get_left(),
                      color=PERI, stroke_width=1.5, buff=0.1,
                      max_tip_length_to_length_ratio=0.1)
            arrows_out.add(a)

        self.play(
            *[FadeIn(cg, shift=RIGHT * 0.3) for cg in cat_grps],
            *[FadeIn(a) for a in arrows_out],
            run_time=0.8,
        )
        self.wait(0.4)

        results_box = panel(3.0, 2.4, fill=SURFACE)
        results_box.to_edge(RIGHT, buff=0.6)
        r_title = sans("Results", size=20, color=EARTH)
        r_title.next_to(results_box, UP, buff=0.1)

        result_items = VGroup()
        for i in range(5):
            item = panel(2.5, 0.35, fill=PANEL2)
            t = mono(f"S2A_T14RQU_2024{i + 1:02d}...", size=11, color=MOON)
            t.move_to(item)
            result_items.add(VGroup(item, t))
        result_items.arrange(DOWN, buff=0.06).move_to(results_box)

        arrows_in = VGroup()
        for cg in cat_grps:
            a = Arrow(cg[0].get_right(), results_box.get_left(),
                      color=EARTH, stroke_width=1.5, buff=0.1,
                      max_tip_length_to_length_ratio=0.1)
            arrows_in.add(a)

        self.play(FadeIn(results_box), FadeIn(r_title),
                  *[FadeIn(a) for a in arrows_in], run_time=0.6)
        for item in result_items:
            self.play(FadeIn(item, shift=DOWN * 0.1), run_time=0.25)
        self.wait(0.4)

        chip = stat_chip("One query, many catalogs",
                         "federated search across providers", PERI, width=5.5)
        chip.to_edge(DOWN, buff=0.35).to_edge(LEFT, buff=0.6)
        self.play(FadeIn(chip, shift=UP * 0.15), run_time=0.6)
        cleanup(self, hold=1.5)


class S07_GeoParquetPushdown(PacedScene):
    """GeoParquet predicate pushdown: 2.6B rows → spatial filter → handful."""

    def construct(self):
        self.camera.background_color = BG
        tag = scene_tag("geoparquet at scale", accent=EARTH)
        self.play(FadeIn(tag), run_time=0.6)

        big_box = panel(3.5, 3.0, fill=PANEL2)
        big_lbl = sans("2.6B buildings", size=20, color=EARTH)
        big_sub = caption("Overture Maps on S3", size=13)
        big_lbl.move_to(big_box.get_center() + UP * 0.2)
        big_sub.next_to(big_lbl, DOWN, buff=0.1)

        row_groups = VGroup()
        for _ in range(6):
            rg = Rectangle(width=2.8, height=0.28, color=DIM, stroke_width=0.8)
            rg.set_fill(DIM, opacity=0.06)
            row_groups.add(rg)
        row_groups.arrange(DOWN, buff=0.04)
        row_groups.next_to(big_sub, DOWN, buff=0.2)
        rg_lbl = caption("row groups", size=10, color=DIM)
        rg_lbl.next_to(row_groups, DOWN, buff=0.06)

        big_grp = VGroup(big_box, big_lbl, big_sub, row_groups, rg_lbl)
        big_grp.to_edge(LEFT, buff=0.6)
        self.play(FadeIn(big_grp), run_time=0.7)
        self.wait(0.4)

        filter_box = panel(2.4, 1.6, fill=SURFACE)
        f_title = sans("Spatial Filter", size=18, color=AMBER)
        f_code = mono("bbox ∩ Austin", size=14, color=AMBER)
        f_title.move_to(filter_box.get_center() + UP * 0.2)
        f_code.next_to(f_title, DOWN, buff=0.12)
        filter_grp = VGroup(filter_box, f_title, f_code).move_to(ORIGIN)

        arr1 = Arrow(big_box.get_right(), filter_box.get_left(),
                     color=EARTH, stroke_width=2.0, buff=0.12,
                     max_tip_length_to_length_ratio=0.1)
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

        arr2 = Arrow(filter_box.get_right(), result_box.get_left(),
                     color=EARTH, stroke_width=2.0, buff=0.12,
                     max_tip_length_to_length_ratio=0.1)
        self.play(FadeIn(result_grp), FadeIn(arr2), run_time=0.6)
        self.wait(0.4)

        chip = stat_chip("Predicate pushdown",
                         "skip row groups → read only matching data", EARTH, width=5.5)
        chip.to_edge(DOWN, buff=0.35)
        self.play(FadeIn(chip, shift=UP * 0.15), run_time=0.6)
        cleanup(self, hold=1.5)


class S08_ContrastiveLearning(PacedScene):
    """Contrastive learning: positive pair pulled together, negative repelled."""

    def construct(self):
        self.camera.background_color = BG
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

        arr_a = Arrow(border_a.get_bottom(), enc_a.get_top(),
                      color=PERI, stroke_width=1.5, buff=0.08,
                      max_tip_length_to_length_ratio=0.12)
        arr_b = Arrow(border_b.get_bottom(), enc_b.get_top(),
                      color=EARTH, stroke_width=1.5, buff=0.08,
                      max_tip_length_to_length_ratio=0.12)
        self.play(FadeIn(enc_a), FadeIn(enc_a_lbl), FadeIn(enc_b), FadeIn(enc_b_lbl),
                  FadeIn(arr_a), FadeIn(arr_b), run_time=0.6)
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
            dot = Dot(space.get_center() + RIGHT * dx + UP * dy,
                      radius=0.05, color=DIM)
            dot.set_fill(DIM, opacity=0.3)
            bg_dots.add(dot)
        self.play(FadeIn(bg_dots), run_time=0.4)

        dot_a = Dot(space.get_center() + LEFT * 1.2 + UP * 0.8,
                    radius=0.1, color=PERI)
        dot_a.set_fill(PERI, opacity=0.9)
        tag_a = caption("z_A", size=12, color=PERI)
        tag_a.next_to(dot_a, UP, buff=0.06)

        dot_b = Dot(space.get_center() + RIGHT * 1.0 + DOWN * 0.6,
                    radius=0.1, color=EARTH)
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
        self.play(FadeIn(neg_lbl), neg_dot.animate.shift(RIGHT * 0.6 + DOWN * 0.4),
                  run_time=0.7)

        repel_lbl = sans("repel", size=18, color=CORAL)
        repel_lbl.next_to(neg_dot, DOWN, buff=0.15)
        self.play(FadeIn(repel_lbl), run_time=0.4)
        self.wait(0.4)

        chip = stat_chip("Learn by comparison",
                         "similar tiles close, different tiles far", PERI, width=5.5)
        chip.to_edge(DOWN, buff=0.35).to_edge(LEFT, buff=0.6)
        self.play(FadeIn(chip, shift=UP * 0.15), run_time=0.6)
        cleanup(self, hold=1.5)


class S09_MAEMaskedModeling(PacedScene):
    """MAE: mask patches, encoder + decoder side-by-side left-to-right."""

    def construct(self):
        self.camera.background_color = BG
        tag = scene_tag("masked autoencoder", accent=AMBER)
        self.play(FadeIn(tag), run_time=0.6)

        rows, cols, cell = 6, 6, 0.42
        rng = np.random.RandomState(7)

        # Original satellite tile (far left)
        patches = satellite_tile(rows, cols, cell, seed=7)
        tile_border = SurroundingRectangle(
            patches, color=BORDER, stroke_width=1.5, buff=0.05)
        tile_lbl = caption("satellite tile", size=14, color=DIM)
        tile_lbl.next_to(tile_border, UP, buff=0.1)
        tile_grp = VGroup(patches, tile_border, tile_lbl)
        tile_grp.to_edge(LEFT, buff=0.55).shift(UP * 0.3)
        self.play(FadeIn(tile_grp), run_time=0.7)
        self.wait(0.4)

        # 75% masking overlay
        mask_indices = rng.choice(
            rows * cols, size=int(0.75 * rows * cols), replace=False)
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
        enc_grp.next_to(tile_grp, RIGHT, buff=0.7).align_to(tile_grp, UP).shift(DOWN * 0.4)

        arr1 = Arrow(tile_border.get_right(), enc_box.get_left(),
                     color=AMBER, stroke_width=1.8, buff=0.12,
                     max_tip_length_to_length_ratio=0.1)
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

        arr2 = Arrow(enc_box.get_right(), dec_box.get_left(),
                     color=AMBER, stroke_width=1.8, buff=0.12,
                     max_tip_length_to_length_ratio=0.1)
        self.play(FadeIn(dec_grp), FadeIn(arr2), run_time=0.6)
        self.wait(0.3)

        # Reconstructed tile (far right) — recolor masked patches green
        recon_tile = satellite_tile(rows, cols, cell, seed=7)
        for idx in mask_indices:
            recon_tile[idx].set_fill(EARTH, opacity=0.55)
        recon_border = SurroundingRectangle(
            recon_tile, color=EARTH, stroke_width=1.5, buff=0.05)
        recon_lbl = caption("reconstructed", size=14, color=EARTH)
        recon_lbl.next_to(recon_border, UP, buff=0.1)
        recon_grp = VGroup(recon_tile, recon_border, recon_lbl)
        recon_grp.next_to(dec_grp, RIGHT, buff=0.7).align_to(enc_grp, UP)

        arr3 = Arrow(dec_box.get_right(), recon_border.get_left(),
                     color=EARTH, stroke_width=1.8, buff=0.12,
                     max_tip_length_to_length_ratio=0.1)
        self.play(FadeIn(recon_grp, shift=RIGHT * 0.2), FadeIn(arr3), run_time=0.7)
        self.wait(0.4)

        chip = stat_chip("Learn by reconstruction",
                         "no labels needed — self-supervised", AMBER, width=5.5)
        chip.to_edge(DOWN, buff=0.35)
        self.play(FadeIn(chip, shift=UP * 0.15), run_time=0.6)
        cleanup(self, hold=1.5)


class S10_PixelVsPatchEmbedding(PacedScene):
    """Two parallel L-to-R pipelines: pixel vs patch embeddings."""

    def construct(self):
        self.camera.background_color = BG
        tag = scene_tag("pixel vs patch embeddings", accent=CORAL)
        self.play(FadeIn(tag), run_time=0.6)

        cell = 0.35
        y_top = UP * 1.4   # pixel row
        y_bot = DOWN * 1.6  # patch row

        # ── helper: build one horizontal pipeline row ──
        def _pipeline_row(
            row_label, model_box_label, model_names,
            out_rows, out_cols, out_cell, out_count_str, out_desc,
            accent, y_anchor, tile_seed,
        ):
            # input tile
            inp = satellite_tile(6, 6, cell, seed=tile_seed)
            inp_b = SurroundingRectangle(
                inp, color=BORDER, stroke_width=1.5, buff=0.04)
            inp_grp = VGroup(inp, inp_b)

            # model box
            m_box = panel(2.0, 1.2, fill=SURFACE)
            m_lbl = sans(model_box_label, size=18, color=accent)
            m_lbl.move_to(m_box)
            m_grp = VGroup(m_box, m_lbl)

            # output embedding grid (colored bars arranged as grid)
            out_bars = VGroup()
            for r in range(out_rows):
                for c in range(out_cols):
                    bar = Rectangle(
                        width=out_cell, height=out_cell,
                        color=accent, stroke_width=0.8)
                    bar.set_fill(accent, opacity=0.15 + 0.04 * (r + c))
                    bar.move_to(RIGHT * c * out_cell + DOWN * r * out_cell)
                    out_bars.add(bar)
            out_bars.center()
            out_b = SurroundingRectangle(
                out_bars, color=accent, stroke_width=1.5, buff=0.04)
            out_grp = VGroup(out_bars, out_b)

            # arrange L → R
            row_grp = VGroup(inp_grp, m_grp, out_grp).arrange(RIGHT, buff=0.6)
            row_grp.move_to(ORIGIN).shift(y_anchor)

            # labels
            row_title = sans(row_label, size=18, color=accent)
            row_title.next_to(inp_grp, UP, buff=0.12)
            count_lbl = caption(out_count_str, size=12, color=accent)
            count_lbl.next_to(out_grp, DOWN, buff=0.08)
            desc_lbl = caption(out_desc, size=11, color=DIM)
            desc_lbl.next_to(count_lbl, DOWN, buff=0.04)
            models_lbl = caption(model_names, size=12, color=accent)
            models_lbl.next_to(m_grp, DOWN, buff=0.08)

            # arrows
            a1 = Arrow(inp_b.get_right(), m_box.get_left(),
                       color=accent, stroke_width=1.5, buff=0.08,
                       max_tip_length_to_length_ratio=0.1)
            a2 = Arrow(m_box.get_right(), out_b.get_left(),
                       color=accent, stroke_width=1.5, buff=0.08,
                       max_tip_length_to_length_ratio=0.1)

            return VGroup(
                inp_grp, m_grp, out_grp,
                row_title, count_lbl, desc_lbl, models_lbl,
                a1, a2,
            )

        # ── TOP: pixel-level ──
        px_row = _pipeline_row(
            row_label="Pixel Embedding",
            model_box_label="Pixel Model",
            model_names="Presto, SatCLIP",
            out_rows=6, out_cols=6, out_cell=cell,
            out_count_str="36 vectors — one per pixel",
            out_desc="high spatial detail",
            accent=PERI, y_anchor=y_top, tile_seed=11,
        )
        self.play(FadeIn(px_row), run_time=0.8)
        self.wait(0.4)

        # ── BOTTOM: patch-level ──
        pa_row = _pipeline_row(
            row_label="Patch Embedding",
            model_box_label="Patch Model",
            model_names="SatMAE, Clay, DOFA",
            out_rows=3, out_cols=3, out_cell=cell * 2,
            out_count_str="9 vectors — one per patch",
            out_desc="richer semantics",
            accent=AMBER, y_anchor=y_bot, tile_seed=11,
        )
        self.play(FadeIn(pa_row), run_time=0.8)
        self.wait(0.5)

        cleanup(self, hold=1.5)


class S11_PRUEPipeline(PacedScene):
    """PRUE: Field boundary segmentation at global scale."""

    def construct(self):
        self.camera.background_color = BG
        tag = scene_tag("field boundary segmentation", accent=EARTH)
        self.play(FadeIn(tag), run_time=0.6)

        title = sans("PRUE", size=32, color=EARTH)
        subtitle = caption(
            "Practical Recipe for Field Boundary Segmentation at Scale",
            size=15, color=DIM,
        )
        subtitle.next_to(title, DOWN, buff=0.1)
        VGroup(title, subtitle).to_edge(UP, buff=0.8)
        self.play(FadeIn(title), FadeIn(subtitle), run_time=0.6)
        self.wait(0.3)

        stages = [
            ("Sentinel-2\nImagery", PERI),
            ("Tile\n256 px", AMBER),
            ("U-Net", EARTH),
            ("Merge\nPolygons", CORAL),
            ("Global\nMosaic", EARTH),
        ]
        stage_grps = VGroup()
        for name, color in stages:
            box = panel(2.0, 1.4, fill=SURFACE)
            lbl = sans(name, size=16, color=color)
            lbl.move_to(box)
            stage_grps.add(VGroup(box, lbl))
        stage_grps.arrange(RIGHT, buff=0.4).move_to(ORIGIN + DOWN * 0.2)

        for i, sg in enumerate(stage_grps):
            self.play(FadeIn(sg, shift=RIGHT * 0.2), run_time=0.45)
            if i < len(stage_grps) - 1:
                arr = Arrow(
                    sg[0].get_right(), stage_grps[i + 1][0].get_left(),
                    color=stages[i][1], stroke_width=1.8, buff=0.08,
                    max_tip_length_to_length_ratio=0.1,
                )
                self.play(FadeIn(arr), run_time=0.25)
        self.wait(0.4)

        soon = panel(4.5, 0.6, fill=CORAL, stroke=CORAL)
        soon_lbl = sans("Global predictions — coming soon", size=16, color=BG)
        soon_lbl.move_to(soon)
        soon_grp = VGroup(soon, soon_lbl)
        soon_grp.next_to(stage_grps, DOWN, buff=0.5)

        stats = VGroup(
            stat_chip("76% IoU", "field boundary accuracy", EARTH, width=3.0, height=1.3),
            stat_chip("18 models", "evaluated on FTW", PERI, width=3.0, height=1.3),
            stat_chip("5 countries", "models released", AMBER, width=3.0, height=1.3),
        )
        stats.arrange(RIGHT, buff=0.3)
        stats.next_to(soon_grp, DOWN, buff=0.3)
        self.play(FadeIn(soon_grp), run_time=0.5)
        cleanup(self, hold=2.0)


class S12_CloudNativeVsDownload(PacedScene):
    """Split-screen: download everything (old) vs cloud-native streaming (new)."""

    def construct(self):
        self.camera.background_color = BG
        tag = scene_tag("old way vs new way", accent=CORAL)
        self.play(FadeIn(tag), run_time=0.6)

        divider = DashedLine(UP * 3.2, DOWN * 3.2, color=DIM,
                             stroke_width=1.0, dash_length=0.12)
        self.play(FadeIn(divider), run_time=0.4)

        # LEFT: old way
        old_title = sans("Download Everything", size=20, color=CORAL)
        old_title.to_edge(LEFT, buff=1.2).to_edge(UP, buff=1.2)

        cloud = panel(2.5, 1.0, fill=PANEL2)
        cloud_lbl = caption("Cloud Storage", size=13, color=DIM)
        cloud_lbl.move_to(cloud)
        cloud.next_to(old_title, DOWN, buff=0.4)

        disk = panel(2.5, 1.0, fill=SURFACE)
        disk_lbl = caption("Local Disk", size=13, color=CORAL)
        disk_lbl.move_to(disk)
        disk.next_to(cloud, DOWN, buff=1.0)

        big_arr = Arrow(cloud.get_bottom(), disk.get_top(),
                        color=CORAL, stroke_width=3.0, buff=0.08,
                        max_tip_length_to_length_ratio=0.08)
        dl_size = mono("47 GB", size=18, color=CORAL)
        dl_size.next_to(big_arr, RIGHT, buff=0.15)

        old_steps = VGroup(
            caption("1. download full scene", size=12, color=MOON),
            caption("2. convert format", size=12, color=MOON),
            caption("3. clip to AOI", size=12, color=MOON),
            caption("4. load into memory", size=12, color=MOON),
        )
        old_steps.arrange(DOWN, buff=0.06, aligned_edge=LEFT)
        old_steps.next_to(disk, DOWN, buff=0.3)
        old_time = mono("~45 min", size=16, color=CORAL)
        old_time.next_to(old_steps, DOWN, buff=0.2)

        self.play(FadeIn(old_title), run_time=0.3)
        self.play(FadeIn(cloud), FadeIn(cloud_lbl), run_time=0.3)
        self.play(FadeIn(big_arr), FadeIn(dl_size), run_time=0.4)
        self.play(FadeIn(disk), FadeIn(disk_lbl), run_time=0.3)
        self.play(FadeIn(old_steps), FadeIn(old_time), run_time=0.5)
        self.wait(0.3)

        # RIGHT: new way
        new_title = sans("Stream What You Need", size=20, color=EARTH)
        new_title.to_edge(RIGHT, buff=1.0).to_edge(UP, buff=1.2)

        cloud2 = panel(2.5, 1.0, fill=PANEL2)
        cloud2_lbl = caption("COG on S3", size=13, color=PERI)
        cloud2_lbl.move_to(cloud2)
        cloud2.next_to(new_title, DOWN, buff=0.4)

        mem = panel(2.5, 1.0, fill=SURFACE)
        mem_lbl = caption("In-Memory Array", size=13, color=EARTH)
        mem_lbl.move_to(mem)
        mem.next_to(cloud2, DOWN, buff=1.0)

        thin_arr = Arrow(cloud2.get_bottom(), mem.get_top(),
                         color=EARTH, stroke_width=1.5, buff=0.08,
                         max_tip_length_to_length_ratio=0.1)
        dl_size2 = mono("12 MB", size=18, color=EARTH)
        dl_size2.next_to(thin_arr, LEFT, buff=0.15)

        new_steps = VGroup(
            caption("1. range-read AOI tiles", size=12, color=MOON),
            caption("2. decode in memory", size=12, color=MOON),
            caption("3. ready for analysis", size=12, color=MOON),
        )
        new_steps.arrange(DOWN, buff=0.06, aligned_edge=LEFT)
        new_steps.next_to(mem, DOWN, buff=0.3)
        new_time = mono("~3 sec", size=16, color=EARTH)
        new_time.next_to(new_steps, DOWN, buff=0.2)

        self.play(FadeIn(new_title), run_time=0.3)
        self.play(FadeIn(cloud2), FadeIn(cloud2_lbl), run_time=0.3)
        self.play(FadeIn(thin_arr), FadeIn(dl_size2), run_time=0.4)
        self.play(FadeIn(mem), FadeIn(mem_lbl), run_time=0.3)
        self.play(FadeIn(new_steps), FadeIn(new_time), run_time=0.5)
        self.wait(0.5)

        chip = stat_chip("900× faster",
                         "stream only the bytes you need", EARTH, width=4.5)
        chip.to_edge(DOWN, buff=0.3).to_edge(RIGHT, buff=0.8)
        self.play(FadeIn(chip, shift=UP * 0.15), run_time=0.6)
        cleanup(self, hold=2.0)


class S13_ProductionPipeline(PacedScene):
    """Post-processing + productionization: model output is just the start."""

    def construct(self):
        self.camera.background_color = BG
        tag = scene_tag("production pipeline", accent=CORAL)
        self.play(FadeIn(tag), run_time=0.6)

        title = sans("After Inference", size=28, color=CORAL)
        title.to_edge(UP, buff=0.85).to_edge(LEFT, buff=0.9)
        self.play(FadeIn(title), run_time=0.5)

        # ── Row 1: Post-processing ──
        post_steps = [
            ("Patch\nExtraction", PERI),
            ("Distributed\nInference", PERI),
            ("Overlap\nMerging", AMBER),
            ("Binary\nMorphology", AMBER),
            ("Land Cover\nFilter", EARTH),
            ("Polygonize", EARTH),
            ("Area/Vertex\nFilter", EARTH),
        ]
        row1_lbl = sans("Post-processing", size=18, color=AMBER)
        row1_lbl.next_to(title, DOWN, buff=0.35).to_edge(LEFT, buff=0.9)
        self.play(FadeIn(row1_lbl), run_time=0.3)

        row1_boxes = VGroup()
        for name, color in post_steps:
            box = panel(1.5, 1.0, fill=SURFACE)
            lbl = sans(name, size=12, color=color)
            if lbl.width > box.width - 0.15:
                lbl.scale((box.width - 0.15) / lbl.width)
            lbl.move_to(box)
            row1_boxes.add(VGroup(box, lbl))
        row1_boxes.arrange(RIGHT, buff=0.22)
        row1_boxes.next_to(row1_lbl, DOWN, buff=0.2)
        # scale to fit frame width
        if row1_boxes.width > 12.0:
            row1_boxes.scale(12.0 / row1_boxes.width)

        row1_arrows = VGroup()
        for i in range(len(row1_boxes) - 1):
            a = Arrow(
                row1_boxes[i][0].get_right(),
                row1_boxes[i + 1][0].get_left(),
                color=DIM, stroke_width=1.2, buff=0.04,
                max_tip_length_to_length_ratio=0.15,
            )
            row1_arrows.add(a)

        for i, bx in enumerate(row1_boxes):
            anims = [FadeIn(bx, shift=RIGHT * 0.15)]
            if i > 0:
                anims.append(FadeIn(row1_arrows[i - 1]))
            self.play(*anims, run_time=0.3)
        self.wait(0.4)

        # ── Row 2: Productionization ──
        prod_steps = [
            ("Spatial\nPartition", PERI),
            ("Quantize", PERI),
            ("STAC\nCatalog", AMBER),
            ("COG\nOverviews", AMBER),
            ("PMTiles", CORAL),
        ]
        row2_lbl = sans("Productionization", size=18, color=CORAL)
        row2_lbl.next_to(row1_boxes, DOWN, buff=0.45).to_edge(LEFT, buff=0.9)
        self.play(FadeIn(row2_lbl), run_time=0.3)

        row2_boxes = VGroup()
        for name, color in prod_steps:
            box = panel(1.8, 1.0, fill=SURFACE)
            lbl = sans(name, size=12, color=color)
            if lbl.width > box.width - 0.15:
                lbl.scale((box.width - 0.15) / lbl.width)
            lbl.move_to(box)
            row2_boxes.add(VGroup(box, lbl))
        row2_boxes.arrange(RIGHT, buff=0.3)
        row2_boxes.next_to(row2_lbl, DOWN, buff=0.2)
        if row2_boxes.width > 12.0:
            row2_boxes.scale(12.0 / row2_boxes.width)

        row2_arrows = VGroup()
        for i in range(len(row2_boxes) - 1):
            a = Arrow(
                row2_boxes[i][0].get_right(),
                row2_boxes[i + 1][0].get_left(),
                color=DIM, stroke_width=1.2, buff=0.04,
                max_tip_length_to_length_ratio=0.15,
            )
            row2_arrows.add(a)

        for i, bx in enumerate(row2_boxes):
            anims = [FadeIn(bx, shift=RIGHT * 0.15)]
            if i > 0:
                anims.append(FadeIn(row2_arrows[i - 1]))
            self.play(*anims, run_time=0.3)
        self.wait(0.4)

        # Connecting arrow between rows (center of row1 down to center of row2)
        bridge = Arrow(
            row1_boxes.get_bottom(),
            row2_boxes.get_top(),
            color=CORAL, stroke_width=2.0, buff=0.08,
            max_tip_length_to_length_ratio=0.1,
        )
        self.play(FadeIn(bridge), run_time=0.4)

        # Takeaway chip
        chip = stat_chip(
            "The extra mile",
            "separates production from prototype",
            CORAL, width=5.5,
        )
        chip.to_edge(DOWN, buff=0.3)
        self.play(FadeIn(chip, shift=UP * 0.15), run_time=0.6)
        cleanup(self, hold=2.0)


# ── S14: Cloud-Native Geospatial Timeline ────────────────────────────────


class S14_CNGTimeline(PacedScene):
    """Horizontal timeline showing the evolution of CNG formats 2015-2025."""

    def construct(self):
        self.camera.background_color = BG
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
            dot = Dot(point=[x, line.get_y(), 0], radius=0.06, color=accent)
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
                color=BORDER, stroke_width=1,
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


# ── S15: Foundation Model Comparison ─────────────────────────────────────


class S15_GeoFMComparison(PacedScene):
    """Table comparing 8 geospatial foundation models, built row by row."""

    def construct(self):
        self.camera.background_color = BG
        tag = scene_tag("foundation model landscape", accent=EARTH)
        self.play(FadeIn(tag), run_time=0.6)

        # Column definitions: (header, width)
        cols = [
            ("Model", 1.8),
            ("Architecture", 1.8),
            ("Params", 1.5),
            ("Pretraining Data", 2.0),
            ("Year", 0.9),
        ]
        col_widths = [c[1] for c in cols]
        total_w = sum(col_widths) + 0.3 * (len(cols) - 1)

        # Row data: (model, arch, params, data, year, accent)
        rows = [
            ("Prithvi 2.0", "ViT-MAE", "300–600M", "4.2M HLS", "2024", EARTH),
            ("Clay 1.5", "ViT+DINOv2", "632M", "70M multi-sensor", "2024", EARTH),
            ("SatMAE", "ViT-L MAE", "~304M", "363K fMoW", "2022", EARTH),
            ("Scale-MAE", "ViT-L MAE", "~323M", "363K fMoW", "2023", EARTH),
            ("DOFA", "ViT+Hypernetwork", "86–304M", "8M 5-sensor", "2024", EARTH),
            ("SatCLIP", "ViT+Siren", "256-dim", "100K S2", "2024", AMBER),
            ("GeoCLIP", "CLIP ViT-L/14", "314M", "4.7M Flickr", "2023", AMBER),
            ("Presto", "Transformer", "402K", "21.5M pixels", "2023", CORAL),
        ]

        def make_row(cells, is_header=False):
            """Build a row as a VGroup of text cells in panel backgrounds."""
            items = VGroup()
            x = -total_w / 2
            for j, (text, w) in enumerate(zip(cells, col_widths)):
                bg = panel(w, 0.48, fill=PANEL2 if is_header else SURFACE)
                if is_header:
                    lbl = sans(text, size=12, color=PERI)
                else:
                    lbl = mono(text, size=11, color=MOON)
                if lbl.width > w - 0.15:
                    lbl.scale((w - 0.15) / lbl.width)
                lbl.move_to(bg)
                bg.move_to([x + w / 2, 0, 0])
                items.add(VGroup(bg, lbl))
                x += w + 0.3
            return items

        # Header
        header = make_row([c[0] for c in cols], is_header=True)
        header.move_to(UP * 3.0)
        self.play(FadeIn(header), run_time=0.4)

        # Data rows
        row_groups = []
        for i, (model, arch, params, data, year, accent) in enumerate(rows):
            row = make_row([model, arch, params, data, year])
            # Color the model name cell with accent
            row[0][1].set_color(accent)
            row.move_to(UP * (3.0 - (i + 1) * 0.52))
            row_groups.append(row)
            self.play(FadeIn(row, shift=RIGHT * 0.15), run_time=0.25)

        self.wait(0.4)

        # Highlight Presto (smallest) and Clay (largest)
        presto_rect = SurroundingRectangle(
            row_groups[7], color=CORAL, stroke_width=2, buff=0.04,
        )
        clay_rect = SurroundingRectangle(
            row_groups[1], color=EARTH, stroke_width=2, buff=0.04,
        )
        self.play(Create(presto_rect), Create(clay_rect), run_time=0.5)
        self.wait(0.6)
        self.play(FadeOut(presto_rect), FadeOut(clay_rect), run_time=0.3)

        chip = stat_chip("8 models, no single winner", "GEO-Bench 2024", CORAL, width=5.5)
        chip.to_edge(DOWN, buff=0.35)
        self.play(FadeIn(chip, shift=UP * 0.15), run_time=0.6)
        cleanup(self, hold=2.0)


# ── S16: The Flywheel ────────────────────────────────────────────────────


class S16_Flywheel(PacedScene):
    """Animated cycle diagram: People → Models → Global Datasets → People."""

    def construct(self):
        self.camera.background_color = BG
        tag = scene_tag("the flywheel", accent=AMBER)
        self.play(FadeIn(tag), run_time=0.6)

        # Three nodes in triangle
        top_pos = UP * 1.8
        bl_pos = DOWN * 1.2 + LEFT * 2.8
        br_pos = DOWN * 1.2 + RIGHT * 2.8

        def make_node(label, accent, pos, w=2.8):
            bg = panel(w, 1.0, fill=SURFACE)
            lbl = sans(label, size=24, color=accent)
            if lbl.width > bg.width - 0.3:
                lbl.scale((bg.width - 0.3) / lbl.width)
            lbl.move_to(bg)
            node = VGroup(bg, lbl)
            node.move_to(pos)
            return node

        people = make_node("People", CORAL, top_pos)
        models = make_node("Models", PERI, bl_pos)
        datasets = make_node("Global Datasets", EARTH, br_pos, w=3.2)

        self.play(FadeIn(people), FadeIn(models), FadeIn(datasets), run_time=0.6)
        self.wait(0.3)

        # Curved arrows between nodes
        def curved_arrow(start_node, end_node, label_text, angle=0.6):
            start = start_node[0].get_edge_center(
                (end_node.get_center() - start_node.get_center())
            )
            end = end_node[0].get_edge_center(
                (start_node.get_center() - end_node.get_center())
            )
            arrow = CurvedArrow(
                start, end,
                color=DIM, stroke_width=2.0,
                angle=angle,
            )
            lbl = caption(label_text, size=14)
            lbl.move_to(arrow.point_from_proportion(0.5) + UP * 0.25)
            return VGroup(arrow, lbl)

        # People → Models (left side, going down)
        a1_start = people[0].get_bottom() + LEFT * 0.6
        a1_end = models[0].get_top() + RIGHT * 0.4
        a1 = CurvedArrow(a1_start, a1_end, color=DIM, stroke_width=2.0, angle=-0.5)
        a1_lbl = caption("train", size=15)
        a1_lbl.move_to(a1.point_from_proportion(0.5) + LEFT * 0.45)

        # Models → Datasets (bottom, going right)
        a2_start = models[0].get_right() + DOWN * 0.1
        a2_end = datasets[0].get_left() + DOWN * 0.1
        a2 = CurvedArrow(a2_start, a2_end, color=DIM, stroke_width=2.0, angle=-0.5)
        a2_lbl = caption("produce", size=15)
        a2_lbl.move_to(a2.point_from_proportion(0.5) + DOWN * 0.45)

        # Datasets → People (right side, going up)
        a3_start = datasets[0].get_top() + RIGHT * 0.6
        a3_end = people[0].get_bottom() + RIGHT * 0.6
        a3 = CurvedArrow(a3_start, a3_end, color=DIM, stroke_width=2.0, angle=-0.5)
        a3_lbl = caption("inspire", size=15)
        a3_lbl.move_to(a3.point_from_proportion(0.5) + RIGHT * 0.45)

        self.play(Create(a1), FadeIn(a1_lbl), run_time=0.5)
        self.play(Create(a2), FadeIn(a2_lbl), run_time=0.5)
        self.play(Create(a3), FadeIn(a3_lbl), run_time=0.5)
        self.wait(0.3)

        # Pulse arrows to suggest continuous cycle
        arrows = VGroup(a1, a2, a3)
        self.play(ScaleInPlace(arrows, 1.06), run_time=0.3)
        self.play(ScaleInPlace(arrows, 1 / 1.06), run_time=0.3)
        self.play(ScaleInPlace(arrows, 1.06), run_time=0.3)
        self.play(ScaleInPlace(arrows, 1 / 1.06), run_time=0.3)

        chip = stat_chip("The Flywheel", "data → models → people → data", AMBER, width=5.5)
        chip.to_edge(DOWN, buff=0.25)
        self.play(FadeIn(chip, shift=UP * 0.15), run_time=0.6)
        cleanup(self, hold=2.0)


# ── S17: 80/20 Transition ───────────────────────────────────────────────


class S17_EightyTwenty(PacedScene):
    """Punchy stat slide: 80/20 — model vs pipeline."""

    def construct(self):
        self.camera.background_color = BG
        tag = scene_tag("the reality", accent=CORAL)
        self.play(FadeIn(tag), run_time=0.6)

        big = sans("80 / 20", size=96, color=CORAL)
        big.move_to(UP * 0.6)
        self.play(FadeIn(big), run_time=0.7)
        self.wait(0.8)

        line1 = sans("Model is 20% of the work.", size=28, color=MOON)
        line1.next_to(big, DOWN, buff=0.5)
        self.play(FadeIn(line1, shift=UP * 0.2), run_time=0.5)
        self.wait(0.5)

        line2 = sans("Pipeline is the other 80%.", size=28, color=MOON)
        line2.next_to(line1, DOWN, buff=0.3)
        self.play(FadeIn(line2, shift=UP * 0.2), run_time=0.5)

        cleanup(self, hold=2.5)
