from manim import *
import numpy as np

class Training(Scene):
    def construct(self):
        # ─── Title ───
        title = Text("Training Process", font_size=36, color=GREEN)
        self.play(Write(title))
        self.wait(2.2)
        self.play(title.animate.scale(0.6).to_edge(UP))

        # ─── Training Loop as a circular flow ───
        steps = [
            (r"z_0", "Sample\nlatent", BLUE),
            (r"t", "Sample\ntimestep", GREY),
            (r"\epsilon", "Sample\nnoise", RED),
            (r"z_t", "Create\nnoisy input", BLUE_D),
            (r"\hat{\epsilon}", "Predict\nnoise", ORANGE),
            (r"L", "Compute\nloss", GREEN),
        ]

        dots = VGroup()
        descs = VGroup()
        for i, (tex, desc, color) in enumerate(steps):
            d = LabeledDot(label=MathTex(tex, font_size=20), color=color, radius=0.4)
            t = Text(desc, font_size=12, line_spacing=0.6).next_to(d, DOWN, buff=0.15)
            dots.add(d)
            descs.add(t)

        # Arrange in a circle
        angle_step = TAU / len(steps)
        radius = 2.2
        for i, (d, t) in enumerate(zip(dots, descs)):
            angle = PI/2 - i * angle_step  # start from top
            pos = np.array([radius * np.cos(angle), radius * np.sin(angle), 0])
            d.move_to(pos)
            t.next_to(d, DOWN, buff=0.15)
            if angle < -PI/2 or angle > PI/2:
                t.next_to(d, UP, buff=0.15)

        # Curved arrows between steps
        flow_arrows = VGroup()
        for i in range(len(steps)):
            j = (i + 1) % len(steps)
            a = CurvedArrow(
                dots[i].get_center() + 0.45 * (dots[j].get_center() - dots[i].get_center()).astype(float) / np.linalg.norm((dots[j].get_center() - dots[i].get_center()).astype(float)),
                dots[j].get_center() + 0.45 * (dots[i].get_center() - dots[j].get_center()).astype(float) / np.linalg.norm((dots[i].get_center() - dots[j].get_center()).astype(float)),
                angle=-TAU/12,
                color=WHITE,
                stroke_width=1.5
            )
            flow_arrows.add(a)

        # Animate step by step
        for i in range(len(steps)):
            self.play(FadeIn(dots[i], scale=0.5), FadeIn(descs[i]))
            if i > 0:
                self.play(Create(flow_arrows[i-1]), run_time=0.4)
            self.wait(0.6)
        self.play(Create(flow_arrows[-1]), run_time=0.4)
        self.wait(15.0)
        self.play(*[FadeOut(m) for m in self.mobjects])

        # ─── Loss equation ───
        loss_title = Text("Loss Function", font_size=32, color=ORANGE)
        self.play(Write(loss_title))
        self.wait(2.2)
        self.play(loss_title.animate.scale(0.6).to_edge(UP))

        loss_eq = MathTex(
            r"L = \mathbb{E}_{t,\, z_0,\, \epsilon}",
            r"\Big[\,\|",
            r"\epsilon",
            r"-",
            r"\epsilon_\theta(z_t, t)",
            r"\|^2\,\Big]",
            font_size=38
        )
        loss_eq[2].set_color(BLUE)
        loss_eq[4].set_color(ORANGE)

        self.play(Write(loss_eq), run_time=1.5)
        self.wait(4.4)

        note = MathTex(
            r"\text{Operates on MusicVAE latent codes } z, \text{ not raw MIDI tokens}",
            font_size=24, color=GREEN
        ).next_to(loss_eq, DOWN, buff=0.6)
        self.play(Write(note))
        self.wait(4.4)

        # ─── Loss curve ───
        axes = Axes(
            x_range=[0, 10, 2], y_range=[0, 1, 0.2],
            x_length=5, y_length=2.5,
            axis_config={"color": GREY, "stroke_width": 1.5, "include_numbers": False},
            tips=False
        ).next_to(note, DOWN, buff=0.5)

        x_lbl = Text("Epochs", font_size=14, color=GREY).next_to(axes, DOWN, buff=0.1)
        y_lbl = Text("Loss", font_size=14, color=GREY).next_to(axes, LEFT, buff=0.1)

        curve = axes.plot(
            lambda x: 0.85 * np.exp(-0.45 * x) + 0.05,
            x_range=[0.01, 10], color=GREEN, stroke_width=2.5
        )

        self.play(Create(axes), FadeIn(x_lbl), FadeIn(y_lbl))
        self.play(Create(curve), run_time=2)

        dataset = Text("Dataset: Lakh MIDI (170K+ files)", font_size=18, color=BLUE)
        dataset.next_to(axes, RIGHT, buff=0.3)
        self.play(FadeIn(dataset))
        self.wait(22.5)

        self.play(*[FadeOut(m) for m in self.mobjects])
