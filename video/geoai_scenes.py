"""UT Austin GeoAI Talk — Cloud-Native Geospatial & GeoAI Pipelines (Isaac Corley)"""
import random
import numpy as np
from manim import (
    BOLD,
    DOWN,
    LEFT,
    NORMAL,
    RIGHT,
    UP,
    Arrow,
    DashedLine,
    Dot,
    FadeIn,
    FadeOut,
    Group,
    Line,
    Rectangle,
    RoundedRectangle,
    Scene,
    Square,
    Text,
    VGroup,
    config,
)

BG      = "#F4F4EB"
SURFACE = "#EAEADE"
PANEL2  = "#DFDFD4"
BORDER  = "#C8C2B2"

MOON    = "#3B1E1C"
DIM     = "#8F7F73"

EARTH   = "#1E5B46"
CORAL   = "#BE3E1F"
AMBER   = "#C96A1E"
PERI    = "#4A6BA8"

MONO = "Menlo"
SANS = "Space Grotesk"

config.background_color = BG

random.seed(7)
np.random.seed(7)

def mono(text, size=28, color=MOON, weight=NORMAL):
    return Text(text, font=MONO, font_size=size, color=color, weight=weight)

def sans(text, size=42, color=MOON, weight=BOLD):
    return Text(text, font=SANS, font_size=size, color=color, weight=weight)

def caption(text, color=DIM, size=18):
    return mono(text, size=size, color=color)

def panel(width, height, radius=0.22, fill=SURFACE, stroke=BORDER, stroke_width=1.2):
    return RoundedRectangle(
        width=width, height=height, corner_radius=radius,
        color=stroke, stroke_width=stroke_width,
        fill_color=fill, fill_opacity=1.0,
    )

def scene_tag(text_str, accent=CORAL):
    tag = caption(text_str, color=DIM).to_edge(UP, buff=0.7)
    bar = Line(LEFT * 0.4, RIGHT * 0.4, color=accent, stroke_width=3)
    bar.next_to(tag, LEFT, buff=0.3)
    g = VGroup(bar, tag)
    g.to_edge(LEFT, buff=0.9).to_edge(UP, buff=0.7)
    return g

def stat_chip(headline, sub, color, width=4.2, height=1.9):
    card = panel(width, height, radius=0.22, fill=SURFACE, stroke=BORDER)
    h = sans(headline, size=28, color=color, weight=BOLD)
    s = caption(sub, color=DIM)
    if h.width > card.width - 0.4:
        h.scale((card.width - 0.4) / h.width)
    if s.width > card.width - 0.5:
        s.scale((card.width - 0.5) / s.width)
    h.move_to(card.get_center() + UP * 0.26)
    s.move_to(card.get_center() + DOWN * 0.38)
    return VGroup(card, h, s)

def cleanup(scene, hold=1.0):
    scene.wait(hold)
    scene.play(FadeOut(Group(*scene.mobjects)), run_time=0.6)

def _mini_grid(rows, cols, cell, color, fill_color=None, fill_opacity=0.15):
    squares = VGroup()
    for r in range(rows):
        for c in range(cols):
            sq = Square(side_length=cell, color=color, stroke_width=0.8)
            if fill_color:
                sq.set_fill(fill_color, opacity=fill_opacity)
            sq.move_to(RIGHT * c * cell + DOWN * r * cell)
            squares.add(sq)
    squares.center()
    return squares

def _format_card(name, desc, icon_mob, accent, w=2.8, h=1.5):
    card = panel(w, h, fill=SURFACE)
    n = sans(name, size=22, color=accent, weight=BOLD)
    d = caption(desc, size=13)
    if d.width > w - 0.3:
        d.scale((w - 0.3) / d.width)
    n.move_to(card.get_top() + DOWN * 0.35)
    d.next_to(n, DOWN, buff=0.12)
    icon_mob.scale_to_fit_width(min(0.7, w - 0.4))
    icon_mob.next_to(d, DOWN, buff=0.15)
    return VGroup(card, n, d, icon_mob)

class S01_CloudNativeStack(Scene):
    def construct(self):
        self.camera.background_color = BG
        tag = scene_tag("the data stack", accent=PERI)
        self.play(FadeIn(tag), run_time=0.6)

        base = panel(11.0, 0.9, fill=PANEL2)
        base_lbl = sans("Object Storage", size=22, color=PERI, weight=BOLD)
        base_sub = caption("S3 / GCS / Azure Blob", size=14)
        base_lbl.move_to(base.get_center() + UP * 0.12)
        base_sub.next_to(base_lbl, DOWN, buff=0.08)
        base_grp = VGroup(base, base_lbl, base_sub)
        base_grp.to_edge(DOWN, buff=0.55)
        self.play(FadeIn(base_grp), run_time=0.7)
        self.wait(0.4)

        cog_icon = _mini_grid(3, 4, 0.13, PERI, fill_color=PERI, fill_opacity=0.12)
        cog = _format_card("COG", "Cloud-Optimized GeoTIFF", cog_icon, PERI, w=2.6, h=1.4)

        gp_cols = VGroup()
        for i in range(4):
            col = Rectangle(width=0.12, height=0.5, color=EARTH, stroke_width=0.8)
            col.set_fill(EARTH, opacity=0.15 + i * 0.07)
            gp_cols.add(col)
        gp_cols.arrange(RIGHT, buff=0.06)
        gpq = _format_card("GeoParquet", "Columnar vectors", gp_cols, PERI, w=2.6, h=1.4)

        zarr_grid = _mini_grid(2, 2, 0.22, AMBER, fill_color=AMBER, fill_opacity=0.12)
        depth = VGroup()
        for sq in zarr_grid[:2]:
            corner = sq.get_corner(UP + RIGHT)
            l1 = Line(corner, corner + RIGHT * 0.08 + UP * 0.08, color=AMBER, stroke_width=0.7)
            depth.add(l1)
        zarr_icon = VGroup(zarr_grid, depth)
        zarr = _format_card("Zarr", "N-D arrays / chunks", zarr_icon, PERI, w=2.6, h=1.4)

        cards = VGroup(cog, gpq, zarr).arrange(RIGHT, buff=0.35)
        cards.next_to(base_grp, UP, buff=0.3)

        for card in [cog, gpq, zarr]:
            self.play(FadeIn(card, shift=UP * 0.3), run_time=0.55)
            self.wait(0.2)

        stac_panel = panel(8.5, 0.8, fill=SURFACE)
        stac_lbl = sans("STAC", size=22, color=PERI, weight=BOLD)
        stac_sub = caption("metadata catalog", size=13)
        stac_lbl.move_to(stac_panel.get_center() + UP * 0.1)
        stac_sub.next_to(stac_lbl, DOWN, buff=0.06)
        stac_grp = VGroup(stac_panel, stac_lbl, stac_sub)
        stac_grp.next_to(cards, UP, buff=0.3)
        self.play(FadeIn(stac_grp, shift=UP * 0.25), run_time=0.6)

        dashes = VGroup()
        for card in [cog, gpq, zarr]:
            d = DashedLine(
                stac_panel.get_bottom(),
                card[0].get_top(),
                color=DIM, stroke_width=1.0, dash_length=0.08,
            )
            dashes.add(d)
        self.play(FadeIn(dashes), run_time=0.5)
        self.wait(0.4)

        pm_icon = _mini_grid(2, 3, 0.11, PERI, fill_color=PERI, fill_opacity=0.1)
        pm = _format_card("PMTiles", "Tile serving", pm_icon, PERI, w=2.0, h=1.2)
        pm.next_to(cards, RIGHT, buff=0.35).align_to(cards, DOWN)
        self.play(FadeIn(pm, shift=RIGHT * 0.3), run_time=0.5)
        self.wait(0.3)

        arrows = VGroup()
        targets = [cog, gpq, zarr, pm]
        for t in targets:
            start = base_grp[0].get_top()
            end = t[0].get_bottom()
            sx = np.array([end[0], start[1], 0.0])
            a = Arrow(sx, end, color=PERI, stroke_width=1.8,
                      buff=0.08, max_tip_length_to_length_ratio=0.15)
            arrows.add(a)
        self.play(FadeIn(arrows, shift=UP * 0.15), run_time=0.7)

        range_lbl = caption("HTTP range requests", size=14, color=PERI)
        range_lbl.next_to(arrows, LEFT, buff=0.15).align_to(base_grp, UP).shift(UP * 0.45)
        self.play(FadeIn(range_lbl), run_time=0.4)
        self.wait(0.6)

        chip = stat_chip("No servers needed",
                         "stream directly from object storage", PERI, width=5.5)
        chip.to_edge(UP, buff=0.35).to_edge(RIGHT, buff=0.6)
        self.play(FadeIn(chip, shift=DOWN * 0.2), run_time=0.6)

        cleanup(self, hold=1.5)

class S02_InferencePipeline(Scene):
    def construct(self):
        self.camera.background_color = BG
        tag = scene_tag("inference at scale", accent=EARTH)
        self.play(FadeIn(tag), run_time=0.6)

        scene_p = panel(3.5, 3.0, fill=PANEL2)
        grid = _mini_grid(8, 8, 0.32, DIM, fill_color=PERI, fill_opacity=0.06)
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
                sq.move_to(scene_p.get_center()
                           + RIGHT * (c - 1.5) * 0.64
                           + DOWN * (r - 1.5) * 0.64)
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
        for i in range(3):
            t = Square(side_length=0.55, color=EARTH, stroke_width=1.2)
            t.set_fill(EARTH, opacity=0.08)
            sample_tiles.add(t)
        sample_tiles.arrange(DOWN, buff=0.15)
        sample_tiles.move_to(RIGHT * 0.8)
        tile_lbl = caption("256 px tiles", size=12)
        tile_lbl.next_to(sample_tiles, DOWN, buff=0.1)

        self.play(
            *[FadeIn(t, shift=RIGHT * 0.4) for t in sample_tiles],
            FadeIn(tile_lbl),
            run_time=0.7,
        )
        self.wait(0.4)

        model_box = panel(1.8, 1.6, fill=SURFACE)
        m_lbl = sans("Model", size=20, color=EARTH, weight=BOLD)
        nn_bars = VGroup()
        widths = [0.8, 0.5, 0.8]
        for w in widths:
            bar = Rectangle(width=w, height=0.18, color=EARTH, stroke_width=1.0)
            bar.set_fill(EARTH, opacity=0.12)
            nn_bars.add(bar)
        nn_bars.arrange(DOWN, buff=0.1)
        m_lbl.next_to(nn_bars, UP, buff=0.12)
        nn_grp = VGroup(m_lbl, nn_bars).move_to(model_box)
        model_all = VGroup(model_box, nn_grp).move_to(RIGHT * 3.0)

        arr_in = Arrow(sample_tiles.get_right(), model_box.get_left(),
                       color=EARTH, stroke_width=1.8, buff=0.1,
                       max_tip_length_to_length_ratio=0.12)
        self.play(FadeIn(model_all), FadeIn(arr_in), run_time=0.6)
        self.wait(0.4)

        pred_tiles = VGroup()
        for i in range(3):
            t = Square(side_length=0.55, color=EARTH, stroke_width=1.2)
            t.set_fill(EARTH, opacity=0.3)
            pred_tiles.add(t)
        pred_tiles.arrange(DOWN, buff=0.15).move_to(RIGHT * 5.2)

        arr_out = Arrow(model_box.get_right(), pred_tiles.get_left(),
                        color=EARTH, stroke_width=1.8, buff=0.1,
                        max_tip_length_to_length_ratio=0.12)
        self.play(FadeIn(arr_out), FadeIn(pred_tiles, shift=RIGHT * 0.3), run_time=0.6)
        self.wait(0.4)

        out_lbl = caption("COG / GeoParquet", size=13, color=EARTH)
        out_lbl.next_to(pred_tiles, DOWN, buff=0.15)
        self.play(FadeIn(out_lbl), run_time=0.4)

        note = caption("tiles reassemble into mosaic", size=14, color=DIM)
        note.to_edge(DOWN, buff=0.4)
        self.play(FadeIn(note), run_time=0.5)

        cleanup(self, hold=1.5)

class S03_TorchGeoSampling(Scene):
    def construct(self):
        self.camera.background_color = BG
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

        both = VGroup(img_grp, lbl_grp).to_edge(LEFT, buff=1.0)
        self.play(FadeIn(img_grp), run_time=0.6)
        self.play(FadeIn(lbl_grp), run_time=0.6)
        self.wait(0.4)

        overlap = Rectangle(width=3.0, height=2.0, color=AMBER, stroke_width=2.0)
        overlap.set_fill(AMBER, opacity=0.12)
        overlap.move_to(
            (img_rect.get_center() + lbl_rect.get_center()) / 2
        )
        ov_lbl = caption("intersection", size=12, color=AMBER)
        ov_lbl.next_to(overlap, UP, buff=0.06)
        self.play(FadeIn(overlap), FadeIn(ov_lbl), run_time=0.6)

        code = mono("dataset = imagery & labels", size=16, color=AMBER)
        code.next_to(both, DOWN, buff=0.5)
        self.play(FadeIn(code), run_time=0.5)
        self.wait(0.5)

        patches = VGroup()
        rng = np.random.RandomState(7)
        for _ in range(4):
            px = rng.uniform(-1.2, 1.2)
            py = rng.uniform(-0.7, 0.7)
            patch = Square(side_length=0.5, color=AMBER, stroke_width=1.8)
            patch.set_fill(AMBER, opacity=0.18)
            patch.move_to(overlap.get_center() + RIGHT * px + UP * py)
            patches.add(patch)

        for p in patches:
            self.play(FadeIn(p), run_time=0.35)
        self.wait(0.3)

        loader_box = panel(2.2, 2.0, fill=SURFACE)
        loader_lbl = sans("DataLoader", size=18, color=AMBER, weight=BOLD)
        batch_lbl = caption("batch_size=16", size=12)
        loader_lbl.move_to(loader_box.get_center() + UP * 0.3)
        batch_lbl.next_to(loader_lbl, DOWN, buff=0.1)
        loader_all = VGroup(loader_box, loader_lbl, batch_lbl)
        loader_all.to_edge(RIGHT, buff=1.0)

        arr = Arrow(overlap.get_right(), loader_box.get_left(),
                    color=AMBER, stroke_width=1.8, buff=0.15,
                    max_tip_length_to_length_ratio=0.1)
        self.play(FadeIn(loader_all), FadeIn(arr), run_time=0.6)
        self.wait(0.3)

        self.play(
            *[p.animate.move_to(loader_box.get_center()) for p in patches],
            run_time=0.7,
        )
        self.play(*[FadeOut(p) for p in patches], run_time=0.3)

        train_box = panel(1.8, 1.0, fill=SURFACE)
        train_lbl = sans("Train", size=18, color=EARTH, weight=BOLD)
        train_lbl.move_to(train_box)
        train_grp = VGroup(train_box, train_lbl)
        train_grp.next_to(loader_all, DOWN, buff=0.4)
        arr2 = Arrow(loader_box.get_bottom(), train_box.get_top(),
                     color=EARTH, stroke_width=1.8, buff=0.08,
                     max_tip_length_to_length_ratio=0.12)
        self.play(FadeIn(train_grp), FadeIn(arr2), run_time=0.5)
        self.wait(0.5)

        insight = caption("CRS + resolution + alignment = automatic", size=15, color=AMBER)
        insight.to_edge(DOWN, buff=0.45)
        self.play(FadeIn(insight), run_time=0.5)

        cleanup(self, hold=1.5)

class S04_EmbeddingRetrieval(Scene):
    def construct(self):
        self.camera.background_color = BG
        tag = scene_tag("embedding retrieval", accent=CORAL)
        self.play(FadeIn(tag), run_time=0.6)

        q_tile = panel(1.4, 1.4, fill=PANEL2)
        q_grid = _mini_grid(3, 3, 0.32, DIM, fill_color=PERI, fill_opacity=0.08)
        q_grid.move_to(q_tile)
        q_lbl = caption("query tile", size=13)
        q_lbl.next_to(q_tile, DOWN, buff=0.1)
        q_grp = VGroup(q_tile, q_grid, q_lbl).to_edge(LEFT, buff=0.8).shift(UP * 0.4)
        self.play(FadeIn(q_grp), run_time=0.6)
        self.wait(0.3)

        enc_box = panel(1.8, 1.2, fill=SURFACE)
        enc_lbl = sans("Encoder", size=18, color=CORAL, weight=BOLD)
        enc_sub = caption("foundation model", size=11)
        enc_lbl.move_to(enc_box.get_center() + UP * 0.15)
        enc_sub.next_to(enc_lbl, DOWN, buff=0.06)
        enc_grp = VGroup(enc_box, enc_lbl, enc_sub).next_to(q_grp, RIGHT, buff=0.6)

        arr1 = Arrow(q_tile.get_right(), enc_box.get_left(),
                     color=CORAL, stroke_width=1.8, buff=0.1,
                     max_tip_length_to_length_ratio=0.12)
        self.play(FadeIn(enc_grp), FadeIn(arr1), run_time=0.6)
        self.wait(0.3)

        bits = "1 0 1 1 0 0 1 0 1 1"
        emb_row = mono(bits, size=16, color=CORAL)
        emb_row.next_to(enc_box, RIGHT, buff=0.5)
        arr2 = Arrow(enc_box.get_right(), emb_row.get_left(),
                     color=CORAL, stroke_width=1.8, buff=0.1,
                     max_tip_length_to_length_ratio=0.12)
        self.play(FadeIn(arr2), FadeIn(emb_row), run_time=0.6)
        self.wait(0.4)

        space_panel = panel(4.5, 2.8, fill=PANEL2)
        space_panel.to_edge(RIGHT, buff=0.5).shift(DOWN * 0.9)
        sp_lbl = caption("embedding space", size=13, color=DIM)
        sp_lbl.next_to(space_panel, UP, buff=0.08)

        rng = np.random.RandomState(42)
        colors_list = [EARTH, PERI, AMBER, DIM]
        dots = VGroup()
        for _ in range(30):
            dx = rng.uniform(-1.8, 1.8)
            dy = rng.uniform(-1.1, 1.1)
            c = colors_list[rng.randint(0, 4)]
            dot = Dot(
                space_panel.get_center() + RIGHT * dx + UP * dy,
                radius=0.06, color=c,
            )
            dot.set_fill(c, opacity=0.7)
            dots.add(dot)

        self.play(FadeIn(space_panel), FadeIn(sp_lbl), FadeIn(dots), run_time=0.7)
        self.wait(0.4)

        q_dot = Dot(space_panel.get_center() + LEFT * 0.3 + UP * 0.2,
                    radius=0.1, color=CORAL)
        q_dot.set_fill(CORAL, opacity=0.9)
        q_tag = caption("query", size=11, color=CORAL)
        q_tag.next_to(q_dot, UP, buff=0.08)
        self.play(FadeIn(q_dot), FadeIn(q_tag), run_time=0.5)
        self.wait(0.3)

        dists = [
            (np.linalg.norm(d.get_center() - q_dot.get_center()), i)
            for i, d in enumerate(dots)
        ]
        dists.sort()
        nn_lines = VGroup()
        for _, idx in dists[:4]:
            line = Line(q_dot.get_center(), dots[idx].get_center(),
                        color=CORAL, stroke_width=1.5)
            nn_lines.add(line)
            dots[idx].set_color(CORAL)
        self.play(FadeIn(nn_lines), run_time=0.6)
        self.wait(0.4)

        res_lbl = caption("top-K matches", size=13, color=CORAL)
        res_tiles = VGroup()
        for i in range(4):
            t = panel(0.7, 0.7, fill=SURFACE)
            g = _mini_grid(2, 2, 0.2, DIM, fill_color=CORAL, fill_opacity=0.1)
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

        chip = stat_chip("Search billions of embeddings",
                         "in milliseconds", CORAL, width=5.5)
        chip.to_edge(LEFT, buff=0.7).to_edge(DOWN, buff=0.4)
        if chip.get_bottom()[1] < -3.4:
            chip.shift(UP * 0.3)
        self.play(FadeIn(chip, shift=UP * 0.15), run_time=0.6)

        cleanup(self, hold=1.5)
