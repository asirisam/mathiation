from manim import *
import numpy as np

# Configure TikTok portrait resolution
config.pixel_width = 1080
config.pixel_height = 1920
config.frame_width = 6
config.frame_height = 6 * (1920 / 1080)
config.background_color = BLACK

class PairedTrigGraphs(Scene):
    def construct(self):
        # -------- Title clip --------
        title_text = Text("Trig Visualisation", font_size=30, color=YELLOW)
        self.play(Write(title_text), run_time=2)
        self.wait(2)
        self.play(FadeOut(title_text))

        # -------- Graphs --------
        x_min = -4 * np.pi
        x_max = 4 * np.pi
        x_vals = np.linspace(x_min, x_max, 220)
        speed = 2.0
        side_padding = 1.0
        bottom_padding = 1.0

        # Define pairs: (function1, label1, y_range1, function2, label2, y_range2)
        trig_pairs = [
            (np.sin, "sin(x)", [-1, 1],
             lambda x: 1/np.sin(x), "csc(x)", [-2, 2]),
            (np.cos, "cos(x)", [-1, 1],
             lambda x: 1/np.cos(x), "sec(x)", [-2, 2]),
            (np.tan, "tan(x)", [-2, 2],
             lambda x: 1/np.tan(x), "cot(x)", [-2, 2])
        ]

        for fn1, label1, y1, fn2, label2, y2 in trig_pairs:
            self.show_trig_pair(fn1, label1, y1, fn2, label2, y2,
                                x_vals, x_min, x_max, speed, side_padding, bottom_padding)
            self.wait(2)
            self.clear()

        # -------- Finishing clip --------
        end_text = Text("✅ Nailed it!", font_size=30, color=YELLOW)
        end_text.to_edge(DOWN, buff=0.5)
        self.play(FadeIn(end_text), run_time=1.5)
        self.wait(2)
        self.play(FadeOut(end_text))

    # --------------------- Existing methods below ---------------------
    def show_trig_pair(self, fn1, label1, y_range1, fn2, label2, y_range2,
                        x_vals, x_min, x_max, speed, side_padding, bottom_padding):
        top_padding = 1.5
        footer_height = bottom_padding
        graph_slot_height = (config.frame_height - top_padding - footer_height) / 2.2

        title = Text(f"{label1} vs {label2}", font_size=32, color=YELLOW)
        title.to_edge(UP, buff=top_padding)
        self.play(Write(title), run_time=1)

        def make_axes(y_center, y_range):
            axes_width = config.frame_width - 2*side_padding
            axes_height = graph_slot_height*0.9
            axes = Axes(
                x_range=(x_min, x_max, np.pi/2),
                y_range=y_range,
                x_length=axes_width,
                y_length=axes_height,
                axis_config={"color": WHITE},
                tips=False
            )
            axes.move_to([0, y_center, 0])
            return axes

        top_y = title.get_bottom()[1] - 0.15
        center1 = top_y - graph_slot_height/2
        center2 = center1 - graph_slot_height

        axes1 = make_axes(center1, y_range1)
        axes2 = make_axes(center2, y_range2)

        self.play(Create(axes1), Create(axes2), run_time=1.5)

        def add_axis_labels(axes, y_range):
            labels = VGroup()
            pi_labels = [np.pi/2, 3*np.pi/2, 5*np.pi/2, 7*np.pi/2, -np.pi/2, -3*np.pi/2, -5*np.pi/2, -7*np.pi/2]
            for x in pi_labels:
                text = MathTex(rf"{int(2*x/np.pi)}\pi/2" if x != np.pi/2 else r"\pi/2", font_size=12, color=BLUE)
                text.next_to(axes.c2p(x, 0), DOWN*0.25)
                labels.add(text)

            y_ticks = np.arange(y_range[0], y_range[1]+0.01, 0.5)
            for y in y_ticks:
                if abs(y) < 1e-6:
                    continue
                text = MathTex(f"{y}", font_size=18, color=BLUE)
                text.next_to(axes.c2p(0, y), LEFT*0.25)
                labels.add(text)

            for l in labels:
                l.set_opacity(0)
                self.add(l)
                self.play(l.animate.set_opacity(1), run_time=0.05)
            return labels

        add_axis_labels(axes1, y_range1)
        add_axis_labels(axes2, y_range2)

        graph1 = self.safe_plot(axes1, fn1, x_min, x_max, y_range1[1])
        graph2 = self.safe_plot(axes2, fn2, x_min, x_max, y_range2[1])
        self.play(Create(graph1), Create(graph2), run_time=2)

        dots1 = self.create_dots(axes1, fn1, x_vals, y_range1[1])
        dots2 = self.create_dots(axes2, fn2, x_vals, y_range2[1])

        shift1 = 0.0
        shift2 = 0.0

        def update_dots1(mob, dt):
            nonlocal shift1
            shift1 += speed*dt
            for i, dot in enumerate(mob):
                new_x = ((x_vals[i]+shift1 - x_min) % (x_max-x_min)) + x_min
                y = fn1(new_x)
                if not np.isfinite(y) or abs(y) > y_range1[1]:
                    y = np.sign(y)*y_range1[1]
                dot.move_to(axes1.c2p(new_x, y))

        def update_dots2(mob, dt):
            nonlocal shift2
            shift2 += speed*dt
            for i, dot in enumerate(mob):
                new_x = ((x_vals[i]+shift2 - x_min) % (x_max-x_min)) + x_min
                y = fn2(new_x)
                if not np.isfinite(y) or abs(y) > y_range2[1]:
                    y = np.sign(y)*y_range2[1]
                dot.move_to(axes2.c2p(new_x, y))

        dots1.add_updater(update_dots1)
        dots2.add_updater(update_dots2)
        self.add(dots1, dots2)
        self.wait(5)
        dots1.clear_updaters()
        dots2.clear_updaters()

    def create_dots(self, axes, fn, x_vals, y_clip):
        dots = VGroup()
        for x in x_vals:
            y = fn(x)
            if not np.isfinite(y) or abs(y) > y_clip:
                y = np.sign(y)*y_clip
            dot = Dot(axes.c2p(x, y), radius=0.04, color=YELLOW)
            dots.add(dot)
        return dots

    def safe_plot(self, axes, fn, x_min, x_max, threshold=2):
        group = VGroup()
        xs = np.arange(x_min, x_max, 0.005)
        seg = []
        for x in xs:
            y = fn(x)
            if not np.isfinite(y) or abs(y) > threshold:
                if len(seg) > 1:
                    pts = [axes.c2p(xx, max(min(fn(xx), threshold), -threshold)) for xx in seg]
                    curve = VMobject()
                    curve.set_points_as_corners(pts)
                    curve.set_stroke(color=BLUE, width=3)
                    group.add(curve)
                seg = []
            else:
                seg.append(x)
        if len(seg) > 1:
            pts = [axes.c2p(xx, max(min(fn(xx), threshold), -threshold)) for xx in seg]
            curve = VMobject()
            curve.set_points_as_corners(pts)
            curve.set_stroke(color=BLUE, width=3)
            group.add(curve)
        return group
