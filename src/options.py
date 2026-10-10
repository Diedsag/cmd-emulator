"""Модуль разбора параметров команд."""

from dataclasses import dataclass

OPTION_PREFIX = "-"
OPTION_PREFIX_LENGTH = 1
LONG_FLAG = "l"
ALL_FLAG = "a"
HUMAN_FLAG = "h"


@dataclass
class LsOptions:
    """Параметры команды ls."""

    long: bool = False
    show_all: bool = False
    human: bool = False


def parse_ls_options(
    args: list[str],
) -> tuple[LsOptions, list[str], str]:
    """Разобрать аргументы команды ls.

    Args:
        args: Аргументы команды.

    Returns:
        Опции, список путей и текст ошибки.
    """
    options = LsOptions()
    paths: list[str] = []
    unknown: list[str] = []

    for arg in args:
        if _is_option_group(arg):
            unknown.extend(_apply_option_group(arg, options))
        else:
            paths.append(arg)

    if unknown:
        joined = "".join(unknown)
        return options, paths, f"ls: unknown option -- {joined}"

    return options, paths, ""


def _is_option_group(arg: str) -> bool:
    """Проверить, является ли аргумент группой флагов."""
    return (
        arg.startswith(OPTION_PREFIX)
        and len(arg) > OPTION_PREFIX_LENGTH
    )


def _apply_option_group(
    arg: str,
    options: LsOptions,
) -> list[str]:
    """Применить группу флагов."""
    unknown: list[str] = []

    for char in arg[OPTION_PREFIX_LENGTH:]:
        _apply_option(char, options, unknown)

    return unknown


def _apply_option(
    char: str,
    options: LsOptions,
    unknown: list[str],
) -> None:
    """Применить один флаг."""
    if char == LONG_FLAG:
        options.long = True
    elif char == ALL_FLAG:
        options.show_all = True
    elif char == HUMAN_FLAG:
        options.human = True
    else:
        unknown.append(char)