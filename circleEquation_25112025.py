from manim import *
import numpy as np

# TikTok portrait
config.pixel_width = 1080
config.pixel_height = 1920
config.frame_width = 6
config.frame_height = 6 * (1920 / 1080)
config.background_color = BLACK

class CircleEquationProof(Scene):
    def construct(self):

        # -----------------------------
        # Title
        # -----------------------------
        title = Text("Equation of a Circle", font_size=48, color=YELLOW)
        title.move_to(ORIGIN)
        self.play(FadeIn(title, shift=UP))
        self.wait(2)
        self.play(FadeOut(title, shift=DOWN))

        # -----------------------------
        # Question with padding
        # -----------------------------
        left_padding = 1.0
        right_padding = 1.0
        top_padding = 1.5

        text_width = config.frame_width - left_padding - right_padding

        question = Text(
            "Prove the equation of a circle",
            font_size=46,
            color=ORANGE
        )
        equation = MathTex(
            r"(x-h)^2 + (y-k)^2 = r^2",
            font_size=48,
            color=BLUE
        )

        question_group = VGroup(question, equation).arrange(DOWN, buff=0.5)
        question_group.set_width(text_width)

        # vertically centred WITH top padding
        question_group.move_to(
            ORIGIN + UP * (top_padding / 2)
        )

        self.play(FadeIn(question_group, shift=UP))
        self.wait(2)
        self.play(FadeOut(question_group, shift=DOWN))

        # -------------------------------------------------------
        # Circle Drawing (separate slide, before steps)
        # -------------------------------------------------------
        center = Dot(ORIGIN, color=YELLOW)
        center_label = MathTex("(h,k)", color=YELLOW).next_to(center, DOWN)

        circle = Circle(radius=2.5, color=BLUE)
        circle.move_to(ORIGIN)

        point = Dot(RIGHT*2 + UP*1, color=RED)
        point_label = MathTex("(x,y)", color=RED).next_to(point, RIGHT)

        radius_line = Line(center.get_center(), point.get_center(), color=GREEN)
        radius_label = MathTex("r", color=GREEN).next_to(radius_line, UP*0.2)

        self.play(Create(circle), FadeIn(center), Write(center_label))
        self.play(FadeIn(point), Write(point_label))
        self.play(Create(radius_line), Write(radius_label))
        self.wait(1.5)

        # fade everything before moving to next slide
        self.play(
            FadeOut(point),
            FadeOut(point_label),
            FadeOut(radius_line),
            FadeOut(radius_label),
            FadeOut(circle),
            FadeOut(center),
            FadeOut(center_label)
        )

        # -------------------------------------------------------
        # STEPS SLIDE (starts AFTER circle drawing)
        # -------------------------------------------------------
        left_padding = 1.2
        right_padding = 0.3
        text_width = config.frame_width - left_padding - right_padding
        start_y = config.frame_height / 4
        steps_group = VGroup()

        # --- stickman function (unchanged) ---
        def create_stickman(center_point):
            head_radius = 0.15
            body_length = 0.4
            arm_length = 0.25
            leg_length = 0.4
            head = Circle(radius=head_radius, color=YELLOW).move_to(center_point + UP*(body_length/2))
            body_top = center_point + UP*(head_radius - 0.075)
            body_bottom = center_point + DOWN*(body_length - head_radius)
            body = Line(body_top, body_bottom, color=YELLOW)
            arm_y_offset = -0.05
            arm_left = Line(body_top + LEFT*0.05 + UP*arm_y_offset,
                            body_top + LEFT*arm_length + DOWN*0.05, color=YELLOW)
            arm_right = Line(body_top + RIGHT*0.05 + UP*arm_y_offset,
                             body_top + RIGHT*arm_length + UP*0.05, color=YELLOW)
            leg_left = Line(body_bottom,
                            body_bottom + LEFT*leg_length + DOWN*0.4, color=YELLOW)
            leg_right = Line(body_bottom,
                             body_bottom + RIGHT*leg_length + DOWN*0.4, color=YELLOW)
            return VGroup(head, body, arm_left, arm_right, leg_left, leg_right)

        # --- step adding behaviour (unchanged) ---
        def add_step(step_mob):
            step_mob.set_width(min(step_mob.width, text_width))
            steps_group.add(step_mob)

            if len(steps_group) == 1:
                step_mob.move_to(UP * start_y)
            else:
                step_mob.next_to(steps_group[-2], DOWN, buff=0.7)

            stickman = create_stickman(step_mob.get_bottom() + DOWN*0.4)
            self.add(stickman)

            pointer = Line(
                stickman[3].get_end(),
                stickman[3].get_end() + RIGHT*0.5,
                color=YELLOW, stroke_width=2
            )
            self.add(pointer)

            def update_man(pointer, step_mob, alpha):
                start = step_mob.get_left()
                end = step_mob.get_right()
                target = start + alpha * (end - start)
                pointer.put_start_and_end_on(stickman[3].get_end(), target)

            self.play(
                Write(step_mob, run_time=1.5),
                UpdateFromAlphaFunc(pointer, lambda mob, alpha: update_man(mob, step_mob, alpha))
            )

            self.remove(stickman, pointer)

            if len(steps_group) > 4:
                shift_amount = steps_group[-5].height + 0.7
                self.play(steps_group.animate.shift(UP*shift_amount), run_time=0.5)
            else:
                self.wait(0.5)

        # -----------------------------
        # Steps List (proof)
        # -----------------------------
        steps_list = [
            MathTex(r"\text{A circle = all points distance } r \text{ from } (h,k)", font_size=36, color=BLUE),
            MathTex(r"d = \sqrt{(x-h)^2 + (y-k)^2}", font_size=40, color=YELLOW),
            MathTex(r"\text{For any point on the circle: } d = r", font_size=36, color=GREEN),
            MathTex(r"\sqrt{(x-h)^2 + (y-k)^2} = r", font_size=38, color=RED),
            MathTex(r"(x-h)^2 + (y-k)^2 = r^2", font_size=42, color=ORANGE),
            MathTex(r"\boxed{(x-h)^2 + (y-k)^2 = r^2}", font_size=48, color=BLUE),
        ]

        for step in steps_list:
            add_step(step)

        # Ending
        self.wait(1.5)
        self.clear()
        final_text = Text("You proved it!", font_size=40, color=YELLOW)
        self.play(Write(final_text))
        self.wait(2)