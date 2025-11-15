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
        left_padding = 1.5
        right_padding = 0.3
        text_width = config.frame_width - left_padding - right_padding

        # Title
        title = Text("Step Into the World of Trig", font_size=32, color=YELLOW)
        title.move_to(ORIGIN)
        self.play(FadeIn(title, shift=UP))
        self.wait(1.5)
        self.play(FadeOut(title, shift=DOWN))

        # Question
        question = Text("Q: Ready to solve?", font_size=30, color=WHITE)
        function_expr = MathTex(
            r"2\cos^2 x - 3\sin x = 0",
            font_size=42, color=BLUE
        )
        question.next_to(function_expr, UP, buff=0.5)
        question_group = VGroup(question, function_expr).move_to(ORIGIN)
        self.play(Write(question_group))
        self.wait(1.5)
        self.play(FadeOut(question_group, shift=DOWN))

        # Step-by-step solution
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

        steps_list = [
            MathTex(r"2\cos^2 x - 3\sin x = 0", font_size=40, color=ORANGE),
            MathTex(r"\text{Use } \cos^2 x = 1 - \sin^2 x", font_size=38, color=GREEN),
            MathTex(r"2(1 - \sin^2 x) - 3\sin x = 0", font_size=38, color=GREEN),
            MathTex(r"-2\sin^2 x - 3\sin x + 2 = 0", font_size=38, color=GREEN),
            MathTex(r"2\sin^2 x + 3\sin x - 2 = 0", font_size=38, color=YELLOW),
            MathTex(r"\text{Quadratic formula: } \sin x = \frac{-3 \pm \sqrt{9 + 16}}{4}", font_size=36, color=ORANGE),
            MathTex(r"\sin x = \frac{-3 + 5}{4} = \frac{1}{2}, \quad \sin x = \frac{-3 - 5}{4} = -2", font_size=36, color=GREEN),
            MathTex(r"\text{Only } \sin x = \frac{1}{2} \text{ is valid}", font_size=36, color=YELLOW),
            MathTex(r"\text{\checkmark General solution accounts for infinite cycles!}", font_size=32, color=YELLOW),
            MathTex(r"x = \frac{\pi}{6} + 2n\pi \text{ or } x = \frac{5\pi}{6} + 2n\pi, \quad n \in \mathbb{Z}", font_size=36, color=YELLOW)
        ]

        for step in steps_list:
            add_step(step)

        self.wait(1.5)

        # -----------------------------
        # Graph of function f(x) with zeros labelled
        # -----------------------------
        self.clear()
        top_padding = 1.5

        function_expr = MathTex(
            r"f(x) = 2\cos^2 x - 3\sin x",
            font_size=40, color=BLUE
        )
        function_expr.set_width(text_width)
        function_expr.to_edge(UP, buff=top_padding)
        self.play(Write(function_expr, run_time=1.5))

        axes_width = text_width
        axes_height = axes_width * (config.frame_height / config.frame_width) * 0.5

        axes = Axes(
            x_range=[0, 4*np.pi, np.pi/6],
            y_range=[-3, 3, 1],
            x_length=axes_width,
            y_length=axes_height,
            axis_config={"color": WHITE},
        ).next_to(function_expr, DOWN, buff=0.8)

        f = lambda x: 2*np.cos(x)**2 - 3*np.sin(x)
        graph = axes.plot(f, color=BLUE, stroke_width=4)

        # Horizontal line y=0
        y_zero = axes.get_horizontal_line(axes.c2p(0, 0), color=WHITE)

        # Zero crossings in [0, 4π]
        sol_x = [np.pi/6, 5*np.pi/6, np.pi/6 + 2*np.pi, 5*np.pi/6 + 2*np.pi]
        points = VGroup(*[Dot(axes.c2p(x, f(x)), radius=0.06, color=YELLOW) for x in sol_x])

        # Add x-axis labels at zero points
        zero_labels_dict = {
            np.pi/6: r"\frac{\pi}{6}",
            5*np.pi/6: r"\frac{5\pi}{6}",
            np.pi/6 + 2*np.pi: r"\frac{13\pi}{6}",
            5*np.pi/6 + 2*np.pi: r"\frac{17\pi}{6}"
        }
        zero_labels = VGroup()
        for x_val, label_text in zero_labels_dict.items():
            label = MathTex(label_text, font_size=28, color=YELLOW)
            label.next_to(axes.c2p(x_val, 0), DOWN, buff=0.1)
            zero_labels.add(label)

        self.play(Create(axes), run_time=1.5)
        self.play(Create(graph), run_time=2)
        self.play(Create(y_zero))
        self.play(LaggedStartMap(FadeIn, points, shift=UP, lag_ratio=0.1), run_time=2)
        self.play(LaggedStartMap(FadeIn, zero_labels, shift=UP, lag_ratio=0.1), run_time=2)
        self.wait(2)

        # Closing
        self.clear()
        final_text = Text("Nailed it!", font_size=32, color=YELLOW)
        final_text.move_to(ORIGIN)
        self.play(Write(final_text, run_time=2))
        self.wait(2)
