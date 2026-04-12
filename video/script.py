"""
RSIM CVPR IMW 2026 Talk Video — Warm Ivory Edition

Paper: Are Pretrained Image Matchers Good Enough for SAR-Optical Satellite Registration?
Authors: Isaac Corley, Alex Stoken, Gabriele Berton

Theme: Anthropic / TG warm ivory preset.
  BG = ivory, brown body text, coral/earth/amber/peri accents.
  One dominant accent per scene. Every content block sits on a panel.

Accent assignments (one dominant per scene):
  S01 Title            CORAL  (the hook)
  S02 PhysicsGap       AMBER  (SAR is the intruder)
  S03 Question         PERI   (study design)
  S04 Pipeline         EARTH  (the method)
  S05 Tiled            AMBER  (mechanism)
  S06 Leaderboard      CORAL  (the surprise ranking)
  S07 DINO             EARTH  (the aha)
  S08 Protocol         CORAL  (33x swing = bad)
  S09 Affine           EARTH  (the fix)
  S10 Cross            PERI   (robustness)
  S11 Pareto           EARTH  (the runtime win)
  S12 Recipe           MOON CTA pill
"""

import random

import numpy as np
from manim import (
    BOLD,
    DEGREES,
    DOWN,
    LEFT,
    NORMAL,
    ORIGIN,
    PI,
    RIGHT,
    UP,
    Arc,
    Arrow,
    Brace,
    Create,
    DashedLine,
    Dot,
    FadeIn,
    FadeOut,
    GrowFromCenter,
    Group,
    Line,
    Rectangle,
    RoundedRectangle,
    Scene,
    Square,
    Star,
    SurroundingRectangle,
    Text,
    Transform,
    VGroup,
    Write,
    config,
)

# ---------- Palette (warm ivory) ----------
BG      = "#F4F4EB"
SURFACE = "#EAEADE"
PANEL2  = "#DFDFD4"
BORDER  = "#C8C2B2"

MOON    = "#3B1E1C"   # body text
DIM     = "#8F7F73"   # captions, axes

EARTH   = "#1E5B46"   # forest green — "good" / positive
CORAL   = "#BE3E1F"   # coral red — attention / problem
AMBER   = "#C96A1E"   # warm amber — data emphasis / SAR
PERI    = "#4A6BA8"   # periwinkle — secondary / systems

MONO = "Menlo"
SANS = "Space Grotesk"

config.background_color = BG

random.seed(7)
np.random.seed(7)


# ---------- Helpers ----------
def mono(text, size=28, color=MOON, weight=NORMAL):
    return Text(text, font=MONO, font_size=size, color=color, weight=weight)


def sans(text, size=42, color=MOON, weight=BOLD):
    return Text(text, font=SANS, font_size=size, color=color, weight=weight)


def label(text, color=MOON, size=22):
    return mono(text, size=size, color=color)


def caption(text, color=DIM, size=18):
    return mono(text, size=size, color=color)


def panel(width, height, radius=0.22, fill=SURFACE, stroke=BORDER, stroke_width=1.2):
    return RoundedRectangle(
        width=width, height=height, corner_radius=radius,
        color=stroke, stroke_width=stroke_width,
        fill_color=fill, fill_opacity=1.0,
    )


def accent_bar(length=0.9, color=CORAL, stroke=4):
    return Line(LEFT * length / 2, RIGHT * length / 2, color=color, stroke_width=stroke)


def header_with_rule(text_str, color=MOON, accent=CORAL, size=38):
    h = sans(text_str, size=size, color=color, weight=BOLD)
    bar = accent_bar(length=h.width * 0.28, color=accent, stroke=5)
    bar.next_to(h, DOWN, buff=0.22, aligned_edge=LEFT).align_to(h, LEFT)
    return VGroup(h, bar)


def scene_tag(text_str, accent=CORAL):
    """Top-left scene rubric: short stub bar + muted mono tag."""
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
    # Clamp both headline and sub to card width
    if h.width > card.width - 0.4:
        h.scale((card.width - 0.4) / h.width)
    if s.width > card.width - 0.5:
        s.scale((card.width - 0.5) / s.width)
    h.move_to(card.get_center() + UP * 0.26)
    s.move_to(card.get_center() + DOWN * 0.38)
    return VGroup(card, h, s)


def cleanup(scene, hold=1.0):
    """Hold final frame for narration breathing room, then fade."""
    scene.wait(hold)
    scene.play(FadeOut(Group(*scene.mobjects)), run_time=0.6)


# ---------- Scene 01: Title + Hurricane Hook ----------
class S01_Title(Scene):
    def construct(self):
        self.camera.background_color = BG

        tag = scene_tag("the setup", accent=CORAL)
        self.play(FadeIn(tag), run_time=0.6)

        # Hurricane spiral in coral
        spiral = VGroup()
        for i, (r, alpha, rot) in enumerate(
            [
                (1.35, 0.95, 0),
                (1.10, 0.75, -35),
                (0.85, 0.58, -70),
                (0.65, 0.42, -105),
                (0.48, 0.3, -140),
            ]
        ):
            arc = Arc(
                radius=r,
                angle=3.2,
                start_angle=rot * DEGREES,
                color=CORAL,
                stroke_width=5 - i * 0.5,
            ).set_opacity(alpha)
            spiral.add(arc)
        eye = Dot(radius=0.08, color=MOON)
        spiral.add(eye)
        spiral.move_to(ORIGIN + UP * 2.1)

        self.play(GrowFromCenter(spiral), run_time=2.0)
        self.play(spiral.animate.rotate(-0.6 * PI), run_time=2.4)

        # Title block
        title_txt = sans("Are Pretrained Image Matchers", size=34, color=MOON, weight=BOLD)
        title_txt2 = sans("Good Enough for", size=34, color=MOON, weight=BOLD)
        title_txt3 = sans("SAR-Optical Registration?", size=34, color=CORAL, weight=BOLD)
        title_block = VGroup(title_txt, title_txt2, title_txt3).arrange(DOWN, buff=0.18)
        title_block.next_to(spiral, DOWN, buff=0.4)

        # Coral rule under title
        rule = Line(LEFT * 2.2, RIGHT * 2.2, color=CORAL, stroke_width=3.5)
        rule.next_to(title_block, DOWN, buff=0.25)

        authors = caption(
            "Isaac Corley  .  Alex Stoken  .  Gabriele Berton",
            color=DIM,
        )
        venue = caption("CVPR 2026  .  Image Matching Workshop", color=EARTH)
        credit = VGroup(authors, venue).arrange(DOWN, buff=0.1)
        credit.next_to(rule, DOWN, buff=0.22)

        self.play(Write(title_txt), run_time=1.0)
        self.play(Write(title_txt2), run_time=0.9)
        self.play(Write(title_txt3), run_time=1.2)
        self.play(Create(rule), run_time=0.5)
        self.play(FadeIn(credit, shift=UP * 0.2), run_time=0.9)
        cleanup(self)


# ---------- Scene 02: Physics Gap ----------
class S02_PhysicsGap(Scene):
    def construct(self):
        self.camera.background_color = BG

        heading = header_with_rule(
            "optical and SAR see different worlds",
            color=MOON, accent=AMBER, size=34,
        )
        heading.to_edge(UP, buff=0.7).to_edge(LEFT, buff=0.9)
        self.play(Write(heading[0]), run_time=0.9)
        self.play(Create(heading[1]), run_time=0.4)

        # Two card panels — pulled up so callouts fit beneath captions
        opt_card = panel(3.4, 3.4, radius=0.22, fill=SURFACE, stroke=BORDER)
        opt_card.move_to(LEFT * 3.3 + DOWN * 0.15)
        sar_card = panel(3.4, 3.4, radius=0.22, fill=SURFACE, stroke=BORDER)
        sar_card.move_to(RIGHT * 3.3 + DOWN * 0.15)

        opt_lbl = mono("OPTICAL", size=20, color=PERI, weight=BOLD)
        opt_lbl.next_to(opt_card, UP, buff=0.15)
        sar_lbl = mono("SAR", size=20, color=AMBER, weight=BOLD)
        sar_lbl.next_to(sar_card, UP, buff=0.15)

        opt_sub = caption("reflected sunlight", color=DIM)
        opt_sub.next_to(opt_card, DOWN, buff=0.15)
        sar_sub = caption("microwave backscatter", color=DIM)
        sar_sub.next_to(sar_card, DOWN, buff=0.15)

        self.play(
            FadeIn(opt_card), FadeIn(sar_card),
            FadeIn(opt_lbl), FadeIn(sar_lbl),
            FadeIn(opt_sub), FadeIn(sar_sub),
            run_time=1.4,
        )

        # Optical buildings — peri blue rectangles on ivory
        opt_buildings = VGroup()
        rng = random.Random(1)
        coords = []
        for _ in range(14):
            x = rng.uniform(-1.15, 1.15)
            y = rng.uniform(-1.15, 1.15)
            w = rng.uniform(0.2, 0.4)
            h = rng.uniform(0.2, 0.4)
            coords.append((x, y, w, h))
            b = Rectangle(
                width=w, height=h,
                color=PERI, fill_color=PERI, fill_opacity=0.9, stroke_width=0,
            )
            b.move_to(opt_card.get_center() + np.array([x, y, 0]))
            opt_buildings.add(b)

        self.play(FadeIn(opt_buildings, lag_ratio=0.06), run_time=1.8)
        self.wait(1.2)

        # SAR card: speckle + shifted/stretched amber rectangles (layover)
        sar_speckle = VGroup()
        for _ in range(240):
            x = rng.uniform(-1.55, 1.55)
            y = rng.uniform(-1.55, 1.55)
            d = Dot(
                radius=rng.uniform(0.012, 0.028),
                color=AMBER,
            ).set_opacity(rng.uniform(0.25, 0.85))
            d.move_to(sar_card.get_center() + np.array([x, y, 0]))
            sar_speckle.add(d)
        sar_buildings = VGroup()
        for (x, y, w, h) in coords:
            nb = Rectangle(
                width=w, height=h * 1.35,
                color=AMBER, fill_color=AMBER, fill_opacity=0.92, stroke_width=0,
            )
            nb.move_to(sar_card.get_center() + np.array([x + 0.12, y + 0.22, 0]))
            sar_buildings.add(nb)

        self.play(
            FadeIn(sar_speckle, lag_ratio=0.006),
            FadeIn(sar_buildings, lag_ratio=0.06),
            run_time=2.4,
        )
        self.wait(1.8)

        # Callouts at the bottom — mono chips
        callout_words = ["speckle noise", "layover", "contrast inversion"]
        callout_group = VGroup()
        for word in callout_words:
            c = panel(2.3, 0.55, radius=0.18, fill=PANEL2, stroke=BORDER)
            t = mono(word, size=14, color=CORAL)
            t.move_to(c.get_center())
            callout_group.add(VGroup(c, t))
        callout_group.arrange(RIGHT, buff=0.3)
        callout_group.move_to(np.array([0, -2.7, 0]))

        for c in callout_group:
            self.play(FadeIn(c, shift=UP * 0.15), run_time=0.6)

        self.wait(3.5)
        cleanup(self)


# ---------- Scene 03: Research Question ----------
class S03_Question(Scene):
    def construct(self):
        self.camera.background_color = BG

        heading = header_with_rule(
            "the research question",
            color=MOON, accent=PERI, size=36,
        )
        heading.to_edge(UP, buff=0.7).to_edge(LEFT, buff=0.9)
        self.play(Write(heading[0]), run_time=0.9)
        self.play(Create(heading[1]), run_time=0.4)

        # Four chips in a 2x2 grid on soft cards
        chip_data = [
            ("24", "pretrained matcher families"),
            ("0-shot", "no fine-tuning, no adaptation"),
            ("3", "cross-modal datasets"),
            ("fixed", "deterministic protocol"),
        ]
        chip_group = VGroup()
        for head, sub in chip_data:
            card = panel(5.0, 1.6, radius=0.2, fill=SURFACE, stroke=BORDER)
            h = sans(head, size=36, color=PERI, weight=BOLD)
            s = caption(sub, color=DIM)
            if s.width > card.width - 0.6:
                s.scale((card.width - 0.6) / s.width)
            h.move_to(card.get_center() + UP * 0.28)
            s.move_to(card.get_center() + DOWN * 0.35)
            chip_group.add(VGroup(card, h, s))
        # 2x2 layout
        top = VGroup(chip_group[0], chip_group[1]).arrange(RIGHT, buff=0.4)
        bot = VGroup(chip_group[2], chip_group[3]).arrange(RIGHT, buff=0.4)
        grid = VGroup(top, bot).arrange(DOWN, buff=0.4)
        grid.next_to(heading, DOWN, buff=0.5).align_to(heading, LEFT)
        # Re-center horizontally on the page
        grid.move_to(np.array([0, grid.get_center()[1], 0]))

        for row in [top, bot]:
            for c in row:
                self.play(FadeIn(c, shift=UP * 0.2), run_time=0.5)

        self.wait(1.5)

        # The question as a full-width banner
        q_card = panel(11.5, 1.1, radius=0.35, fill=PANEL2, stroke=CORAL, stroke_width=2)
        q_card.next_to(grid, DOWN, buff=0.6)
        q_txt = sans(
            "Do natural-image matchers transfer to overhead SAR?",
            size=26, color=MOON, weight=BOLD,
        )
        q_txt.move_to(q_card.get_center())
        self.play(FadeIn(q_card), Write(q_txt), run_time=1.6)
        cleanup(self)


# ---------- Scene 04: Pipeline ----------
class S04_Pipeline(Scene):
    def construct(self):
        self.camera.background_color = BG

        heading = header_with_rule(
            "zero-shot matching protocol",
            color=MOON, accent=EARTH, size=34,
        )
        heading.to_edge(UP, buff=0.7).to_edge(LEFT, buff=0.9)
        self.play(Write(heading[0]), run_time=0.9)
        self.play(Create(heading[1]), run_time=0.4)

        # Four pipeline stages, each a panel with a colored top rule
        stages = [
            ("NORMALIZE", "percentile / CLAHE", PERI),
            ("TILE",      "768x768 / 256 ovlp",  AMBER),
            ("MATCH",     "pretrained matcher",  CORAL),
            ("FILTER",    "affine-RANSAC",       EARTH),
        ]
        nodes = VGroup()
        for head, sub, accent in stages:
            card = panel(3.0, 1.9, radius=0.2, fill=SURFACE, stroke=BORDER)
            h = sans(head, size=22, color=accent, weight=BOLD)
            s = caption(sub, color=DIM)
            if s.width > card.width - 0.4:
                s.scale((card.width - 0.4) / s.width)
            rule = Line(LEFT * 0.5, RIGHT * 0.5, color=accent, stroke_width=3)
            h.move_to(card.get_center() + UP * 0.35)
            rule.next_to(h, DOWN, buff=0.14)
            s.move_to(card.get_center() + DOWN * 0.5)
            nodes.add(VGroup(card, h, rule, s))
        nodes.arrange(RIGHT, buff=0.25)
        nodes.shift(DOWN * 0.3)

        arrows = VGroup()
        for i in range(3):
            a = Arrow(
                start=nodes[i].get_right(),
                end=nodes[i + 1].get_left(),
                color=DIM, buff=0.08, stroke_width=3,
                max_tip_length_to_length_ratio=0.3,
            )
            arrows.add(a)

        for i, n in enumerate(nodes):
            self.play(FadeIn(n, shift=UP * 0.2), run_time=0.8)
            if i < 3:
                self.play(Create(arrows[i]), run_time=0.45)
            self.wait(0.3)

        self.wait(0.8)

        # Pulse the sequence twice
        for _ in range(2):
            for n in nodes:
                self.play(n[0].animate.set_stroke(width=3.5), run_time=0.3)
                self.play(n[0].animate.set_stroke(width=1.2), run_time=0.3)

        # Outcome chip
        outcome_card = panel(5.8, 0.9, radius=0.45, fill=SURFACE, stroke=EARTH, stroke_width=2)
        outcome_txt = mono("-> mean tie-point error (px)", size=18, color=EARTH, weight=BOLD)
        outcome_txt.move_to(outcome_card.get_center())
        outcome = VGroup(outcome_card, outcome_txt)
        outcome.next_to(nodes, DOWN, buff=0.75)
        self.play(FadeIn(outcome, shift=UP * 0.15), run_time=1.1)
        cleanup(self)


# ---------- Scene 05: Tiled Matching ----------
class S05_Tiled(Scene):
    def construct(self):
        self.camera.background_color = BG

        heading = header_with_rule(
            "tiled correspondence on large scenes",
            color=MOON, accent=AMBER, size=32,
        )
        heading.to_edge(UP, buff=0.7).to_edge(LEFT, buff=0.9)
        self.play(Write(heading[0]), run_time=0.9)
        self.play(Create(heading[1]), run_time=0.4)

        scene_w, scene_h = 4.5, 3.2
        opt_card = panel(scene_w + 0.3, scene_h + 0.3, radius=0.2)
        opt_card.move_to(LEFT * 3.4 + DOWN * 0.4)
        sar_card = panel(scene_w + 0.3, scene_h + 0.3, radius=0.2)
        sar_card.move_to(RIGHT * 3.4 + DOWN * 0.4)

        opt_lbl = mono("optical basemap", size=14, color=PERI).next_to(opt_card, UP, buff=0.1)
        sar_lbl = mono("SAR scene", size=14, color=AMBER).next_to(sar_card, UP, buff=0.1)

        self.play(FadeIn(opt_card), FadeIn(sar_card), FadeIn(opt_lbl), FadeIn(sar_lbl), run_time=1.2)

        # Speckle field on SAR card
        speckle = VGroup()
        rng = random.Random(3)
        for _ in range(260):
            x = rng.uniform(-scene_w / 2 + 0.05, scene_w / 2 - 0.05)
            y = rng.uniform(-scene_h / 2 + 0.05, scene_h / 2 - 0.05)
            d = Dot(radius=rng.uniform(0.01, 0.024), color=AMBER).set_opacity(
                rng.uniform(0.3, 0.85)
            )
            d.move_to(sar_card.get_center() + np.array([x, y, 0]))
            speckle.add(d)

        # Peri-blue building blobs on optical card
        blobs = VGroup()
        coords = []
        for _ in range(16):
            x = rng.uniform(-scene_w / 2 + 0.2, scene_w / 2 - 0.2)
            y = rng.uniform(-scene_h / 2 + 0.2, scene_h / 2 - 0.2)
            w = rng.uniform(0.2, 0.4)
            h = rng.uniform(0.2, 0.4)
            coords.append((x, y, w, h))
            b = Rectangle(width=w, height=h, color=PERI, fill_color=PERI, fill_opacity=0.75, stroke_width=0)
            b.move_to(opt_card.get_center() + np.array([x, y, 0]))
            blobs.add(b)

        self.play(FadeIn(blobs, lag_ratio=0.04), FadeIn(speckle, lag_ratio=0.003), run_time=1.5)
        self.wait(0.8)

        # Tile grid overlay — stroke only, coral accents
        def tile_grid(card_center, scene_w, scene_h):
            g = VGroup()
            tile_w = scene_w / 2.4
            tile_h = scene_h / 2.4
            for dx in [-1.0, 0, 1.0]:
                for dy in [-1.0, 0, 1.0]:
                    t = RoundedRectangle(
                        width=tile_w, height=tile_h, corner_radius=0.06,
                        color=CORAL, stroke_width=1.8, fill_opacity=0,
                    )
                    t.set_stroke(opacity=0.7)
                    t.move_to(card_center + np.array([dx * tile_w * 0.55, dy * tile_h * 0.55, 0]))
                    g.add(t)
            return g

        opt_tiles = tile_grid(opt_card.get_center(), scene_w, scene_h)
        sar_tiles = tile_grid(sar_card.get_center(), scene_w, scene_h)
        self.play(Create(opt_tiles, lag_ratio=0.12), Create(sar_tiles, lag_ratio=0.12), run_time=2.0)
        self.wait(1.0)

        # Highlight center tile in each card
        ct_opt = opt_tiles[4]
        ct_sar = sar_tiles[4]
        self.play(
            ct_opt.animate.set_stroke(color=EARTH, width=3.5, opacity=1),
            ct_sar.animate.set_stroke(color=EARTH, width=3.5, opacity=1),
            run_time=0.9,
        )
        self.wait(0.4)

        # Match lines between highlighted tiles
        lines = VGroup()
        for _ in range(14):
            x1 = rng.uniform(-0.55, 0.55)
            y1 = rng.uniform(-0.45, 0.45)
            x2 = x1 + rng.uniform(-0.05, 0.05)
            y2 = y1 + rng.uniform(-0.05, 0.05)
            p1 = ct_opt.get_center() + np.array([x1, y1, 0])
            p2 = ct_sar.get_center() + np.array([x2, y2, 0])
            is_in = rng.random() > 0.2
            ln = Line(p1, p2, color=EARTH if is_in else CORAL, stroke_width=1.8).set_opacity(
                0.9 if is_in else 0.75
            )
            lines.add(ln)
        self.play(Create(lines, lag_ratio=0.12), run_time=2.0)
        self.wait(1.0)

        # Legend
        leg_card = panel(4.2, 0.6, radius=0.18, fill=PANEL2, stroke=BORDER)
        l1 = Line(ORIGIN, RIGHT * 0.35, color=EARTH, stroke_width=4)
        l1t = mono("inliers", size=14, color=EARTH)
        l2 = Line(ORIGIN, RIGHT * 0.35, color=CORAL, stroke_width=4)
        l2t = mono("outliers", size=14, color=CORAL)
        leg = VGroup(l1, l1t, l2, l2t).arrange(RIGHT, buff=0.18)
        leg.move_to(leg_card.get_center())
        legend = VGroup(leg_card, leg).to_edge(DOWN, buff=0.55)
        self.play(FadeIn(legend), run_time=0.9)
        cleanup(self)


# ---------- Scene 06: Leaderboard ----------
class S06_Leaderboard(Scene):
    def construct(self):
        self.camera.background_color = BG

        heading = header_with_rule(
            "SpaceNet9 leaderboard",
            color=MOON, accent=CORAL, size=36,
        )
        heading.to_edge(UP, buff=0.7).to_edge(LEFT, buff=0.9)
        sub = caption("mean tie-point error (px)  .  lower is better", color=DIM)
        sub.next_to(heading, DOWN, buff=0.35).align_to(heading, LEFT)
        self.play(Write(heading[0]), run_time=0.9)
        self.play(Create(heading[1]), run_time=0.4)
        self.play(FadeIn(sub), run_time=0.4)

        data = [
            ("RoMa",          3.0, True),
            ("XoFTR",         3.0, True),
            ("RoMa+LoFTR",    3.3, False),
            ("MINIMA-RoMa",   3.4, False),
            ("MA-ELoFTR",     3.4, False),
            ("RoMaV2",        3.6, False),
            ("MINIMA-XoFTR",  3.8, False),
            ("GIM-DKM",       4.1, False),
            ("SuperPoint-LG", 4.4, False),
            ("LoFTR",         5.1, False),
        ]

        # Hard-coded x columns to keep mono labels aligned
        NAME_X = -4.9
        BAR_START_X = -2.6
        y_top = 1.85
        y_step = 0.46
        scale = 0.65  # px per unit error

        rows = VGroup()
        bars = []
        labels_val = []
        values = []
        for i, (name, err, hi) in enumerate(data):
            y = y_top - i * y_step
            name_txt = mono(name, size=16, color=MOON if hi else DIM)
            name_txt.move_to(np.array([NAME_X, y, 0])).align_to(
                np.array([NAME_X, 0, 0]), LEFT
            )
            color = CORAL if hi else PERI
            bar = RoundedRectangle(
                width=0.01, height=0.3, corner_radius=0.04,
                color=color, stroke_width=0, fill_color=color, fill_opacity=1.0,
            )
            bar.move_to(np.array([BAR_START_X, y, 0])).align_to(
                np.array([BAR_START_X, 0, 0]), LEFT
            )
            val = mono(f"{err:.1f}", size=14, color=color, weight=BOLD)
            rows.add(name_txt)
            bars.append(bar)
            labels_val.append(val)
            values.append(err)

        # Axis
        axis_y = y_top - len(data) * y_step + 0.1
        axis = Line(
            np.array([BAR_START_X, axis_y, 0]),
            np.array([BAR_START_X + 6.5 * scale, axis_y, 0]),
            color=DIM, stroke_width=1.2,
        )
        ticks = VGroup()
        for v in [0, 2, 4, 6]:
            tx = BAR_START_X + v * scale
            tk = Line(
                np.array([tx, axis_y - 0.06, 0]),
                np.array([tx, axis_y + 0.06, 0]),
                color=DIM, stroke_width=1,
            )
            lb = caption(str(v), color=DIM).scale(0.7).next_to(tk, DOWN, buff=0.06)
            ticks.add(tk, lb)

        self.play(FadeIn(rows, lag_ratio=0.08), run_time=1.4)
        self.play(Create(axis), FadeIn(ticks), run_time=0.7)
        self.wait(0.5)

        for bar, err, val_txt in zip(bars, values, labels_val):
            target = bar.copy()
            target.stretch_to_fit_width(err * scale)
            target.move_to(np.array([BAR_START_X, bar.get_y(), 0])).align_to(
                np.array([BAR_START_X, 0, 0]), LEFT
            )
            val_txt.next_to(target, RIGHT, buff=0.14)
            self.add(bar)
            self.play(Transform(bar, target), FadeIn(val_txt), run_time=0.45)

        self.wait(2.0)

        # Chyron as coral rule + text (not a panel — readability first)
        chyron_card = panel(11.5, 0.9, radius=0.35, fill=SURFACE, stroke=CORAL, stroke_width=2)
        chyron_txt = sans(
            "RoMa ties XoFTR  .  RoMa has ZERO cross-modal training",
            size=22, color=MOON, weight=BOLD,
        )
        chyron_txt.move_to(chyron_card.get_center())
        chyron = VGroup(chyron_card, chyron_txt).to_edge(DOWN, buff=0.55)
        self.play(FadeIn(chyron_card), Write(chyron_txt), run_time=1.8)
        cleanup(self)


# ---------- Scene 07: DINOv2 Hypothesis ----------
class S07_DINO(Scene):
    def construct(self):
        self.camera.background_color = BG

        heading = header_with_rule(
            "why does RoMa work without cross-modal data?",
            color=MOON, accent=EARTH, size=30,
        )
        heading.to_edge(UP, buff=0.7).to_edge(LEFT, buff=0.9)
        self.play(Write(heading[0]), run_time=0.9)
        self.play(Create(heading[1]), run_time=0.4)

        # Four-node flow diagram
        def flow_box(head, sub, color, width=2.2):
            card = panel(width, 1.1, radius=0.18, fill=SURFACE, stroke=BORDER)
            h = sans(head, size=18, color=color, weight=BOLD)
            s = caption(sub, color=DIM)
            h.move_to(card.get_center() + UP * 0.22)
            s.move_to(card.get_center() + DOWN * 0.25)
            return VGroup(card, h, s)

        n1 = flow_box("web", "internet-scale", DIM)
        n2 = flow_box("DINOv2", "frozen backbone", EARTH)
        n3 = flow_box("features", "shared space", AMBER)
        n4 = flow_box("RoMa", "regression head", EARTH)
        flow = VGroup(n1, n2, n3, n4).arrange(RIGHT, buff=0.35)
        flow.shift(UP * 1.3)

        arrows = VGroup()
        for i in range(3):
            a = Arrow(
                start=flow[i].get_right(),
                end=flow[i + 1].get_left(),
                color=DIM, buff=0.08, stroke_width=2.5,
                max_tip_length_to_length_ratio=0.3,
            )
            arrows.add(a)

        for b in flow:
            self.play(FadeIn(b, shift=UP * 0.15), run_time=0.55)
        self.play(Create(arrows), run_time=0.6)
        self.wait(1.0)

        # Feature-space scatter: before (separated) and after (merged)
        box_w, box_h = 4.0, 2.6
        left_card = panel(box_w, box_h, radius=0.22, fill=SURFACE, stroke=BORDER)
        right_card = panel(box_w, box_h, radius=0.22, fill=SURFACE, stroke=BORDER)
        left_card.move_to(LEFT * 2.8 + DOWN * 1.6)
        right_card.move_to(RIGHT * 2.8 + DOWN * 1.6)

        lb_before = caption("pixel space", color=DIM).next_to(left_card, UP, buff=0.1)
        lb_after = mono("DINOv2 feature space", size=14, color=EARTH, weight=BOLD).next_to(
            right_card, UP, buff=0.1
        )

        self.play(FadeIn(left_card), FadeIn(right_card), Write(lb_before), Write(lb_after), run_time=0.9)

        rng = random.Random(5)
        opt_before = VGroup()
        sar_before = VGroup()
        opt_after = VGroup()
        sar_after = VGroup()
        for _ in range(26):
            ox = rng.uniform(-1.7, -0.35)
            oy = rng.uniform(-0.95, 0.95)
            sx = rng.uniform(0.35, 1.7)
            sy = rng.uniform(-0.95, 0.95)
            opt_before.add(Dot(left_card.get_center() + np.array([ox, oy, 0]), radius=0.055, color=PERI))
            sar_before.add(Dot(left_card.get_center() + np.array([sx, sy, 0]), radius=0.055, color=AMBER))

            mox = rng.uniform(-0.9, 0.9)
            moy = rng.uniform(-0.9, 0.9)
            msx = rng.uniform(-0.9, 0.9)
            msy = rng.uniform(-0.9, 0.9)
            opt_after.add(Dot(right_card.get_center() + np.array([mox, moy, 0]), radius=0.055, color=PERI))
            sar_after.add(Dot(right_card.get_center() + np.array([msx, msy, 0]), radius=0.055, color=AMBER))

        self.play(FadeIn(opt_before, lag_ratio=0.05), FadeIn(sar_before, lag_ratio=0.05), run_time=1.3)
        self.wait(1.2)
        self.play(FadeIn(opt_after, lag_ratio=0.05), FadeIn(sar_after, lag_ratio=0.05), run_time=1.3)
        self.wait(1.0)

        # Caption below both cards
        cap_card = panel(9.0, 0.75, radius=0.35, fill=PANEL2, stroke=BORDER)
        cap_txt = mono(
            "emergent modality invariance  (working hypothesis)",
            size=16, color=EARTH, weight=BOLD,
        )
        cap_txt.move_to(cap_card.get_center())
        cap = VGroup(cap_card, cap_txt).to_edge(DOWN, buff=0.55)
        self.play(FadeIn(cap), run_time=1.0)
        cleanup(self)


# ---------- Scene 08: Protocol Sensitivity ----------
class S08_Protocol(Scene):
    def construct(self):
        self.camera.background_color = BG

        heading = header_with_rule(
            "protocol choices can dominate matcher choice",
            color=MOON, accent=CORAL, size=30,
        )
        heading.to_edge(UP, buff=0.7).to_edge(LEFT, buff=0.9)
        self.play(Write(heading[0]), run_time=0.9)
        self.play(Create(heading[1]), run_time=0.4)

        # Plot on a card
        plot_card = panel(11.5, 4.2, radius=0.22, fill=SURFACE, stroke=BORDER)
        plot_card.move_to(DOWN * 0.5)
        self.play(FadeIn(plot_card), run_time=0.6)

        # Axes inside the card
        x_left, x_right = -5.2, 5.2
        y_bot, y_top = -2.1, 0.9
        x_axis = Line(np.array([x_left, y_bot, 0]), np.array([x_right, y_bot, 0]),
                      color=DIM, stroke_width=1.2)
        y_axis = Line(np.array([x_left, y_bot, 0]), np.array([x_left, y_top, 0]),
                      color=DIM, stroke_width=1.2)
        y_label = caption("mean error (px)", color=DIM).rotate(PI / 2)
        y_label.next_to(y_axis, LEFT, buff=0.15)

        self.play(Create(x_axis), Create(y_axis), Write(y_label), run_time=0.8)

        matchers = [
            ("RoMa",      3.0, 0.4),
            ("XoFTR",     3.0, 0.3),
            ("MA-ELoFTR", 3.4, 0.6),
            ("MINIMA-R",  3.4, 0.5),
            ("LoFTR",     5.1, 1.1),
            ("XFeat",     6.5, 1.8),
            ("MASt3R",    4.5, 1.5),
        ]

        def y_for(err):
            return np.interp(err, [2.5, 12.0], [y_top - 0.3, y_bot + 0.2])

        xs = np.linspace(x_left + 1.0, x_right - 1.0, len(matchers))
        cols = VGroup()
        bullets = VGroup()
        rng = random.Random(11)
        for (name, mean_err, spread), xc in zip(matchers, xs):
            dots = VGroup()
            for _ in range(22):
                dy = rng.gauss(0, spread * 0.4)
                dx = rng.uniform(-0.18, 0.18)
                err = mean_err + dy
                if err < 2.5:
                    err = 2.5 + rng.random() * 0.2
                y = y_for(err)
                if mean_err < 4:
                    c = PERI
                elif mean_err < 5.5:
                    c = AMBER
                else:
                    c = CORAL
                dots.add(Dot(np.array([xc + dx, y, 0]), radius=0.05, color=c).set_opacity(0.85))
            mean_marker = Line(
                np.array([xc - 0.3, y_for(mean_err), 0]),
                np.array([xc + 0.3, y_for(mean_err), 0]),
                color=MOON, stroke_width=3.5,
            )
            lbl = caption(name, color=DIM).scale(0.75)
            lbl.move_to(np.array([xc, y_bot - 0.28, 0]))
            cols.add(dots, mean_marker)
            bullets.add(lbl)

        self.play(FadeIn(cols, lag_ratio=0.05), FadeIn(bullets, lag_ratio=0.08), run_time=2.4)
        self.wait(1.5)

        # Bracket on the widest column (XFeat)
        widest_x = xs[5]
        bracket = Brace(
            Line(
                np.array([widest_x + 0.3, y_for(4.5), 0]),
                np.array([widest_x + 0.3, y_for(10), 0]),
            ),
            RIGHT,
            color=CORAL,
        )
        bracket_lbl = caption("protocol swing", color=CORAL).scale(0.85)
        bracket_lbl.next_to(bracket, RIGHT, buff=0.1)
        self.play(GrowFromCenter(bracket), FadeIn(bracket_lbl), run_time=1.2)
        self.wait(2.0)

        # Huge 33x callout — outside the plot card, upper-right whitespace
        big = sans("33x", size=120, color=CORAL, weight=BOLD)
        big.move_to(np.array([4.3, 2.4, 0]))
        sub = caption("error swing, one matcher", color=DIM)
        sub.next_to(big, DOWN, buff=0.15)
        self.play(FadeIn(big, scale=1.3), run_time=1.2)
        self.play(Write(sub), run_time=0.9)
        cleanup(self)


# ---------- Scene 09: Affine vs Homography ----------
class S09_Affine(Scene):
    def construct(self):
        self.camera.background_color = BG

        heading = header_with_rule(
            "orthorectified satellites want affine, not homography",
            color=MOON, accent=EARTH, size=28,
        )
        heading.to_edge(UP, buff=0.7).to_edge(LEFT, buff=0.9)
        self.play(Write(heading[0]), run_time=0.9)
        self.play(Create(heading[1]), run_time=0.4)

        # Two card panels
        left_card = panel(4.5, 3.8, radius=0.22, fill=SURFACE, stroke=BORDER)
        right_card = panel(4.5, 3.8, radius=0.22, fill=SURFACE, stroke=BORDER)
        left_card.move_to(LEFT * 3.3 + DOWN * 0.5)
        right_card.move_to(RIGHT * 3.3 + DOWN * 0.5)

        left_lbl = mono("AFFINE  (6 DoF)", size=18, color=EARTH, weight=BOLD)
        left_lbl.next_to(left_card, UP, buff=0.15)
        right_lbl = mono("HOMOGRAPHY  (8 DoF)", size=18, color=CORAL, weight=BOLD)
        right_lbl.next_to(right_card, UP, buff=0.15)

        self.play(FadeIn(left_card), FadeIn(right_card), Write(left_lbl), Write(right_lbl), run_time=1.0)

        grid_left = self.make_grid(color=EARTH, center=left_card.get_center())
        grid_right = self.make_grid(color=CORAL, center=right_card.get_center())

        self.play(Create(grid_left), Create(grid_right), run_time=1.6)
        self.wait(0.9)

        # Affine: clean rotate + skew
        self.play(
            grid_left.animate.rotate(10 * DEGREES).shift(RIGHT * 0.15),
            run_time=1.6,
        )
        self.play(
            grid_left.animate.apply_matrix(
                np.array([[1.0, 0.15, 0], [0.0, 1.0, 0], [0, 0, 1]])
            ),
            run_time=1.5,
        )
        self.wait(1.0)

        # Homography warp
        cr = right_card.get_center()
        def warp(point):
            x, y, z = point - cr
            denom = 1 + 0.12 * x + 0.08 * y
            nx = (1.0 * x + 0.1 * y) / denom
            ny = (0.05 * x + 1.0 * y) / denom
            return np.array([nx + cr[0], ny + cr[1], z])

        self.play(grid_right.animate.apply_function(warp), run_time=2.0)
        self.wait(1.0)

        # Number reveal on a pill
        num_card = panel(7.5, 1.0, radius=0.4, fill=PANEL2, stroke=BORDER)
        nums = VGroup(
            sans("9.74 px", size=30, color=EARTH, weight=BOLD),
            mono("vs", size=18, color=DIM),
            sans("12.34 px", size=30, color=CORAL, weight=BOLD),
        ).arrange(RIGHT, buff=0.55)
        nums.move_to(num_card.get_center())
        num_row = VGroup(num_card, nums).to_edge(DOWN, buff=0.55)
        self.play(FadeIn(num_card), FadeIn(nums, shift=UP * 0.2), run_time=1.2)
        cleanup(self)

    def make_grid(self, color, center):
        g = VGroup()
        size = 2.6
        n = 6
        step = size / n
        for i in range(n + 1):
            v = Line(
                np.array([-size / 2 + i * step, -size / 2, 0]),
                np.array([-size / 2 + i * step, size / 2, 0]),
                color=color, stroke_width=2,
            )
            h = Line(
                np.array([-size / 2, -size / 2 + i * step, 0]),
                np.array([size / 2, -size / 2 + i * step, 0]),
                color=color, stroke_width=2,
            )
            g.add(v, h)
        g.shift(center)
        return g


# ---------- Scene 10: Cross-Dataset Transfer ----------
class S10_Cross(Scene):
    def construct(self):
        self.camera.background_color = BG

        heading = header_with_rule(
            "does the ranking hold across datasets?",
            color=MOON, accent=PERI, size=32,
        )
        heading.to_edge(UP, buff=0.7).to_edge(LEFT, buff=0.9)
        self.play(Write(heading[0]), run_time=0.9)
        self.play(Create(heading[1]), run_time=0.4)

        # Three dataset cards
        def ds_card(name, metric, value, accent):
            card = panel(3.6, 2.2, radius=0.22, fill=SURFACE, stroke=BORDER)
            rule = Line(LEFT * 0.7, RIGHT * 0.7, color=accent, stroke_width=3)
            nm = sans(name, size=24, color=accent, weight=BOLD)
            mt = caption(metric, color=DIM)
            val = sans(value, size=30, color=MOON, weight=BOLD)
            nm.move_to(card.get_center() + UP * 0.7)
            rule.next_to(nm, DOWN, buff=0.15)
            mt.move_to(card.get_center() + DOWN * 0.05)
            val.move_to(card.get_center() + DOWN * 0.55)
            return VGroup(card, nm, rule, mt, val)

        sn9 = ds_card("SpaceNet9", "mean tie-point err", "3.0 px", PERI)
        srif = ds_card("SRIF", "mean corner err", "47.0 px", AMBER)
        sarp = ds_card("SARptical", "AUROC retrieval", "0.57", EARTH)
        cards = VGroup(sn9, srif, sarp).arrange(RIGHT, buff=0.5).shift(UP * 0.6)

        for c in cards:
            self.play(FadeIn(c, shift=UP * 0.2), run_time=1.0)
            self.wait(0.4)
        self.wait(1.0)

        # Banner (moon-ish fill to read as the conclusion)
        banner = panel(11.0, 1.0, radius=0.45, fill=PANEL2, stroke=PERI, stroke_width=2)
        banner.next_to(cards, DOWN, buff=0.65)
        btxt = sans(
            "MINIMA-RoMa  .  strongest zero-failure cross-dataset consistency",
            size=20, color=MOON, weight=BOLD,
        )
        btxt.move_to(banner.get_center())
        self.play(FadeIn(banner), Write(btxt), run_time=1.6)

        for c in cards:
            start = np.array([c.get_center()[0], banner.get_top()[1], 0])
            a = Arrow(
                start=start,
                end=c.get_bottom(),
                color=PERI, buff=0.08, stroke_width=2.5,
                max_tip_length_to_length_ratio=0.35,
            )
            self.play(Create(a), run_time=0.45)

        cleanup(self)


# ---------- Scene 11: Runtime Pareto ----------
class S11_Pareto(Scene):
    def construct(self):
        self.camera.background_color = BG

        heading = header_with_rule(
            "error vs runtime  .  XoFTR is the Pareto star",
            color=MOON, accent=EARTH, size=28,
        )
        heading.to_edge(UP, buff=0.7).to_edge(LEFT, buff=0.9)
        self.play(Write(heading[0]), run_time=0.9)
        self.play(Create(heading[1]), run_time=0.4)

        plot = panel(12.0, 4.8, radius=0.22, fill=SURFACE, stroke=BORDER)
        plot.move_to(DOWN * 0.5)
        self.play(FadeIn(plot), run_time=0.6)

        x_left, x_right = -5.2, 5.2
        y_bot, y_top = -2.4, 1.3
        xa = Line(np.array([x_left, y_bot, 0]), np.array([x_right, y_bot, 0]), color=DIM, stroke_width=1.2)
        ya = Line(np.array([x_left, y_bot, 0]), np.array([x_left, y_top, 0]), color=DIM, stroke_width=1.2)
        xlab = caption("runtime per pair (s)", color=DIM).next_to(xa, DOWN, buff=0.22)
        ylab = caption("mean error (px)", color=DIM).rotate(PI / 2).next_to(ya, LEFT, buff=0.22)

        self.play(Create(xa), Create(ya), Write(xlab), Write(ylab), run_time=0.8)

        def x_for(t):
            return np.interp(t, [0, 12], [x_left + 0.3, x_right - 0.3])
        def y_for(e):
            return np.interp(e, [2.5, 7.0], [y_top - 0.2, y_bot + 0.3])

        tick_g = VGroup()
        for t in [0, 2, 4, 6, 8, 10, 12]:
            tk = Line(
                np.array([x_for(t), y_bot - 0.08, 0]),
                np.array([x_for(t), y_bot + 0.08, 0]),
                color=DIM, stroke_width=1.2,
            )
            lb = caption(str(t), color=DIM).scale(0.7).next_to(tk, DOWN, buff=0.05)
            tick_g.add(tk, lb)
        for e in [3, 4, 5, 6, 7]:
            tk = Line(
                np.array([x_left - 0.08, y_for(e), 0]),
                np.array([x_left + 0.08, y_for(e), 0]),
                color=DIM, stroke_width=1.2,
            )
            lb = caption(str(e), color=DIM).scale(0.7).next_to(tk, LEFT, buff=0.08)
            tick_g.add(tk, lb)
        self.play(FadeIn(tick_g), run_time=0.5)

        points = [
            ("XoFTR",         0.4, 3.0, np.array([0.75, 0.48, 0])),
            ("RoMa",          5.0, 3.0, UP * 0.4),
            ("MA-ELoFTR",     4.7, 3.4, DOWN * 0.4 + LEFT * 0.25),
            ("MINIMA-RoMa",   5.5, 3.7, DOWN * 0.4 + RIGHT * 0.3),
            ("LoFTR",         5.6, 5.1, UP * 0.4),
            ("XFeat",         0.3, 6.5, RIGHT * 0.45),
            ("SuperPoint-LG", 0.4, 4.4, DOWN * 0.35 + RIGHT * 0.8),
            ("MASt3R",        2.5, 4.5, UP * 0.4),
            ("OmniGlue",     11.5, 5.6, UP * 0.4 + LEFT * 0.2),
        ]

        dots = VGroup()
        labels = VGroup()
        xoftr_dot = None
        for name, t, e, offset in points:
            p = np.array([x_for(t), y_for(e), 0])
            is_xoftr = name == "XoFTR"
            d = Dot(
                p,
                radius=0.13 if is_xoftr else 0.085,
                color=EARTH if is_xoftr else PERI,
            ).set_opacity(1 if is_xoftr else 0.85)
            lbl = mono(name, size=11, color=MOON if is_xoftr else DIM, weight=BOLD if is_xoftr else NORMAL)
            lbl.move_to(p + offset)
            dots.add(d)
            labels.add(lbl)
            if is_xoftr:
                xoftr_dot = d

        self.play(FadeIn(dots, lag_ratio=0.10), FadeIn(labels, lag_ratio=0.10), run_time=2.2)
        self.wait(1.0)

        # Pareto frontier: (XFeat 0.3, 6.5) -> (XoFTR 0.4, 3.0) -> (RoMa 5.0, 3.0)
        frontier = DashedLine(
            np.array([x_for(0.3), y_for(6.5), 0]),
            np.array([x_for(0.4), y_for(3.0), 0]),
            color=EARTH, stroke_width=2,
        )
        frontier2 = DashedLine(
            np.array([x_for(0.4), y_for(3.0), 0]),
            np.array([x_for(5.0), y_for(3.0), 0]),
            color=EARTH, stroke_width=2,
        )
        self.play(Create(frontier), Create(frontier2), run_time=1.4)
        self.wait(0.8)

        star = Star(n=5, outer_radius=0.32, color=EARTH, fill_opacity=0.0, stroke_width=3)
        star.move_to(xoftr_dot.get_center())
        self.play(GrowFromCenter(star), run_time=0.9)

        tag_card = panel(7.0, 0.75, radius=0.35, fill=PANEL2, stroke=BORDER)
        tag_txt = mono(
            "top-tier accuracy at 0.4s/pair  .  ~12x faster than RoMa",
            size=16, color=EARTH, weight=BOLD,
        )
        tag_txt.move_to(tag_card.get_center())
        tag = VGroup(tag_card, tag_txt).to_edge(DOWN, buff=0.55)
        self.play(FadeIn(tag), run_time=1.1)
        cleanup(self)


# ---------- Scene 12: Takeaways + Recipe + CTA ----------
class S12_Recipe(Scene):
    def construct(self):
        self.camera.background_color = BG

        heading = header_with_rule(
            "takeaways",
            color=MOON, accent=EARTH, size=42,
        )
        heading.to_edge(UP, buff=0.7).to_edge(LEFT, buff=0.9)
        self.play(Write(heading[0]), run_time=0.9)
        self.play(Create(heading[1]), run_time=0.4)

        # Three stat chips on an arranged row
        c1 = stat_chip("DINOv2 backbones", "emergent modality invariance", EARTH,
                       width=4.2, height=2.0)
        c2 = stat_chip("protocol > matcher", "accuracy swings 33x", CORAL,
                       width=4.2, height=2.0)
        c3 = stat_chip("affine wins", "9.74 vs 12.34 px, ortho", PERI,
                       width=4.2, height=2.0)
        takes = VGroup(c1, c2, c3).arrange(RIGHT, buff=0.3)
        takes.shift(UP * 1.3)

        for c in takes:
            self.play(FadeIn(c, shift=UP * 0.2), run_time=0.9)
            self.wait(0.3)

        # Recipe banner
        recipe_card = panel(12.0, 1.3, radius=0.3, fill=PANEL2, stroke=EARTH, stroke_width=2)
        recipe_title = mono("DEPLOYMENT RECIPE", size=14, color=EARTH, weight=BOLD)
        recipe_title.move_to(recipe_card.get_center() + UP * 0.32)
        recipe_body = mono(
            "affine  .  768 tile / 128 overlap  .  percentile norm  .  RANSAC <= 10 px  .  RoMa or MINIMA-RoMa",
            size=13, color=MOON,
        )
        recipe_body.move_to(recipe_card.get_center() + DOWN * 0.18)
        recipe = VGroup(recipe_card, recipe_title, recipe_body)
        recipe.next_to(takes, DOWN, buff=0.35)
        self.play(FadeIn(recipe_card), Write(recipe_title), Write(recipe_body), run_time=1.8)
        self.wait(0.6)

        # CTA pill (the one MOON-filled object in the video)
        cta_card = panel(6.4, 0.9, radius=0.45, fill=MOON, stroke=MOON)
        cta_txt = sans("github.com/isaaccorley/rsim", size=22, color=BG, weight=BOLD)
        cta_txt.move_to(cta_card.get_center())
        cta = VGroup(cta_card, cta_txt)
        cta.next_to(recipe, DOWN, buff=0.35)

        credit = caption(
            "Isaac Corley  .  Taylor Geospatial  .  CVPR IMW 2026",
            color=DIM,
        )
        credit.next_to(cta, DOWN, buff=0.18)

        self.play(GrowFromCenter(cta_card), Write(cta_txt), run_time=1.2)
        self.play(FadeIn(credit), run_time=0.6)
        cleanup(self)
