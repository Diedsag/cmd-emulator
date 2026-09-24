"""Тесты модуля команд."""

import pytest

from src.commands import execute, cmd_ls, cmd_cd


def test_ls_stub() -> None:
    """Тест заглушки ls."""
    result = cmd_ls(["-la"])
    assert "ls" in result
    assert "-la" in result


def test_cd_stub() -> None:
    """Тест заглушки cd."""
    result = cmd_cd(["/tmp"])
    assert "cd" in result
    assert "/tmp" in result


def test_execute_unknown_command() -> None:
    """Тест выполнения неизвестной команды."""
    with pytest.raises(ValueError) as exc_info:
        execute("unknown", [])
    assert "неизвестная команда" in str(exc_info.value)


def test_execute_ls() -> None:
    """Тест выполнения ls через диспетчер."""
    result = execute("ls", ["-a"])
    assert "ls" in result