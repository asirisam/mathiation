from manim import *
import numpy as np

# TikTok portrait
config.pixel_width = 1080
config.pixel_height = 1920
config.frame_width = 6
config.frame_height = 6 * (1920 / 1080)
config.background_color = BLACK

class LightClockTimeDilation(Scene):
    def construct(self):
        # -----------------------------
        # Title slide
        # -----------------------------
        title = Text("Time Dialation", font_size=36, color=YELLOW)
        title.move_to(ORIGIN)
        self.play(FadeIn(title, shift=UP))
        self.wait(2)
        self.play(FadeOut(title, shift=DOWN))

        # -----------------------------
        # Question slide after title
        # -----------------------------
        question = Text("Q: What is it?", font_size=36, color=ORANGE)
        equation = MathTex(r"\Delta t = \frac{\Delta t_0}{\sqrt{1 - v^2/c^2}}", font_size=36, color=BLUE)
        question_group = VGroup(question, equation).arrange(DOWN, buff=0.5)
        question_group.move_to(ORIGIN)
        self.play(FadeIn(question_group, shift=UP))
        self.wait(2)
        self.play(FadeOut(question_group, shift=DOWN))
        question2 = Text("Let's consider", font_size=36, color=GREEN)
        equation2 = Text("a Light Clock", font_size=36, color=RED)
        question_group2 = VGroup(question2, equation2).arrange(DOWN, buff=0.5)
        question_group2.move_to(ORIGIN)
        self.play(FadeIn(question_group2, shift=UP))
        self.wait(2)
        self.play(FadeOut(question_group2, shift=DOWN))

        # -----------------------------
        # Light clock explanation with symbols at top
        # -----------------------------
        top_padding = 1.5
        left_pad = 1.0
        right_pad = 1.0
        text_width = config.frame_width - left_pad - right_pad

        # Explanations of symbols
        explanations = VGroup(
            Text("L = distance between mirrors", font_size=28, color=BLUE),
            Text("Δt₀ = proper time (stationary clock)", font_size=28, color=GREEN),
            Text("Δt = dilated time (moving clock)", font_size=28, color=ORANGE),
            Text("v = speed of moving clock", font_size=28, color=RED),
            Text("c = speed of light", font_size=28, color=YELLOW)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        explanations.set_width(text_width)
        explanations.to_edge(UP, buff=top_padding)
        self.play(Write(explanations))
        self.wait(1.5)

        # -----------------------------
        # Light clocks animation
        # -----------------------------
        clock_height = 2.0
        clock_width = 1.0
        vertical_spacing = 0.2

        # Stationary clock (left)
        floor_s = Line(LEFT*2 + DOWN*1, LEFT*2 + RIGHT*clock_width + DOWN*1, color=BLUE)
        ceiling_s = Line(LEFT*2 + UP*1, LEFT*2 + RIGHT*clock_width + UP*1, color=BLUE)
        photon_s = Dot(color=BLUE).move_to(floor_s.get_center() + UP*0.05)
        label_s = Text("Stationary\nΔt₀", font_size=24, color=BLUE).next_to(floor_s, DOWN, buff=vertical_spacing)

        # Moving clock (right)
        floor_m = Line(RIGHT*1 + DOWN*1, RIGHT*1 + RIGHT*clock_width + DOWN*1, color=RED)
        ceiling_m = Line(RIGHT*1 + UP*1, RIGHT*1 + RIGHT*clock_width + UP*1, color=RED)
        clock_m = VGroup(floor_m, ceiling_m)
        # Start photon 1.0 left from current
        photon_m = Dot(color=YELLOW).move_to(floor_m.get_center() - RIGHT*1 + UP*0.05)
        label_m = Text("Moving\nΔt", font_size=24, color=RED).next_to(floor_m, DOWN, buff=vertical_spacing)

        # Labels for L
        L_line = Line(floor_s.get_center(), ceiling_s.get_center(), color=WHITE)
        L_label = MathTex("L", color=WHITE).next_to(L_line.get_right(), RIGHT*0.1)

        self.add(floor_s, ceiling_s, photon_s, label_s)
        self.add(clock_m, photon_m, label_m, L_line, L_label)

        # -----------------------------
        # Animate photon bouncing naturally
        # -----------------------------
        total_frames = 250
        photon_speed_s = 0.05
        photon_speed_m = 0.03  # slower for moving clock to show time dilation
        photon_dir_s = 1
        photon_dir_m = 1

        clock_start = RIGHT*1
        clock_end = RIGHT*3

        for alpha in np.linspace(0, 1, total_frames):
            # Move moving clock horizontally
            new_center = clock_start + alpha * (clock_end - clock_start)
            dx = new_center - clock_m.get_center()
            clock_m.shift(dx)

            # Stationary photon vertical bounce
            top_s = ceiling_s.get_center()[1]
            bottom_s = floor_s.get_center()[1]
            photon_y_s = photon_s.get_center()[1] + photon_dir_s * photon_speed_s
            if photon_y_s >= top_s:
                photon_y_s = top_s
                photon_dir_s *= -1
            elif photon_y_s <= bottom_s:
                photon_y_s = bottom_s
                photon_dir_s *= -1
            photon_s.move_to(np.array([photon_s.get_center()[0], photon_y_s, 0]))

            # Moving photon diagonal bounce (slower)
            top_m = ceiling_m.get_center()[1]
            bottom_m = floor_m.get_center()[1]
            photon_y_m = photon_m.get_center()[1] + photon_dir_m * photon_speed_m
            if photon_y_m >= top_m:
                photon_y_m = top_m
                photon_dir_m *= -1
            elif photon_y_m <= bottom_m:
                photon_y_m = bottom_m
                photon_dir_m *= -1
            photon_m.move_to(np.array([photon_m.get_center()[0] + 0.01, photon_y_m, 0]))

            self.wait(0.02)

        #self.wait(1)
        self.play(FadeOut(clock_m), FadeOut(photon_m), FadeOut(label_m))
        self.play(FadeOut(floor_s), FadeOut(ceiling_s), FadeOut(photon_s), FadeOut(label_s))
        self.play(FadeOut(L_line), FadeOut(L_label))
        self.play(FadeOut(explanations))

        # -----------------------------
        # Step-by-step scrolling equations
        # -----------------------------
        left_padding = 1.5
        right_padding = 0.3
        text_width = config.frame_width - left_padding - right_padding
        start_y = config.frame_height / 4
        steps_group = VGroup()

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
            arm_left = Line(body_top + LEFT*0.05 + UP*arm_y_offset, body_top + LEFT*arm_length + DOWN*0.05, color=YELLOW)
            arm_right = Line(body_top + RIGHT*0.05 + UP*arm_y_offset, body_top + RIGHT*arm_length + UP*0.05, color=YELLOW)
            leg_left = Line(body_bottom, body_bottom + LEFT*leg_length + DOWN*0.4, color=YELLOW)
            leg_right = Line(body_bottom, body_bottom + RIGHT*leg_length + DOWN*0.4, color=YELLOW)
            return VGroup(head, body, arm_left, arm_right, leg_left, leg_right)

        def add_step(step_mob):
            step_mob.set_width(min(step_mob.width, text_width))
            steps_group.add(step_mob)
            if len(steps_group) == 1:
                step_mob.move_to(UP * start_y)
            else:
                step_mob.next_to(steps_group[-2], DOWN, buff=0.7)

            stickman = create_stickman(step_mob.get_bottom() + DOWN*0.4)
            self.add(stickman)
            pointer_length = 0.4
            pointer = Line(stickman[3].get_end(), stickman[3].get_end() + RIGHT*pointer_length, color=YELLOW, stroke_width=2)
            self.add(pointer)

            def update_man(pointer, step_mob, alpha):
                start = step_mob.get_left()
                end = step_mob.get_right()
                target_pos = start + alpha*(end - start)
                pointer.put_start_and_end_on(stickman[3].get_end(), stickman[3].get_end() + 0.5*(target_pos - stickman[3].get_end()))

            self.play(
                Write(step_mob, run_time=1.5, rate_func=linear),
                UpdateFromAlphaFunc(pointer, lambda mob, alpha: update_man(mob, step_mob, alpha))
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

        # Steps in simple words with Pythagorean triangle
        steps_list = [
            MathTex(r"\text{Proper time: } \Delta t_0 = 2L/c", font_size=38, color=GREEN),
            MathTex(r"\text{Moving clock: light travels diagonal}", font_size=36, color=ORANGE),

            # Pythagorean triangle
            VGroup(
                Line(LEFT*1 + DOWN*0.5, LEFT*1 + UP*0.5, color=YELLOW),          # vertical = L
                Line(LEFT*1 + DOWN*0.5, RIGHT*1 + DOWN*0.5, color=RED),          # horizontal = v Δt / 2
                Line(LEFT*1 + UP*0.5, RIGHT*1 + DOWN*0.5, color=BLUE),           # hypotenuse = c Δt / 2
                MathTex("L", font_size=28, color=YELLOW).next_to(LEFT*1 + UP*0.0, LEFT),
                MathTex(r"v \Delta t/2", font_size=28, color=RED).next_to(RIGHT*0.0 + DOWN*0.5, DOWN),
                MathTex(r"c \Delta t/2", font_size=28, color=BLUE).next_to(RIGHT*0.7 + UP*0.0, UP)
            ),

            MathTex(r"(c \Delta t / 2)^2 = L^2 + (v \Delta t / 2)^2", font_size=40, color=YELLOW),
            MathTex(r"c^2 \Delta t^2 = v^2 \Delta t^2 + 4L^2", font_size=38, color=GREEN),
            MathTex(r"\Delta t^2 (c^2 - v^2) = 4L^2", font_size=38, color=ORANGE),
            MathTex(r"\Delta t = \frac{2L}{\sqrt{c^2 - v^2}}", font_size=38, color=YELLOW),
            MathTex(r"\Delta t = \frac{\Delta t_0}{\sqrt{1 - v^2/c^2}} = \gamma \Delta t_0", font_size=40, color=BLUE),
        ]

        for step in steps_list:
            add_step(step)

        self.wait(1.5)
        # Closing
        self.clear()
        final_text = Text("Nailed it!", font_size=32, color=YELLOW)
        final_text.move_to(ORIGIN)
        self.play(Write(final_text, run_time=2))
        self.wait(2)
