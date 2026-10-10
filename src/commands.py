"""Модуль команд эмулятора оболочки."""

import calendar
from datetime import datetime
from typing import Callable

from src.context import ShellContext
from src.listing import (
    filter_entries,
    format_entry,
    format_long,
    format_short,
)
from src.options import parse_ls_options

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
    """Вывести содержимое директории."""
    options, paths, error = parse_ls_options(args)
    if error:
        return error

    target = ctx.current_dir
    if paths:
        node = ctx.resolve_path(paths[0])
        if not node:
            return f"ls: '{paths[0]}': не найдено"
        target = node

    if not target.is_dir:
        if options.long:
            return format_entry(target, options.human)
        return target.name

    names = filter_entries(target, options.show_all)
    if options.long:
        return format_long(target, names, options.human)

    return format_short(names)


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
    cmd: str,
    args: list[str],
    ctx: ShellContext,
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