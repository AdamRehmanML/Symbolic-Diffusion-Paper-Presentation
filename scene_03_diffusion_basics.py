from manim import *
import numpy as np


def _make_swissroll(n=300, seed=42):
    """Generate 2D swissroll-like spiral data (ported from Welch Labs)."""
    rng = np.random.default_rng(seed)
    t = np.linspace(np.pi / 2, 5 * np.pi, n)
    noise = rng.normal(0, 0.08, n)
    x = t * np.cos(t) / (5 * np.pi) + noise
    y = t * np.sin(t) / (5 * np.pi) + rng.normal(0, 0.08, n)
    return np.column_stack([x, y])


class DiffusionBasics(Scene):
    """Scene 3 — Diffusion fundamentals with Swissroll visual + markov chain diagram."""

    def construct(self):

        # ══════════════════════════════════════
        # Part A: Markov Chain DDPM Diagram
        #   (directly inspired by markov_chain.py)
        # ══════════════════════════════════════

        title_a = Text("DDPM: A Markov Chain", font_size=36, color=GREEN)
        self.play(Write(title_a))
        self.wait(3.5)
        self.play(title_a.animate.scale(0.55).to_edge(UP))

        # --- States ---
        labels = ["x_0", "x_1", "x_2", "\\cdots", "x_{T-1}", "x_T"]
        colors = [BLUE, BLUE_D, BLUE_E, GREY, DARK_BLUE, GREY_D]

        states = VGroup()
        for lbl, col in zip(labels, colors):
            s = LabeledDot(
                label=MathTex(lbl, font_size=22),
                color=col, radius=0.35,
            )
            states.add(s)
        states.arrange(RIGHT, buff=1.2).shift(UP * 0.2)

        # --- Forward arrows (top, white) ---
        forward_arrows = VGroup()
        for i in range(len(states) - 1):
            a = CurvedArrow(
                states[i].get_right(), states[i + 1].get_left(),
                angle=-TAU / 10, color=WHITE, stroke_width=1.5,
            )
            forward_arrows.add(a)

        q_label = MathTex(
            r"q(x_t \mid x_{t-1})", font_size=24, color=WHITE,
        ).next_to(forward_arrows[0], UP, buff=0.15)

        # --- Reverse arrows (bottom, yellow) ---
        reverse_arrows = VGroup()
        for i in range(len(states) - 1):
            a = CurvedArrow(
                states[i + 1].get_left(), states[i].get_right(),
                angle=-TAU / 10, color=ORANGE, stroke_width=1.5,
            )
            reverse_arrows.add(a)

        p_label = MathTex(
            r"p_\theta(x_{t-1} \mid x_t)", font_size=24, color=ORANGE,
        ).next_to(reverse_arrows[-1], DOWN, buff=0.15)

        # Annotations
        data_lbl = Text("clean data", font_size=16, color=BLUE).next_to(states[0], DOWN, buff=0.6)
        noise_lbl = Text("pure noise", font_size=16, color=GREY).next_to(states[-1], DOWN, buff=0.6)

        # Animate (mirror markov_chain.py flow)
        self.play(FadeIn(states[0]), FadeIn(states[-1]))
        self.play(
            LaggedStart(*[FadeIn(s) for s in states[1:-1]], lag_ratio=0.1),
        )
        self.wait(2.2)

        # Forward
        self.play(
            LaggedStart(*[Create(a) for a in forward_arrows], lag_ratio=0.08),
            Write(q_label),
        )
        self.play(Indicate(q_label))
        self.play(FadeIn(data_lbl), FadeIn(noise_lbl))
        self.wait(6.6)

        # Reverse
        self.play(
            LaggedStart(*[Create(a) for a in reverse_arrows], lag_ratio=0.08),
            Write(p_label),
        )
        self.play(Indicate(p_label))
        self.wait(6.6)

        # Shrink to top
        chain_group = VGroup(
            states, forward_arrows, reverse_arrows,
            q_label, p_label, data_lbl, noise_lbl,
        )
        self.play(chain_group.animate.scale(0.7).to_edge(UP, buff=0.25), run_time=0.8)

        # --- Forward equation ---
        fwd_eq = MathTex(
            r"q(x_t \mid x_{t-1})",
            r"=",
            r"\mathcal{N}\!\left(x_t;\, \sqrt{1-\beta_t}\, x_{t-1},\, \beta_t \mathbf{I}\right)",
            font_size=30,
        )
        fwd_eq[0].set_color(WHITE)
        fwd_eq.next_to(chain_group, DOWN, buff=0.4)
        self.play(Write(fwd_eq), run_time=1.5)
        self.wait(4.4)

        # --- Reverse equation ---
        rev_eq = MathTex(
            r"p_\theta(x_{t-1} \mid x_t)",
            r"=",
            r"\mathcal{N}\!\left(x_{t-1};\, \mu_\theta(x_t,t),\, \sigma_t^2 \mathbf{I}\right)",
            font_size=30, color=ORANGE,
        )
        rev_eq.next_to(fwd_eq, DOWN, buff=0.35)
        self.play(Write(rev_eq), run_time=1.5)
        self.wait(15.0)

        self.play(*[FadeOut(m) for m in self.mobjects])

        # ══════════════════════════════════════
        # Part B: Swissroll Forward Diffusion
        #   (ported from Welch Labs p40_51.py)
        # ══════════════════════════════════════

        title_b = Text("Forward Process on 2-D Data", font_size=32, color=GREEN)
        self.play(Write(title_b))
        self.wait(2.2)
        self.play(title_b.animate.scale(0.55).to_edge(UP))

        # Axes (matching Welch Labs style)
        axes = Axes(
            x_range=[-1.4, 1.4, 0.5],
            y_range=[-1.4, 1.4, 0.5],
            x_length=5.5, y_length=5.5,
            axis_config={
                "color": GREY,
                "stroke_width": 1.5,
                "include_tip": True,
                "include_ticks": False,
                "tip_length": 0.15,
            },
        ).shift(DOWN * 0.3)

        # Generate swissroll data
        data = _make_swissroll(n=200, seed=42)
        scale = 3.0  # map [-1,1] data to axes

        dots = VGroup()
        for pt in data:
            screen_pt = axes.c2p(pt[0], pt[1])
            d = Dot(screen_pt, radius=0.04, color=ORANGE, fill_opacity=0.8)
            dots.add(d)

        self.play(Create(axes), run_time=0.8)
        self.play(LaggedStart(*[FadeIn(d, scale=0.3) for d in dots], lag_ratio=0.005), run_time=1.5)
        self.wait(4.4)

        # Step counter (ported from Welch Labs)
        step_text = Text("STEP", font_size=16, color=GREY).to_corner(DR, buff=0.6).shift(UP * 0.3)
        step_num = Text("0", font_size=28, color=GREY).next_to(step_text, UP, buff=0.1)
        self.play(FadeIn(step_text), FadeIn(step_num))

        # --- Forward diffusion: add noise over 50 steps ---
        n_steps = 50
        rng = np.random.default_rng(123)

        # Pre-compute random walks
        noise_scale = np.linspace(0.005, 0.04, n_steps)
        positions = data.copy()
        
        # STORE HISTORY FOR REVERSE
        history = [positions.copy()]

        for step in range(n_steps):
            noise = rng.normal(0, noise_scale[step], positions.shape)
            positions = positions + noise
            history.append(positions.copy())

            anims = []
            for i, d in enumerate(dots):
                target = axes.c2p(positions[i, 0], positions[i, 1])
                anims.append(d.animate.move_to(target))

            new_num = Text(str(step + 1), font_size=28, color=GREY).next_to(step_text, UP, buff=0.1)

            self.play(
                *anims,
                Transform(step_num, new_num),
                run_time=0.08,
                rate_func=linear,
            )

        self.wait(2.2)

        # Fade dots to grey to show they're now noise
        self.play(dots.animate.set_color(GREY_D).set_opacity(0.4), run_time=0.8)

        pure_noise = MathTex(
            r"x_T \sim \mathcal{N}(0, \mathbf{I})",
            font_size=30, color=GREY,
        ).next_to(axes, DOWN, buff=0.3)
        self.play(Write(pure_noise))
        self.wait(20.0)

        # ══════════════════════════════════════
        # NEW: Reverse Process (Denoising) GIF
        # ══════════════════════════════════════
        title_rev = Text("Reverse Process (Denoising)", font_size=32, color=ORANGE)
        self.play(
            FadeOut(pure_noise),
            Transform(title_b, title_rev.scale(0.55).to_edge(UP)),
        )
        self.wait(5.0)

        # Color the dots back to indicate active sampling
        self.play(dots.animate.set_color(ORANGE).set_opacity(0.8), run_time=0.8)

        # Animate backward using stored history
        for step in range(n_steps - 1, -1, -1):
            target_positions = history[step]
            anims = []
            for i, d in enumerate(dots):
                target = axes.c2p(target_positions[i, 0], target_positions[i, 1])
                anims.append(d.animate.move_to(target))

            new_num = Text(str(step), font_size=28, color=GREY).next_to(step_text, UP, buff=0.1)

            self.play(
                *anims,
                Transform(step_num, new_num),
                run_time=0.08,
                rate_func=linear,
            )
            
        self.wait(10.0)
        recovered = Text("Data Distribution Recovered!", font_size=28, color=ORANGE).next_to(axes, DOWN, buff=0.3)
        self.play(Write(recovered))
        self.wait(15.0)

        self.play(*[FadeOut(m) for m in self.mobjects])

        # ══════════════════════════════════════
        # Part C: Training Objective
        # ══════════════════════════════════════

        title_c = Text("Training Objective", font_size=36, color=GREEN)
        self.play(Write(title_c))
        self.wait(2.2)
        self.play(title_c.animate.scale(0.6).to_edge(UP))

        loss = MathTex(
            r"L_{\text{simple}}", # 0
            r"=", # 1
            r"\mathbb{E}_{t,\, x_0,\, \epsilon}", # 2
            r"\Big[\,\|", # 3
            r"\epsilon", # 4
            r"-", # 5
            r"\epsilon_\theta(x_t, t)", # 6
            r"\|^2\,\Big]", # 7
            font_size=38,
        )
        loss[0].set_color(GREEN)
        loss[4].set_color(BLUE)
        loss[6].set_color(ORANGE)

        # Legend using LabeledDots
        eps_dot = LabeledDot(label=MathTex(r"\epsilon", font_size=20), color=BLUE, radius=0.25)
        eps_desc = Text("= true noise (sampled)", font_size=17)
        eps_row = VGroup(eps_dot, eps_desc).arrange(RIGHT, buff=0.2)

        epsth_dot = LabeledDot(label=MathTex(r"\epsilon_\theta", font_size=17, color=BLACK), color=ORANGE, radius=0.25)
        epsth_desc = Text("= predicted noise (U-Net)", font_size=17)
        epsth_row = VGroup(epsth_dot, epsth_desc).arrange(RIGHT, buff=0.2)

        legend = VGroup(eps_row, epsth_row).arrange(DOWN, buff=0.3, aligned_edge=LEFT)
        legend.next_to(loss, DOWN, buff=0.6)

        # Break down the equation dynamically
        self.play(Write(VGroup(loss[0], loss[1], loss[2], loss[3], loss[7])), run_time=1.5)
        self.wait(5.0)

        self.play(Write(loss[4]), FadeIn(eps_row))
        self.wait(10.0)

        self.play(Write(loss[5]))
        self.play(Write(loss[6]), FadeIn(epsth_row))
        self.wait(10.0)

        # Add focus box
        box = SurroundingRectangle(loss, color=GREEN, buff=0.15, stroke_width=2)
        self.play(Create(box))
        self.wait(22.5)

        # self.play(*[FadeOut(m) for m in self.mobjects])
