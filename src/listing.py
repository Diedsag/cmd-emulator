"""Модуль форматирования выводов ls."""

from src.vfs import VFSNode

HIDDEN_PREFIX = "."
SHORT_SEPARATOR = "  "
DIR_MARKER = "d"
FILE_MARKER = "-"
SIZE_PLACEHOLDER = "-"
SIZE_WIDTH = 7
BYTE_SUFFIX = "B"
KILOBYTE = 1024
MEGABYTE = KILOBYTE * 1024
GIGABYTE = MEGABYTE * 1024
SIZE_UNITS = (
    (GIGABYTE, "G"),
    (MEGABYTE, "M"),
    (KILOBYTE, "K"),
)


def filter_entries(
    node: VFSNode,
    show_all: bool,
) -> list[str]:
    """Вернуть отсортированные имена записей."""
    names = sorted(node.children.keys())

    if show_all:
        return names

    return [
        name
        for name in names
        if not name.startswith(HIDDEN_PREFIX)
    ]


def format_short(names: list[str]) -> str:
    """Форматировать короткий список."""
    return SHORT_SEPARATOR.join(names)


def format_long(
    node: VFSNode,
    names: list[str],
    human: bool,
) -> str:
    """Форматировать длинный список."""
    lines = [
        format_entry(node.children[name], human)
        for name in names
    ]
    return "\n".join(lines)


def format_entry(child: VFSNode, human: bool) -> str:
    """Форматировать одну запись."""
    marker = DIR_MARKER if child.is_dir else FILE_MARKER
    size = _format_node_size(child, human)
    return f"{marker} {size:>{SIZE_WIDTH}} {child.name}"


def _format_node_size(child: VFSNode, human: bool) -> str:
    """Вернуть размер для вывода."""
    if child.is_dir:
        return SIZE_PLACEHOLDER

    raw_size = len(child.content.encode("utf-8"))
    return _format_size(raw_size, human)


def _format_size(size: int, human: bool) -> str:
    """Форматировать размер."""
    if not human:
        return str(size)

    for limit, suffix in SIZE_UNITS:
        if size >= limit:
            value = size / limit
            return f"{value:.1f}{suffix}"

    return f"{size}{BYTE_SUFFIX}"