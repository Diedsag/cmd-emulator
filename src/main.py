"""Точка входа эмулятора оболочки."""

from src.gui import ShellGUI


def main() -> None:
    """Создать и запустить эмулятор."""
    app = ShellGUI()
    app.run()


if __name__ == "__main__":
    main()