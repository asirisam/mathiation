from manim import *
import numpy as np

# Configure TikTok portrait resolution
config.pixel_width = 1080
config.pixel_height = 1920
config.frame_width = 6
config.frame_height = 6 * (1920 / 1080)
config.background_color = BLACK

class Root2Irrational(Scene):
    def construct(self):
        # -----------------------------
        # Step-by-step solution
        # -----------------------------
        left_padding = 1.0
        right_padding = 1.0
        text_width = config.frame_width - left_padding - right_padding

        # Title
        title = Text("Irrational Rebel", font_size=40, color=YELLOW)
        title.move_to(ORIGIN)
        self.play(FadeIn(title, shift=UP))
        self.wait(1.5)
        self.play(FadeOut(title, shift=DOWN))

        # Question (vertically and horizontally centered)
        question_text = (
            "Q: Prove that √2 is irrational.\n"
            "Use contradiction and any required theorem."
        )
        question = Text(
            question_text,
            font_size=30,
            color=WHITE,
            line_spacing=1.2,
        )
        question.set_width(config.frame_width - left_padding - right_padding)  # horizontal padding
        question.move_to(ORIGIN)  # vertical center

        self.play(Write(question))
        self.wait(2)
        self.play(FadeOut(question, shift=DOWN))

        # Step scroll container
        steps_group = VGroup()
        start_y = config.frame_height / 4

        # Stickman generator
        def create_stickman(center_point, gender="male"):
            color = BLUE if gender == "male" else PINK
            head_radius = 0.15
            body_length = 0.5
            arm_length = 0.3
            leg_length = 0.4

            head = Circle(radius=head_radius, color=color, fill_opacity=1).move_to(center_point + UP * (body_length/2))
            body_top = center_point + UP * (head_radius - 0.05)
            body_bottom = center_point + DOWN * (body_length - head_radius)
            body = Line(body_top, body_bottom, color=color)

            arm_left = Line(body_top, body_top + LEFT * arm_length + DOWN * arm_length, color=color)
            arm_right = Line(body_top + RIGHT * 0.05, body_top + RIGHT * arm_length + DOWN * 0.05, color=color)

            leg_left = Line(body_bottom, body_bottom + LEFT * leg_length + DOWN * 0.35, color=color)
            leg_right = Line(body_bottom, body_bottom + RIGHT * leg_length + DOWN * 0.35, color=color)

            stickman = VGroup(head, body, arm_left, arm_right, leg_left, leg_right)
            return stickman

        # Method to animate steps
        def add_step(step_mob, gender="male"):
            step_mob.set_width(min(step_mob.width, text_width))
            steps_group.add(step_mob)

            if len(steps_group) == 1:
                step_mob.move_to(UP * start_y)
            else:
                step_mob.next_to(steps_group[-2], DOWN, buff=0.7)

            stickman = create_stickman(step_mob.get_bottom() + DOWN * 0.4, gender=gender)
            self.add(stickman)

            pointer_color = BLUE if gender == "male" else PINK
            pointer_length = 0.4
            pointer = Line(stickman[3].get_end(), stickman[3].get_end() + RIGHT * pointer_length,
                           color=pointer_color, stroke_width=2)
            self.add(pointer)

            def update_pointer(pointer, step_mob, alpha):
                start = step_mob.get_left()
                end = step_mob.get_right()
                target_pos = start + alpha * (end - start)
                pointer.put_start_and_end_on(
                    stickman[3].get_end(),
                    stickman[3].get_end() + 0.5 * (target_pos - stickman[3].get_end())
                )

            self.play(
                Write(step_mob, run_time=1.5, rate_func=linear),
                UpdateFromAlphaFunc(pointer, lambda mob, alpha: update_pointer(mob, step_mob, alpha))
            )

            self.remove(stickman, pointer)

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

        # Steps for the irrationality of √2
        steps_list = [
            MathTex(r"\textbf{Theorem: } \sqrt{2} \text{ is irrational}", font_size=42, color=YELLOW),
            MathTex(r"\text{Proof uses: Contradiction}", font_size=38, color=ORANGE),
            MathTex(r"\text{Step 1: Assume } \sqrt{2} = \frac{p}{q}", font_size=38, color=WHITE),
            MathTex(r"\text{where } p,q \text{ are integers in lowest terms}", font_size=34, color=GREEN),
            MathTex(r"\text{Step 2: Square both sides}", font_size=38, color=ORANGE),
            MathTex(r"2 = \frac{p^2}{q^2} \Rightarrow p^2 = 2q^2", font_size=40, color=BLUE),
            MathTex(r"\text{Step 3: } p^2 \text{ is even } \Rightarrow p \text{ is even}", font_size=38, color=PINK),
            MathTex(r"p = 2k", font_size=40, color=WHITE),
            MathTex(r"\text{Step 4: Substitute } p = 2k", font_size=38, color=ORANGE),
            MathTex(r"4k^2 = 2q^2 \Rightarrow q^2 \text{ is even}", font_size=40, color=BLUE),
            MathTex(r"\text{So } q \text{ is even}", font_size=38, color=PINK),
            MathTex(r"\text{Step 5: Contradiction!}", font_size=38, color=RED),
            MathTex(r"\text{Both } p \text{ and } q \text{ even }", font_size=36, color=RED),
            MathTex(r"\text{But fraction was in lowest terms}", font_size=36, color=RED),
            MathTex(r"\textbf{Conclusion: } \sqrt{2} \text{ is irrational}", font_size=42, color=YELLOW),
        ]

        # play steps
        for step in steps_list:
            add_step(step)

        self.wait(1.5)

        # Ending text
        self.clear()
        final_text = Text("Nailed it!", font_size=40, color=YELLOW)
        final_text.move_to(ORIGIN)
        self.play(Write(final_text, run_time=2))
        self.wait(2)