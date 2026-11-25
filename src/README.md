# Natural Control source code

The proof of concept: a voice assistant that reads email and websites, and sends or adds anything only after the user says yes.

| Path | What it is |
|---|---|
| `poc/` | The Python package, one file per module in the Module Guide |
| `tests/` | Automatic tests, run by CI on every pull request |
| `pyproject.toml`, `uv.lock` | Dependencies, pinned |
| `.env.example` | The keys the system needs; copy to `.env.local` |
| `TraceToDesign.md` | Tracing from the code to the design documents |

## Run the tests

Install [uv](https://docs.astral.sh/uv/), then:

```sh
cd src
uv run ruff check .
uv run pytest
```

No keys are needed for the tests.
