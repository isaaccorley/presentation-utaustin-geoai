"""UT Austin GeoAI Talk — Extended scenes S05–S17 (Isaac Corley)"""

from manim import (
    DOWN,
    LEFT,
    RIGHT,
    UP,
    Arrow,
    DashedLine,
    FadeIn,
    VGroup,
)

from _theme import (
    BG,
    CORAL,
    DIM,
    EARTH,
    MOON,
    PANEL2,
    PERI,
    SURFACE,
    PacedScene,
    caption,
    cleanup,
    mono,
    panel,
    scene_tag,
    stat_chip,
)


class S12_CloudNativeVsDownload(PacedScene):
    """Split-screen: download everything (old) vs cloud-native streaming (new)."""

    def construct(self):
        self.camera.background_color = BG  # ty: ignore[invalid-assignment]
        tag = scene_tag("old way vs new way", accent=CORAL)
        self.play(FadeIn(tag), run_time=0.6)

        divider = DashedLine(UP * 3.2, DOWN * 3.2, color=DIM, stroke_width=1.0, dash_length=0.12)
        self.play(FadeIn(divider), run_time=0.4)

        cloud = panel(2.5, 1.0, fill=PANEL2)
        cloud_lbl = caption("Cloud Storage", size=13, color=DIM)
        cloud.to_edge(LEFT, buff=1.2).to_edge(UP, buff=1.25)
        cloud_lbl.move_to(cloud)

        disk = panel(2.5, 1.0, fill=SURFACE)
        disk_lbl = caption("Local Disk", size=13, color=CORAL)
        disk.next_to(cloud, DOWN, buff=0.9)
        disk_lbl.move_to(disk)

        big_arr = Arrow(
            cloud.get_bottom(),
            disk.get_top(),
            color=CORAL,
            stroke_width=3.0,
            buff=0.08,
            max_tip_length_to_length_ratio=0.08,
        )
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

        self.play(FadeIn(cloud), FadeIn(cloud_lbl), run_time=0.3)
        self.play(FadeIn(big_arr), FadeIn(dl_size), run_time=0.4)
        self.play(FadeIn(disk), FadeIn(disk_lbl), run_time=0.3)
        self.play(FadeIn(old_steps), FadeIn(old_time), run_time=0.5)
        self.wait(0.3)

        cloud2 = panel(2.5, 1.0, fill=PANEL2)
        cloud2_lbl = caption("COG on S3", size=13, color=PERI)
        cloud2.to_edge(RIGHT, buff=1.2).to_edge(UP, buff=1.25)
        cloud2_lbl.move_to(cloud2)

        mem = panel(2.5, 1.0, fill=SURFACE)
        mem_lbl = caption("In-Memory Array", size=13, color=EARTH)
        mem.next_to(cloud2, DOWN, buff=0.9)
        mem_lbl.move_to(mem)

        thin_arr = Arrow(
            cloud2.get_bottom(),
            mem.get_top(),
            color=EARTH,
            stroke_width=1.5,
            buff=0.08,
            max_tip_length_to_length_ratio=0.1,
        )
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

        self.play(FadeIn(cloud2), FadeIn(cloud2_lbl), run_time=0.3)
        self.play(FadeIn(thin_arr), FadeIn(dl_size2), run_time=0.4)
        self.play(FadeIn(mem), FadeIn(mem_lbl), run_time=0.3)
        self.play(FadeIn(new_steps), FadeIn(new_time), run_time=0.5)
        self.wait(0.5)

        chip = stat_chip("900x faster", "stream only the bytes you need", EARTH, width=4.5)
        chip.to_edge(DOWN, buff=0.3).to_edge(RIGHT, buff=0.8)
        self.play(FadeIn(chip, shift=UP * 0.15), run_time=0.6)
        cleanup(self, hold=2.0)
