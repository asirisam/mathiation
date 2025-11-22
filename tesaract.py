from manim import *
import numpy as np

# Configure TikTok portrait resolution
config.pixel_width = 1080
config.pixel_height = 1920
config.frame_width = 6
config.frame_height = 6 * (1920 / 1080)
config.background_color = BLACK

class SchwarzschildScene(Scene):
    def construct(self):
        # -----------------------------
        # Step-by-step explanation
        # -----------------------------
        left_padding = 1.5
        right_padding = 0.3
        text_width = config.frame_width - left_padding - right_padding

        # Title
        title = Text("Schwarzschild Radius 🌑", font_size=36, color=YELLOW)
        title.move_to(ORIGIN)
        self.play(FadeIn(title, shift=UP))
        self.wait(1.5)
        self.play(FadeOut(title, shift=DOWN))

        # Question
        question = Text("Q: How small must a planet be", font_size=30, color=WHITE)
        question2 = Text("to become a black hole?", font_size=30, color=WHITE)
        question_group = VGroup(question, question2).arrange(DOWN, buff=0.3).move_to(ORIGIN)
        self.play(Write(question_group))
        self.wait(1.5)
        self.play(FadeOut(question_group, shift=DOWN))

        # Step group setup
        steps_group = VGroup()
        start_y = config.frame_height / 4

        def add_step(step_mob):
            step_mob.set_width(min(step_mob.width, text_width))
            steps_group.add(step_mob)

            if len(steps_group) == 1:
                step_mob.move_to(UP * start_y)
            else:
                step_mob.next_to(steps_group[-2], DOWN, buff=0.7)

            self.play(Write(step_mob), run_time=1)
            if len(steps_group) > 4:
                prev_step = steps_group[-5]
                shift_amount = prev_step.height + 0.7
                self.play(
                    steps_group.animate.shift(UP * shift_amount),
                    run_time=0.5,
                    rate_func=smooth
                )
            else:
                self.wait(0.5)

        # Steps of symbolic derivation
        steps_list = [
            MathTex(r"\text{Consider a spherical mass } M.", font_size=40, color=ORANGE),

            MathTex(r"\text{By Birkhoff's Theorem, its exterior metric}", font_size=36, color=GREEN),
            MathTex(r"\text{must be the Schwarzschild solution.}", font_size=36, color=GREEN),

            MathTex(r"\text{Schwarzschild metric has a horizon at } r=r_s.", font_size=40, color=YELLOW),

            MathTex(
                r"ds^2 = -\left(1-\frac{2GM}{c^2 r}\right)c^2 dt^2 + \cdots",
                font_size=38, color=BLUE
            ),

            MathTex(
                r"\text{Horizon occurs when } 1-\frac{2GM}{c^2 r}=0.",
                font_size=38, color=GREEN
            ),

            MathTex(
                r"\Rightarrow r_s = \frac{2GM}{c^2}",
                font_size=46, color=YELLOW
            ),

            MathTex(
                r"\text{Thus, the planet becomes a black hole if}",
                font_size=36, color=ORANGE
            ),

            MathTex(
                r"\boxed{\,R \le r_s = \frac{2GM}{c^2}\,}",
                font_size=48, color=YELLOW
            ),

            MathTex(
                r"\text{Optional density form:}", font_size=34, color=GREEN
            ),

            MathTex(
                r"r_s = \sqrt{\frac{3c^2}{8\pi G\,\rho}}",
                font_size=44, color=BLUE
            ),
        ]

        for step in steps_list:
            add_step(step)

        self.wait(2)

        # Final closing text
        self.clear()
        final_text = Text("Schwarzschild radius derived! 🌑", font_size=34, color=YELLOW)
        final_text.move_to(ORIGIN)
        self.play(Write(final_text, run_time=2))
        self.wait(2)