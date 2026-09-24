"""Модуль команд эмулятора оболочки."""

from typing import Callable


CommandHandler = Callable[[list[str]], str]

COMMANDS: dict[str, CommandHandler] = {}


def register(name: str) -> Callable:
    """Зарегистрировать команду в реестре.

    Args:
        name: Имя команды.

    Returns:
        Декоратор, регистрирующий функцию.
    """
    def decorator(func: CommandHandler) -> CommandHandler:
        COMMANDS[name] = func
        return func
    return decorator


@register("ls")
def cmd_ls(args: list[str]) -> str:
    """Заглушка команды ls.

    Args:
        args: Аргументы команды.

    Returns:
        Строка с именем команды и аргументами.
    """
    return f"ls: заглушка; аргументы: {args}"


@register("cd")
def cmd_cd(args: list[str]) -> str:
    """Заглушка команды cd.

    Args:
        args: Аргументы команды.

    Returns:
        Строка с именем команды и аргументами.
    """
    return f"cd: заглушка; аргументы: {args}"


def execute(cmd: str, args: list[str]) -> str:
    """Выполнить команду по имени.

    Args:
        cmd: Имя команды.
        args: Список аргументов.

    Returns:
        Результат выполнения команды.

    Raises:
        ValueError: Если команда не найдена.
    """
    if cmd not in COMMANDS:
        raise ValueError(
            f"Ошибка: неизвестная команда '{cmd}'"
        )
    return COMMANDS[cmd](args)