"""Модуль разбора команд оболочки."""


def parse_command(line: str) -> tuple[str, list[str]]:
    """Разделить строку ввода на команду и аргументы.

    Используется простое разделение по пробелам.

    Args:
        line: Строка ввода пользователя.

    Returns:
        Кортеж из имени команды и списка аргументов.
    """
    parts = line.strip().split()
    if not parts:
        return "", []
    return parts[0], parts[1:]