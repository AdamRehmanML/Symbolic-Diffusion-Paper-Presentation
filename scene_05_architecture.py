from manim import *
import os


def _parallelogram(width=1.6, height=1.0, skew=0.3, color=BLUE, fill_opacity=0.15):
    """Create a parallelogram shape (encoder/decoder style)."""
    pts = [
        [-width / 2 + skew, height / 2, 0],
        [width / 2 + skew, height / 2, 0],
        [width / 2 - skew, -height / 2, 0],
        [-width / 2 - skew, -height / 2, 0],
    ]
    return Polygon(*[p for p in pts], color=color, fill_opacity=fill_opacity, stroke_width=2)


class Architecture(Scene):
    """Scene 5 — Pipeline with parallelograms + imported architecture images."""

    def construct(self):
        # ═══════════════════════════════════════
        # Part A: Full Pipeline Flowchart
        # ═══════════════════════════════════════
        title = Text("Proposed Architecture", font_size=36, color=GREEN)
        self.play(Write(title))
        self.wait(2.2)
        self.play(title.animate.scale(0.6).to_edge(UP))

        # MIDI → Encoder → Latent → DDPM → Latent → Decoder → MIDI
        midi_in = VGroup(
            RoundedRectangle(height=0.8, width=1.4, corner_radius=0.3, color=GREY),
            Text("MIDI", font_size=16, color=GREY),
        )

        # Encoder as parallelogram
        enc_para = _parallelogram(width=1.6, height=1.0, skew=0.25, color=BLUE, fill_opacity=0.15)
        enc_text = Text("MusicVAE\nEncoder", font_size=14)
        encoder = VGroup(enc_para, enc_text)

        latent_in = LabeledDot(
            label=Tex("Latent\\\\Seq.", font_size=18), color=GREEN, radius=0.45,
        )

        ddpm = VGroup(
            Rectangle(height=1.4, width=1.8, color=ORANGE, fill_opacity=0.15, stroke_width=3),
            Text("DDPM", font_size=16, color=ORANGE),
        )

        latent_out = LabeledDot(
            label=Tex("Denoised\\\\Latent", font_size=18), color=GREEN, radius=0.45,
        )

        # Decoder as parallelogram (mirrored skew)
        dec_para = _parallelogram(width=1.6, height=1.0, skew=-0.25, color=BLUE, fill_opacity=0.15)
        dec_text = Text("MusicVAE\nDecoder", font_size=14)
        decoder = VGroup(dec_para, dec_text)

        midi_out = VGroup(
            RoundedRectangle(height=0.8, width=1.4, corner_radius=0.3, color=GREEN),
            Text("MIDI", font_size=16, color=GREEN),
        )

        pipeline = VGroup(midi_in, encoder, latent_in, ddpm, latent_out, decoder, midi_out)
        pipeline.arrange(RIGHT, buff=0.35).scale(0.85)

        arrows = VGroup()
        for i in range(6):
            a = Arrow(
                pipeline[i].get_right(), pipeline[i + 1].get_left(),
                buff=0.05, color=WHITE, stroke_width=2,
            )
            arrows.add(a)

        for i in range(7):
            if i == 0:
                self.play(FadeIn(pipeline[i], shift=RIGHT * 0.2))
            else:
                self.play(GrowArrow(arrows[i - 1]), FadeIn(pipeline[i], shift=RIGHT * 0.2))
            self.wait(0.4)

        self.play(Indicate(ddpm, color=ORANGE, scale_factor=1.08))
        highlight = SurroundingRectangle(
            VGroup(latent_in, ddpm, latent_out),
            color=ORANGE, buff=0.15, stroke_width=2,
        )
        hl_label = Text("Diffusion in continuous latent space", font_size=18, color=ORANGE)
        hl_label.next_to(highlight, DOWN, buff=0.2)
        self.play(Create(highlight), Write(hl_label))
        self.wait(15.0)
        self.play(*[FadeOut(m) for m in self.mobjects])

        # ═══════════════════════════════════════
        # Part B: U-Net Architecture (imported image)
        # ═══════════════════════════════════════
        unet_title = Text("Denoising Network: U-Net", font_size=32, color=ORANGE)
        self.play(Write(unet_title))
        self.wait(2.2)
        self.play(unet_title.animate.scale(0.6).to_edge(UP))

        unet_img_path = os.path.join(os.path.dirname(__file__) or ".", "assets", "unet.png")
        if os.path.exists(unet_img_path):
            unet_img = ImageMobject(unet_img_path).scale_to_fit_width(10).shift(DOWN * 0.3)
            self.play(FadeIn(unet_img, scale=0.9))
        else:
            placeholder = Text(
                "Place U-Net diagram at:\nassets/unet.png",
                font_size=20, color=GREY,
            )
            self.play(Write(placeholder))

        unet_note = Text(
            "Encoder-decoder with skip connections\nTime embedding injected at each level",
            font_size=16, color=GREY,
        ).to_edge(DOWN, buff=0.3)
        self.play(Write(unet_note))
        self.wait(18.8)
        self.play(*[FadeOut(m) for m in self.mobjects])

        # ═══════════════════════════════════════
        # Part C: Transformer Architecture (imported image)
        # ═══════════════════════════════════════
        tf_title = Text("Alternative: Transformer Backbone", font_size=32, color=TEAL)
        self.play(Write(tf_title))
        self.wait(2.2)
        self.play(tf_title.animate.scale(0.6).to_edge(UP))

        tf_img_path = os.path.join(os.path.dirname(__file__) or ".", "assets", "transformer.png")
        if os.path.exists(tf_img_path):
            tf_img = ImageMobject(tf_img_path).scale_to_fit_width(8).shift(DOWN * 0.3)
            self.play(FadeIn(tf_img, scale=0.9))
        else:
            placeholder = Text(
                "Place Transformer diagram at:\nassets/transformer.png",
                font_size=20, color=GREY,
            )
            self.play(Write(placeholder))

        tf_note = Text(
            "Transformers: better at long-range dependencies\nU-Net: better at local spatial structure",
            font_size=16, color=GREY,
        ).to_edge(DOWN, buff=0.3)
        box = SurroundingRectangle(tf_note, color=GREY, buff=0.1, stroke_width=1)
        self.play(Write(tf_note), Create(box))
        self.wait(22.5)

        # self.play(*[FadeOut(m) for m in self.mobjects])
