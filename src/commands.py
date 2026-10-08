"""Модуль команд эмулятора оболочки."""

import calendar
from datetime import datetime
from typing import Callable

from src.context import ShellContext
from src.vfs import VFSNode

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


@register("mkdir", "Создать директорию в памяти")
def cmd_mkdir(args: list[str], ctx: ShellContext) -> str:
    """Создать новую директорию в текущей папке VFS."""
    if not args:
        return "mkdir: отсутствует имя директории"
    name = args[0]
    if name in ctx.current_dir.children:
        return f"mkdir: '{name}': уже существует"
    new_node = VFSNode(name, True, ctx.current_dir)
    ctx.current_dir.children[name] = new_node
    return ""


@register("rm", "Удалить файл или директорию из памяти")
def cmd_rm(args: list[str], ctx: ShellContext) -> str:
    """Удалить указанный узел из текущей директории VFS."""
    if not args:
        return "rm: отсутствует операнд"
    name = args[0]
    if name not in ctx.current_dir.children:
        return f"rm: '{name}': не найдено"
    del ctx.current_dir.children[name]
    return ""


@register("help", "Вывести список доступных команд")
def cmd_help(args: list[str], ctx: ShellContext) -> str:
    """Вывести отсортированный список команд с описаниями."""
    lines: list[str] = []
    for name in sorted(COMMANDS.keys()):
        desc = DESCRIPTIONS.get(name, "")
        lines.append(f"{name:<10} {desc}")
    return "\n".join(lines)


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