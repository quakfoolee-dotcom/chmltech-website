"""Re-extract every model (not only the top 60) from Arena's published dataset for the Text, Vision and WebDev boards.
Source: https://huggingface.co/datasets/lmarena-ai/leaderboard-dataset (split 'latest', category 'overall').
Usage: python3 content/llm/arena_full.py <folder with *.latest.parquet>   -> content/llm/raw/arena_full.scores.json
Rows use the research schema (content/llm/SPEC.md); board names match raw/arena.scores.json so build_dataset.py can swap them in."""
import json, os, sys
import pandas as pd

BOARDS = {"text_style_control": ("Arena Text (style control, default view)", "https://arena.ai/leaderboard/text"),
          "vision_style_control": ("Arena Vision (style control, default view)", "https://arena.ai/leaderboard/vision"),
          "webdev": ("Arena WebDev / Code Arena", "https://arena.ai/leaderboard/webdev")}
src, out = sys.argv[1], []
for cfg, (name, url) in BOARDS.items():
    d = pd.read_parquet(os.path.join(src, cfg + ".latest.parquet"))
    d = d[d.category == "overall"]
    d = d[d.leaderboard_publish_date == d.leaderboard_publish_date.max()]
    for r in d.itertuples():
        out.append(dict(benchmark=name, model_as_listed=r.model_name, developer=r.organization, scaffold=None, setting=None, score=float(r.rating),
                        unit="Arena score (Bradley-Terry, Elo-like scale)", score_ci=f"95% CI {r.rating_lower:.6f} to {r.rating_upper:.6f}",
                        rank=int(r.rank), votes_or_n=int(r.vote_count) if r.vote_count == r.vote_count else None, cost_per_task_usd=None, cost_total_usd=None,
                        result_date=str(r.leaderboard_publish_date)[:10], self_reported=False, source_url=url, source_type="primary", retrieved_date="2026-11-12",
                        notes=f"From https://huggingface.co/datasets/lmarena-ai/leaderboard-dataset config '{cfg}', split 'latest', category 'overall'; all rows kept."))
    print(name, len(d), "rows, published", d.leaderboard_publish_date.max())
json.dump(out, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "raw", "arena_full.scores.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
