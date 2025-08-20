
- **Strengths:** Fast iteration, vast DS/ML ecosystem, great readability, batteries‑included.
    
- **Use when:** APIs, automation, DS/ML, scripting, prototypes that may go prod.
    
- **Caveats:** Single‑threaded CPU‑bound work limited by GIL (mitigations: multiprocessing, C extensions, pypy, asyncio for I/O).
    
- **Key tools:** `pip/uv`, `poetry` or `pip-tools`, `pytest`, `ruff` (lint+format), `mypy`, `FastAPI/Django/Flask`, `SQLModel/SQLAlchemy`, `pydantic`, `celery/rye`, `docker`.
    