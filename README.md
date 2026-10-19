# SharePoint AI Assistant Platform — Python API

Python port of [spo-assistants-api](https://github.com/brianpmccullough/spo-assistants-api),
exposing the same HTTP contract so the
[spo-assistants-spfx](https://github.com/brianpmccullough/spo-assistants-spfx) client
can target either backend.

## Tech stack

Python 3.14 · uv · FastAPI · Pydantic

## Getting started

Requires [uv](https://docs.astral.sh/uv/).

```bash
uv sync                    # install dependencies
cp .env.example .env       # then fill in values
uv run fastapi dev         # http://127.0.0.1:8000 (docs at /docs)
uv run ruff check          # lint
uv run pyright             # type check
uv run pytest              # tests
```