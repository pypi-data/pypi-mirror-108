"""Prepends some text to a relative URL."""

try:
    import config  # noqa: F401
except ModuleNotFoundError:
    from . import config  # noqa: F401

from replace import replace


def relative_url_prefixer(filePath: str, newText: str) -> None:
    """Prepends some text to a relative URL."""
    replace(
        filePath,
        r'(?<!(\/|<|\w|:))((\/)(\w{0,}))',
        f'{newText}\\2',
        False
    )
