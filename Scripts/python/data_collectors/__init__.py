"""
Data Collectors Package
Unified data collection system for GitHub and protocol tracking

Do not import .main here: it triggers runpy RuntimeWarning for
`python -m data_collectors.main` because main is loaded before __main__ runs.
"""

__version__ = "1.0.0"

__all__ = ["UnifiedDataCollector"]


def __getattr__(name: str):
    if name == "UnifiedDataCollector":
        from .main import UnifiedDataCollector

        return UnifiedDataCollector
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
