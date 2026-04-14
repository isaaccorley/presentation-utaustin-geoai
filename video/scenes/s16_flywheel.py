"""UT Austin GeoAI Talk — Extended scenes S05–S17 (Isaac Corley)"""

from manim import (
    DOWN,
    LEFT,
    RIGHT,
    UP,
    Create,
    CurvedArrow,
    FadeIn,
    ScaleInPlace,
    VGroup,
)

from _theme import (
    AMBER,
    BG,
    CORAL,
    DIM,
    EARTH,
    PERI,
    SURFACE,
    PacedScene,
    caption,
    cleanup,
    panel,
    sans,
    scene_tag,
    stat_chip,
)


class S16_Flywheel(PacedScene):
    """Animated cycle diagram: People → Models → Global Datasets → People."""

    def construct(self):
        self.camera.background_color = BG  # ty: ignore[invalid-assignment]
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
            start = start_node[0].get_edge_center(end_node.get_center() - start_node.get_center())
            end = end_node[0].get_edge_center(start_node.get_center() - end_node.get_center())
            arrow = CurvedArrow(
                start,
                end,
                color=DIM,
                stroke_width=2.0,
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
