from manim import *
import numpy as np


def _make_swissroll(n=200, seed=42):
    """Generate 2D swissroll-like spiral data."""
    rng = np.random.default_rng(seed)
    t = np.linspace(np.pi / 2, 5 * np.pi, n)
    x = t * np.cos(t) / (5 * np.pi) + rng.normal(0, 0.08, n)
    y = t * np.sin(t) / (5 * np.pi) + rng.normal(0, 0.08, n)
    return np.column_stack([x, y])


class Generation(Scene):
    """Scene 7 — Generation via reverse diffusion + infilling."""

    def construct(self):

        # ══════════════════════════════════════
        # Part A: Reverse Diffusion (Swissroll)
        #   Ported from Welch Labs p40_51.py
        # ══════════════════════════════════════

        title = Text("Reverse Diffusion: Generating Data", font_size=32, color=GREEN)
        self.play(Write(title))
        self.wait(2.2)
        self.play(title.animate.scale(0.55).to_edge(UP))

        # Axes
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

        self.play(Create(axes), run_time=0.6)

        # Start with random noise dots (Gaussian)
        n_dots = 150
        rng = np.random.default_rng(99)
        noise_positions = rng.normal(0, 0.9, (n_dots, 2))

        dots = VGroup()
        for pt in noise_positions:
            screen_pt = axes.c2p(pt[0], pt[1])
            d = Dot(screen_pt, radius=0.04, color=GREY_D, fill_opacity=0.5)
            dots.add(d)

        noise_label = MathTex(r"x_T \sim \mathcal{N}(0, \mathbf{I})", font_size=26, color=GREY)
        noise_label.next_to(axes, DOWN, buff=0.2)

        self.play(
            LaggedStart(*[FadeIn(d, scale=0.3) for d in dots], lag_ratio=0.005),
            Write(noise_label),
            run_time=1.2,
        )
        self.wait(4.4)

        # Step counter
        step_text = Text("STEP", font_size=16, color=GREY).to_corner(DR, buff=0.6).shift(UP * 0.3)
        step_num = Text("T", font_size=28, color=GREY).next_to(step_text, UP, buff=0.1)
        self.play(FadeIn(step_text), FadeIn(step_num))

        # --- Reverse: noise → spiral ---
        # Pre-compute target spiral
        target_data = _make_swissroll(n=n_dots, seed=99)
        n_rev_steps = 40

        # Interpolate: positions go from noise → spiral
        for step in range(n_rev_steps):
            t = (step + 1) / n_rev_steps
            # Smooth interpolation with decreasing noise
            interp = (1 - t) * noise_positions + t * target_data
            # Add decreasing noise for realism
            jitter = rng.normal(0, 0.03 * (1 - t), interp.shape)
            current = interp + jitter

            anims = []
            for i, d in enumerate(dots):
                target_pt = axes.c2p(current[i, 0], current[i, 1])
                anims.append(d.animate.move_to(target_pt))

            # Update color: grey → yellow as we denoise
            new_color = interpolate_color(GREY_D, ORANGE, t)
            new_opacity = 0.5 + 0.5 * t

            step_val = str(n_rev_steps - step)
            new_num = Text(step_val, font_size=28, color=GREY).next_to(step_text, UP, buff=0.1)

            self.play(
                *anims,
                dots.animate.set_color(new_color).set_opacity(new_opacity),
                Transform(step_num, new_num),
                run_time=0.1,
                rate_func=linear,
            )

        self.play(FadeOut(noise_label))

        clean_label = MathTex(r"x_0 \approx p_{\text{data}}", font_size=26, color=ORANGE)
        clean_label.next_to(axes, DOWN, buff=0.2)
        self.play(Write(clean_label))
        self.wait(2.2)

        # Advantage callout
        adv = MathTex(
            r"\text{Non-autoregressive} \rightarrow \text{no exposure bias!}",
            font_size=26, color=ORANGE,
        ).next_to(clean_label, DOWN, buff=0.3)
        box = SurroundingRectangle(adv, color=ORANGE, buff=0.1, stroke_width=2)
        self.play(Write(adv), Create(box))
        self.wait(15.0)

        self.play(*[FadeOut(m) for m in self.mobjects])

        # ══════════════════════════════════════
        # Part B: Single Trajectory (TracedPath)
        #   Inspired by Welch Labs CustomTracedPath
        # ══════════════════════════════════════

        title2 = Text("Following One Sample", font_size=32, color=ORANGE)
        self.play(Write(title2))
        self.wait(0.6)
        self.play(title2.animate.scale(0.55).to_edge(UP))

        # Smaller axes
        axes2 = Axes(
            x_range=[-1.4, 1.4, 0.5],
            y_range=[-1.4, 1.4, 0.5],
            x_length=5, y_length=5,
            axis_config={
                "color": GREY,
                "stroke_width": 1.5,
                "include_tip": True,
                "include_ticks": False,
                "tip_length": 0.15,
            },
        ).shift(DOWN * 0.3)
        self.play(Create(axes2), run_time=0.5)

        # Single trajectory: noise → clean
        n_traj_steps = 60
        start_pt = np.array([0.7, -0.5])
        end_pt = np.array([-0.3, 0.6])  # target on spiral

        # Build a wandering path
        traj_rng = np.random.default_rng(77)
        path_points = [start_pt.copy()]
        for s in range(n_traj_steps):
            t = (s + 1) / n_traj_steps
            # Drift toward target + random jitter
            drift = (end_pt - path_points[-1]) * 0.06
            jitter = traj_rng.normal(0, 0.04 * (1 - t * 0.8), 2)
            path_points.append(path_points[-1] + drift + jitter)

        # Place dot at start
        moving_dot = Dot(axes2.c2p(*start_pt), radius=0.07, color=ORANGE)
        start_label = MathTex(r"x_T", font_size=22, color=GREY).next_to(moving_dot, UR, buff=0.1)
        self.play(FadeIn(moving_dot), Write(start_label))

        # TracedPath (Community manim's built-in)
        trace = TracedPath(
            moving_dot.get_center,
            stroke_color=ORANGE,
            stroke_width=2.5,
            stroke_opacity=0.6,
        )
        self.add(trace)

        # Animate the trajectory
        for i, pt in enumerate(path_points[1:]):
            self.play(
                moving_dot.animate.move_to(axes2.c2p(pt[0], pt[1])),
                run_time=0.06,
                rate_func=linear,
            )

        end_label = MathTex(r"x_0", font_size=22, color=BLUE).next_to(moving_dot, UR, buff=0.1)
        self.play(
            moving_dot.animate.set_color(BLUE),
            FadeOut(start_label),
            Write(end_label),
        )

        eq = MathTex(
            r"x_{t-1} = \mu_\theta(x_t, t) + \sigma_t\, z",
            font_size=28, color=ORANGE,
        ).next_to(axes2, DOWN, buff=0.35)
        self.play(Write(eq))
        self.wait(18.8)
        self.play(*[FadeOut(m) for m in self.mobjects])

        # ══════════════════════════════════════
        # Part C: Conditional Infilling
        # ══════════════════════════════════════

        title3 = Text("Conditional Infilling", font_size=36, color=ORANGE)
        self.play(Write(title3))
        self.wait(2.2)
        self.play(title3.animate.scale(0.6).to_edge(UP))

        # Melody bars as LabeledDots
        bar_labels = ["Bar 1", "Bar 2", "Bar 3", "?", "?", "?", "Bar 7", "Bar 8"]
        bar_colors = [BLUE, BLUE, BLUE, GREY_D, GREY_D, GREY_D, BLUE, BLUE]

        bars = VGroup()
        for lbl, col in zip(bar_labels, bar_colors):
            b = LabeledDot(
                label=Tex(lbl, font_size=14),
                color=col, radius=0.4,
            )
            bars.add(b)
        bars.arrange(RIGHT, buff=0.3)

        bar_arrows = VGroup()
        for i in range(7):
            a = Arrow(bars[i].get_right(), bars[i + 1].get_left(), buff=0.03, stroke_width=1.5, color=WHITE)
            bar_arrows.add(a)

        self.play(
            LaggedStart(*[FadeIn(b) for b in bars], lag_ratio=0.08),
            LaggedStart(*[GrowArrow(a) for a in bar_arrows], lag_ratio=0.05),
        )
        self.wait(4.4)

        # Highlight gap
        gap_rect = SurroundingRectangle(
            VGroup(bars[3], bars[4], bars[5]),
            color=RED, buff=0.15, stroke_width=2,
        )
        gap_lbl = Text("Gap to infill", font_size=18, color=RED).next_to(gap_rect, DOWN, buff=0.2)
        self.play(Create(gap_rect), Write(gap_lbl))
        self.wait(6.6)

        # Fill the gap
        new_bars = VGroup()
        for i in range(3, 6):
            nb = LabeledDot(
                label=Tex(f"Bar {i+1}", font_size=14, color=BLACK),
                color=ORANGE, radius=0.4,
            ).move_to(bars[i])
            new_bars.add(nb)

        self.play(
            *[Transform(bars[i], new_bars[j]) for j, i in enumerate(range(3, 6))],
            gap_rect.animate.set_color(GREEN),
            gap_lbl.animate.become(
                Text("Infilled!", font_size=18, color=GREEN).next_to(gap_rect, DOWN, buff=0.2)
            ),
            run_time=1.5,
        )
        self.wait(4.4)

        method = MathTex(
            r"\text{Replace known bars at each } t \rightarrow \text{constrains generation}",
            font_size=22, color=ORANGE,
        ).next_to(gap_lbl, DOWN, buff=0.5)
        self.play(Write(method))
        self.wait(22.5)

        self.play(*[FadeOut(m) for m in self.mobjects])
