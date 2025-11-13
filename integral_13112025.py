from manim import *

# Configure TikTok portrait resolution
config.pixel_width = 1080
config.pixel_height = 1920
config.frame_width = 6  # Width in Manim units
config.frame_height = 6 * (1920 / 1080)  # Maintain aspect ratio
config.background_color = BLACK

class SinSquareIntegralScene(Scene):
    def construct(self):
        # Increased left padding
        left_padding = 1.5  # increased from 0.3
        right_padding = 0.3  # keep right padding as before

        # Available width for text
        text_width = config.frame_width - left_padding - right_padding

        # Title
        title = Text("Solving the Integral 🎯", font_size=60, color=YELLOW)
        title.scale_to_fit_width(text_width)
        title.move_to(ORIGIN)
        self.play(FadeIn(title))
        self.wait(2)
        self.play(FadeOut(title))

        # Question
        question = Text("Q: Evaluate the integral:", font_size=48, color=WHITE)
        integral_expr = MathTex(
            r"I = \int_0^{\infty} \frac{\sin^2 x}{x^2} \, dx",
            font_size=60, color=BLUE
        )

        question.scale_to_fit_width(text_width)
        integral_expr.scale_to_fit_width(text_width)

        question_group = VGroup(question, integral_expr)
        integral_expr.next_to(question, DOWN, buff=0.5)
        question_group.move_to(ORIGIN)  # vertically centered
        self.play(Write(question), Write(integral_expr))
        self.wait(3)
        self.play(FadeOut(question), FadeOut(integral_expr))

        # Solution steps
        steps_group = VGroup()
        top_margin = 1.0
        steps_group.shift(DOWN * top_margin)

        def add_step(step_mob):
            # Apply horizontal margin with increased left padding
            step_mob.scale_to_fit_width(text_width)
            steps_group.add(step_mob)
            if len(steps_group) == 1:
                step_mob.to_edge(UP)
            else:
                step_mob.next_to(steps_group[-2], DOWN, buff=0.7)
            self.play(Write(step_mob))
            self.wait(1.5)
            if len(steps_group) > 3:
                prev_step = steps_group[-4]
                buffer = 0.7
                shift_amount = prev_step.height + buffer
                self.play(
                    steps_group.animate.shift(UP * shift_amount),
                    run_time=1.0,
                    rate_func=smooth
                )

        # Step-by-step solution
        steps_list = [
            MathTex(r"\sin^2 x = \frac{1 - \cos(2x)}{2}", font_size=50, color=ORANGE),
            MathTex(r"I = \frac{1}{2}\int_0^{\infty} \frac{1 - \cos(2x)}{x^2}\,dx", font_size=50, color=ORANGE),
            MathTex(r"\text{Let } I(a) = \int_0^{\infty} \frac{1 - \cos(ax)}{x^2}\,dx", font_size=50, color=GREEN),
            MathTex(r"I'(a) = \int_0^{\infty} \frac{\sin(ax)}{x}\,dx", font_size=50, color=GREEN),
            MathTex(r"I'(a) = \frac{\pi}{2}", font_size=55, color=RED),
            MathTex(r"I(a) = \frac{\pi a}{2} + C", font_size=50, color=ORANGE),
            MathTex(r"I(0) = 0 \Rightarrow C = 0", font_size=45, color=ORANGE),
            MathTex(r"I(a) = \frac{\pi a}{2}", font_size=55, color=YELLOW),
            MathTex(r"I = \frac{1}{2} I(2)", font_size=55, color=GREEN),
            MathTex(r"I = \frac{1}{2} \times \frac{\pi \times 2}{2}", font_size=55, color=GREEN),
            MathTex(r"I = \frac{\pi}{2}", font_size=70, color=PURPLE),
        ]

        for step in steps_list:
            add_step(step)

        self.wait(3)

        # Celebration
        self.clear()
        celebration = Text("✅ Final Answer: I = π/2 🎉", font_size=55, color=YELLOW)
        celebration.scale_to_fit_width(text_width)
        celebration.move_to(ORIGIN)
        self.play(Write(celebration))
        self.wait(3)
