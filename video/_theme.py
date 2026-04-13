"""Shared visual theme and helpers for GeoAI talk Manim scenes."""
import numpy as np
from manim import (
    BOLD,
    DOWN,
    LEFT,
    NORMAL,
    RIGHT,
    UP,
    FadeOut,
    Group,
    Line,
    RoundedRectangle,
    Scene,
    Square,
    Text,
    VGroup,
    config,
)

# ── Palette ──────────────────────────────────────────────────────────────

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

# ── Typography ───────────────────────────────────────────────────────────

MONO = "Menlo"
SANS = "Space Grotesk"

# ── Global config ────────────────────────────────────────────────────────

config.background_color = BG
config.pixel_width = 2560
config.pixel_height = 1440
config.frame_rate = 60

# Timing multiplier — set >1 to slow everything down
PACE = 2.0

# ── Factories ────────────────────────────────────────────────────────────


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


class PacedScene(Scene):
    """Scene subclass that applies PACE multiplier to all animations."""

    def play(self, *args, **kwargs):
        if "run_time" in kwargs:
            kwargs["run_time"] = kwargs["run_time"] * PACE
        super().play(*args, **kwargs)

    def wait(self, duration=1.0, **kwargs):
        super().wait(duration * PACE, **kwargs)


def cleanup(scene, hold=1.0):
    scene.wait(hold)
    scene.play(FadeOut(Group(*scene.mobjects)), run_time=0.6)


def mini_grid(rows, cols, cell, color, fill_color=None, fill_opacity=0.15):
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


def satellite_tile(rows, cols, cell, seed=42):
    """Grid of patches colored to simulate satellite imagery (green/brown/gray)."""
    rng = np.random.RandomState(seed)
    palette = ["#2D5F3A", "#4A7C59", "#6B8E5A", "#8B7355", "#A09070",
               "#7A8B6F", "#5C7A4A", "#9E8C6C", "#667755", "#3E6B48"]
    squares = VGroup()
    for r in range(rows):
        for c in range(cols):
            sq = Square(side_length=cell, stroke_width=0.6, color=BORDER)
            color = palette[rng.randint(len(palette))]
            sq.set_fill(color, opacity=rng.uniform(0.5, 0.85))
            sq.move_to(RIGHT * c * cell + DOWN * r * cell)
            squares.add(sq)
    squares.center()
    return squares


def format_card(name, desc, icon_mob, accent, w=2.8, h=1.5):
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
