from manim import *

class MarkovChain(Scene):
    def construct(self):
        # 1. Create States
        state_0 = LabeledDot(label=MathTex("x_{t-1}"), color=BLUE).shift(LEFT * 2)
        state_1 = LabeledDot(label=MathTex("x_t"), color=DARK_BLUE).shift(RIGHT * 2)

        # 2. Create Transition Arrows (Curved to allow for both directions)
        # Forward Process (q)
        forward_arrow = CurvedArrow(state_0.get_right(), state_1.get_left(), angle=-TAU/8, color=WHITE)
        q_label = MathTex("q(x_t|x_{t-1})", font_size=30).next_to(forward_arrow, UP)

        # Reverse Process (p)
        reverse_arrow = CurvedArrow(state_1.get_left(), state_0.get_right(), angle=-TAU/8, color=YELLOW)
        p_label = MathTex("p_{\\theta}(x_{t-1}|x_t)", font_size=30, color=YELLOW).next_to(reverse_arrow, DOWN)

        # 3. Animate
        self.play(FadeIn(state_0), FadeIn(state_1))
        self.wait(1)

        # Show Forward Process
        self.play(Create(forward_arrow), Write(q_label))
        self.play(Indicate(q_label))
        self.wait(1)

        # Show Reverse Process
        self.play(Create(reverse_arrow), Write(p_label))
        self.play(Indicate(p_label))
        
        # 4. Final Grouping and move to corner (leaving space for your webcam!)
        full_chain = VGroup(state_0, state_1, forward_arrow, reverse_arrow, q_label, p_label)
        self.play(full_chain.animate.scale(0.8).to_edge(UP))
        
        self.wait(2)
