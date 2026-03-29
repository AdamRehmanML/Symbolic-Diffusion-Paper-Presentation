from manim import *

class Generation(Scene):
    def construct(self):
        # ─── Part A: Unconditional Generation ───
        title = Text("Unconditional Generation", font_size=36, color=GREEN)
        self.play(Write(title))
        self.wait(0.5)
        self.play(title.animate.scale(0.6).to_edge(UP))

        # Reverse diffusion as state chain (like markov_chain.py)
        step_labels = ["z_T", "z_{T-1}", "\\cdots", "z_1", "z_0"]
        step_colors = [GREY_D, GREY, GREY, BLUE_D, BLUE]

        states = VGroup()
        for i, (lbl, col) in enumerate(zip(step_labels, step_colors)):
            s = LabeledDot(
                label=MathTex(lbl, font_size=20),
                color=col, radius=0.4
            )
            states.add(s)
        states.arrange(RIGHT, buff=0.8)

        # Reverse arrows
        rev_arrows = VGroup()
        for i in range(len(states) - 1):
            a = CurvedArrow(
                states[i].get_right(), states[i+1].get_left(),
                angle=-TAU/10, color=YELLOW
            )
            rev_arrows.add(a)

        p_label = MathTex(r"p_\theta", font_size=22, color=YELLOW).next_to(rev_arrows[0], UP, buff=0.1)

        # Input noise label
        noise_lbl = Text("Gaussian noise", font_size=16, color=RED).next_to(states[0], DOWN, buff=0.3)
        # Output clean label
        clean_lbl = Text("Clean latent", font_size=16, color=GREEN).next_to(states[-1], DOWN, buff=0.3)

        self.play(FadeIn(states[0]), FadeIn(noise_lbl))
        for i in range(len(states) - 1):
            self.play(Create(rev_arrows[i]), FadeIn(states[i+1]), run_time=0.5)
        self.play(Write(p_label), FadeIn(clean_lbl))
        self.wait(1)

        # Decode step
        decode_arr = Arrow(states[-1].get_right(), states[-1].get_right() + RIGHT*1.5, buff=0.1, color=GREEN)
        decode_lbl = Text("Decode", font_size=16, color=GREEN).next_to(decode_arr, UP, buff=0.05)
        midi_dot = LabeledDot(
            label=Tex("MIDI", font_size=18), color=GREEN, radius=0.35
        ).next_to(decode_arr, RIGHT, buff=0.1)

        self.play(GrowArrow(decode_arr), Write(decode_lbl), FadeIn(midi_dot, scale=0.5))
        self.wait(1)

        # Advantage callout
        adv = MathTex(
            r"\text{Non-autoregressive} \rightarrow \text{no exposure bias!}",
            font_size=26, color=YELLOW
        ).next_to(states, DOWN, buff=1.2)
        box = SurroundingRectangle(adv, color=YELLOW, buff=0.1, stroke_width=2)
        self.play(Write(adv), Create(box))
        self.wait(2.5)
        self.play(*[FadeOut(m) for m in self.mobjects])

        # ─── Part B: Conditional Infilling ───
        title2 = Text("Conditional Infilling", font_size=36, color=YELLOW)
        self.play(Write(title2))
        self.wait(0.5)
        self.play(title2.animate.scale(0.6).to_edge(UP))

        # Melody bars as labeled dots
        bar_labels = ["Bar 1", "Bar 2", "Bar 3", "?", "?", "?", "Bar 7", "Bar 8"]
        bar_colors = [BLUE, BLUE, BLUE, GREY_D, GREY_D, GREY_D, BLUE, BLUE]

        bars = VGroup()
        for lbl, col in zip(bar_labels, bar_colors):
            b = LabeledDot(
                label=Tex(lbl, font_size=14),
                color=col, radius=0.4
            )
            bars.add(b)
        bars.arrange(RIGHT, buff=0.3)

        # Arrows
        bar_arrows = VGroup()
        for i in range(7):
            a = Arrow(bars[i].get_right(), bars[i+1].get_left(), buff=0.03, stroke_width=1.5, color=WHITE)
            bar_arrows.add(a)

        self.play(
            LaggedStart(*[FadeIn(b) for b in bars], lag_ratio=0.08),
            LaggedStart(*[GrowArrow(a) for a in bar_arrows], lag_ratio=0.05)
        )
        self.wait(1)

        # Highlight gap
        gap_rect = SurroundingRectangle(
            VGroup(bars[3], bars[4], bars[5]),
            color=RED, buff=0.15, stroke_width=2
        )
        gap_lbl = Text("Gap to infill", font_size=18, color=RED).next_to(gap_rect, DOWN, buff=0.2)
        self.play(Create(gap_rect), Write(gap_lbl))
        self.wait(1.5)

        # Fill in the gap — change colors
        new_bars = VGroup()
        for i in range(3, 6):
            new_b = LabeledDot(
                label=Tex(f"Bar {i+1}", font_size=14),
                color=YELLOW, radius=0.4
            ).move_to(bars[i])
            new_bars.add(new_b)

        self.play(
            *[Transform(bars[i], new_bars[j]) for j, i in enumerate(range(3, 6))],
            gap_rect.animate.set_color(GREEN),
            gap_lbl.animate.become(Text("Infilled!", font_size=18, color=GREEN).next_to(gap_rect, DOWN, buff=0.2)),
            run_time=1.5
        )
        self.wait(1)

        method = MathTex(
            r"\text{Replace known bars at each reverse step} \rightarrow \text{constrains generation}",
            font_size=22, color=YELLOW
        ).next_to(gap_lbl, DOWN, buff=0.5)
        self.play(Write(method))
        self.wait(3)

        self.play(*[FadeOut(m) for m in self.mobjects])
