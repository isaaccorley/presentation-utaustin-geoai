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
    EARTH,
    MOON,
    PANEL2,
    PERI,
    SURFACE,
    PacedScene,
    cleanup,
    mono,
    panel,
    sans,
    scene_tag,
    stat_chip,
)


class S06_STACSearchFanout(PacedScene):
    """STAC search fanning across catalogs, results streaming back."""

    def construct(self):
        self.camera.background_color = BG  # ty: ignore[invalid-assignment]
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
            a = Arrow(
                q_box.get_right(),
                cg[0].get_left(),
                color=PERI,
                stroke_width=1.5,
                buff=0.1,
                max_tip_length_to_length_ratio=0.1,
            )
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
            a = Arrow(
                cg[0].get_right(),
                results_box.get_left(),
                color=EARTH,
                stroke_width=1.5,
                buff=0.1,
                max_tip_length_to_length_ratio=0.1,
            )
            arrows_in.add(a)

        self.play(
            FadeIn(results_box), FadeIn(r_title), *[FadeIn(a) for a in arrows_in], run_time=0.6
        )
        for item in result_items:
            self.play(FadeIn(item, shift=DOWN * 0.1), run_time=0.25)
        self.wait(0.4)

        chip = stat_chip(
            "One query, many catalogs", "federated search across providers", PERI, width=5.5
        )
        chip.to_edge(DOWN, buff=0.35).to_edge(LEFT, buff=0.6)
        self.play(FadeIn(chip, shift=UP * 0.15), run_time=0.6)
        cleanup(self, hold=1.5)
