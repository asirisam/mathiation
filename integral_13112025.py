from manim import *
import numpy as np

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
            step_mob.set_width(min(step_mob.width, text_width))
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

        # Step-by-step solution
        steps_list = [
            MathTex(r"\sin^2 x = \frac{1 - \cos(2x)}{2}", font_size=42, color=ORANGE),
            MathTex(r"I = \frac{1}{2}\int_0^{\infty} \frac{1 - \cos(2x)}{x^2}\,dx", font_size=42, color=ORANGE),
            MathTex(r"\text{Let } I(a) = \int_0^{\infty} \frac{1 - \cos(ax)}{x^2}\,dx", font_size=40, color=GREEN),
            MathTex(r"\text{Differentiate w.r.t. } a: I'(a) = \frac{d}{da} \int_0^\infty \frac{1 - \cos(ax)}{x^2} dx", font_size=40, color=GREEN),
            MathTex(r"I'(a) = \int_0^\infty \frac{\partial}{\partial a} \frac{1 - \cos(ax)}{x^2} dx", font_size=40, color=GREEN),
            MathTex(r"I'(a) = \int_0^{\infty} \frac{\sin(ax)}{x}\,dx", font_size=40, color=GREEN),
            MathTex(r"I'(a) = \frac{\pi}{2}", font_size=38, color=RED),
            MathTex(r"I(a) = \frac{\pi a}{2} + C", font_size=40, color=ORANGE),
            MathTex(r"I(0) = 0 \Rightarrow C = 0", font_size=40, color=ORANGE),
            MathTex(r"I(a) = \frac{\pi a}{2}", font_size=38, color=YELLOW),
            MathTex(r"I = \frac{1}{2} I(2)", font_size=38, color=GREEN),
            MathTex(r"I = \frac{1}{2} \times \frac{\pi \times 2}{2}", font_size=38, color=GREEN),
            MathTex(r"I = \frac{\pi}{2}", font_size=36, color=PURPLE),
        ]

        for step in steps_list:
            add_step(step)

        self.wait(2)

        # -----------------------------
        # Graph on a new page
        # -----------------------------
        self.clear()

        # Re-show the question at the top
        question = Text("Q: Evaluate the integral:", font_size=36, color=WHITE).to_edge(UP)
        integral_expr = MathTex(
            r"I = \int_0^{\infty} \frac{\sin^2 x}{x^2} \, dx",
            font_size=40, color=BLUE
        ).next_to(question, DOWN, buff=0.3)
        self.play(Write(question), Write(integral_expr))
        self.wait(1.5)

        # Graph padding
        padding = 1.5
        axes_width = config.frame_width - 2 * padding
        axes_height = config.frame_height - 2 * padding - 1  # minus space for question

        axes = Axes(
            x_range=[0, 20, 2],
            y_range=[0, 1, 0.2],
            x_length=axes_width,
            y_length=axes_height,
            axis_config={"color": WHITE},
        ).next_to(integral_expr, DOWN, buff=padding/2)

        # Colorful graph and area
        graph = axes.plot(lambda x: (np.sin(x)**2)/(x**2) if x != 0 else 1, color=BLUE, stroke_width=4)
        area = axes.get_area(graph, x_range=[0, 20], color=PURPLE, opacity=0.4)

        # Animated points for luxury effect
        points = VGroup(*[Dot(axes.c2p(x, (np.sin(x)**2)/(x**2) if x!=0 else 1), radius=0.04, color=YELLOW) for x in np.linspace(0,20,50)])
        graph_label = MathTex(r"\frac{\sin^2 x}{x^2}", font_size=36, color=YELLOW).next_to(axes, UP)

        # Animation sequence
        self.play(Create(axes), run_time=1.5)
        self.play(Create(graph), FadeIn(graph_label), run_time=2)
        self.play(LaggedStartMap(FadeIn, points, shift=UP, lag_ratio=0.05), run_time=2.5)
        self.wait(1)
        self.play(FadeIn(area, shift=UP), run_time=2)

        self.wait(3)

        # Final answer
        self.clear()
        celebration = Text("✅ Final Answer: I = π/2 🎉", font_size=40, color=YELLOW)
        celebration.move_to(ORIGIN)
        self.play(Write(celebration))
        self.wait(5)
