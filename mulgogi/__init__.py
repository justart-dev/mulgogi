"""mulgogi - A fishing game in your terminal."""

try:
    from importlib.metadata import version
    __version__ = version("mulgogi")
except Exception:
    __version__ = "0.4.7"
