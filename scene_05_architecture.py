from manim import *

class Architecture(Scene):
    def construct(self):
        # ─── Title ───
        title = Text("Proposed Architecture", font_size=36, color=GREEN)
        self.play(Write(title))
        self.wait(0.5)
        self.play(title.animate.scale(0.6).to_edge(UP))

        # ─── Full pipeline as a flowchart ───
        # MIDI → Encoder → Latent → DDPM → Latent → Decoder → MIDI
        midi_in = VGroup(
            RoundedRectangle(height=0.8, width=1.4, corner_radius=0.3, color=GREY),
            Text("MIDI", font_size=16, color=GREY)
        )
        encoder = VGroup(
            Rectangle(height=1.2, width=1.6, color=BLUE),
            Text("MusicVAE\nEncoder", font_size=14)
        )
        latent_in = LabeledDot(
            label=Tex("Latent\\\\Seq.", font_size=18), color=GREEN, radius=0.45
        )
        ddpm = VGroup(
            Rectangle(height=1.4, width=1.8, color=YELLOW, fill_opacity=0.15, stroke_width=3),
            Text("DDPM\n(U-Net)", font_size=16, color=YELLOW)
        )
        latent_out = LabeledDot(
            label=Tex("Denoised\\\\Latent", font_size=18), color=GREEN, radius=0.45
        )
        decoder = VGroup(
            Rectangle(height=1.2, width=1.6, color=BLUE),
            Text("MusicVAE\nDecoder", font_size=14)
        )
        midi_out = VGroup(
            RoundedRectangle(height=0.8, width=1.4, corner_radius=0.3, color=GREEN),
            Text("MIDI", font_size=16, color=GREEN)
        )

        pipeline = VGroup(midi_in, encoder, latent_in, ddpm, latent_out, decoder, midi_out)
        pipeline.arrange(RIGHT, buff=0.35).scale(0.85)

        arrows = VGroup()
        for i in range(6):
            a = Arrow(
                pipeline[i].get_right(), pipeline[i+1].get_left(),
                buff=0.05, color=WHITE, stroke_width=2
            )
            arrows.add(a)

        # Animate left-to-right
        for i in range(7):
            if i == 0:
                self.play(FadeIn(pipeline[i], shift=RIGHT * 0.2))
            else:
                self.play(GrowArrow(arrows[i-1]), FadeIn(pipeline[i], shift=RIGHT * 0.2))
            self.wait(0.3)

        # Highlight the DDPM block
        self.play(Indicate(ddpm, color=YELLOW, scale_factor=1.08))
        self.wait(1)

        # Highlight box around latent+DDPM section
        highlight = SurroundingRectangle(
            VGroup(latent_in, ddpm, latent_out),
            color=YELLOW, buff=0.15, stroke_width=2
        )
        hl_label = Text("Diffusion in continuous latent space", font_size=18, color=YELLOW)
        hl_label.next_to(highlight, DOWN, buff=0.2)
        self.play(Create(highlight), Write(hl_label))
        self.wait(2.5)
        self.play(*[FadeOut(m) for m in self.mobjects])

        # ─── U-Net Detail ───
        unet_title = Text("Denoising Network: U-Net", font_size=32, color=YELLOW)
        self.play(Write(unet_title))
        self.wait(0.5)
        self.play(unet_title.animate.scale(0.6).to_edge(UP))

        # Simplified U-shape
        widths = [3.5, 2.8, 2.0, 1.2]  # down path
        down_blocks = VGroup()
        for i, w in enumerate(widths):
            r = Rectangle(height=0.5, width=w, color=BLUE, fill_opacity=0.1 + i*0.1, stroke_width=1.5)
            down_blocks.add(r)
        down_blocks.arrange(DOWN, buff=0.1).shift(LEFT * 2)

        # Bottleneck
        bottleneck = Rectangle(height=0.6, width=0.8, color=RED, fill_opacity=0.3, stroke_width=2)
        bn_label = Text("BN", font_size=12, color=RED)
        bn = VGroup(bottleneck, bn_label).next_to(down_blocks, DOWN, buff=0.15)

        # Up path
        up_blocks = VGroup()
        for i, w in enumerate(reversed(widths)):
            r = Rectangle(height=0.5, width=w, color=GREEN, fill_opacity=0.1 + (3-i)*0.1, stroke_width=1.5)
            up_blocks.add(r)
        up_blocks.arrange(DOWN, buff=0.1).shift(RIGHT * 2)

        # Skip connections
        skips = VGroup()
        for d, u in zip(down_blocks, reversed(list(up_blocks))):
            s = DashedLine(d.get_right(), u.get_left(), color=GREY, dash_length=0.08, stroke_width=1)
            skips.add(s)

        # Time embedding
        t_emb = VGroup(
            Circle(radius=0.3, color=YELLOW, fill_opacity=0.2, stroke_width=1.5),
            MathTex("t", font_size=20, color=YELLOW)
        ).next_to(bn, RIGHT, buff=0.8)
        t_arr = Arrow(t_emb.get_left(), bn.get_right(), buff=0.05, color=YELLOW, stroke_width=1.5)

        # Labels
        down_lbl = Text("Downsample", font_size=14, color=BLUE).next_to(down_blocks, LEFT, buff=0.3)
        up_lbl = Text("Upsample", font_size=14, color=GREEN).next_to(up_blocks, RIGHT, buff=0.3)
        skip_lbl = Text("Skip connections", font_size=14, color=GREY).next_to(skips, UP, buff=0.2)

        self.play(
            LaggedStart(*[FadeIn(b, shift=DOWN*0.1) for b in down_blocks], lag_ratio=0.1),
            FadeIn(down_lbl)
        )
        self.play(FadeIn(bn, scale=0.8))
        self.play(
            LaggedStart(*[FadeIn(b, shift=DOWN*0.1) for b in up_blocks], lag_ratio=0.1),
            FadeIn(up_lbl)
        )
        self.play(LaggedStart(*[Create(s) for s in skips], lag_ratio=0.05), FadeIn(skip_lbl))
        self.play(FadeIn(t_emb, shift=LEFT*0.2), GrowArrow(t_arr))

        # Input/output labels
        inp = MathTex(r"z_t", font_size=24, color=BLUE).next_to(down_blocks[0], UP, buff=0.2)
        out = MathTex(r"\hat{\epsilon}", font_size=24, color=GREEN).next_to(up_blocks[-1], DOWN, buff=0.2)
        self.play(Write(inp), Write(out))
        self.wait(3)

        self.play(*[FadeOut(m) for m in self.mobjects])
