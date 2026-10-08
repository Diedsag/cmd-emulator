"""Модуль команд эмулятора оболочки."""

import calendar
from datetime import datetime
from typing import Callable

from src.context import ShellContext

CommandHandler = Callable[[list[str], ShellContext], str]

COMMANDS: dict[str, CommandHandler] = {}
DESCRIPTIONS: dict[str, str] = {}


def register(name: str, desc: str) -> Callable:
    """Зарегистрировать команду в реестре.

    Args:
        name: Имя команды.
        desc: Описание команды.

    Returns:
        Декоратор, регистрирующий функцию.
    """
    def decorator(func: CommandHandler) -> CommandHandler:
        COMMANDS[name] = func
        DESCRIPTIONS[name] = desc
        return func
    return decorator


@register("ls", "Вывести содержимое директории")
def cmd_ls(args: list[str], ctx: ShellContext) -> str:
    """Вывести содержимое текущей директории."""
    target = ctx.current_dir
    if args:
        node = ctx.resolve_path(args[0])
        if not node:
            return f"ls: '{args[0]}': не найдено"
        target = node
    if not target.is_dir:
        return target.name
    entries = sorted(target.children.keys())
    return "  ".join(entries) if entries else ""


@register("cd", "Сменить текущую директорию")
def cmd_cd(args: list[str], ctx: ShellContext) -> str:
    """Сменить текущую директорию."""
    if not args:
        ctx.current_dir = ctx.vfs.root
        return ""
    node = ctx.resolve_path(args[0])
    if not node:
        return f"cd: '{args[0]}': не найдено"
    if not node.is_dir:
        return f"cd: '{args[0]}': не каталог"
    ctx.current_dir = node
    return ""


@register("cal", "Вывести календарь на текущий месяц")
def cmd_cal(args: list[str], ctx: ShellContext) -> str:
    """Вывести календарь на текущий месяц."""
    now = datetime.now()
    return calendar.month(now.year, now.month)


@register("date", "Вывести текущую дату и время")
def cmd_date(args: list[str], ctx: ShellContext) -> str:
    """Вывести текущую дату и время."""
    now = datetime.now()
    return now.strftime("%a %b %d %H:%M:%S %Y")


def execute(
    cmd: str, args: list[str], ctx: ShellContext
) -> str:
    """Выполнить команду по имени.

    Args:
        cmd: Имя команды.
        args: Список аргументов.
        ctx: Контекст эмулятора.

    Returns:
        Результат выполнения команды.

    Raises:
        ValueError: Если команда не найдена.
    """
    if cmd not in COMMANDS:
        raise ValueError(
            f"Ошибка: неизвестная команда '{cmd}'"
        )
    return COMMANDS[cmd](args, ctx)