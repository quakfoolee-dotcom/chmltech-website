# AI-agent process engineering benchmark - V1 (2026-11-27)
Tasks (3 sets, 35 tasks), reference solutions computed in code (bench_set1/2_V1.py; need numpy, scipy, iapws, CoolProp),
grading script, agents' answers (Claude Haiku/Sonnet/Opus 5.5, reasoning-only and with-code runs), set-3 rubric and scores.
Changelog V1: methane reference from the Setzmann-Wagner EOS (CoolProp); temperature tolerances as absolute +-0.5 K;
overall conversion graded to +-0.001; task 9 reference uses the stated 208.3 kW. Results unchanged: 298/300.
Second red-team validation (2026-11-27): prompts_V1.md added (run conditions and model identifiers); strict,
consistently applied set-3 scores added to rubric_scores_set3.json (16/19/18); paper appendix now prints grade_V1.py.
