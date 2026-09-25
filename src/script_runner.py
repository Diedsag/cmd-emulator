"""Модуль выполнения стартовых скриптов."""

import os
from typing import Callable, Optional

from src.parser import parse_command
from src.commands import execute


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
    if not os.path.isfile(script_path):
        return f"Файл скрипта '{script_path}' не найден."

    try:
        with open(script_path, "r", encoding="utf-8") as file:
            for line in file:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue

                output_callback(line + "\n", "command")

                cmd, args = parse_command(line)
                if not cmd:
                    output_callback("\n", "result")
                    continue

                if cmd == "exit":
                    output_callback(
                        "Ошибка: команда exit в скрипте запрещена.\n",
                        "error"
                    )
                    return "Вызов команды exit"

                try:
                    result = execute(cmd, args)
                    output_callback(result + "\n", "result")
                except ValueError as err:
                    output_callback(str(err) + "\n", "error")
                    return str(err)

                output_callback("\n", "result")
    except Exception as err:
        return f"Ошибка чтения: {err}"

    return None