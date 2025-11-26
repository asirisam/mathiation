from manim import *
import numpy as np

# Configure TikTok portrait resolution
config.pixel_width = 1080
config.pixel_height = 1920
config.frame_width = 6
config.frame_height = 6 * (1920 / 1080)
config.background_color = BLACK

class DiffScene(Scene):
    def construct(self):
        # -----------------------------
        # Step-by-step solution
        # -----------------------------
        left_padding = 1.5
        right_padding = 0.3
        text_width = config.frame_width - left_padding - right_padding

        # Title
        title = Text("The Hidden Derivative 🎯", font_size=30, color=YELLOW)
        title.move_to(ORIGIN)
        self.play(FadeIn(title, shift=UP))
        self.wait(1.5)
        self.play(FadeOut(title, shift=DOWN))

        # Question
        question = Text("Q: Let's differentiate:", font_size=30, color=WHITE)
        function_expr = MathTex(
            r"f(x)=\dfrac{x^{3}\ln x}{\sqrt{1+x^{2}}}",
            font_size=42, color=BLUE
        )
        question.next_to(function_expr, UP, buff=0.5)
        question_group = VGroup(question, function_expr).move_to(ORIGIN)
        self.play(Write(question_group))
        self.wait(1.5)
        self.play(FadeOut(question_group, shift=DOWN))

        # Step group setup
        steps_group = VGroup()
        start_y = config.frame_height / 4

        def add_step(step_mob):
            step_mob.set_width(min(step_mob.width, text_width))
            steps_group.add(step_mob)

            if len(steps_group) == 1:
                step_mob.move_to(UP * start_y)
            else:
                step_mob.next_to(steps_group[-2], DOWN, buff=0.7)

            self.play(Write(step_mob), run_time=1)
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

        # Step-by-step solution
        steps_list = [
            MathTex(r"\text{Given } f(x)=\dfrac{x^{3}\ln x}{\sqrt{1+x^{2}}}", font_size=40, color=ORANGE),
            # Split long line 1 into 2
            MathTex(r"\text{Treat as } f(x)=\dfrac{u(x)}{v(x)},", font_size=38, color=GREEN),
            MathTex(r"\text{with } u=x^{3}\ln x, \quad v=(1+x^{2})^{1/2}", font_size=38, color=GREEN),
            MathTex(r"\text{Quotient rule: }(u/v)'=\dfrac{u'v-uv'}{v^{2}}", font_size=40, color=ORANGE),
            MathTex(r"\text{So } f'(x)=\dfrac{u'v-uv'}{v^{2}}", font_size=40, color=GREEN),
            # Split long line 2 into 2
            MathTex(r"\text{Compute } u = x^{3}\ln x,", font_size=38, color=GREEN),
            MathTex(r"\text{(product): } u' = (x^{3})' \ln x + x^{3} (\ln x)'", font_size=38, color=GREEN),
            MathTex(r"(x^{3})'=3x^{2}, \quad (\ln x)'=\dfrac{1}{x}", font_size=36, color=GREEN),
            MathTex(r"\therefore\ u' = 3x^{2}\ln x + x^{2}", font_size=40, color=YELLOW),
            # Split long line 3 into 2
            MathTex(r"\text{Now } v = (1+x^{2})^{1/2},", font_size=38, color=GREEN),
            MathTex(r"\Rightarrow v' = \tfrac{1}{2}(1+x^{2})^{-1/2} \cdot 2x = \dfrac{x}{\sqrt{1+x^{2}}}", font_size=38, color=GREEN),
            MathTex(r"\text{Substitute into quotient rule:}", font_size=36, color=ORANGE),
            MathTex(
                r"f'(x)=\dfrac{\big(3x^{2}\ln x + x^{2}\big)\sqrt{1+x^{2}} - x^{3}\ln x\cdot\dfrac{x}{\sqrt{1+x^{2}}}}{(1+x^{2})}",
                font_size=36, color=YELLOW
            ),
            MathTex(
                r"f'(x)=\dfrac{\dfrac{\big(3x^{2}\ln x + x^{2}\big)(1+x^{2}) - x^{4}\ln x}{\sqrt{1+x^{2}}}}{(1+x^{2})}",
                font_size=36, color=GREEN
            ),
            MathTex(
                r"\boxed{\,f'(x)=\dfrac{\big(3x^{2}\ln x + x^{2}\big)(1+x^{2}) - x^{4}\ln x}{(1+x^{2})^{3/2}}\,}",
                font_size=38, color=YELLOW
            ),
            MathTex(
                r"\boxed{\,f'(x)=\dfrac{x^{2}\Big((3\ln x + 1)(1+x^{2}) - x^{2}\ln x\Big)}{(1+x^{2})^{3/2}}\,}",
                font_size=34, color=YELLOW
            ),
        ]

        for step in steps_list:
            add_step(step)

        self.wait(1.5)

        # -----------------------------
        # Graph: function first
        # -----------------------------
        self.clear()
        top_padding = 1.5

        function_expr = MathTex(
            r"f(x)=\dfrac{x^{3}\ln x}{\sqrt{1+x^{2}}}",
            font_size=40, color=BLUE
        )
        if function_expr.width > text_width:
            function_expr.set_width(text_width)
        function_expr.to_edge(UP, buff=top_padding)
        self.play(Write(function_expr, run_time=1.5))

        axes_width = text_width
        axes_height = axes_width * (config.frame_height / config.frame_width) * 0.5

        axes = Axes(
            x_range=[0.1, 5, 0.5],
            y_range=[-1, 40, 5],
            x_length=axes_width,
            y_length=axes_height,
            axis_config={"color": WHITE},
        ).next_to(function_expr, DOWN, buff=0.8)

        f = lambda x: (x**3 * np.log(x)) / np.sqrt(1 + x**2)
        graph = axes.plot(f, color=BLUE, stroke_width=4)
        points = VGroup(*[Dot(axes.c2p(x, f(x)), radius=0.04, color=YELLOW) for x in np.linspace(0.1, 5, 80)])

        self.play(Create(axes), run_time=1.5)
        self.play(Create(graph), run_time=2)
        self.play(LaggedStartMap(FadeIn, points, shift=UP, lag_ratio=0.05), run_time=2.5)
        self.wait(2)

        # -----------------------------
        # Graph: derivative last
        # -----------------------------
        self.clear()
        derivative_expr = MathTex(
            r"f'(x)=\dfrac{\big(3x^{2}\ln x + x^{2}\big)(1+x^{2}) - x^{4}\ln x}{(1+x^{2})^{3/2}}",
            font_size=36, color=YELLOW
        )
        if derivative_expr.width > text_width:
            derivative_expr.set_width(text_width)
        derivative_expr.to_edge(UP, buff=top_padding)
        self.play(Write(derivative_expr, run_time=1.5))

        axes2 = Axes(
            x_range=[0.1, 5, 0.5],
            y_range=[-2, 25, 5],
            x_length=axes_width,
            y_length=axes_height,
            axis_config={"color": WHITE},
        ).next_to(derivative_expr, DOWN, buff=0.8)

        fp = lambda x: (((3*x**2*np.log(x) + x**2)*(1+x**2) - x**4*np.log(x)) / (1+x**2)**(3/2))
        graph2 = axes2.plot(fp, color=YELLOW, stroke_width=4)
        points2 = VGroup(*[Dot(axes2.c2p(x, fp(x)), radius=0.04, color=RED) for x in np.linspace(0.1, 5, 80)])

        self.play(Create(axes2), run_time=1.5)
        self.play(Create(graph2), run_time=2)
        self.play(LaggedStartMap(FadeIn, points2, shift=UP, lag_ratio=0.05), run_time=2.5)
        self.wait(2)

        # Closing
        self.clear()
        final_text = Text("✅ Nailed it! 🎉", font_size=30, color=YELLOW)
        final_text.move_to(ORIGIN)
        self.play(Write(final_text, run_time=2))
        self.wait(2)