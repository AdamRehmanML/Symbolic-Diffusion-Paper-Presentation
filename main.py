"""
main.py — Hub-and-spoke presentation with zoom navigation.

Usage:
    manim -ql --disable_caching main.py FullPresentation
    manim -qm --disable_caching main.py FullPresentation
"""

from manim import *

from scene_01_intro import Intro
from scene_02_background import Background
from scene_03_diffusion_basics import DiffusionBasics
from scene_04_musicvae import MusicVAEScene
from scene_05_architecture import Architecture
from scene_06_training import Training
from scene_07_generation import Generation
from scene_08_results import Results
from scene_09_conclusion import Conclusion


class FullPresentation(MovingCameraScene):
    """Hub-based presentation: 3 topic nodes with camera zoom in/out."""

    def construct(self):

        # ═══════════════════════════════════════
        # 1. Intro (before hub)
        # ═══════════════════════════════════════
        Intro.construct(self)
        self.wait(0.6)

        # ═══════════════════════════════════════
        # 2. Build the Hub
        # ═══════════════════════════════════════
        hub_title = Text(
            "Symbolic Music Generation with Diffusion Models",
            font_size=28, color=WHITE,
        ).to_edge(UP, buff=0.5)

        # Three topic nodes
        ddpm_node = VGroup(
            Circle(radius=0.9, color=BLUE, fill_opacity=0.15, stroke_width=3),
            Text("Markov Chains\n& Theory", font_size=20, color=BLUE),
        )
        arch_node = VGroup(
            Circle(radius=0.9, color=ORANGE, fill_opacity=0.15, stroke_width=3),
            Text("Latent VAE\nArchitecture", font_size=20, color=ORANGE),
        )
        meth_node = VGroup(
            Circle(radius=0.9, color=GREEN, fill_opacity=0.15, stroke_width=3),
            Text("Training &\nGeneration", font_size=20, color=GREEN),
        )

        # Subtitles
        ddpm_sub = Text("Forward & Reverse Diffusion", font_size=12, color=GREY).next_to(ddpm_node, DOWN, buff=0.15)
        arch_sub = Text("Continuous Embeddings", font_size=12, color=GREY).next_to(arch_node, DOWN, buff=0.15)
        meth_sub = Text("Loss Objective & Results", font_size=12, color=GREY).next_to(meth_node, DOWN, buff=0.15)

        nodes = VGroup(
            VGroup(ddpm_node, ddpm_sub),
            VGroup(arch_node, arch_sub),
            VGroup(meth_node, meth_sub),
        )
        nodes.arrange(RIGHT, buff=1.8).shift(DOWN * 0.3)

        # Connecting lines
        conn1 = DashedLine(ddpm_node.get_right(), arch_node.get_left(), color=GREY, dash_length=0.08)
        conn2 = DashedLine(arch_node.get_right(), meth_node.get_left(), color=GREY, dash_length=0.08)

        hub_group = VGroup(hub_title, nodes, conn1, conn2)

        # Store default camera state
        default_width = self.camera.frame.width
        default_center = self.camera.frame.get_center().copy()

        # Animate hub entrance
        self.play(
            Write(hub_title),
            LaggedStart(*[FadeIn(n, scale=0.7) for n in nodes], lag_ratio=0.15),
            run_time=1.5,
        )
        self.play(Create(conn1), Create(conn2))
        self.wait(6.6)

        # ═══════════════════════════════════════
        # Helper: zoom into a node, play scenes, zoom back
        # ═══════════════════════════════════════
        def zoom_section(node_group, node_circle, scene_classes, check_color):
            """Highlight node, zoom in, play content, zoom back, add checkmark."""
            node_vg, node_sub = node_group[0], node_group[1]

            # Highlight the selected node
            self.play(
                node_circle.animate.set_fill(opacity=0.35),
                Indicate(node_vg, color=check_color, scale_factor=1.1),
            )
            self.wait(0.6)

            # Zoom camera into the node
            self.play(
                self.camera.frame.animate.set(width=4).move_to(node_vg.get_center()),
                *[FadeOut(m) for m in hub_group if m is not node_group],
                run_time=1.5,
            )
            self.wait(0.6)

            # Fade out the node itself before playing content
            self.play(FadeOut(node_vg), FadeOut(node_sub))

            # Reset camera for content (standard frame)
            self.play(
                self.camera.frame.animate.set(width=default_width).move_to(ORIGIN),
                run_time=0.5,
            )

            # Play section scenes
            for SceneClass in scene_classes:
                SceneClass.construct(self)
                self.wait(0.4)

            # Group any mobjects left on screen after the final scene (the final frame)
            # This allows us to transition from the scene back to the hub smoothly
            leftover_mobjects = VGroup(*[m for m in self.mobjects if m not in [self.camera.frame, self.camera, node_vg, node_sub] and m not in hub_group])
            
            check = Text("✓", font_size=28, color=check_color).move_to(node_vg.get_center())

            # Zoom back out to hub layout effect: 
            # Shrink the remaining scene elements back into the node while fading them out,
            # and simultaneously fade the hub back in
            if len(leftover_mobjects) > 0:
                self.play(
                    leftover_mobjects.animate.scale(0.05).move_to(node_vg.get_center()).set_opacity(0),
                    *[FadeIn(m) for m in hub_group],
                    run_time=1.2,
                )
                self.remove(*leftover_mobjects)
            else:
                self.play(*[FadeIn(m) for m in hub_group], run_time=1.2)
                
            self.play(FadeIn(check, scale=1.5))
            self.wait(7.5)

            return check

        # ═══════════════════════════════════════
        # 3. DDPM Section
        # ═══════════════════════════════════════
        check1 = zoom_section(
            nodes[0], ddpm_node[0],
            [Background, DiffusionBasics],
            BLUE,
        )

        # ═══════════════════════════════════════
        # 4. Architectures Section
        # ═══════════════════════════════════════
        check2 = zoom_section(
            nodes[1], arch_node[0],
            [MusicVAEScene, Architecture],
            ORANGE,
        )

        # ═══════════════════════════════════════
        # 5. Methods Section
        # ═══════════════════════════════════════
        check3 = zoom_section(
            nodes[2], meth_node[0],
            [Training, Generation, Results],
            GREEN,
        )

        # ═══════════════════════════════════════
        # 6. Conclusion (after hub)
        # ═══════════════════════════════════════
        self.play(*[FadeOut(m) for m in self.mobjects])
        Conclusion.construct(self)
