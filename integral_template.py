from manim import *

# Configure TikTok portrait resolution
config.pixel_width = 1080
config.pixel_height = 1920
config.frame_width = 6  # Width in Manim units
config.frame_height = 6 * (1920 / 1080)  # Maintain aspect ratio
config.background_color = BLACK

class LogIntegralScrollingScene(Scene):
    def construct(self):
        # Title (centered vertically, scaled to fit screen width with margin)
        title = Text("Logarithmic Integral Fun! 🎵", font_size=60, color=YELLOW)
        title.scale_to_fit_width(config.frame_width - 1)
        title.move_to(ORIGIN)
        self.play(FadeIn(title))
        self.wait(2)
        self.play(FadeOut(title))

        # Question and integral (vertically centered)
        question = Text("Q: Solve the integral:", font_size=48, color=WHITE)
        integral_expr = MathTex(
            r"I = \int_0^{\infty} \frac{\ln(x^2)}{x^2 + a^2} \, dx",
            font_size=60, color=BLUE
        )

        # Apply left/right margin
        question.scale_to_fit_width(config.frame_width - 1)
        integral_expr.scale_to_fit_width(config.frame_width - 1)

        # Group and center vertically
        question_group = VGroup(question, integral_expr)
        integral_expr.next_to(question, DOWN, buff=0.5)
        question_group.move_to(ORIGIN)  # center vertically and horizontally

        self.play(Write(question), Write(integral_expr))
        self.wait(3)
        self.play(FadeOut(question), FadeOut(integral_expr))

        # Group to hold solution steps
        steps_group = VGroup()
        top_margin = 1.0  # Top margin
        steps_group.shift(DOWN * top_margin)  # initial downward shift

        # Function to add a step with scrolling
        def add_step(step_mob):
            steps_group.add(step_mob)
            # Position below previous step
            if len(steps_group) == 1:
                step_mob.to_edge(UP)
            else:
                step_mob.next_to(steps_group[-2], DOWN, buff=0.7)
            # Animate step appearing
            self.play(Write(step_mob))
            self.wait(1.5)
            # Scroll entire group upwards
            if len(steps_group) > 4:
                prev_step = steps_group[-5]
                buffer = 0.7
                shift_amount = prev_step.height + buffer
                self.play(
                    steps_group.animate.shift(UP * shift_amount),
                    run_time=1.0,
                    rate_func=smooth
                )

        # Steps of the solution
        steps_list = [
            MathTex(r"\ln(x^2) = 2 \ln(x)", font_size=50, color=ORANGE),
            MathTex(r"I = 2 \int_0^{\infty} \frac{\ln(x)}{x^2 + a^2} \, dx", font_size=50, color=ORANGE),
            MathTex(r"x = a t, \quad dx = a \, dt", font_size=45, color=ORANGE),
            MathTex(r"I = 2 \int_0^{\infty} \frac{\ln(a t)}{a^2(t^2 + 1)} \, a \, dt", font_size=45, color=ORANGE),
            MathTex(r"I = \frac{2}{a} \int_0^{\infty} \frac{\ln(a t)}{t^2 + 1} \, dt", font_size=50, color=ORANGE),
            MathTex(r"\ln(a t) = \ln(a) + \ln(t)", font_size=50, color=ORANGE),
            MathTex(r"I = \frac{2}{a} \left[ \ln(a) \int_0^{\infty} \frac{dt}{t^2 + 1} + \int_0^{\infty} \frac{\ln(t)}{t^2 + 1} \, dt \right]", font_size=40, color=ORANGE),
            MathTex(r"\int \frac{dt}{t^2 + 1} = arctan(t)+C", font_size=45, color=GREEN),
            MathTex(r"\int_0^{\infty} \frac{dt}{t^2 + 1} = \frac{\pi}{2}", font_size=45, color=GREEN),
            MathTex(r"\frac{2}{a} \cdot \ln(a) \cdot \frac{\pi}{2} = \frac{\pi \ln(a)}{a}", font_size=50, color=RED),
            MathTex(r"t=\frac{1}{u},\quad dt=-\frac{1}{u^{2}}\,du", font_size=45, color=GREEN),
            MathTex(r"J=\int_{0}^{\infty}\frac{\ln t}{t^{2}+1}\,dt", font_size=45, color=GREEN),
            MathTex(r"=\int_{\infty}^{0}\frac{\ln(1/u)}{(1/u)^{2}+1}\left(-\frac{1}{u^{2}}\,du\right)", font_size=45, color=GREEN),
            MathTex(r"=\int_{0}^{\infty}\frac{\ln(1/u)}{1+u^{2}}\,du", font_size=45, color=GREEN),
            MathTex(r"=\int_{0}^{\infty}\frac{-\ln u}{1+u^{2}}\,du", font_size=45, color=GREEN),
            MathTex(r"\Rightarrow J=-J \quad\Rightarrow\quad J=0", font_size=45, color=GREEN),
            MathTex(r"I = \frac{\pi \ln(a)}{a}", font_size=60, color=PURPLE)
        ]

        # Add steps with scrolling and left/right margin
        for step in steps_list:
            step.scale_to_fit_width(config.frame_width - 1)  # ensures 0.5 unit margin each side
            add_step(step)

        # Wait 3 seconds before celebration
        self.wait(3)

        # ✅ Celebration on a new page (centered vertically, scaled to fit screen)
        self.clear()
        celebration = Text("✅ Done! Math + Logs = Fun! 🎉", font_size=50, color=YELLOW)
        celebration.scale_to_fit_width(config.frame_width - 1)  # left/right margin
        celebration.move_to(ORIGIN)  # vertical and horizontal center
        self.play(Write(celebration))
        self.wait(3)
