"""Модуль графического интерфейса эмулятора."""

import getpass
import socket
import tkinter as tk
from tkinter import ttk
from typing import Optional

from src.parser import parse_command
from src.commands import execute
from src.context import ShellContext

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
INFO_FG = "#9aa0a6"


class ShellGUI:
    """Графический интерфейс эмулятора оболочки."""

    def __init__(
        self,
        vfs_path: Optional[str] = None,
        script_path: Optional[str] = None
    ) -> None:
        """Создать окно и виджеты эмулятора."""
        self.vfs_path = vfs_path
        self.script_path = script_path
        self.context = ShellContext()

        self.root = tk.Tk()
        self._setup_window()
        self._setup_widgets()
        self._bind_events()
        self._load_vfs()
        self._show_motd()
        self._show_prompt()

        if self.script_path:
            self._run_startup_script()

    def _load_vfs(self) -> None:
        """Загрузить VFS из указанной директории."""
        if not self.vfs_path:
            return
        try:
            self.context.load_vfs(self.vfs_path)
            print(f"[DEBUG] VFS загружена: {self.vfs_path}")
        except ValueError as err:
            print(f"[DEBUG] Ошибка VFS: {err}")
            self._append_text(str(err) + "\n", "error")

    def _show_motd(self) -> None:
        """Вывести сообщение из файла motd."""
        motd = self.context.vfs.get_motd()
        if motd:
            self._append_text(motd + "\n", "info")

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
        self.output.tag_configure(
            "info", foreground=INFO_FG
        )

    def _bind_events(self) -> None:
        """Привязать обработчики событий."""
        self.entry.bind("<Return>", self._on_enter)

    def _append_text(
        self, text: str, tag: str = ""
    ) -> None:
        """Добавить строку в поле вывода."""
        self.output.config(state=tk.NORMAL)
        if tag:
            self.output.insert(tk.END, text, tag)
        else:
            self.output.insert(tk.END, text)
        self.output.see(tk.END)
        self.output.config(state=tk.DISABLED)

    def _show_prompt(self) -> None:
        """Вывести приглашение к вводу."""
        path = self.context.current_dir.get_path()
        self._append_text(f"{path} $ ", "prompt")

    def _run_startup_script(self) -> None:
        """Выполнить стартовый скрипт при запуске."""
        from src.script_runner import run_script

        self._append_text(
            f"--- Скрипт: {self.script_path} ---\n",
            "info"
        )
        error = run_script(
            self.script_path, self._append_text, self.context
        )
        if error:
            self._append_text(
                f"--- Ошибка: {error} ---\n", "error"
            )
        else:
            self._append_text(
                "--- Скрипт завершён ---\n", "info"
            )
        self._show_prompt()

    def _on_enter(self, event: tk.Event) -> str:
        """Обработать нажатие клавиши Enter."""
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
        """Выполнить команду и вывести результат."""
        try:
            result = execute(cmd, args, self.context)
            if result:
                self._append_text(result + "\n")
        except ValueError as err:
            self._append_text(str(err) + "\n", "error")

    def _execute_exit(self, args: list[str]) -> None:
        """Закрыть приложение или вывести ошибку."""
        if args:
            msg = "Ошибка: exit не принимает аргументов.\n"
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