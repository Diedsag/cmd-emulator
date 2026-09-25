"""Модуль выполнения стартовых скриптов."""

import os
from typing import Callable, Optional

from src.parser import parse_command
from src.commands import execute


def _read_script(script_path: str) -> Optional[list[str]]:
    """Прочитать и очистить строки скрипта.

    Args:
        script_path: Путь к файлу скрипта.

    Returns:
        Список строк или None при ошибке.
    """
    if not os.path.isfile(script_path):
        return None
    with open(script_path, "r", encoding="utf-8") as file:
        return [line.strip() for line in file if line.strip()]


def _run_single_command(
    cmd: str,
    args: list[str],
    output: Callable[[str, str], None]
) -> Optional[str]:
    """Выполнить одну команду и вывести результат.

    Args:
        cmd: Имя команды.
        args: Аргументы команды.
        output: Функция для вывода текста.

    Returns:
        Сообщение об ошибке или None.
    """
    if cmd == "exit":
        msg = "Ошибка: команда exit в скрипте запрещена.\n"
        output(msg, "error")
        return "Вызов команды exit"
    try:
        result = execute(cmd, args)
        output((result or "") + "\n", "result")
        return None
    except ValueError as err:
        output(str(err) + "\n", "error")
        return str(err)


def _process_line(
    line: str,
    output: Callable[[str, str], None]
) -> Optional[str]:
    """Обработать одну строку скрипта.

    Args:
        line: Строка команды.
        output: Функция для вывода текста.

    Returns:
        Сообщение об ошибке или None.
    """
    if line.startswith("#"):
        return None
    output(line + "\n", "command")
    cmd, args = parse_command(line)
    if not cmd:
        return None
    return _run_single_command(cmd, args, output)


def run_script(
    script_path: str,
    output_callback: Callable[[str, str], None]
) -> Optional[str]:
    """Выполнить стартовый скрипт построчно.

    Args:
        script_path: Путь к файлу скрипта.
        output_callback: Функция для вывода текста и тега.

    Returns:
        Сообщение об ошибке или None при успехе.
    """
    try:
        lines = _read_script(script_path)
    except OSError as err:
        return f"Ошибка чтения: {err}"
    if lines is None:
        return f"Файл '{script_path}' не найден."
    for line in lines:
        error = _process_line(line, output_callback)
        if error:
            return error
    return None