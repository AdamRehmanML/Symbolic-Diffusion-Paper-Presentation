from manim import *

# AlphaXiv Color Palette
AX_BLACK = "#0f0f0f"
AX_CYAN = "#00e5ff" 
AX_WHITE = "#e0e0e0"

class Intro(Scene):
    def construct(self):
        self.camera.background_color = AX_BLACK

        # 1. Text Elements
        title = Text(
            "Symbolic Music Generation\nwith Diffusion Models", 
            font="sans-serif", weight=BOLD, color=AX_WHITE, line_spacing=0.8
        ).scale(0.8)
        
        authors = Text("Mittal et al. (2021)", font="sans-serif", color=AX_CYAN, font_size=24)
        presenter = Text("Presenter: Adam Rehman", font="sans-serif", color=AX_WHITE, font_size=20)
        
        # Group and Arrange
        header_group = VGroup(title, authors, presenter).arrange(DOWN, buff=0.5)

        # 2. Animate the Text Entry
        self.play(Write(title, run_time=1.5))
        self.play(FadeIn(authors, shift=UP*0.3))
        self.wait(1)
        self.play(FadeIn(presenter, shift=UP*0.2))
        self.wait(2)

        # 3. Transition to the Paper Image
        # Make sure you have 'paper_screenshot.png' in the same folder!
        try:
            paper_img = ImageMobject("paper_screenshot.png")
            paper_img.height = 7.5 # Set height to 5 units
        except:
            # Fallback placeholder if image isn't found
            paper_img = Rectangle(height=5, width=4, color=AX_CYAN).add(Text("Paper Image", font_size=20))

        # Animation: Shrink text to top and bring in image
        self.play(
            header_group.animate.scale(0.5).to_edge(UP, buff=0.3),
            FadeIn(paper_img, shift=UP*0.5),
            run_time=1.5
        )
        
        # Add a "Highlight" over the paper title on the image
        focus_box = SurroundingRectangle(paper_img, color=AX_CYAN, buff=0.1, stroke_width=2)
        self.play(Create(focus_box))
        
        self.wait(3)
