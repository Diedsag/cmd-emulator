"""Модуль выполнения стартовых скриптов."""

import os
from typing import Callable, Optional

from src.parser import parse_command
from src.commands import execute
from src.context import ShellContext


def _read_script(path: str) -> Optional[list[str]]:
    """Прочитать и очистить строки скрипта."""
    if not os.path.isfile(path):
        return None
    with open(path, "r", encoding="utf-8") as file:
        return [l.strip() for l in file if l.strip()]


def _run_command(
    cmd: str,
    args: list[str],
    output: Callable[[str, str], None],
    ctx: ShellContext
) -> Optional[str]:
    """Выполнить одну команду скрипта."""
    if cmd == "exit":
        msg = "Ошибка: команда exit в скрипте запрещена.\n"
        output(msg, "error")
        return "Вызов команды exit"
    try:
        result = execute(cmd, args, ctx)
        output((result or "") + "\n", "result")
        return None
    except ValueError as err:
        output(str(err) + "\n", "error")
        return str(err)


def _process_line(
    line: str,
    output: Callable[[str, str], None],
    ctx: ShellContext
) -> Optional[str]:
    """Обработать одну строку скрипта."""
    if line.startswith("#"):
        return None
    output(line + "\n", "command")
    cmd, args = parse_command(line)
    if not cmd:
        return None
    return _run_command(cmd, args, output, ctx)


def run_script(
    script_path: str,
    output_callback: Callable[[str, str], None],
    ctx: ShellContext
) -> Optional[str]:
    """Выполнить стартовый скрипт построчно."""
    try:
        lines = _read_script(script_path)
    except OSError as err:
        return f"Ошибка чтения: {err}"
    if lines is None:
        return f"Файл '{script_path}' не найден."
    for line in lines:
        error = _process_line(line, output_callback, ctx)
        if error:
            return error
    return None