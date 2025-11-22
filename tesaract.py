from manim import *
import numpy as np

# Configure TikTok portrait resolution
config.pixel_width = 1080
config.pixel_height = 1920
config.frame_width = 6
config.frame_height = 6 * (1920 / 1080)
config.background_color = BLACK

class PlayfulTesseractScene(Scene):
    def construct(self):
        size = 2.5  # larger scale
        verts4d = [np.array([(-1 if ((i >> k) & 1) == 0 else 1) * size for k in range(4)]) for i in range(16)]

        def hamming_distance(a, b):
            return sum(x != y for x, y in zip(a, b))

        edges = [(i, j) for i, vi in enumerate(verts4d)
                 for j, vj in enumerate(verts4d) if i < j and hamming_distance(vi > 0, vj > 0) == 1]

        # Tesseract edges
        edge_lines = VGroup(*[Line(ORIGIN, ORIGIN, color=WHITE, stroke_width=2) for _ in edges])
        self.add(edge_lines)

        # 4D rotation helper
        def rotate_4d(v, a, b, phi):
            v = v.copy()
            ca = np.cos(phi)
            sa = np.sin(phi)
            x_a = v[a]
            x_b = v[b]
            v[a] = ca * x_a - sa * x_b
            v[b] = sa * x_a + ca * x_b
            return v

        # 4D -> 3D -> 2D projection
        def project_4d_to_3d(v4):
            w_offset = 6.0
            factor = 1 / (w_offset - v4[3])
            return v4[:3] * factor * 3

        def project_3d_to_2d(v3):
            z_offset = 5.0
            factor = 1 / (z_offset - v3[2])
            return np.array([v3[0] * factor, v3[1] * factor, 0])

        def project_4d_to_2d(v4):
            return project_3d_to_2d(project_4d_to_3d(v4))

        # -----------------------------
        # Tesseract rotation updater
        # -----------------------------
        def tesseract_updater(mob, dt):
            t = self.renderer.time
            # playful random wobble in rotation
            angle_xy = 0.5 * t + 0.1 * np.sin(1.2*t)
            angle_zw = 0.3 * t + 0.1 * np.cos(0.7*t)
            angle_xz = 0.4 * t + 0.1 * np.sin(0.5*t)
            rotated = []
            for v in verts4d:
                r = rotate_4d(v, 0, 1, angle_xy)
                r = rotate_4d(r, 2, 3, angle_zw)
                r = rotate_4d(r, 0, 2, angle_xz)
                rotated.append(r)
            pts2d = [project_4d_to_2d(v) for v in rotated]
            for idx, (i, j) in enumerate(edges):
                mob[idx].put_start_and_end_on(pts2d[i], pts2d[j])

        edge_lines.add_updater(tesseract_updater)

        # Label
        label = Text("Playful Tesseract in 4D → 3D", font_size=28, color=BLUE)
        label.to_edge(DOWN, buff=0.5)
        self.play(Write(label))

        # -----------------------------
        # Fun vertex animation
        # -----------------------------
        vertices = VGroup(*[Dot(project_4d_to_2d(v), color=YELLOW, radius=0.15) for v in verts4d])
        self.play(LaggedStartMap(FadeIn, vertices, shift=UP, lag_ratio=0.15))
        self.play(LaggedStartMap(
            ApplyMethod, vertices,
            lambda m: (m.scale, 1.5),
            run_time=1, lag_ratio=0.1,
            rate_func=there_and_back
        ))
        self.play(FadeOut(vertices))

        # -----------------------------
        # Fun edges animation
        # -----------------------------
        edge_highlight = VGroup(*[Line(edge_lines[i].get_start(), edge_lines[i].get_end(),
                                       color=GREEN, stroke_width=3) for i in range(len(edges))])
        self.play(LaggedStartMap(Write, edge_highlight, lag_ratio=0.05))
        self.play(LaggedStartMap(FadeOut, edge_highlight, lag_ratio=0.05))

        # -----------------------------
        # Fun faces animation
        # -----------------------------
        face_lines = VGroup(*[Line(edge_lines[i].get_start(), edge_lines[i].get_end(),
                                   color=ORANGE, stroke_width=2) for i in range(len(edges))])
        self.play(FadeIn(face_lines))
        self.play(LaggedStartMap(
            ApplyMethod, face_lines,
            lambda m: (m.scale, 1.1),
            run_time=1, lag_ratio=0.05,
            rate_func=there_and_back
        ))
        self.play(FadeOut(face_lines))

        # -----------------------------
        # Fun cubes animation
        # -----------------------------
        cube_lines = VGroup(*[Line(edge_lines[i].get_start(), edge_lines[i].get_end(),
                                   color=PURPLE, stroke_width=2) for i in range(len(edges))])
        self.play(FadeIn(cube_lines))
        self.play(LaggedStartMap(
            ApplyMethod, cube_lines,
            lambda m: (m.shift, UP*0.1 + RIGHT*0.1),
            run_time=1, lag_ratio=0.05,
            rate_func=there_and_back
        ))
        self.play(FadeOut(cube_lines))

        # -----------------------------
        # Question & Answer
        # -----------------------------
        question = Text("Q: How many vertices, edges, faces, cubes?", font_size=32, color=YELLOW)
        question.to_edge(UP, buff=0.5)
        self.play(Write(question))
        self.wait(1)
        answer = Text("Vertices: 16\nEdges: 32\nFaces: 24\nCubes: 8", font_size=32, color=WHITE)
        answer.to_edge(DOWN, buff=0.5)
        self.play(Write(answer))
        self.wait(2)

        # -----------------------------
        # Dynamic continuous rotation
        # -----------------------------
        for _ in range(4):
            self.play(Rotate(edge_lines, angle=2*np.pi, axis=OUT, run_time=3))
            self.wait(0.5)

        # Cleanup
        edge_lines.remove_updater(tesseract_updater)
        self.play(FadeOut(edge_lines), FadeOut(question), FadeOut(answer), FadeOut(label))
        self.wait(0.5)

        final_text = Text("4D in 3D — Mind blown!", font_size=36, color=YELLOW)
        final_text.move_to(ORIGIN)
        self.play(Write(final_text))
        self.wait(2)
