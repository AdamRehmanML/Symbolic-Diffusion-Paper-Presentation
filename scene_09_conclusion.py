from manim import *

class Conclusion(Scene):
    def construct(self):
        # ─── Key Takeaways ───
        title = Text("Key Takeaways", font_size=36, color=GREEN)
        self.play(Write(title))
        self.wait(0.5)
        self.play(title.animate.scale(0.6).to_edge(UP))

        # Three takeaway nodes connected in a triangle
        t1 = LabeledDot(
            label=Tex("Latent\\\\Diffusion", font_size=18),
            color=BLUE, radius=0.55
        ).shift(UP * 0.5 + LEFT * 3)
        t1_desc = Text("Diffusion in MusicVAE's\ncontinuous latent space", font_size=16).next_to(t1, DOWN, buff=0.25)

        t2 = LabeledDot(
            label=Tex("Long-form\\\\Music", font_size=18),
            color=GREEN, radius=0.55
        ).shift(UP * 0.5 + RIGHT * 3)
        t2_desc = Text("64 bars of coherent\nmelody generation", font_size=16).next_to(t2, DOWN, buff=0.25)

        t3 = LabeledDot(
            label=Tex("Flexible\\\\Infilling", font_size=18),
            color=YELLOW, radius=0.55
        ).shift(DOWN * 2)
        t3_desc = Text("No retraining needed\nfor conditional tasks", font_size=16).next_to(t3, DOWN, buff=0.25)

        # Connecting arrows
        a1 = CurvedArrow(t1.get_right(), t2.get_left(), angle=-TAU/12, color=WHITE)
        a2 = CurvedArrow(t2.get_bottom(), t3.get_top(), angle=-TAU/12, color=WHITE)
        a3 = CurvedArrow(t3.get_left(), t1.get_bottom(), angle=-TAU/12, color=WHITE)

        self.play(FadeIn(t1), FadeIn(t1_desc))
        self.play(Create(a1), FadeIn(t2), FadeIn(t2_desc))
        self.play(Create(a2), FadeIn(t3), FadeIn(t3_desc))
        self.play(Create(a3))
        self.wait(2.5)
        self.play(*[FadeOut(m) for m in self.mobjects])

        # ─── Limitations ───
        lim_title = Text("Limitations", font_size=32, color=RED)
        self.play(Write(lim_title))
        self.wait(0.5)
        self.play(lim_title.animate.scale(0.6).to_edge(UP))

        lims = [
            "Quality bounded by MusicVAE reconstruction",
            "Only monophonic melodies (single track)",
            "Slower sampling than autoregressive models",
        ]

        lim_dots = VGroup()
        for i, text in enumerate(lims):
            d = LabeledDot(
                label=MathTex(str(i+1), font_size=20),
                color=RED, radius=0.25
            )
            t = Text(text, font_size=20)
            row = VGroup(d, t).arrange(RIGHT, buff=0.3)
            lim_dots.add(row)
        lim_dots.arrange(DOWN, buff=0.35, aligned_edge=LEFT).next_to(lim_title, DOWN, buff=0.5)

        for d in lim_dots:
            self.play(FadeIn(d, shift=RIGHT * 0.2), run_time=0.5)
            self.wait(0.4)
        self.wait(2)
        self.play(*[FadeOut(m) for m in self.mobjects])

        # ─── Thank You ───
        thanks = Text("Thank You!", font_size=48, color=GREEN, weight=BOLD)
        questions = Text("Questions?", font_size=28, color=YELLOW)
        ref = Text(
            'Mittal et al., "Symbolic Music Generation\nwith Diffusion Models", ISMIR 2021',
            font_size=18, color=GREY, line_spacing=0.7
        )
        end = VGroup(thanks, questions, ref).arrange(DOWN, buff=0.5)

        self.play(Write(thanks, run_time=1))
        self.play(FadeIn(questions, shift=UP * 0.2))
        self.play(FadeIn(ref, shift=UP * 0.15))
        self.wait(3)
        self.play(*[FadeOut(m) for m in self.mobjects])
