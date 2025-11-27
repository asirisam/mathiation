from manim import *
import numpy as np

# TikTok portrait
config.pixel_width = 1080
config.pixel_height = 1920
config.frame_width = 6
config.frame_height = 6 * (1920 / 1080)
config.background_color = BLACK

LEFT_PAD = 1.0
RIGHT_PAD = 1.0
TOP_PAD = 1.5
SAFE_WIDTH = config.frame_width - LEFT_PAD - RIGHT_PAD

class YangMillsMassGap(Scene):
    def construct(self):

        # ===========================
        # Title Block
        # ===========================
        title = Text(
            "Yang–Mills Theory\nand the Mass Gap",
            font_size=48,
            color=YELLOW
        ).set(width=SAFE_WIDTH)

        subtitle = Text(
            "A Millennium Prize Problem",
            font_size=28,
            color=GREY
        ).set(width=SAFE_WIDTH)

        title_group = VGroup(title, subtitle).arrange(DOWN, buff=0.3)
        title_group.move_to(UP * TOP_PAD)

        self.play(FadeIn(title_group, shift=UP), run_time=1.8)
        self.wait(1.0)
        self.play(FadeOut(title_group, shift=DOWN), run_time=0.8)

        # ===========================
        # Question / Hook
        # ===========================
        hook = Text(
            "What is Yang–Mills theory?",
            font_size=44,
            color=ORANGE
        ).set(width=SAFE_WIDTH)
        hook.to_edge(UP, buff=TOP_PAD)

        self.play(Write(hook), run_time=1.2)
        self.wait(0.8)

        short_answer = Text(
            "A framework describing force fields built from\n"
            "non-abelian symmetry groups (e.g. SU(N)).",
            font_size=30,
            t2c={"non-abelian": RED}
        ).set(width=SAFE_WIDTH)
        short_answer.move_to(UP * 0.5)

        self.play(FadeIn(short_answer, shift=UP), run_time=1.0)
        self.wait(1.0)
        self.play(FadeOut(hook), FadeOut(short_answer), run_time=0.8)

        # ===========================
        # Steps (scrollable)
        # ===========================
        start_y = config.frame_height/4
        steps_group = VGroup()

        def create_stickman(center_point):
            head_radius = 0.15
            body_length = 0.4
            arm_length = 0.25
            leg_length = 0.4

            head = Circle(radius=head_radius, color=YELLOW).move_to(center_point + UP*(body_length/2))
            body_top = center_point + UP*(head_radius - 0.075)
            body_bottom = center_point + DOWN*(body_length - head_radius)
            body = Line(body_top, body_bottom, color=YELLOW)

            arm_left = Line(
                body_top + LEFT*0.05 + DOWN*0.05,
                body_top + LEFT*arm_length + DOWN*0.05,
                color=YELLOW
            )
            arm_right = Line(
                body_top + RIGHT*0.05 + UP*0.05,
                body_top + RIGHT*arm_length + UP*0.05,
                color=YELLOW
            )

            leg_left = Line(
                body_bottom,
                body_bottom + LEFT*leg_length + DOWN*0.4,
                color=YELLOW
            )
            leg_right = Line(
                body_bottom,
                body_bottom + RIGHT*leg_length + DOWN*0.4,
                color=YELLOW
            )

            return VGroup(head, body, arm_left, arm_right, leg_left, leg_right)

        def add_step(step_mob, highlight=False):
            step_mob.set(width=min(step_mob.width, SAFE_WIDTH))

            if highlight:
                rect = SurroundingRectangle(step_mob, color=RED, buff=0.12, stroke_width=3)
                step_group = VGroup(step_mob, rect)
            else:
                step_group = step_mob

            steps_group.add(step_group)

            if len(steps_group) == 1:
                step_group.move_to(UP * start_y)
            else:
                step_group.next_to(steps_group[-2], DOWN, buff=0.7)

            stickman = create_stickman(step_group.get_bottom() + DOWN * 0.8)
            self.add(stickman)

            arm_end = stickman[3].get_end()
            pointer = Line(arm_end, arm_end + RIGHT*0.5, color=GREEN, stroke_width=5)
            self.add(pointer)

            def update_pointer(mob, alpha):
                start = step_group.get_left()
                end = step_group.get_right()
                target = start + alpha * (end - start)
                mob.put_start_and_end_on(arm_end, target)

            self.play(
                Write(step_mob, run_time=0.7),
                UpdateFromAlphaFunc(pointer, update_pointer)
            )

            self.remove(stickman, pointer)

            if len(steps_group) > 4:
                shift_amount = steps_group[-5].height + 0.7
                self.play(steps_group.animate.shift(UP * shift_amount), run_time=0.25)
            else:
                self.wait(0.4)

        # ===========================
        # Steps list with MathTex + explanations
        # ===========================
        steps_list = [
            MathTex(r"F_{\mu\nu} = \partial_\mu A_\nu - \partial_\nu A_\mu + [A_\mu, A_\nu]", font_size=34, color=BLUE),
            Text("Yang–Mills field tensor: describes how the field changes in space-time", font_size=26, color=WHITE),
            Text("F_{μν} = field strength tensor", font_size=26, color=WHITE),
            Text("A_μ = gauge field (vector potential)", font_size=26, color=WHITE),
            Text("∂_μ = partial derivative w.r.t spacetime coordinate x^μ", font_size=26, color=WHITE),
            Text("[A_μ, A_ν] = commutator due to non-abelian nature", font_size=26, color=WHITE),

            MathTex(r"\mathcal{L} = -\frac{1}{4} \mathrm{Tr} (F_{\mu\nu} F^{\mu\nu})", font_size=32, color=TEAL),
            Text("Yang–Mills Lagrangian: encodes the dynamics of the fields", font_size=26, color=WHITE),
            Text("ℒ = Lagrangian density", font_size=26, color=WHITE),
            Text("Tr = trace over gauge group indices", font_size=26, color=WHITE),

            MathTex(r"D^\mu F_{\mu\nu} = 0", font_size=32, color=GREEN),
            Text("Classical equations of motion for Yang–Mills fields", font_size=26, color=WHITE),
            Text("D^μ = covariant derivative (includes gauge fields)", font_size=26, color=WHITE),

            MathTex(r"\hat{H} |\psi \rangle = E |\psi \rangle", font_size=32, color=ORANGE),
            Text("Quantum version: Hamiltonian acting on quantum states", font_size=26, color=WHITE),
            Text("Ĥ = Hamiltonian operator", font_size=26, color=WHITE),
            Text("|ψ⟩ = quantum state vector", font_size=26, color=WHITE),
            Text("E = energy eigenvalue", font_size=26, color=WHITE),

            MathTex(r"\Delta = \min(E > 0) > 0", font_size=36, color=YELLOW),
            Text("Mass gap: the lowest non-zero energy state has positive mass", font_size=28, color=WHITE),
            Text("Δ = mass gap (energy difference between ground and first excited state)", font_size=26, color=WHITE),

            MathTex(r"\text{Prove existence + } \Delta > 0 \text{ on } \mathbb{R}^{3+1}", font_size=32, color=WHITE),
            Text("Open problem:", font_size=28, color=WHITE),
            Text("Mathematically unsolved because:", font_size=28, color=WHITE),
            Text("• Yang–Mills equations are nonlinear", font_size=28, color=WHITE),
            Text("• Fields self-interact, making analytic solutions in 4D unknown", font_size=28, color=WHITE),
            Text("• Lattice simulations suggest a gap exists, but proof is missing", font_size=28, color=WHITE)
        ]

        highlight_indices = [0, 6, 10, 13, 18, 21]  # highlight Mass gap and open problem

        for idx, step in enumerate(steps_list):
            step.set(width=SAFE_WIDTH)
            add_step(step, highlight=(idx in highlight_indices))

        self.wait(1.0)

        # ===========================
        # Gauge Field Rings (Conceptual)
        # ===========================
        self.clear()

        gauge_title = Text(
            "Gauge Field — Conceptual Picture",
            font_size=38,
            color=ORANGE
        ).set(width=SAFE_WIDTH)
        gauge_title.to_edge(UP, buff=TOP_PAD)

        self.play(Write(gauge_title), run_time=1.3)

        center = ORIGIN + DOWN * 0.2
        rings = VGroup()

        for i in range(4):
            radius = 0.5 + i * 0.35
            arrows = VGroup()
            for theta in np.linspace(0, TAU, 16, endpoint=False):
                start = center + radius * np.array([np.cos(theta), np.sin(theta), 0])
                end = center + radius * np.array([np.cos(theta + 0.15), np.sin(theta + 0.15), 0])
                arr = Line(start, end).add_tip(tip_length=0.08)
                arrows.add(arr)

            arrows.set_opacity(0.9)
            rings.add(arrows)

        rings.set_color_by_gradient(BLUE, PURPLE)
        rings.move_to(center)

        self.play(LaggedStartMap(Create, rings, lag_ratio=0.08), run_time=2.2)
        self.wait(0.6)

        anims = []
        for i, ring in enumerate(rings):
            angle = 0.4 * ((-1) ** i)
            anims.append(Rotate(ring, angle=angle, run_time=3, rate_func=there_and_back))

        self.play(*anims)
        self.wait(0.6)

        caption = Text(
            "Non-abelian fields interact with each other —\nvisual hint of complex dynamics",
            font_size=26,
            t2c={"interact": RED}
        ).set(width=SAFE_WIDTH)
        caption.next_to(rings, DOWN, buff=0.8)

        self.play(Write(caption), run_time=1.0)
        self.wait(1.0)

        # ===========================
        # Mass Gap Spectrum
        # ===========================
        self.play(
            FadeOut(gauge_title),
            FadeOut(caption),
            FadeOut(rings),
            run_time=0.6
        )
        self.wait(0.2)

        energy_title = Text(
            "Mass Gap — energy spectrum",
            font_size=36,
            color=ORANGE
        ).set(width=SAFE_WIDTH)
        energy_title.to_edge(UP, buff=TOP_PAD)

        self.play(Write(energy_title), run_time=1.0)

        axis = Line(LEFT*0.5 + DOWN*1.5, LEFT*0.5 + UP*1.5, stroke_width=4)

        energies = [0.0, 1.2, 2.0, 2.8]
        ticks = VGroup()
        labels = VGroup()

        for e in energies:
            y = -1.5 + (e/3.0)*3.0
            tick = Line(LEFT*0.5 + RIGHT*0.6, LEFT*0.5 - RIGHT*0.6).move_to([0, y, 0])
            ticks.add(tick)
            lbl = Text(f"{e:.1f}", font_size=20).next_to(tick, RIGHT, buff=0.2)
            labels.add(lbl)

        gap_brace = BraceBetweenPoints(ticks[0].get_right(), ticks[1].get_right(), direction=RIGHT)
        gap_label = Text("Mass gap Δ", font_size=28, color=YELLOW)

        level_bars = VGroup()
        for i, tick in enumerate(ticks):
            bar = Rectangle(width=1.4, height=0.05, fill_opacity=1).move_to(
                tick.get_center() + RIGHT*0.2
            )
            if i == 0:
                bar.set_fill(GREY)
            elif i == 1:
                bar.set_fill(GREEN)
            else:
                bar.set_fill(BLUE)
            level_bars.add(bar)

        self.play(
            Create(axis),
            *[Create(t) for t in ticks],
            *[Write(l) for l in labels],
            run_time=1.2
        )

        self.play(Create(level_bars), run_time=0.8)
        self.play(GrowFromCenter(gap_brace), Write(gap_label), run_time=0.8)

        mg_caption = Text(
            "Mass gap means: first excited state sits a finite\n"
            "amount (Δ) above the ground (zero) energy.",
            font_size=26
        ).set(width=SAFE_WIDTH)
        mg_caption.next_to(level_bars, DOWN, buff=0.6)

        self.play(Write(mg_caption), run_time=1.0)
        self.wait(1.0)

        # ===========================
        # Final Slide
        # ===========================
        self.play(
            FadeOut(energy_title), FadeOut(axis),
            FadeOut(ticks), FadeOut(labels),
            FadeOut(level_bars), FadeOut(gap_brace),
            FadeOut(gap_label), FadeOut(mg_caption),
            run_time=0.6
        )
        self.wait(0.2)

        final_title = Text(
            "Why this matters",
            font_size=40,
            color=ORANGE
        ).set(width=SAFE_WIDTH)
        final_title.to_edge(UP, buff=TOP_PAD)

        bullets = VGroup(
            Text("• Explains how most visible mass emerges", font_size=28),
            Text("• Deep link between maths and the real world", font_size=28),
            Text("• Clay Millennium Prize: prove existence + Δ > 0", font_size=28,
                 t2c={"Δ > 0": YELLOW})
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4)

        bullets.set(width=SAFE_WIDTH)
        bullets.move_to(DOWN * 0.1)

        self.play(Write(final_title), run_time=1.0)
        self.play(FadeIn(bullets, shift=DOWN), run_time=1.0)
        self.wait(1.0)


        self.play(FadeOut(final_title), FadeOut(bullets), run_time=0.8)
        self.wait(0.5)

        end_text = Text("Nailed it!", font_size=48, color=YELLOW)
        end_text.move_to(ORIGIN)
        self.play(Write(end_text), run_time=1.4)
        self.wait(1.0)