# SFV wave 2, pass 2 (R21 trace-first, 2026-10-28)

- `inputs/`: every trace mask `src/builds/sfv/wave2_build.py` reads (the build's `WORK` folder). To rebuild from the repo, point `WORK` at `sfv/wave2/r21/inputs`.
- `inputs/r21/`: the pass 2 traces. Each is an x4 Real-ESRGAN upscale of Brad's pull or the archive source, perspective-rectified where the sign was photographed at an angle, thresholded and cleaned inside the budget.
- `calib/`: the cleanup budget and how it was measured on Hattiesburg + Hammond v2 (`CLEANUP_BUDGET.md`), plus the edge-metric scripts and region lists.
- `tools/`: the trace-prep helpers (colour select, clean, rectify, skeleton prune/straighten, smoothing test).

Standard: project docs `claude/NT_R21_TRACE_FIRST.md` and `claude/NT_PRODUCT_STANDARDS.md` (L42-L44, S9 SOURCE).
