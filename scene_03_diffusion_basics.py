from manim import *

class DiffusionBasics(Scene):
    def construct(self):
        # ─── Part A: Forward Process ───
        title = Text("Forward Diffusion Process", font_size=36, color=GREEN)
        self.play(Write(title))
        self.wait(1)
        self.play(title.animate.scale(0.6).to_edge(UP))

        # Equation
        equation = MathTex(
            r"q(x_t | x_{t-1}) = \mathcal{N}(x_t;\, \sqrt{1 - \beta_t}\, x_{t-1},\, \beta_t \mathbf{I})",
            font_size=32
        )
        self.play(Write(equation))
        self.wait(2)
        self.play(equation.animate.to_edge(UP, buff=0.8).scale(0.8))

        # Forward chain as LabeledDots (like markov_chain.py)
        n = 6
        labels_txt = ["x_0", "x_1", "x_2", "\\cdots", "x_{T-1}", "x_T"]
        colors = [BLUE, BLUE_D, BLUE_E, GREY, DARK_BLUE, GREY_D]
        
        states = VGroup()
        for i in range(n):
            s = LabeledDot(
                label=MathTex(labels_txt[i], font_size=22),
                color=colors[i], radius=0.4
            )
            states.add(s)
        states.arrange(RIGHT, buff=0.7)

        # Forward arrows with q labels
        fwd_arrows = VGroup()
        for i in range(n - 1):
            a = CurvedArrow(
                states[i].get_right(), states[i+1].get_left(),
                angle=-TAU/10, color=WHITE
            )
            fwd_arrows.add(a)

        q_label = MathTex(r"q(\cdot)", font_size=22, color=YELLOW).next_to(fwd_arrows[0], UP, buff=0.15)
        noise_label = Text("+ noise", font_size=16, color=RED).next_to(fwd_arrows, DOWN, buff=0.15)

        self.play(LaggedStart(*[FadeIn(s) for s in states], lag_ratio=0.12))
        self.play(
            LaggedStart(*[Create(a) for a in fwd_arrows], lag_ratio=0.08),
            Write(q_label), FadeIn(noise_label)
        )
        self.wait(2)

        # ─── Part B: Reverse Process ───
        # Move forward chain up
        fwd_group = VGroup(states, fwd_arrows, q_label, noise_label)
        self.play(fwd_group.animate.shift(UP * 0.8), FadeOut(equation))

        rev_title = Text("Reverse Process (Learned)", font_size=28, color=YELLOW).to_edge(UP)
        self.play(Write(rev_title))

        rev_eq = MathTex(
            r"p_\theta(x_{t-1}|x_t) = \mathcal{N}(x_{t-1};\, \mu_\theta(x_t, t),\, \sigma_t^2 \mathbf{I})",
            font_size=30, color=YELLOW
        ).next_to(states, DOWN, buff=0.8)
        self.play(Write(rev_eq))
        self.wait(1)

        # Reverse arrows
        rev_arrows = VGroup()
        for i in range(n - 1):
            a = CurvedArrow(
                states[i+1].get_left(), states[i].get_right(),
                angle=-TAU/10, color=YELLOW
            )
            rev_arrows.add(a)

        p_label = MathTex(r"p_\theta(\cdot)", font_size=22, color=YELLOW).next_to(rev_arrows[-1], DOWN, buff=0.15)
        denoise_label = Text("denoise", font_size=16, color=GREEN).next_to(rev_arrows, UP, buff=0.6)

        self.play(
            LaggedStart(*[Create(a) for a in rev_arrows], lag_ratio=0.08),
            Write(p_label), FadeIn(denoise_label)
        )
        self.wait(2)
        self.play(*[FadeOut(m) for m in self.mobjects])

        # ─── Part C: Training Objective ───
        obj_title = Text("Training Objective", font_size=36, color=GREEN)
        self.play(Write(obj_title))
        self.wait(0.5)
        self.play(obj_title.animate.scale(0.6).to_edge(UP))

        loss = MathTex(
            r"L_{\text{simple}}",
            r"=",
            r"\mathbb{E}_{t,\, x_0,\, \epsilon}",
            r"\Big[\,\|",
            r"\epsilon",
            r"-",
            r"\epsilon_\theta(x_t, t)",
            r"\|^2\,\Big]",
            font_size=38
        )
        loss[0].set_color(GREEN)
        loss[4].set_color(BLUE)
        loss[6].set_color(YELLOW)

        self.play(Write(loss), run_time=1.5)
        self.wait(1)

        # Color-coded explanation using LabeledDots
        eps_dot = LabeledDot(label=MathTex(r"\epsilon", font_size=20), color=BLUE, radius=0.3)
        eps_desc = Text("= sampled noise", font_size=18)
        eps_row = VGroup(eps_dot, eps_desc).arrange(RIGHT, buff=0.2)

        epsth_dot = LabeledDot(label=MathTex(r"\epsilon_\theta", font_size=18), color=YELLOW, radius=0.3)
        epsth_desc = Text("= predicted noise", font_size=18)
        epsth_row = VGroup(epsth_dot, epsth_desc).arrange(RIGHT, buff=0.2)

        legend = VGroup(eps_row, epsth_row).arrange(DOWN, buff=0.3, aligned_edge=LEFT)
        legend.next_to(loss, DOWN, buff=0.7)

        self.play(FadeIn(legend))

        box = SurroundingRectangle(loss, color=GREEN, buff=0.15, stroke_width=2)
        self.play(Create(box))
        self.wait(3)

        self.play(*[FadeOut(m) for m in self.mobjects])
