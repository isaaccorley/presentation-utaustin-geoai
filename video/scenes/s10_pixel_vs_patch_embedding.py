"""UT Austin GeoAI Talk — Extended scenes S05–S17 (Isaac Corley)"""

from manim import (
    DOWN,
    ORIGIN,
    RIGHT,
    UP,
    Arrow,
    FadeIn,
    Rectangle,
    SurroundingRectangle,
    VGroup,
)

from _theme import (
    AMBER,
    BG,
    BORDER,
    CORAL,
    DIM,
    PERI,
    SURFACE,
    PacedScene,
    caption,
    cleanup,
    panel,
    sans,
    satellite_tile,
    scene_tag,
)


class S10_PixelVsPatchEmbedding(PacedScene):
    """Two parallel L-to-R pipelines: pixel vs patch embeddings."""

    def construct(self):
        self.camera.background_color = BG  # ty: ignore[invalid-assignment]
        tag = scene_tag("pixel vs patch embeddings", accent=CORAL)
        self.play(FadeIn(tag), run_time=0.6)

        cell = 0.35
        y_top = UP * 1.4  # pixel row
        y_bot = DOWN * 1.6  # patch row

        # ── helper: build one horizontal pipeline row ──
        def _pipeline_row(
            row_label,
            model_box_label,
            model_names,
            out_rows,
            out_cols,
            out_cell,
            out_count_str,
            out_desc,
            accent,
            y_anchor,
            tile_seed,
        ):
            # input tile
            inp = satellite_tile(6, 6, cell, seed=tile_seed)
            inp_b = SurroundingRectangle(inp, color=BORDER, stroke_width=1.5, buff=0.04)
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
                    bar = Rectangle(width=out_cell, height=out_cell, color=accent, stroke_width=0.8)
                    bar.set_fill(accent, opacity=0.15 + 0.04 * (r + c))
                    bar.move_to(RIGHT * c * out_cell + DOWN * r * out_cell)
                    out_bars.add(bar)
            out_bars.center()
            out_b = SurroundingRectangle(out_bars, color=accent, stroke_width=1.5, buff=0.04)
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
            a1 = Arrow(
                inp_b.get_right(),
                m_box.get_left(),
                color=accent,
                stroke_width=1.5,
                buff=0.08,
                max_tip_length_to_length_ratio=0.1,
            )
            a2 = Arrow(
                m_box.get_right(),
                out_b.get_left(),
                color=accent,
                stroke_width=1.5,
                buff=0.08,
                max_tip_length_to_length_ratio=0.1,
            )

            return VGroup(
                inp_grp,
                m_grp,
                out_grp,
                row_title,
                count_lbl,
                desc_lbl,
                models_lbl,
                a1,
                a2,
            )

        # ── TOP: pixel-level ──
        px_row = _pipeline_row(
            row_label="Pixel Embedding",
            model_box_label="Pixel Model",
            model_names="Presto, SatCLIP",
            out_rows=6,
            out_cols=6,
            out_cell=cell,
            out_count_str="36 vectors — one per pixel",
            out_desc="high spatial detail",
            accent=PERI,
            y_anchor=y_top,
            tile_seed=11,
        )
        self.play(FadeIn(px_row), run_time=0.8)
        self.wait(0.4)

        # ── BOTTOM: patch-level ──
        pa_row = _pipeline_row(
            row_label="Patch Embedding",
            model_box_label="Patch Model",
            model_names="SatMAE, Clay, DOFA",
            out_rows=3,
            out_cols=3,
            out_cell=cell * 2,
            out_count_str="9 vectors — one per patch",
            out_desc="richer semantics",
            accent=AMBER,
            y_anchor=y_bot,
            tile_seed=11,
        )
        self.play(FadeIn(pa_row), run_time=0.8)
        self.wait(0.5)

        cleanup(self, hold=1.5)
