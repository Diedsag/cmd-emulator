"""Модуль графического интерфейса эмулятора."""

import getpass
import socket
import tkinter as tk
from tkinter import ttk

from src.parser import parse_command
from src.commands import execute


WINDOW_WIDTH = 800
WINDOW_HEIGHT = 500
MIN_WIDTH = 600
MIN_HEIGHT = 400

BG_COLOR = "#202124"
OUTPUT_BG = "#111315"
OUTPUT_FG = "#e8eaed"
PROMPT_FG = "#8ab4f8"
COMMAND_FG = "#fbbc04"
ERROR_FG = "#f28b82"


class ShellGUI:
    """Графический интерфейс эмулятора оболочки."""

    def __init__(self) -> None:
        """Создать окно и виджеты эмулятора."""
        self.root = tk.Tk()
        self._setup_window()
        self._setup_widgets()
        self._bind_events()
        self._show_prompt()

    def _setup_window(self) -> None:
        """Настроить заголовок и размер окна."""
        user = getpass.getuser() or "user"
        host = socket.gethostname() or "localhost"
        title = f"Эмулятор-[{user}@{host}]"
        self.root.title(title)
        self.root.geometry(
            f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}"
        )
        self.root.minsize(MIN_WIDTH, MIN_HEIGHT)
        self.root.configure(bg=BG_COLOR)
        self.root.protocol(
            "WM_DELETE_WINDOW", self._on_close
        )

    def _setup_widgets(self) -> None:
        """Создать текстовое поле и поле ввода."""
        style = ttk.Style()
        try:
            style.theme_use("clam")
        except tk.TclError:
            pass

        self.output = tk.Text(
            self.root,
            wrap="word",
            state=tk.DISABLED,
            bg=OUTPUT_BG,
            fg=OUTPUT_FG,
            insertbackground=OUTPUT_FG,
            relief="flat",
            borderwidth=0,
            padx=10,
            pady=10,
            font=("Consolas", 11),
        )
        self.output.pack(
            fill=tk.BOTH, expand=True, padx=10, pady=10
        )

        self._configure_tags()

        self.entry = tk.Entry(
            self.root,
            bg=OUTPUT_BG,
            fg=OUTPUT_FG,
            font=("Consolas", 12),
            insertbackground=OUTPUT_FG,
            relief="flat",
        )
        self.entry.pack(
            fill=tk.X, padx=10, pady=(0, 10), ipady=5
        )

    def _configure_tags(self) -> None:
        """Назначить цвета разным видам текста."""
        self.output.tag_configure(
            "prompt", foreground=PROMPT_FG
        )
        self.output.tag_configure(
            "command", foreground=COMMAND_FG
        )
        self.output.tag_configure(
            "error", foreground=ERROR_FG
        )

    def _bind_events(self) -> None:
        """Привязать обработчики событий."""
        self.entry.bind("<Return>", self._on_enter)

    def _append_text(
        self, text: str, tag: str = ""
    ) -> None:
        """Добавить строку в поле вывода.

        Args:
            text: Текст для вывода.
            tag: Имя тега для раскраски.
        """
        self.output.config(state=tk.NORMAL)
        if tag:
            self.output.insert(tk.END, text, tag)
        else:
            self.output.insert(tk.END, text)
        self.output.see(tk.END)
        self.output.config(state=tk.DISABLED)

    def _show_prompt(self) -> None:
        """Вывести приглашение к вводу."""
        user = getpass.getuser() or "user"
        host = socket.gethostname() or "localhost"
        self._append_text(f"{user}@{host}:~$ ", "prompt")

    def _on_enter(self, event: tk.Event) -> str:
        """Обработать нажатие клавиши Enter.

        Args:
            event: Событие клавиатуры.

        Returns:
            Строка "break" для остановки всплытия.
        """
        line = self.entry.get()
        self.entry.delete(0, tk.END)
        self._append_text(line + "\n", "command")

        cmd, args = parse_command(line)
        if not cmd:
            self._show_prompt()
            return "break"

        if cmd == "exit":
            self._execute_exit(args)
            return "break"

        self._run_command(cmd, args)
        self._show_prompt()
        return "break"

    def _run_command(
        self, cmd: str, args: list[str]
    ) -> None:
        """Выполнить команду и вывести результат.

        Args:
            cmd: Имя команды.
            args: Список аргументов.
        """
        try:
            result = execute(cmd, args)
            self._append_text(result + "\n")
        except ValueError as err:
            self._append_text(str(err) + "\n", "error")

    def _execute_exit(self, args: list[str]) -> None:
        """Закрыть приложение или вывести ошибку.

        Args:
            args: Аргументы команды exit.
        """
        if args:
            msg = "Ошибка: команда exit не принимает аргументов.\n"
            self._append_text(msg, "error")
            self._show_prompt()
            return
        self._on_close()

    def _on_close(self) -> None:
        """Закрыть окно приложения."""
        self.root.destroy()

    def run(self) -> None:
        """Запустить главный цикл обработки событий."""
        self.entry.focus_set()
        self.root.mainloop()