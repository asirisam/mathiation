from manim import *
import numpy as np

# Configure TikTok portrait resolution
config.pixel_width = 1080
config.pixel_height = 1920
config.frame_width = 6
config.frame_height = 6 * (1920 / 1080)
config.background_color = BLACK

class PendulumTheoremProof(Scene):
    def construct(self):
        # -----------------------------
        # Config
        # -----------------------------
        left_padding = 1.0
        right_padding = 1.0
        text_width = config.frame_width - left_padding - right_padding

        # Title
        title = Text("Motion Secrets", font_size=32, color=YELLOW)
        title.move_to(ORIGIN)  # vertically centered
        self.play(FadeIn(title, shift=UP))
        self.wait(1.5)
        self.play(FadeOut(title, shift=DOWN))

        # Question
        question = Text("Q: Period of a simple Pendulum?", font_size=30, color=WHITE)
        function_expr = Text(
            "Linearised Pendulum Equation\n"
            "T = 2π√(L/g)",
            font_size=26, color=BLUE, line_spacing=1.2
        )
        question.next_to(function_expr, UP, buff=0.5)
        question_group = VGroup(question, function_expr)
        question_group.set_width(text_width)  # limit width to fit screen
        question_group.move_to(ORIGIN)
        self.play(Write(question_group))
        self.wait(2)
        self.play(FadeOut(question_group, shift=DOWN))

        # -----------------------------
        # Pendulum diagram with legends and oscillation
        # -----------------------------
        L = 3.0  # pendulum length
        theta0 = 30 * DEGREES  # max angle
        pivot = np.array([0, 1.5, 0])

        # Explanations of symbols
        top_padding = 1.5
        explanations = VGroup(
            Text("Mass m at the end of a Massless Rod", font_size=28, color=BLUE),
            Text("Lenght of a Massless Rod: L", font_size=28, color=GREEN),
            Text("Displaced by an angle θ(t) from the vertical", font_size=28, color=ORANGE),
            Text("Gravity g acts downward", font_size=28, color=RED)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        explanations.set_width(text_width)
        explanations.to_edge(UP, buff=top_padding)
        self.play(Write(explanations))
        self.wait(1.5)

        # Create vertical line as reference
        vertical_line = Line(pivot, pivot + DOWN*L, color=GRAY, stroke_width=2)

        # Initial bob position
        bob_pos = pivot + L * np.array([np.sin(theta0), -np.cos(theta0), 0])
        rod = Line(pivot, bob_pos, color=WHITE, stroke_width=4)
        bob = Dot(bob_pos, radius=0.15, color=YELLOW)
        pivot_dot = Dot(pivot, radius=0.08, color=RED)

        # Angle arc and label
        angle_arc = Arc(
            start_angle=-PI/2,  # start from vertical
            angle=theta0,
            radius=0.5,
            arc_center=pivot,
            color=BLUE
        )
        theta_label = MathTex(r"\theta(t)", font_size=28, color=BLUE)
        theta_label.next_to(angle_arc.point_from_proportion(0.5), UP + LEFT*0.05)

        # Length, mass, and gravity labels
        length_label = MathTex("L", font_size=28, color=GREEN)
        length_label.move_to((pivot + bob_pos)/2 + RIGHT*0.2)
        mass_label = MathTex("m", font_size=28, color=ORANGE)
        mass_label.next_to(bob, UP + RIGHT*0.1)
        g_arrow = Arrow(start=bob.get_center(), end=bob.get_center() + DOWN*0.5, color=RED, buff=0)
        g_label = MathTex("g", font_size=28, color=RED)
        g_label.next_to(g_arrow.get_end(), RIGHT*0.1)

        pendulum_group = VGroup(
            rod, bob, pivot_dot, vertical_line, angle_arc,
            theta_label, length_label, mass_label, g_arrow, g_label
        )
        self.add(pendulum_group)

        def pendulum_updater(mob, dt):
            t = self.renderer.time
            angle = theta0 * np.cos(np.sqrt(9.8/L) * t)
            new_bob = pivot + L * np.array([np.sin(angle), -np.cos(angle), 0])
            mob[0].put_start_and_end_on(pivot, new_bob)
            mob[1].move_to(new_bob)

            # Draw θ from vertical to bob (pivot line as origin)
            if angle >= 0:  # bob swings right (clockwise)
                mob[4].become(
                    Arc(start_angle=-PI/2, angle=angle, radius=0.5, arc_center=pivot, color=BLUE)
                )
            else:  # bob swings left (anticlockwise)
                mob[4].become(
                    Arc(start_angle=-PI/2, angle=angle, radius=0.5, arc_center=pivot, color=BLUE)
                )
            mob[5].next_to(mob[4].point_from_proportion(0.5), UP + LEFT*0.05)
            mob[6].move_to((pivot + new_bob)/2 + RIGHT*0.2)
            mob[7].next_to(new_bob, UP + RIGHT*0.1)
            mob[8].put_start_and_end_on(new_bob, new_bob + DOWN*0.5)
            mob[9].next_to(mob[8].get_end(), RIGHT*0.1)

        pendulum_group.add_updater(pendulum_updater)
        self.wait(7)
        pendulum_group.remove_updater(pendulum_updater)
        self.wait(0.5)

        # -----------------------------
        # Step-by-step solution (after pendulum)
        # -----------------------------
        self.clear()
        steps_group = VGroup()
        start_y = config.frame_height / 4

        def create_stickman(center_point):
            head_radius = 0.15
            body_length = 0.4
            arm_length = 0.25
            leg_length = 0.4
            head = Circle(radius=head_radius, color=YELLOW).move_to(center_point + UP * (body_length / 2))
            body_top = center_point + UP * (head_radius - 0.075)
            body_bottom = center_point + DOWN * (body_length - head_radius)
            body = Line(body_top, body_bottom, color=YELLOW)
            arm_left = Line(body_top + LEFT*0.05, body_top + LEFT*arm_length + DOWN*0.05, color=YELLOW)
            arm_right = Line(body_top + RIGHT*0.05, body_top + RIGHT*arm_length + UP*0.05, color=YELLOW)
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
            stickman = create_stickman(step_mob.get_bottom() + DOWN * 0.4)
            self.add(stickman)
            pointer = Line(
                stickman[3].get_end(),
                stickman[3].get_end() + RIGHT * 0.4,
                color=YELLOW,
                stroke_width=2
            )
            self.add(pointer)
            def update_man(pointer, step_mob, alpha):
                start = step_mob.get_left()
                end = step_mob.get_right()
                target = start + alpha * (end - start)
                pointer.put_start_and_end_on(
                    stickman[3].get_end(),
                    stickman[3].get_end() + 0.5 * (target - stickman[3].get_end())
                )
            self.play(
                Write(step_mob, run_time=1.5, rate_func=linear),
                UpdateFromAlphaFunc(pointer, lambda mob, a: update_man(mob, step_mob, a))
            )
            self.remove(stickman, pointer)
            if len(steps_group) > 3:
                prev_step = steps_group[-4]
                shift_amt = prev_step.height + 0.7
                self.play(steps_group.animate.shift(UP * shift_amt), run_time=0.5)
            else:
                self.wait(0.5)

        # -----------------------------
        # Pendulum theorem steps
        # -----------------------------
        steps_list = [
            MathTex(r"\text{Apply Newton's 2nd law along tangential direction}", font_size=32, color=ORANGE),
            MathTex(r"s = L \theta \implies a_\text{tangential} = L \frac{d^2 \theta}{dt^2}", font_size=36, color=GREEN),
            MathTex(r"F = m a_\text{tangential} \implies m L \frac{d^2 \theta}{dt^2} = - m g \sin \theta", font_size=36, color=YELLOW),
            MathTex(r"\frac{d^2 \theta}{dt^2} + \frac{g}{L} \sin \theta = 0", font_size=38, color=ORANGE),
            MathTex(r"\text{Nonlinear equation; exact for any amplitude}", font_size=32, color=GREEN),
            MathTex(r"\text{For small angles: } \sin \theta \approx \theta", font_size=36, color=YELLOW),
            MathTex(r"\frac{d^2 \theta}{dt^2} + \frac{g}{L} \theta = 0", font_size=38, color=ORANGE),
            MathTex(r"\text{Compare with SHM: } \frac{d^2 x}{dt^2} + \omega^2 x = 0", font_size=36, color=GREEN),
            MathTex(r"\omega = \sqrt{\frac{g}{L}}", font_size=36, color=YELLOW),
            MathTex(r"T = \frac{2 \pi}{\omega} = 2 \pi \sqrt{\frac{L}{g}}", font_size=40, color=ORANGE),
            MathTex(r"\text{Hence, for small oscillations, }", font_size=36, color=GREEN),
            MathTex(r"\text{T is independent of amplitude } \theta_0", font_size=36, color=GREEN)
        ]

        for step in steps_list:
            add_step(step)

        self.wait(2)
        # -----------------------------
        # Closing text (vertically centered)
        # -----------------------------
        self.clear()
        final_text = Text("Nailed it!", font_size=32, color=YELLOW)
        final_text.move_to(ORIGIN)
        self.play(Write(final_text, run_time=2))
        self.wait(1)
