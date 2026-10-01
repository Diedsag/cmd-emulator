"""Модуль контекста эмулятора оболочки."""

from typing import Optional

from src.vfs import VirtualFileSystem, VFSNode


class ShellContext:
    """Контекст работы эмулятора."""

    def __init__(self) -> None:
        """Инициализировать контекст."""
        self.vfs = VirtualFileSystem()
        self.current_dir = self.vfs.root

    def load_vfs(self, path: str) -> None:
        """Загрузить VFS и сбросить текущую директорию."""
        self.vfs.load_from_directory(path)
        self.current_dir = self.vfs.root

    def resolve_path(self, target: str) -> Optional[VFSNode]:
        """Разрешить путь относительно текущей директории."""
        if not target or target == ".":
            return self.current_dir
        if target.startswith("/"):
            start = self.vfs.root
        else:
            start = self.current_dir
        return self._walk_path(start, target)

    def _walk_path(
        self, start: VFSNode, path: str
    ) -> Optional[VFSNode]:
        """Пройти по пути от начального узла."""
        node = start
        parts = [p for p in path.split("/") if p]
        for part in parts:
            if part == ".":
                continue
            if part == "..":
                if node.parent:
                    node = node.parent
                continue
            child = node.children.get(part)
            if not child:
                return None
            node = child
        return node