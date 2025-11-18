from manim import *
from manim.utils.rate_functions import linear, smooth, ease_out_expo, there_and_back_with_pause
import numpy as np
import math

# ---------- Config: TikTok vertical ----------
config.pixel_width = 1080
config.pixel_height = 1920
config.frame_width = 6
config.frame_height = 6 * (1920 / 1080)
config.background_color = "#EDEDED"

# ---------- Utilities ----------
def angle_of(vec):
    return math.atan2(vec[1], vec[0])

def shortest_angle_diff(a, b):
    """Smallest signed difference b - a in radians."""
    diff = (b - a + math.pi) % (2 * math.pi) - math.pi
    return diff

def lerp(a, b, t):
    return a + (b - a) * t

# ---------- Simple articulated 2D rig ----------
class HumanoidRig(VGroup):
    def __init__(self, origin=ORIGIN, scale=1.0, silhouette_color="#0A0A0A", flip=False, **kwargs):
        super().__init__(**kwargs)
        self.origin = np.array(origin)
        self.rig_scale = scale
        self.flip = -1 if flip else 1
        self.sil = silhouette_color

        s = self.rig_scale
        self.len_torso = 0.9 * s
        self.len_upper_arm = 0.45 * s
        self.len_lower_arm = 0.4 * s
        self.len_upper_leg = 0.6 * s
        self.len_lower_leg = 0.6 * s
        self.head_r = 0.18 * s

        pelvis = np.array([0.0, 0.0, 0.0]) + self.origin
        neck = pelvis + UP * self.len_torso
        head_center = neck + UP * (self.head_r + 0.02*s)

        shoulder_offset_x = 0.22 * s * self.flip
        hip_offset_x = 0.12 * s * self.flip

        shoulder_L = neck + LEFT * abs(shoulder_offset_x)
        shoulder_R = neck + RIGHT * abs(shoulder_offset_x) * self.flip
        hip_L = pelvis + LEFT * abs(hip_offset_x)
        hip_R = pelvis + RIGHT * abs(hip_offset_x) * self.flip

        if self.flip == -1:
            shoulder_L, shoulder_R = shoulder_R, shoulder_L
            hip_L, hip_R = hip_R, hip_L

        # Body
        self.pelvis = Dot(pelvis, radius=0.01, color=self.sil)
        self.torso = Line(pelvis, neck, stroke_width=18, color=self.sil)
        self.head = Circle(radius=self.head_r, fill_color=self.sil, fill_opacity=1, stroke_opacity=0).move_to(head_center)

        # Arms
        self.shoulder_L = shoulder_L
        self.elbow_L = shoulder_L + DOWN * 0.28 * s + LEFT * 0.05 * s * self.flip
        self.hand_L = self.elbow_L + DOWN * 0.18 * s + LEFT * 0.05 * s * self.flip
        self.upper_arm_L = Line(self.shoulder_L, self.elbow_L, stroke_width=14, color=self.sil)
        self.lower_arm_L = Line(self.elbow_L, self.hand_L, stroke_width=14, color=self.sil)

        self.shoulder_R = shoulder_R
        self.elbow_R = shoulder_R + DOWN * 0.28 * s + RIGHT * 0.05 * s * self.flip
        self.hand_R = self.elbow_R + DOWN * 0.18 * s + RIGHT * 0.05 * s * self.flip
        self.upper_arm_R = Line(self.shoulder_R, self.elbow_R, stroke_width=14, color=self.sil)
        self.lower_arm_R = Line(self.elbow_R, self.hand_R, stroke_width=14, color=self.sil)

        # Legs
        self.hip_L = hip_L
        self.knee_L = hip_L + DOWN * self.len_upper_leg
        self.foot_L = self.knee_L + DOWN * self.len_lower_leg + LEFT * 0.05 * s * self.flip
        self.upper_leg_L = Line(self.hip_L, self.knee_L, stroke_width=16, color=self.sil)
        self.lower_leg_L = Line(self.knee_L, self.foot_L, stroke_width=16, color=self.sil)

        self.hip_R = hip_R
        self.knee_R = hip_R + DOWN * self.len_upper_leg
        self.foot_R = self.knee_R + DOWN * self.len_lower_leg + RIGHT * 0.05 * s * self.flip
        self.upper_leg_R = Line(self.hip_R, self.knee_R, stroke_width=16, color=self.sil)
        self.lower_leg_R = Line(self.knee_R, self.foot_R, stroke_width=16, color=self.sil)

        # Add all
        self.add(
            self.torso, self.head,
            self.upper_arm_L, self.lower_arm_L, self.upper_arm_R, self.lower_arm_R,
            self.upper_leg_L, self.lower_leg_L, self.upper_leg_R, self.lower_leg_R
        )

        # Parts dict
        self.parts = {
            "torso": self.torso, "head": self.head,
            "upper_arm_L": self.upper_arm_L, "lower_arm_L": self.lower_arm_L,
            "upper_arm_R": self.upper_arm_R, "lower_arm_R": self.lower_arm_R,
            "upper_leg_L": self.upper_leg_L, "lower_leg_L": self.lower_leg_L,
            "upper_leg_R": self.upper_leg_R, "lower_leg_R": self.lower_leg_R,
        }

    # Rotate segment about a point
    def set_segment_angle(self, segment: Line, about_point: np.ndarray, target_angle_rad: float):
        start = np.array(segment.get_start())
        end = np.array(segment.get_end())
        rel_vec = end - about_point
        rel_angle = math.atan2(rel_vec[1], rel_vec[0])
        delta = shortest_angle_diff(rel_angle, target_angle_rad)
        segment.rotate(delta, about_point=about_point)

    # Apply pose
    def apply_pose(self, angle_map):
        if "upper_arm_L" in angle_map:
            self.set_segment_angle(self.upper_arm_L, self.shoulder_L, angle_map["upper_arm_L"])
        if "lower_arm_L" in angle_map:
            self.set_segment_angle(self.lower_arm_L, self.elbow_L, angle_map["lower_arm_L"])
        if "upper_arm_R" in angle_map:
            self.set_segment_angle(self.upper_arm_R, self.shoulder_R, angle_map["upper_arm_R"])
        if "lower_arm_R" in angle_map:
            self.set_segment_angle(self.lower_arm_R, self.elbow_R, angle_map["lower_arm_R"])
        if "upper_leg_L" in angle_map:
            self.set_segment_angle(self.upper_leg_L, self.hip_L, angle_map["upper_leg_L"])
        if "lower_leg_L" in angle_map:
            self.set_segment_angle(self.lower_leg_L, self.knee_L, angle_map["lower_leg_L"])
        if "upper_leg_R" in angle_map:
            self.set_segment_angle(self.upper_leg_R, self.hip_R, angle_map["upper_leg_R"])
        if "lower_leg_R" in angle_map:
            self.set_segment_angle(self.lower_leg_R, self.knee_R, angle_map["lower_leg_R"])

# ---------- AI Pose Keyframes ----------
POSE_KEYFRAMES = [
    {"t": 0.0, "angles":{"upper_arm_R": -30*DEGREES,"lower_arm_R": -10*DEGREES,
                          "upper_arm_L": 140*DEGREES,"lower_arm_L": 150*DEGREES,
                          "upper_leg_R": -90*DEGREES,"lower_leg_R": -100*DEGREES,
                          "upper_leg_L": -95*DEGREES,"lower_leg_L": -105*DEGREES}},
    {"t": 0.8, "angles":{"upper_arm_R": 0*DEGREES,"lower_arm_R": -5*DEGREES,
                          "upper_arm_L": 160*DEGREES,"lower_arm_L": 170*DEGREES,
                          "upper_leg_R": -85*DEGREES,"lower_leg_R": -95*DEGREES,
                          "upper_leg_L": -100*DEGREES,"lower_leg_L": -110*DEGREES}},
    {"t": 1.5, "angles":{"upper_arm_R": -40*DEGREES,"lower_arm_R": -20*DEGREES,
                          "upper_arm_L": 120*DEGREES,"lower_arm_L": 130*DEGREES,
                          "upper_leg_R": -80*DEGREES,"lower_leg_R": -92*DEGREES,
                          "upper_leg_L": -110*DEGREES,"lower_leg_L": -120*DEGREES}},
    {"t": 2.2, "angles":{"upper_arm_L": 80*DEGREES,"lower_arm_L": 40*DEGREES,
                          "upper_arm_R": -80*DEGREES,"lower_arm_R": -60*DEGREES,
                          "upper_leg_R": -60*DEGREES,"lower_leg_R": -70*DEGREES,
                          "upper_leg_L": -120*DEGREES,"lower_leg_L": -130*DEGREES}},
    {"t": 3.2, "angles":{"upper_arm_R": -30*DEGREES,"lower_arm_R": -10*DEGREES,
                          "upper_arm_L": 120*DEGREES,"lower_arm_L": 130*DEGREES,
                          "upper_leg_R": -10*DEGREES,"lower_leg_R": -20*DEGREES,
                          "upper_leg_L": -130*DEGREES,"lower_leg_L": -140*DEGREES}},
    {"t": 4.0, "angles":{"upper_arm_R": 10*DEGREES,"lower_arm_R": 40*DEGREES,
                          "upper_arm_L": 150*DEGREES,"lower_arm_L": 160*DEGREES,
                          "upper_leg_R": -95*DEGREES,"lower_leg_R": -105*DEGREES,
                          "upper_leg_L": -90*DEGREES,"lower_leg_L": -100*DEGREES}},
    {"t": 4.6, "angles":{"upper_arm_R": -30*DEGREES,"lower_arm_R": -10*DEGREES,
                          "upper_arm_L": 170*DEGREES,"lower_arm_L": 170*DEGREES,
                          "upper_leg_R": -120*DEGREES,"lower_leg_R": -130*DEGREES,
                          "upper_leg_L": -120*DEGREES,"lower_leg_L": -130*DEGREES}},
]

# ---------- Scene ----------
class RealisticAIPoseFight(Scene):

    def camera_shake(self, mag=0.04, shakes=4, duration=0.25):
        for _ in range(shakes):
            dx = np.random.uniform(-mag, mag)
            dy = np.random.uniform(-mag * 0.6, mag * 0.6)
            ang = np.random.uniform(-mag * 8, mag * 8) * DEGREES
            self.play(self.camera.animate.shift(RIGHT * dx + UP * dy).rotate(ang),
                      run_time=duration / shakes, rate_func=linear)
        # Reset camera to center
        self.play(self.camera.animate.move_to(ORIGIN).set_angle(0), run_time=0.16)

    def construct(self):
        tempo = 1.0
        sil_color = "#0A0A0A"

        left_rig = HumanoidRig(origin=LEFT*1.6 + DOWN*0.6, scale=1.05, silhouette_color=sil_color, flip=False)
        right_rig = HumanoidRig(origin=RIGHT*1.6 + DOWN*0.6, scale=1.05, silhouette_color=sil_color, flip=True)

        self.add(left_rig, right_rig)

        ground = Ellipse(width=5.2, height=0.8, fill_color="#CFCFCF", fill_opacity=1, stroke_opacity=0).move_to(DOWN*1.05)
        self.add(ground)

        key_times = [kf["t"] for kf in POSE_KEYFRAMES]
        key_angles = [kf["angles"] for kf in POSE_KEYFRAMES]

        def interp_angle_map(t_global):
            if t_global <= key_times[0]:
                return key_angles[0]
            if t_global >= key_times[-1]:
                return key_angles[-1]
            for i in range(len(key_times) - 1):
                t0, t1 = key_times[i], key_times[i+1]
                if t0 <= t_global <= t1:
                    a0, a1 = key_angles[i], key_angles[i+1]
                    local_t = (t_global - t0) / (t1 - t0)
                    out = {}
                    for part in a0.keys():
                        ang0 = float(a0[part])
                        ang1 = float(a1.get(part, ang0))
                        diff = shortest_angle_diff(ang0, ang1)
                        out[part] = ang0 + diff * local_t
                    return out
            return key_angles[-1]

        def make_motion_trail(rig, n=6, fade_power=1.2):
            clones = VGroup()
            for i in range(n):
                c = rig.copy()
                alpha = (1 - i / float(n)) ** fade_power
                for sub in c:
                    if hasattr(sub, "set_fill"):
                        sub.set_fill(opacity=alpha)
                    if hasattr(sub, "set_stroke"):
                        sub.set_stroke(opacity=alpha)
                clones.add(c)
            return clones

        def impact_flash(point, intensity=1.0):
            flash = Circle(radius=0.25*intensity, fill_color=WHITE, fill_opacity=0.95, stroke_opacity=0).move_to(point)
            self.add(flash)
            self.play(flash.animate.scale(2.6).set_fill(opacity=0), run_time=0.16, rate_func=there_and_back_with_pause)
            flash.remove()
            rim = Circle(radius=0.6*intensity, stroke_color=WHITE, stroke_width=2, fill_opacity=0).move_to(point)
            self.play(Create(rim), run_time=0.16)
            self.play(FadeOut(rim), run_time=0.16)
            rim.remove()

        def transition_rig_to(rig, start_t, end_t, duration, rate_func=smooth, motion_blur=True):
            vt = ValueTracker(0.0)
            def updater(mob):
                tg = lerp(start_t, end_t, vt.get_value())
                angle_map = interp_angle_map(tg)
                rig.apply_pose(angle_map)
            dummy = VGroup()
            dummy.add_updater(updater)
            self.add(dummy)
            if motion_blur:
                trail = make_motion_trail(rig, n=6)
                for j, c in enumerate(trail):
                    c.move_to(rig.get_center() + (j/len(trail))*(RIGHT*0.05))
                    self.add(c)
                self.play(vt.animate.set_value(1.0), run_time=duration, rate_func=rate_func)
                self.play(*[FadeOut(t, run_time=0.16) for t in trail], run_time=0.16)
            else:
                self.play(vt.animate.set_value(1.0), run_time=duration, rate_func=rate_func)
            dummy.remove_updater(updater)
            self.remove(dummy)

        # ---------------- Choreography ----------------
        transition_rig_to(left_rig, start_t=0.0, end_t=0.8, duration=0.8*tempo)
        self.play(left_rig.animate.shift(RIGHT*0.22 + UP*0.03), run_time=0.18)
        trail = make_motion_trail(left_rig, n=8)
        for i, t in enumerate(trail):
            t.move_to(left_rig.get_center() + (i / len(trail)) * (RIGHT * 0.25))
            self.add(t)
        self.play(left_rig.animate.shift(RIGHT*0.25), run_time=0.16, rate_func=ease_out_expo)
        self.play(*[FadeOut(t, run_time=0.16) for t in trail], run_time=0.16)

        transition_rig_to(left_rig, start_t=0.8, end_t=1.5, duration=0.35*tempo)
        self.play(right_rig.animate.shift(RIGHT*0.06 + UP*0.03), run_time=0.12)
        self.play(Rotate(right_rig.parts["head"], angle=8*DEGREES, about_point=right_rig.parts["head"].get_center()), run_time=0.12)
        impact_flash(right_rig.parts["head"].get_center() + LEFT*0.05, intensity=0.8)
        self.camera_shake(mag=0.03, shakes=4, duration=0.18)

        victory = Text("VICTORY", font_size=72, weight=BOLD, color="#111111").to_edge(UP, buff=0.8)
        self.play(FadeIn(victory, shift=UP), run_time=0.5)
        self.wait(1.6)
        self.play(FadeOut(victory), FadeOut(left_rig), FadeOut(right_rig), run_time=0.7)
        self.wait(0.3)
