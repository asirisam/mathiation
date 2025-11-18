from manim import *

# Configure TikTok portrait resolution
config.pixel_width = 1080
config.pixel_height = 1920
config.frame_width = 6
config.frame_height = 6 * (1920 / 1080)
config.background_color = BLACK

class AdvancedAlgebra(Scene):
    def construct(self):
        # -----------------------------
        # Step-by-step solution
        # -----------------------------
        left_padding = 1.5
        right_padding = 0.3
        text_width = config.frame_width - left_padding - right_padding

        # Title
        title = Text("Glitch in a Matrix", font_size=32, color=YELLOW)
        title.move_to(ORIGIN)
        self.play(FadeIn(title, shift=UP))
        self.wait(1.5)
        self.play(FadeOut(title, shift=DOWN))

        # Question (multi-line, centered)
        question = Text(
            "Q: Find eigenvalues \n& diagonalizability of",
            font_size=30,
            color=WHITE,
            line_spacing=1.2
        )
        function_expr = MathTex(
            r"A = \begin{bmatrix}4 & 1 & 0\\0 & 4 & 1\\0 & 0 & 4\end{bmatrix}",
            font_size=42, color=BLUE
        )
        question_group = VGroup(question, function_expr)
        question_group.arrange(DOWN, buff=0.5)
        question_group.move_to(ORIGIN)
        self.play(Write(question_group))
        self.wait(1.5)
        self.play(FadeOut(question_group, shift=DOWN))

        # Step-by-step solution
        steps_group = VGroup()
        start_y = config.frame_height / 4

        def create_stickman(center_point):
            """Create a stickman with lower arms and angled left arm downwards."""
            head_radius = 0.15
            body_length = 0.4
            arm_length = 0.25
            leg_length = 0.4

            head = Circle(radius=head_radius, color=YELLOW).move_to(center_point + UP * (body_length / 2))

            body_top = center_point + UP * (head_radius - 0.075)
            body_bottom = center_point + DOWN * (body_length - head_radius)
            body = Line(body_top, body_bottom, color=YELLOW)

            arm_y_offset = -0.05
            arm_left = Line(
                body_top + LEFT * 0.05 + UP * arm_y_offset,
                body_top + LEFT * arm_length + DOWN * 0.05,
                color=YELLOW
            )
            arm_right = Line(
                body_top + RIGHT * 0.05 + UP * arm_y_offset,
                body_top + RIGHT * arm_length + UP * 0.05,
                color=YELLOW
            )

            leg_left = Line(body_bottom, body_bottom + LEFT * leg_length + DOWN * 0.4, color=YELLOW)
            leg_right = Line(body_bottom, body_bottom + RIGHT * leg_length + DOWN * 0.4, color=YELLOW)

            stickman = VGroup(head, body, arm_left, arm_right, leg_left, leg_right)
            return stickman

        def add_step(step_mob):
            """Add a step with stickman appearing below the step, then disappearing."""
            step_mob.set_width(min(step_mob.width, text_width))
            steps_group.add(step_mob)

            # Position the step
            if len(steps_group) == 1:
                step_mob.move_to(UP * start_y)
            else:
                step_mob.next_to(steps_group[-2], DOWN, buff=0.7)

            # Add stickman below the step
            stickman = create_stickman(step_mob.get_bottom() + DOWN * 0.4)
            self.add(stickman)

            pointer_length = 0.4
            pointer = Line(stickman[3].get_end(), stickman[3].get_end() + RIGHT * pointer_length, color=YELLOW, stroke_width=2)
            self.add(pointer)

            def update_man(pointer, step_mob, alpha):
                start = step_mob.get_left()
                end = step_mob.get_right()
                target_pos = start + alpha * (end - start)
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

        # Step-by-step solution content
        steps_list = [
            MathTex(r"\text{Step 1: Find eigenvalues}", font_size=36, color=ORANGE),
            MathTex(r"\text{Characteristic polynomial: } \det(A-\lambda I)=0", font_size=36, color=GREEN),
            MathTex(r"A - \lambda I = \begin{bmatrix}0 & 1 & 0\\0 & 0 & 1\\0 & 0 & 0\end{bmatrix}", font_size=36, color=BLUE),
            MathTex(r"\therefore \lambda = 4 \text{ (triple)}", font_size=36, color=YELLOW),
            MathTex(r"\text{Step 2: Check diagonalizability}", font_size=36, color=ORANGE),
            MathTex(r"\text{Solve }(A-4I)v=0", font_size=36, color=GREEN),
            MathTex(r"\text{Let } v = \begin{bmatrix}x\\y\\z\end{bmatrix}, \text{ then } y=0, z=0 \Rightarrow v=\begin{bmatrix}x\\0\\0\end{bmatrix}", font_size=36, color=YELLOW),
            MathTex(r"\text{Geometric multiplicity = 1}", font_size=36, color=RED),
            MathTex(r"\text{Alegebric multiplicity = 3}", font_size=36, color=RED),
            MathTex(r"\text{GM} = 1 < \text{AM} = 3, \text{ so not diagonalizable}", font_size=36, color=RED),
            MathTex(r"\text{Step 3: Jordan form}", font_size=36, color=ORANGE),
            MathTex(r"\text{Since not diagonalizable, A is already in Jordan form: }", font_size=36, color=GREEN),
            MathTex(r"J = \begin{bmatrix}4 & 1 & 0\\0 & 4 & 1\\0 & 0 & 4\end{bmatrix}", font_size=36, color=BLUE),
            MathTex(r"\text{Summary: } \lambda=4 \text{ (triple)}", font_size=36, color=YELLOW),
            MathTex(r"\text{Diagonalizable? No}", font_size=36, color=YELLOW),
            MathTex(r"J=A", font_size=36, color=YELLOW)
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
