from manim import *
import numpy as np

# Configure TikTok portrait resolution
config.pixel_width = 1080
config.pixel_height = 1920
config.frame_width = 6
config.frame_height = 6 * (1920 / 1080)
config.background_color = BLACK

class SchwarzschildNewtonian(Scene):
    def construct(self):
        # -----------------------------
        # Layout helpers
        # -----------------------------
        left_padding = 1.5
        right_padding = 0.3
        text_width = config.frame_width - left_padding - right_padding
        start_y = config.frame_height / 4

        steps_group = VGroup()

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

        # -----------------------------
        # Title slide
        # -----------------------------
        title = Text("Gravity Collapse", font_size=40, color=YELLOW)
        title.move_to(ORIGIN)
        self.play(FadeIn(title, shift=UP))
        self.wait(2)
        self.play(FadeOut(title, shift=DOWN))

        # -----------------------------
        # Question slide with padding
        # -----------------------------
        q_left_padding = 1.0
        q_right_padding = 1.0
        max_question_width = config.frame_width - q_left_padding - q_right_padding

        question_text1 = Text("Q: What is ", font_size=34, color=WHITE)
        question_text2 = Text("Schwarzschild Radius?", font_size=34, color=WHITE)

        # Apply padding
        question_text1.set_width(max_question_width)
        question_text2.set_width(max_question_width)

        # Arrange vertically and center
        question_group = VGroup(question_text1, question_text2).arrange(DOWN, buff=0.3)
        question_group.move_to(ORIGIN)  # vertically centered

        self.play(Write(question_group, run_time=2))
        self.wait(2)
        self.play(FadeOut(question_group, shift=DOWN))

        # -----------------------------
        # Steps of Newtonian heuristic
        # -----------------------------
        steps = [
            MathTex(r"\text{The Schwarzschild radius is}", font_size=38, color=GREEN),
            MathTex(r"\text{the size an object must shrink to}", font_size=38, color=GREEN),
            MathTex(r"\text{so that even light can’t escape.}", font_size=38, color=GREEN),
            MathTex(r"1.\ \text{Escape velocity: }}", font_size=38, color=ORANGE),
            MathTex(r"v_e = \sqrt{\tfrac{2GM}{r}}", font_size=38, color=ORANGE),
            MathTex(r"2.\ \text{Set escape velocity equal to speed of light: }", font_size=38, color=GREEN),
            MathTex(r"v_e = c", font_size=38, color=GREEN),
            MathTex(r"G \; \text{= gravitational constant}", font_size=34, color=ORANGE),
            MathTex(r"M \; \text{= mass of the object}", font_size=34, color=ORANGE),
            MathTex(r"r \; \text{= distance from the centre (radius)}", font_size=34, color=ORANGE),
            MathTex(r"v_e \; \text{= escape velocity}", font_size=34, color=ORANGE),
            MathTex(r"3.\ \Rightarrow c = \sqrt{\tfrac{2GM}{r}}", font_size=40, color=GREEN),
            MathTex(r"4.\ \text{Square both sides: }", font_size=38, color=YELLOW),
            MathTex(r"c^2 = \tfrac{2GM}{r}", font_size=38, color=YELLOW),
            MathTex(r"5.\ \text{Solve for } r:", font_size=40, color=YELLOW),
            MathTex(r"r = \tfrac{2GM}{c^2}", font_size=40, color=YELLOW),
            MathTex(r"\boxed{r_s = \tfrac{2GM}{c^2}}", font_size=48, color=ORANGE),
            MathTex(r"\text{This radius is}", font_size=38, color=BLUE),
            MathTex(r"\text{the Schwarzschild radius.}", font_size=38, color=BLUE)
        ]

        for s in steps:
            add_step(s)

        self.wait(2)

        # -----------------------------
        # Planet and Schwarzschild radius visualization
        # -----------------------------
        self.clear()

        # Draw planet real radius
        real_radius_circle = Circle(radius=1.5, color=BLUE, stroke_width=4)
        real_radius_label = Text("Real Planet Radius: R", font_size=28, color=BLUE)
        real_radius_label.next_to(real_radius_circle, DOWN)
        line_real = Line(start=real_radius_circle.get_center(), end=real_radius_circle.get_right(), color=BLUE)
        line_real_label = Text("R", font_size=24, color=BLUE).next_to(line_real.get_end(), RIGHT, buff=0.1)

        # Draw Schwarzschild radius vertically
        schwarzschild_radius_circle = Circle(radius=0.8, color=RED, stroke_width=4)
        schwarzschild_label = Text("Schwarzschild Radius: r_s", font_size=28, color=RED)
        schwarzschild_label.next_to(schwarzschild_radius_circle, DOWN, buff=2)
        line_s = Line(start=schwarzschild_radius_circle.get_center(), end=schwarzschild_radius_circle.get_top(), color=RED)
        line_s_label = Text("r_s", font_size=24, color=RED).next_to(line_s.get_end(), UP, buff=0.1)

        # Position them together
        VGroup(
            real_radius_circle, schwarzschild_radius_circle,
            real_radius_label, schwarzschild_label,
            line_real, line_real_label, line_s, line_s_label
        ).move_to(ORIGIN)

        # Animate circles and lines
        self.play(Create(real_radius_circle), Write(real_radius_label))
        self.play(Create(line_real), Write(line_real_label))
        self.wait(1)
        self.play(Create(schwarzschild_radius_circle), Write(schwarzschild_label))
        self.play(Create(line_s), Write(line_s_label))
        self.wait(2)

        # Closing text
        self.clear()
        final_text = Text("Naild it!", font_size=32, color=YELLOW)
        final_text.move_to(ORIGIN)
        self.play(Write(final_text, run_time=2))
        self.wait(2)