from manim import *
import numpy as np

# TikTok portrait
config.pixel_width = 1080
config.pixel_height = 1920
config.frame_width = 6
config.frame_height = 6 * (1920 / 1080)
config.background_color = BLACK

class CircleEquationProof(Scene):
    def construct(self):
        # -----------------------------
        # Title
        # -----------------------------
        title = Text("Quantum Quest", font_size=40, color=YELLOW)
        self.play(FadeIn(title, shift=UP), run_time=2)
        self.wait(0.75)
        self.play(FadeOut(title, shift=DOWN), run_time=1)

        # -----------------------------
        # Question with padding
        # -----------------------------
        left_padding = 1.0
        right_padding = 1.0
        top_padding = 1.5
        text_width = config.frame_width - left_padding - right_padding

        question = Text("Derive Schrödinger's Equation", font_size=46, color=ORANGE)
        equation = MathTex(
            r"i \hbar \frac{\partial}{\partial t} \Psi(\mathbf{r},t) = "
            r"\left[ -\frac{\hbar^2}{2m} \nabla^2 + V(\mathbf{r}) \right] \Psi(\mathbf{r},t]",
            font_size=38, color=BLUE
        )

        question_group = VGroup(question, equation).arrange(DOWN, buff=0.5)
        question_group.set(width=text_width)
        question_group.move_to(ORIGIN + UP * (top_padding / 2))

        self.play(FadeIn(question_group, shift=UP), run_time=1.5)
        self.wait(1.0)
        self.play(FadeOut(question_group, shift=DOWN), run_time=1)

        # -----------------------------
        # Steps slide (animated)
        # -----------------------------
        left_padding = 1.2
        right_padding = 0.3
        text_width = config.frame_width - left_padding - right_padding
        start_y = config.frame_height / 4
        steps_group = VGroup()

        # --- stickman function ---
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
            arm_left = Line(body_top + LEFT*0.05 + UP*arm_y_offset,
                            body_top + LEFT*arm_length + DOWN*0.05, color=YELLOW)
            arm_right = Line(body_top + RIGHT*0.05 + UP*arm_y_offset,
                             body_top + RIGHT*arm_length + UP*0.05, color=YELLOW)
            leg_left = Line(body_bottom,
                            body_bottom + LEFT*leg_length + DOWN*0.4, color=YELLOW)
            leg_right = Line(body_bottom,
                             body_bottom + RIGHT*leg_length + DOWN*0.4, color=YELLOW)
            return VGroup(head, body, arm_left, arm_right, leg_left, leg_right)

        # --- add_step function with Write animation & stickman ---
        def add_step(step_mob):
            step_mob.set(width=min(step_mob.width, text_width))
            steps_group.add(step_mob)

            if len(steps_group) == 1:
                step_mob.move_to(UP * start_y)
            else:
                step_mob.next_to(steps_group[-2], DOWN, buff=0.7)

            stickman = create_stickman(step_mob.get_bottom() + DOWN*0.4)
            self.add(stickman)

            pointer = Line(
                stickman[3].get_end(),
                stickman[3].get_end() + RIGHT*0.5,
                color=YELLOW, stroke_width=2
            )
            self.add(pointer)

            def update_man(pointer, step_mob, alpha):
                start = step_mob.get_left()
                end = step_mob.get_right()
                target = start + alpha * (end - start)
                pointer.put_start_and_end_on(stickman[3].get_end(), target)

            self.play(
                Write(step_mob, run_time=1.5),
                UpdateFromAlphaFunc(pointer, lambda mob, alpha: update_man(mob, step_mob, alpha))
            )

            self.remove(stickman, pointer)

            if len(steps_group) > 4:
                shift_amount = steps_group[-5].height + 0.7
                self.play(steps_group.animate.shift(UP*shift_amount), run_time=0.5)
            else:
                self.wait(0.5)

        # -----------------------------
        # Steps list for Schrödinger equation derivation
        # -----------------------------
        steps_list = [
            MathTex(r"\text{Step 1: Classical energy } E = \frac{p^2}{2m} + V", font_size=32, color=BLUE),
            MathTex(r"\text{Step 2: Replace } p \to -i\hbar\nabla, \ E \to i \hbar \partial_t", font_size=32, color=GREEN),
            MathTex(r"\text{Step 3: Hamiltonian } \hat{H} = \frac{\hat{p}^2}{2m} + V(\mathbf{r})", font_size=32, color=YELLOW),
            MathTex(r"\text{Step 4: Schrödinger eq.: } i \hbar \partial_t \Psi = \hat{H} \Psi", font_size=32, color=ORANGE),
            MathTex(r"\text{Step 5: Substitute kinetic term } \hat{H} = -\frac{\hbar^2}{2m}\nabla^2 + V", font_size=32, color=GREEN),
            MathTex(r"\text{Step 6: Final form } i \hbar \partial_t \Psi = \left[-\frac{\hbar^2}{2m}\nabla^2 + V(\mathbf{r})\right]\Psi", font_size=32, color=BLUE)
        ]

        for step in steps_list:
            add_step(step)
        self.wait(1)

        # -----------------------------
        # Graph slide (1D wavefunction ψ vs x)
        # -----------------------------
        self.clear()
        graph_title = Text("Example Wavefunction", font_size=40, color=ORANGE).to_edge(UP)
        axes = Axes(
            x_range=[0, 10, 1],
            y_range=[-1.5, 1.5, 0.5],
            x_length=6,
            y_length=3,
            tips=False
        ).next_to(graph_title, DOWN, buff=0.5)

        x_vals = np.linspace(0, 10, 200)
        y_vals = np.sin(x_vals)  # simple ψ(x) = sin(x) example
        wavefunction = axes.plot(lambda x: np.sin(x), color=BLUE)

        psi_label = axes.get_graph_label(wavefunction, label="\\Psi(x)")

        self.play(FadeIn(graph_title))
        self.play(Create(axes), run_time=1)
        self.play(Create(wavefunction), Write(psi_label), run_time=2)
        self.wait(2)

        # -----------------------------
        # Final text
        # -----------------------------
        final_text = Text("Quantum Mechanics is Weird!", font_size=40, color=YELLOW)
        self.play(FadeOut(graph_title), FadeOut(axes), FadeOut(wavefunction), FadeOut(psi_label))
        self.play(FadeIn(final_text, shift=UP), run_time=1.5)
        self.wait(2)