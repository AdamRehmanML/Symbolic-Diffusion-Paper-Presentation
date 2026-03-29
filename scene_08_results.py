from manim import *

class Results(Scene):
    def construct(self):
        # ─── Title ───
        title = Text("Results & Evaluation", font_size=36, color=GREEN)
        self.play(Write(title))
        self.wait(0.5)
        self.play(title.animate.scale(0.6).to_edge(UP))

        # ─── Comparison as nodes ───
        # Three models as LabeledDots with scores
        baseline = LabeledDot(
            label=Tex("Baseline\\\\Sampling", font_size=16),
            color=GREY, radius=0.5
        ).shift(LEFT * 3.5)
        rnn = LabeledDot(
            label=Tex("RNN\\\\(AR)", font_size=16),
            color=BLUE, radius=0.5
        )
        ours = LabeledDot(
            label=Tex("DDPM\\\\(Ours)", font_size=16),
            color=GREEN, radius=0.5
        ).shift(RIGHT * 3.5)

        # OA scores
        s1 = MathTex("OA = 0.52", font_size=24, color=GREY).next_to(baseline, DOWN, buff=0.3)
        s2 = MathTex("OA = 0.61", font_size=24, color=BLUE).next_to(rnn, DOWN, buff=0.3)
        s3 = MathTex("OA = 0.72", font_size=24, color=GREEN).next_to(ours, DOWN, buff=0.3)

        # Bar chart below each (simple rectangles)
        b1 = Rectangle(height=0.52*3, width=0.6, color=GREY, fill_opacity=0.3).next_to(s1, DOWN, buff=0.2)
        b2 = Rectangle(height=0.61*3, width=0.6, color=BLUE, fill_opacity=0.3).next_to(s2, DOWN, buff=0.2)
        b3 = Rectangle(height=0.72*3, width=0.6, color=GREEN, fill_opacity=0.3).next_to(s3, DOWN, buff=0.2)

        # Align bar bottoms
        bottom_y = min(b1.get_bottom()[1], b2.get_bottom()[1], b3.get_bottom()[1])
        for b in [b1, b2, b3]:
            b.move_to(b.get_center() + np.array([0, bottom_y - b.get_bottom()[1], 0]))

        # Arrows showing improvement
        arr1 = Arrow(baseline.get_right(), rnn.get_left(), buff=0.1, color=WHITE, stroke_width=1.5)
        arr2 = Arrow(rnn.get_right(), ours.get_left(), buff=0.1, color=WHITE, stroke_width=1.5)

        self.play(FadeIn(baseline), Write(s1), GrowFromEdge(b1, DOWN))
        self.play(GrowArrow(arr1), FadeIn(rnn), Write(s2), GrowFromEdge(b2, DOWN))
        self.play(GrowArrow(arr2), FadeIn(ours), Write(s3), GrowFromEdge(b3, DOWN))
        self.wait(1)

        # Highlight winner
        winner = SurroundingRectangle(VGroup(ours, s3), color=GREEN, buff=0.2, stroke_width=2)
        self.play(Create(winner))
        self.play(Indicate(ours, color=GREEN, scale_factor=1.1))
        self.wait(2)
        self.play(*[FadeOut(m) for m in self.mobjects])

        # ─── Key Findings ───
        find_title = Text("Key Findings", font_size=32, color=YELLOW)
        self.play(Write(find_title))
        self.wait(0.5)
        self.play(find_title.animate.scale(0.6).to_edge(UP))

        findings = [
            ("Coherent long-range structure over 64 bars", GREEN),
            ("No compounding errors (non-autoregressive)", GREEN),
            ("Flexible infilling without retraining", BLUE),
            ("Iterative refinement captures temporal dependencies", YELLOW),
        ]

        dots = VGroup()
        for i, (text, color) in enumerate(findings):
            d = LabeledDot(
                label=MathTex(str(i+1), font_size=20),
                color=color, radius=0.25
            )
            t = Text(text, font_size=20)
            row = VGroup(d, t).arrange(RIGHT, buff=0.3)
            dots.add(row)

        dots.arrange(DOWN, buff=0.35, aligned_edge=LEFT).next_to(find_title, DOWN, buff=0.5)

        for d in dots:
            self.play(FadeIn(d, shift=RIGHT * 0.2), run_time=0.6)
            self.wait(0.5)

        self.wait(2.5)
        self.play(*[FadeOut(m) for m in self.mobjects])
