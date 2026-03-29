from manim import *

class SymbolicDiffusion(Scene):
    def construct(self):
        # 1. LaTeX Math Explanation
        equation = MathTex(
            r"q(x_t | x_{t-1}) = \mathcal{N}(x_t; \sqrt{1 - \beta_t} x_{t-1}, \beta_t \mathbf{I})"
        )
        title = Text("Forward Diffusion Process", font_size=36, color=GREEN).next_to(equation, UP)
        
        self.play(Write(title), Write(equation))
        self.wait(2)
        self.play(FadeOut(title), equation.animate.to_edge(UP).scale(0.7))

        # 2. Drawing a Simplified U-Net / Transformer Block
        # We'll represent a layer as a Rectangle with a label
        unet_block = VGroup(
            Rectangle(height=2, width=3, color=BLUE),
            Text("U-Net", font_size=24)
        )
        
        transformer_block = VGroup(
            Rectangle(height=2, width=3, color=ORANGE),
            Text("Transf.", font_size=24)
        )
        
        blocks = VGroup(unet_block, transformer_block).arrange(RIGHT, buff=1)
        
        # 3. Animate the Neural Network Architecture
        self.play(Create(blocks))
        
        # Adding arrows to show data flow
        arrow_in = Arrow(start=LEFT*3, end=blocks.get_left())
        arrow_out = Arrow(start=blocks.get_right(), end=RIGHT*3)
        
        input_label = Text("Noisy Latent (z_t)", font_size=20).next_to(arrow_in, UP)
        output_label = Text("Predicted Noise", font_size=20).next_to(arrow_out, UP)

        self.play(GrowArrow(arrow_in), Write(input_label))
        self.play(Indicate(unet_block), Indicate(transformer_block))
        self.play(GrowArrow(arrow_out), Write(output_label))
        
        self.wait(3)
