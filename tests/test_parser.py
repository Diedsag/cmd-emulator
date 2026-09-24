"""Тесты модуля парсера команд."""

from src.parser import parse_command


def test_parse_simple_command() -> None:
    """Тест команды без аргументов."""
    cmd, args = parse_command("ls")
    assert cmd == "ls"
    assert args == []


def test_parse_command_with_args() -> None:
    """Тест команды с аргументами."""
    cmd, args = parse_command("cd /home/user")
    assert cmd == "cd"
    assert args == ["/home/user"]


def test_parse_empty_string() -> None:
    """Тест пустой строки."""
    cmd, args = parse_command("")
    assert cmd == ""
    assert args == []


def test_parse_extra_spaces() -> None:
    """Тест строки с лишними пробелами."""
    cmd, args = parse_command("  ls   -la  ")
    assert cmd == "ls"
    assert args == ["-la"]