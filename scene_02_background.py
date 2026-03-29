from manim import *
import random

class Background(Scene):
    def construct(self):
        # ─── Part A: Piano Roll ───
        title_a = Text("What is Symbolic Music?", font_size=36, color=GREEN)
        self.play(Write(title_a))
        self.wait(4.4)
        self.play(title_a.animate.scale(0.6).to_edge(UP))

        # Piano roll grid
        rows, cols = 8, 16
        cell = 0.3
        note_names = ["C", "D", "E", "F", "G", "A", "B", "C'"]
        melody = [0, 2, 4, 5, 4, 2, 3, 5, 7, 5, 4, 2, 0, 2, 4, 0]

        grid = VGroup()
        for r in range(rows):
            for c in range(cols):
                sq = Square(side_length=cell, stroke_width=0.5, stroke_color=GREY)
                sq.move_to(np.array([c * cell, r * cell, 0]))
                if melody[c] == r:
                    sq.set_fill(BLUE, opacity=0.8)
                grid.add(sq)

        labels = VGroup()
        for r in range(rows):
            lbl = Text(note_names[r], font_size=12, color=GREY)
            lbl.next_to(grid[r * cols], LEFT, buff=0.1)
            labels.add(lbl)

        piano_roll = VGroup(grid, labels).center().shift(DOWN * 0.3)
        time_lbl = Text("Time -->", font_size=16, color=GREY).next_to(piano_roll, DOWN, buff=0.2)

        desc = MathTex(r"\text{MIDI} = \text{sequence of discrete note events}", font_size=28).next_to(time_lbl, DOWN, buff=0.3)

        self.play(Create(piano_roll), run_time=1.5)
        self.play(FadeIn(time_lbl), Write(desc))
        self.wait(15.0)
        self.play(*[FadeOut(m) for m in self.mobjects])

        # ─── Part B: Autoregressive Problem ───
        title_b = Text("Autoregressive Models", font_size=36, color=RED)
        self.play(Write(title_b))
        self.wait(2.2)
        self.play(title_b.animate.scale(0.6).to_edge(UP))

        # Token chain as LabeledDots
        states = VGroup()
        for i in range(6):
            s = LabeledDot(label=MathTex(f"x_{{{i}}}", font_size=24), color=BLUE, radius=0.35)
            states.add(s)
        states.arrange(RIGHT, buff=0.8)

        arrows = VGroup()
        for i in range(5):
            a = Arrow(states[i].get_right(), states[i+1].get_left(), buff=0.05, color=WHITE, stroke_width=2)
            arrows.add(a)

        self.play(LaggedStart(*[FadeIn(s) for s in states], lag_ratio=0.15))
        self.play(LaggedStart(*[GrowArrow(a) for a in arrows], lag_ratio=0.1))
        self.wait(4.4)

        # Error propagation - highlight with red
        problem = Text("Exposure bias: errors compound!", font_size=22, color=RED)
        problem.next_to(states, DOWN, buff=0.6)

        # Show error spreading
        err_circles = VGroup()
        for i in range(3, 6):
            c = Circle(radius=0.45, color=RED, stroke_width=2).move_to(states[i])
            err_circles.add(c)
        
        self.play(Create(err_circles[0]), Write(problem))
        self.play(Create(err_circles[1]))
        self.play(Create(err_circles[2]))
        self.wait(15.0)
        self.play(*[FadeOut(m) for m in self.mobjects])

        # ─── Part C: Motivation ───
        title_c = Text("Why Latent Diffusion?", font_size=36, color=ORANGE)
        self.play(Write(title_c))
        self.wait(2.2)
        self.play(title_c.animate.scale(0.6).to_edge(UP))

        # Show the key insight as a simple diagram
        discrete = LabeledDot(label=Tex("Discrete\\\\MIDI", font_size=20), color=RED, radius=0.55).shift(LEFT * 3)
        continuous = LabeledDot(label=Tex("Continuous\\\\Latent", font_size=20), color=GREEN, radius=0.55)
        diffusion = LabeledDot(label=Tex("DDPM", font_size=22), color=BLUE, radius=0.55).shift(RIGHT * 3)

        a1 = Arrow(discrete.get_right(), continuous.get_left(), buff=0.1, color=WHITE)
        a2 = Arrow(continuous.get_right(), diffusion.get_left(), buff=0.1, color=WHITE)
        l1 = MathTex(r"\text{MusicVAE}", font_size=22, color=ORANGE).next_to(a1, UP, buff=0.1)
        l2 = Text("Apply here!", font_size=18, color=GREEN).next_to(a2, UP, buff=0.1)

        cross = Cross(stroke_color=RED, stroke_width=3).scale(0.3).move_to(discrete)
        check = MathTex(r"\checkmark", font_size=40, color=GREEN).next_to(continuous, DOWN, buff=0.3)

        self.play(FadeIn(discrete), FadeIn(continuous), FadeIn(diffusion))
        self.play(GrowArrow(a1), Write(l1))
        self.play(GrowArrow(a2), Write(l2))
        self.wait(4.4)
        self.play(Create(cross))
        self.play(Write(check))

        insight = MathTex(
            r"\text{Can't diffuse discrete tokens} \rightarrow \text{diffuse latent codes instead!}",
            font_size=26, color=ORANGE
        ).next_to(VGroup(discrete, diffusion), DOWN, buff=0.8)
        self.play(Write(insight))
        self.wait(22.5)

        self.play(*[FadeOut(m) for m in self.mobjects])
