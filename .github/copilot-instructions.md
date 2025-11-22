<!-- Copilot instructions for the `mathiation` workspace -->

# Quick orientation for AI coding agents

This repo contains short, self-contained Manim scene scripts used to render short mathematics/physics videos (portrait/TikTok format). The goal for contributors is to add or modify individual scenes (one Scene subclass per file) and keep the visual and timing conventions consistent.

Key facts (big picture)
- Each Python file is a standalone Manim scene (class deriving from `Scene`) intended to be rendered individually. Example files: `tesaract.py`, `integral_template.py`, `timeDialation_19112025.py`, `trigwaves.py`.
- All scenes configure Manim for portrait/TikTok output at top-of-file using `config.pixel_width`, `config.pixel_height`, `config.frame_width`, `config.frame_height`, and `config.background_color = BLACK`. Preserve or update these values consistently when adding scenes.
- Visual flow: title → question → step animations → closing card. Many files follow this pattern and reuse helper methods (for example `show_trig_pair`, `safe_plot`, `create_dots` in `trigwaves.py`). Prefer small, focused helper functions rather than large monolithic construct methods.

How to run locally (developer workflow)
- These are Manim scripts. Render a scene with Manim (example):

  - Render default scene in file:
    manim -pql <filename.py> <SceneClassName>

  - For portrait/TikTok resolution the files set `config` programmatically; you may still pass manim CLI args for quality. Typical quick workflow:
    manim -pql tesaract.py PlayfulTesseractScene

Project-specific conventions and patterns
- File-per-scene: keep one main `Scene` subclass per file. Name the class descriptively (e.g., `LightClockTimeDilation`, `LogIntegralScrollingScene`).
- Config at top: every file sets `config.*` values; do not duplicate conflicting global config changes across helper modules. If you change the aspect ratio, update all scenes that are intended for the same platform.
- Animation pacing: many scripts use small waits (self.wait(0.5) or 1) and grouped `VGroup` scrolling logic for step-by-step solutions (see `integral_template.py` and `permutation_18112025.py`). When adding steps, use `scale_to_fit_width(config.frame_width - 1)` and consistent `buff` values to match spacing.
- Updaters: dynamic movement is implemented with `.add_updater()` and `UpdateFromAlphaFunc` for per-frame updates (see `tesaract.py` and `trigwaves.py`). Preserve performance by limiting heavy per-frame Python work (vectorize or precompute arrays where possible).

Patterns for UI/text/math
- Titles, questions, and final cards are implemented with `Text` and `MathTex` and then centered with `move_to(ORIGIN)` or `to_edge(...)`.
- Math expressions use `MathTex(...)`; scale long equations with `scale_to_fit_width(config.frame_width - 1)` to keep margins consistent.

Dependencies and integration points
- Primary dependency: Manim. The environment must have a Manim installation compatible with the imports (`from manim import *`).
- NumPy is used in many scripts for numeric arrays and trigonometric evaluation (`import numpy as np`). Keep imports minimal and add any new third-party packages to a `requirements.txt` if you introduce them.

What to watch for when editing code
- Don't change global `config` values unintentionally; tests or other scenes may expect the portrait sizing.
- Avoid extremely heavy work inside updaters — prefer precomputed lookups whenever a large number of points is animated (see `safe_plot` in `trigwaves.py`).
- Keep scenes self-contained: adding cross-file imports is allowed, but prefer small helper modules if you need to share utilities. Add a short comment near the top of new shared modules explaining intended usage.

Examples to reference when implementing features
- Portrait + config pattern: `integral_template.py` (top-of-file `config.*` usage)
- Scrolling step UI and step grouping: `integral_template.py`, `permutation_18112025.py`
- Updater-based continuous animation: `tesaract.py`, `trigwaves.py`

If you need more context
- Ask the repo owner for preferred Manim version and rendering flags if you plan to change output format.
- If you add new dependencies, include a `requirements.txt` at the repo root and update this file with the installed versions.

If anything in these instructions is unclear or you want the agent to include additional guidance (CI, branch naming, or a shared utilities module), tell me what to add and I'll iterate.
