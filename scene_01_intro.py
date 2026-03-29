from manim import *

class Intro(Scene):
    def construct(self):
        # 1. Title
        title = Text("Symbolic Music Generation\nwith Diffusion Models", font_size=40, weight=BOLD, line_spacing=0.8)
        authors = Text("Mittal, Engel, Hawthorne, Simon", font_size=24, color=ORANGE)
        venue = Text("ISMIR 2021", font_size=22, color=BLUE)
        presenter = Text("Presented by Adam Rehman", font_size=22, color=GREEN)

        header = VGroup(title, authors, venue, presenter).arrange(DOWN, buff=0.4)

        self.play(Write(title, run_time=1.5))
        self.play(FadeIn(authors, shift=UP * 0.3))
        self.play(FadeIn(venue, shift=UP * 0.2))
        self.play(FadeIn(presenter, shift=UP * 0.2))
        self.wait(15.0)

        # 2. Shrink header, show overview diagram
        self.play(header.animate.scale(0.45).to_edge(UP, buff=0.2))

        # Overview: three key contribution "states" as labeled dots
        c1 = LabeledDot(
            label=Tex("Latent\\\\Diffusion", font_size=22),
            color=BLUE, radius=0.6
        ).shift(LEFT * 3.5 + DOWN * 0.8)
        c2 = LabeledDot(
            label=Tex("Long-form\\\\Generation", font_size=22),
            color=GREEN, radius=0.6
        ).shift(DOWN * 0.8)
        c3 = LabeledDot(
            label=Tex("Conditional\\\\Infilling", font_size=22),
            color=ORANGE, radius=0.6
        ).shift(RIGHT * 3.5 + DOWN * 0.8)

        # Descriptions below each
        d1 = Text("DDPM in MusicVAE\nlatent space", font_size=16, color=BLUE).next_to(c1, DOWN, buff=0.3)
        d2 = Text("64 bars / 1024\ntokens", font_size=16, color=GREEN).next_to(c2, DOWN, buff=0.3)
        d3 = Text("Fill gaps without\nretraining", font_size=16, color=ORANGE).next_to(c3, DOWN, buff=0.3)

        # Connect with arrows
        a1 = Arrow(c1.get_right(), c2.get_left(), buff=0.1, color=WHITE, stroke_width=2)
        a2 = Arrow(c2.get_right(), c3.get_left(), buff=0.1, color=WHITE, stroke_width=2)

        self.play(FadeIn(c1), FadeIn(d1))
        self.play(GrowArrow(a1), FadeIn(c2), FadeIn(d2))
        self.play(GrowArrow(a2), FadeIn(c3), FadeIn(d3))
        self.wait(22.5)

        self.play(*[FadeOut(m) for m in self.mobjects])
