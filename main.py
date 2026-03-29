"""
main.py — Master wrapper that stitches all 9 scenes into one FullPresentation.

Usage (full presentation):
    manim -ql main.py FullPresentation
    manim -qm main.py FullPresentation

Usage (individual scene):
    manim -ql scene_01_intro.py Intro
    manim -ql scene_02_background.py Background
    manim -ql scene_03_diffusion_basics.py DiffusionBasics
    manim -ql scene_04_musicvae.py MusicVAEScene
    manim -ql scene_05_architecture.py Architecture
    manim -ql scene_06_training.py Training
    manim -ql scene_07_generation.py Generation
    manim -ql scene_08_results.py Results
    manim -ql scene_09_conclusion.py Conclusion
"""

from manim import *

from scene_01_intro import Intro
from scene_02_background import Background
from scene_03_diffusion_basics import DiffusionBasics
from scene_04_musicvae import MusicVAEScene
from scene_05_architecture import Architecture
from scene_06_training import Training
from scene_07_generation import Generation
from scene_08_results import Results
from scene_09_conclusion import Conclusion


class FullPresentation(Scene):
    """Plays all 9 scenes back-to-back in a single render."""

    def construct(self):
        scenes = [
            Intro,
            Background,
            DiffusionBasics,
            MusicVAEScene,
            Architecture,
            Training,
            Generation,
            Results,
            Conclusion,
        ]

        for SceneClass in scenes:
            SceneClass.construct(self)
            self.wait(0.3)
