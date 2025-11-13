from manim import *

# Configure TikTok portrait resolution
config.pixel_width = 1080
config.pixel_height = 1920
config.frame_width = 6
config.frame_height = 6 * (1920 / 1080)
config.background_color = BLACK

class SinSquareIntegralScene(Scene):
    def construct(self):
        # Padding and text area
        left_padding = 1.5
        right_padding = 0.3
        text_width = config.frame_width - left_padding - right_padding

        # Title
        title = Text("Solving the Integral 🎯", font_size=44, color=YELLOW)
        title.move_to(ORIGIN)
        self.play(FadeIn(title))
        self.wait(2)
        self.play(FadeOut(title))

        # Question
        question = Text("Q: Evaluate the integral:", font_size=40, color=WHITE)
        integral_expr = MathTex(
            r"I = \int_0^{\infty} \frac{\sin^2 x}{x^2} \, dx",
            font_size=42, color=BLUE
        )

        question.next_to(integral_expr, UP, buff=0.5)
        question_group = VGroup(question, integral_expr).move_to(ORIGIN)
        self.play(Write(question), Write(integral_expr))
        self.wait(3)
        self.play(FadeOut(question), FadeOut(integral_expr))

        # Step group setup
        steps_group = VGroup()
        steps_group.shift(DOWN)

        def add_step(step_mob):
            step_mob.set_width(min(step_mob.width, text_width))  # only shrink if too wide
            steps_group.add(step_mob)
            if len(steps_group) == 1:
                step_mob.to_edge(UP)
            else:
                step_mob.next_to(steps_group[-2], DOWN, buff=0.7)
            self.play(Write(step_mob))
            self.wait(1.2)
            if len(steps_group) > 5:
                prev_step = steps_group[-6]
                shift_amount = prev_step.height + 0.7
                self.play(
                    steps_group.animate.shift(UP * shift_amount),
                    run_time=1.0,
                    rate_func=smooth
                )

        # Step-by-step solution (with added steps)
        steps_list = [
            MathTex(r"\sin^2 x = \frac{1 - \cos(2x)}{2}", font_size=42, color=ORANGE),
            MathTex(r"I = \frac{1}{2}\int_0^{\infty} \frac{1 - \cos(2x)}{x^2}\,dx", font_size=42, color=ORANGE),
            MathTex(r"\text{Let } I(a) = \int_0^{\infty} \frac{1 - \cos(ax)}{x^2}\,dx", font_size=40, color=GREEN),

            # New Step 3a: Show derivative under the integral sign
            MathTex(r"\text{Differentiate w.r.t. } a: I'(a) = \frac{d}{da} \int_0^\infty \frac{1 - \cos(ax)}{x^2} dx", font_size=40, color=GREEN),
            
            # New Step 3b: Show derivative applied
            MathTex(r"I'(a) = \int_0^\infty \frac{\partial}{\partial a} \frac{1 - \cos(ax)}{x^2} dx", font_size=40, color=GREEN),

            # Original Step 4
            MathTex(r"I'(a) = \int_0^{\infty} \frac{\sin(ax)}{x}\,dx", font_size=40, color=GREEN),
            MathTex(r"I'(a) = \frac{\pi}{2}", font_size=38, color=RED),
            MathTex(r"I(a) = \frac{\pi a}{2} + C", font_size=40, color=ORANGE),
            MathTex(r"I(0) = 0 \Rightarrow C = 0", font_size=40, color=ORANGE),
            MathTex(r"I(a) = \frac{\pi a}{2}", font_size=38, color=YELLOW),
            MathTex(r"I = \frac{1}{2} I(2)", font_size=38, color=GREEN),
            MathTex(r"I = \frac{1}{2} \times \frac{\pi \times 2}{2}", font_size=38, color=GREEN),
            MathTex(r"I = \frac{\pi}{2}", font_size=36, color=PURPLE),  # smaller final line
        ]

        for step in steps_list:
            add_step(step)

        self.wait(3)

        # Final answer
        self.clear()
        celebration = Text("✅ Final Answer: I = π/2 🎉", font_size=40, color=YELLOW)
        celebration.move_to(ORIGIN)
        self.play(Write(celebration))
        self.wait(5)
