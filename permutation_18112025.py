from manim import *
import numpy as np

# Configure TikTok portrait resolution
config.pixel_width = 1080
config.pixel_height = 1920
config.frame_width = 6
config.frame_height = 6 * (1920 / 1080)
config.background_color = BLACK

class TrigInfiniteCycle(Scene):
    def construct(self):
        # -----------------------------
        # Step-by-step solution
        # -----------------------------
        left_padding = 1.0
        right_padding = 1.0
        text_width = config.frame_width - left_padding - right_padding

        # Title
        title = Text("Permutations", font_size=38, color=YELLOW)
        title.move_to(ORIGIN)
        self.play(FadeIn(title, shift=UP))
        self.wait(1.5)
        self.play(FadeOut(title, shift=DOWN))

        # Question (vertically centered, larger font)
        question_text = (
            "Q: 10 employees (6 men, 4 women)\n" 
	    "sit around a round table.\n"
            "M1 and M2 cannot sit together,\n" 
	    "women cannot sit together.\n"
            "Find total seating arrangements."
        )
        question = Text(
            question_text, 
            font_size=24,  # increased font
            color=WHITE,
            line_spacing=1.2,
        )
        question.move_to(ORIGIN)  # vertically center
        self.play(Write(question))
        self.wait(2)
        self.play(FadeOut(question, shift=DOWN))

        # Step-by-step solution
        steps_group = VGroup()
        start_y = config.frame_height / 4

        def create_stickman(center_point, gender="male"):
            """Create a realistic stickman with optional dress for female."""
            color = BLUE if gender == "male" else PINK
            head_radius = 0.15
            body_length = 0.5
            arm_length = 0.3
            leg_length = 0.4

            # Head
            head = Circle(radius=head_radius, color=color, fill_opacity=1).move_to(center_point + UP * (body_length/2))

            # Body
            body_top = center_point + UP * (head_radius - 0.05)
            body_bottom = center_point + DOWN * (body_length - head_radius)
            body = Line(body_top, body_bottom, color=color)

            # Arms (left arm angled 45 degrees)
            arm_left = Line(
                body_top,
                body_top + LEFT * arm_length + DOWN * arm_length,
                color=color
            )
            arm_right = Line(
                body_top + RIGHT * 0.05,
                body_top + RIGHT * arm_length + DOWN * 0.05,
                color=color
            )

            # Legs
            leg_left = Line(body_bottom, body_bottom + LEFT * leg_length + DOWN * 0.35, color=color)
            leg_right = Line(body_bottom, body_bottom + RIGHT * leg_length + DOWN * 0.35, color=color)

            # Dress for female
            if gender == "female":
                skirt_top = body_bottom
                skirt_bottom_left = body_bottom + LEFT * 0.2 + DOWN * 0.2
                skirt_bottom_right = body_bottom + RIGHT * 0.2 + DOWN * 0.2
                dress = Polygon(skirt_top, skirt_bottom_left, skirt_bottom_right, color=color, fill_opacity=0.6)
                stickman = VGroup(head, body, arm_left, arm_right, leg_left, leg_right, dress)
            else:
                stickman = VGroup(head, body, arm_left, arm_right, leg_left, leg_right)

            return stickman

        def add_step(step_mob, gender="male"):
            """Add a step with stickman appearing below the step, then disappearing."""
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

        # Steps content
        steps_list = [
            MathTex(r"\text{Step 1: Circular permutation theorem}", font_size=38, color=ORANGE),
            MathTex(r"\text{For n objects around a table: } (n-1)!", font_size=38, color=GREEN),
            MathTex(r"\text{Step 2: Seat 6 men first (ignore M1-M2 restriction)}", font_size=38, color=ORANGE),
            MathTex(r"(6-1)! = 5! = 120", font_size=38, color=BLUE),
            MathTex(r"\text{Step 3: Place 4 women between men}", font_size=38, color=ORANGE),
            MathTex(r"\binom{6}{4} \cdot 4! = 15 \cdot 24 = 360", font_size=38, color=PINK),
            MathTex(r"\text{Step 4: Total arrangements ignoring restriction}", font_size=38, color=ORANGE),
            MathTex(r"120 \cdot 360 = 43200", font_size=38, color=YELLOW),
            MathTex(r"\text{Step 5: Subtract arrangements with M1 and M2 together}", font_size=38, color=ORANGE),
            MathTex(r"\text{Treat M1-M2 as a single block: 5 men entities}", font_size=38, color=GREEN),
            MathTex(r"(5-1)! \cdot 2! = 4! \cdot 2 = 48", font_size=38, color=BLUE),
            MathTex(r"\text{Women placement for this case: } \binom{5}{4} \cdot 4! = 5 \cdot 24 = 120", font_size=38, color=PINK),
            MathTex(r"\text{Invalid arrangements: } 48 \cdot 120 = 5760", font_size=38, color=RED),
            MathTex(r"\text{Step 6: Valid arrangements}", font_size=38, color=ORANGE),
            MathTex(r"43200 - 5760 = 37440", font_size=38, color=YELLOW),
            MathTex(r"\text{Answer: } 37,440 \text{ valid arrangements}", font_size=38, color=YELLOW),
            MathTex(r"\text{Rules or Principles used:}", font_size=36, color=GREEN),
            MathTex(r"\text{Circular permutation}", font_size=36, color=GREEN),
            MathTex(r"\text{combinations}", font_size=36, color=GREEN),
            MathTex(r"\text{complement principle}", font_size=36, color=GREEN)
        ]

        for step in steps_list:
            add_step(step)

        self.wait(1.5)

        # Closing
        self.clear()
        final_text = Text("Nailed it!", font_size=40, color=YELLOW)
        final_text.move_to(ORIGIN)
        self.play(Write(final_text, run_time=2))
        self.wait(2)
