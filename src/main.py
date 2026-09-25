"""Точка входа эмулятора оболочки."""

import argparse

from src.gui import ShellGUI


def parse_args() -> argparse.Namespace:
    """Разобрать аргументы командной строки.

    Returns:
        Пространство имен с аргументами.
    """
    parser = argparse.ArgumentParser(
        description="Эмулятор оболочки ОС"
    )
    parser.add_argument(
        "--vfs-path",
        type=str,
        default=None,
        help="Путь к физическому расположению VFS"
    )
    parser.add_argument(
        "--script-path",
        type=str,
        default=None,
        help="Путь к стартовому скрипту"
    )
    return parser.parse_args()


def main() -> None:
    """Создать и запустить эмулятор."""
    args = parse_args()

    print(f"[DEBUG] VFS path: {args.vfs_path}")
    print(f"[DEBUG] Script path: {args.script_path}")

    app = ShellGUI(
        vfs_path=args.vfs_path,
        script_path=args.script_path
    )
    app.run()


if __name__ == "__main__":
    main()