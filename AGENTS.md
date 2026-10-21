# AGENTS.md

FastAPI micro-service that serves a trained scikit-learn model for tagging consumer complaints (CFPB data). The model is trained elsewhere (see Model lifecycle).

## Commands

- `uv sync` — install deps. **uv only, never pip/manual venv.** Python 3.13 (`.python-version`).
- `uv run fastapi dev` — dev server; auto-discovers root `main.py`.
- No tests, lint, typecheck, or CI exist in this repo — don't invent commands; verify with a server smoke test (`uv run fastapi dev`, then `POST /completion_ml/`).

## Runtime flow (read before changing)

- The real entrypoint is root `main.py`. The console script `api-model-ml` (`[project.scripts]` in `pyproject.toml`) is a stub that prints "Hello" — it does **not** start the API.
- `main.py` downloads `model.pkl` + `lab_enc.pkl` from a GitHub Release **at import time** (module level, before FastAPI starts). Startup requires internet and can be slow; this is the first suspect when the server fails or hangs at boot.
- The release URLs are hard-coded at the top of `main.py` (currently tag `v1.2.1_ML`) — when publishing a new model, update **both** URLs together.
- The download overwrites the committed `src/model/*.pkl`. After running the API these files may show as modified — expected churn; don't commit unless intentionally bumping the model.
- `PATH_PIPELINE`/`PATH_LAB_ENC` in `call_Ml.py` are **CWD-relative** (`src/model/...`), and imports use `src.api_model_ml.call_Ml` (namespace package, `src/` has no `__init__.py`). Both only work when running from the repo root.

## API

- `POST /completion_ml/` with body `{"claims": {"0": "text"}}` (Pydantic `Claims`: `claims: dict[int, str]`), returns the decoded label list.
- The endpoint predicts only `claims[0]` (the first value); other keys are ignored.

## Model lifecycle

- Training/export lives in the **sibling** `Mission_1` repo (`../Mission_1`). Its `.github/workflows/release.yml` trains the model and uploads `model.pkl`/`lab_enc.pkl` to a GitHub Release on publish.
- To change model behavior: train/export in `Mission_1` → publish release → update both URLs in `main.py`.

## Gotchas

- The `if __name__ == "__main__"` block in `src/api_model_ml/call_Ml.py` hard-codes an absolute Windows path to a CSV in `Mission_1`; running that file directly fails unless that path exists.
- README sections about `src/app/exploration.ipynb`, kernel `zenassist`, and the `dev` dependency group describe `Mission_1` — this repo has no notebook and no dev dependency group.
- Comments and docs here are written in **French** — keep new prose/comments in French to match.
