from manim import *

class MusicVAEScene(Scene):
    def construct(self):
        # ─── Title ───
        title = Text("MusicVAE", font_size=36, color=GREEN)
        self.play(Write(title))
        self.wait(2.2)
        self.play(title.animate.scale(0.6).to_edge(UP))

        # ─── VAE Diagram: Encoder → z → Decoder ───
        encoder = VGroup(
            Rectangle(height=2, width=2.5, color=BLUE),
            Text("Encoder\n(Bi-LSTM)", font_size=18)
        )
        z_dot = LabeledDot(
            label=MathTex(r"\mathbf{z}", font_size=26), color=GREEN, radius=0.5
        )
        decoder = VGroup(
            Rectangle(height=2, width=2.5, color=ORANGE),
            Text("Decoder\n(Hier. LSTM)", font_size=18)
        )

        arch = VGroup(encoder, z_dot, decoder).arrange(RIGHT, buff=1.5)

        # Arrows
        arr1 = Arrow(encoder.get_right(), z_dot.get_left(), buff=0.1, color=WHITE)
        arr2 = Arrow(z_dot.get_right(), decoder.get_left(), buff=0.1, color=WHITE)

        # Input / output
        inp_lbl = Text("MIDI\n(2 bars)", font_size=16, color=GREY).next_to(encoder, LEFT, buff=0.5)
        inp_arr = Arrow(inp_lbl.get_right(), encoder.get_left(), buff=0.1, color=GREY)
        out_lbl = Text("Reconstructed\nMIDI", font_size=16, color=GREY).next_to(decoder, RIGHT, buff=0.5)
        out_arr = Arrow(decoder.get_right(), out_lbl.get_left(), buff=0.1, color=GREY)

        self.play(Create(encoder))
        self.play(GrowArrow(arr1), FadeIn(z_dot, scale=0.5))
        self.play(GrowArrow(arr2), Create(decoder))
        self.play(GrowArrow(inp_arr), FadeIn(inp_lbl))
        self.play(GrowArrow(out_arr), FadeIn(out_lbl))
        self.wait(4.4)

        # z dimension annotation
        z_dim = MathTex(r"\mathbf{z} \in \mathbb{R}^{512}", font_size=28, color=GREEN)
        z_dim.next_to(z_dot, DOWN, buff=0.3)
        self.play(Write(z_dim))
        self.wait(6.6)

        # ─── Shrink & show hierarchical latents ───
        vae_all = VGroup(encoder, z_dot, decoder, arr1, arr2, inp_lbl, inp_arr, out_lbl, out_arr, z_dim)
        self.play(vae_all.animate.scale(0.5).to_edge(UP, buff=0.6))

        hier_title = Text("Hierarchical Latent Sequence", font_size=26, color=ORANGE)
        hier_title.shift(UP * 0.2)
        self.play(Write(hier_title))

        # 32 z-latent dots
        z_dots = VGroup()
        for i in range(8):
            d = LabeledDot(
                label=MathTex(f"z_{{{i+1}}}", font_size=14),
                color=GREEN_D, radius=0.25
            )
            z_dots.add(d)

        ellipsis = MathTex(r"\cdots", font_size=30)
        z_end = LabeledDot(
            label=MathTex("z_{32}", font_size=14),
            color=GREEN_D, radius=0.25
        )

        z_row = VGroup(*z_dots, ellipsis, z_end).arrange(RIGHT, buff=0.2)
        z_row.next_to(hier_title, DOWN, buff=0.4)

        # Arrows between them
        z_arrows = VGroup()
        for i in range(7):
            a = Arrow(z_dots[i].get_right(), z_dots[i+1].get_left(), buff=0.02, stroke_width=1.5, color=WHITE)
            z_arrows.add(a)

        self.play(LaggedStart(*[FadeIn(d, scale=0.5) for d in z_dots], lag_ratio=0.05))
        self.play(FadeIn(ellipsis), FadeIn(z_end, scale=0.5))
        self.play(LaggedStart(*[GrowArrow(a) for a in z_arrows], lag_ratio=0.03))

        dim_eq = MathTex(r"32 \times 512 = 16{,}384 \text{ dims}", font_size=24)
        bar_eq = MathTex(r"\rightarrow 64 \text{ bars of music}", font_size=24, color=BLUE)
        VGroup(dim_eq, bar_eq).arrange(RIGHT, buff=0.3).next_to(z_row, DOWN, buff=0.5)

        self.play(Write(dim_eq), Write(bar_eq))
        self.wait(4.4)

        key = MathTex(
            r"\text{Key: continuous space} \rightarrow \text{apply diffusion!}",
            font_size=26, color=ORANGE
        ).next_to(bar_eq, DOWN, buff=0.5)
        box = SurroundingRectangle(key, color=ORANGE, buff=0.15, stroke_width=2)
        self.play(Write(key), Create(box))
        self.wait(22.5)

        self.play(*[FadeOut(m) for m in self.mobjects])
