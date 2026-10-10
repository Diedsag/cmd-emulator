"""Тесты модуля команд."""

import pytest

from src.commands import cmd_cd, cmd_ls, execute
from src.context import ShellContext
from src.vfs import VFSNode

FILE_NAME = "file.txt"
HIDDEN_NAME = ".hidden"
HOME_NAME = "home"
USE_NAME = "use"
DATA_NAME = "data"
BUDDY_NAME = "buddy"
INFO_NAME = "info"
LEVEL1_NAME = "level1"
MISSING_NAME = "missing"
COMPLEX_PATH = "home/use/data/../../buddy/././info"
EMPTY_RESULT = ""
UNKNOWN_OPTION = "-x"
UNKNOWN_COMMAND = "unknown"
ERROR_TEXT = "неизвестная команда"
UNKNOWN_OPTION_TEXT = "unknown option"
NOT_FOUND_TEXT = "не найдено"
LONG_DIR_MARKER = "d"
HUMAN_SIZE_MARKER = "B"


def _make_context() -> ShellContext:
    """Создать контекст с тестовой VFS."""
    ctx = ShellContext()
    root = ctx.vfs.root

    _add_file(root, FILE_NAME, "data")
    _add_file(root, HIDDEN_NAME, "hidden")
    _add_dir(root, LEVEL1_NAME)

    home = _add_dir(root, HOME_NAME)
    use = _add_dir(home, USE_NAME)
    _add_dir(use, DATA_NAME)

    buddy = _add_dir(home, BUDDY_NAME)
    _add_dir(buddy, INFO_NAME)

    ctx.current_dir = root
    return ctx


def _add_file(
    parent: VFSNode,
    name: str,
    content: str,
) -> None:
    """Добавить файл в узел."""
    node = VFSNode(name, False, parent)
    node.content = content
    parent.children[name] = node


def _add_dir(parent: VFSNode, name: str) -> VFSNode:
    """Добавить директорию в узел."""
    node = VFSNode(name, True, parent)
    parent.children[name] = node
    return node


def test_ls_hides_hidden_by_default() -> None:
    """Тест ls без флага -a."""
    ctx = _make_context()
    result = cmd_ls([], ctx)

    assert FILE_NAME in result
    assert HIDDEN_NAME not in result


def test_ls_all_shows_hidden() -> None:
    """Тест ls с флагом -a."""
    ctx = _make_context()
    result = cmd_ls(["-a"], ctx)

    assert HIDDEN_NAME in result


def test_ls_long_format() -> None:
    """Тест ls с флагом -l."""
    ctx = _make_context()
    result = cmd_ls(["-l"], ctx)

    assert HOME_NAME in result
    assert LONG_DIR_MARKER in result


def test_ls_human_size() -> None:
    """Тест ls с флагами -lh."""
    ctx = _make_context()
    result = cmd_ls(["-lh"], ctx)

    assert FILE_NAME in result
    assert HUMAN_SIZE_MARKER in result


def test_ls_combined_flags() -> None:
    """Тест ls с флагами -lha."""
    ctx = _make_context()
    result = cmd_ls(["-lha"], ctx)

    assert HIDDEN_NAME in result
    assert HOME_NAME in result


def test_ls_separate_flags() -> None:
    """Тест ls с отдельными флагами."""
    ctx = _make_context()
    result = cmd_ls(["-l", "-a", "-h"], ctx)

    assert HIDDEN_NAME in result
    assert LONG_DIR_MARKER in result
    assert HUMAN_SIZE_MARKER in result


def test_ls_unknown_option() -> None:
    """Тест неизвестного флага ls."""
    ctx = _make_context()
    result = cmd_ls([UNKNOWN_OPTION], ctx)

    assert UNKNOWN_OPTION_TEXT in result


def test_ls_not_found() -> None:
    """Тест ls для несуществующего пути."""
    ctx = _make_context()
    result = cmd_ls([MISSING_NAME], ctx)

    assert NOT_FOUND_TEXT in result


def test_ls_complex_path() -> None:
    """Тест ls со сложным относительным путём."""
    ctx = _make_context()
    result = cmd_ls([COMPLEX_PATH], ctx)

    assert result == EMPTY_RESULT


def test_cd_complex_relative_path() -> None:
    """Тест cd со сложным относительным путём."""
    ctx = _make_context()
    result = cmd_cd([COMPLEX_PATH], ctx)

    assert result == EMPTY_RESULT
    assert ctx.current_dir.name == INFO_NAME


def test_cd_no_args_returns_root() -> None:
    """Тест cd без аргументов."""
    ctx = _make_context()
    cmd_cd([HOME_NAME], ctx)
    result = cmd_cd([], ctx)

    assert result == EMPTY_RESULT
    assert ctx.current_dir == ctx.vfs.root


def test_cd_not_found() -> None:
    """Тест cd для несуществующей директории."""
    ctx = _make_context()
    result = cmd_cd([MISSING_NAME], ctx)

    assert NOT_FOUND_TEXT in result


def test_execute_unknown_command() -> None:
    """Тест выполнения неизвестной команды."""
    ctx = _make_context()

    with pytest.raises(ValueError) as exc_info:
        execute(UNKNOWN_COMMAND, [], ctx)

    assert ERROR_TEXT in str(exc_info.value)