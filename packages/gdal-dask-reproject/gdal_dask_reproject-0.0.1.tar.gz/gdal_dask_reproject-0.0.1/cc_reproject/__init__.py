try:
    from .version import __version__
except ImportError:
    __version__ = "unknown"

try:
    from .cc_reproject import cc_reproject
except ImportError as e:
    raise ImportError(f"{e}:\n can't find module")