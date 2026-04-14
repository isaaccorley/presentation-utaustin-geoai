"""UT Austin GeoAI Talk — Extended scenes S05–S17 (Isaac Corley)"""

from manim import (
    DOWN,
    LEFT,
    RIGHT,
    UP,
    Arrow,
    FadeIn,
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
    cleanup,
    panel,
    sans,
    scene_tag,
    stat_chip,
)


class S13_ProductionPipeline(PacedScene):
    """Post-processing + productionization: model output is just the start."""

    def construct(self):
        self.camera.background_color = BG  # ty: ignore[invalid-assignment]
        tag = scene_tag("production pipeline", accent=CORAL)
        self.play(FadeIn(tag), run_time=0.6)

        title = sans("After Inference", size=28, color=CORAL)
        title.next_to(tag, DOWN, buff=0.25).to_edge(LEFT, buff=0.9)
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
        row1_lbl.next_to(title, DOWN, buff=0.25).to_edge(LEFT, buff=0.9)
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
        # Scale to fit frame width, then center horizontally
        if row1_boxes.width > 12.0:
            row1_boxes.scale(12.0 / row1_boxes.width)
        row1_boxes.next_to(row1_lbl, DOWN, buff=0.2)
        row1_boxes.set_x(0)  # center horizontally on frame

        row1_arrows = VGroup()
        for i in range(len(row1_boxes) - 1):
            a = Arrow(
                row1_boxes[i][0].get_right(),
                row1_boxes[i + 1][0].get_left(),
                color=DIM,
                stroke_width=1.2,
                buff=0.04,
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
        if row2_boxes.width > 12.0:
            row2_boxes.scale(12.0 / row2_boxes.width)
        row2_boxes.next_to(row2_lbl, DOWN, buff=0.2)
        row2_boxes.set_x(0)  # center horizontally on frame

        row2_arrows = VGroup()
        for i in range(len(row2_boxes) - 1):
            a = Arrow(
                row2_boxes[i][0].get_right(),
                row2_boxes[i + 1][0].get_left(),
                color=DIM,
                stroke_width=1.2,
                buff=0.04,
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
            color=CORAL,
            stroke_width=2.0,
            buff=0.08,
            max_tip_length_to_length_ratio=0.1,
        )
        self.play(FadeIn(bridge), run_time=0.4)

        # Takeaway chip
        chip = stat_chip(
            "The extra mile",
            "separates production from prototype",
            CORAL,
            width=5.5,
        )
        chip.to_edge(DOWN, buff=0.3)
        self.play(FadeIn(chip, shift=UP * 0.15), run_time=0.6)
        cleanup(self, hold=2.0)


# ── S14: Cloud-Native Geospatial Timeline ────────────────────────────────
