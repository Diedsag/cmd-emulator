"""Модуль виртуальной файловой системы."""

import os
from typing import Optional


class VFSNode:
    """Узел виртуальной файловой системы."""

    def __init__(
        self,
        name: str,
        is_dir: bool,
        parent: Optional["VFSNode"] = None
    ) -> None:
        """Инициализировать узел VFS."""
        self.name = name
        self.is_dir = is_dir
        self.parent = parent
        self.children: dict[str, "VFSNode"] = {}
        self.content: str = ""

    def get_path(self) -> str:
        """Вернуть полный путь от корня до узла."""
        parts: list[str] = []
        node: Optional[VFSNode] = self
        while node is not None and node.name != "root":
            parts.append(node.name)
            node = node.parent
        parts.reverse()
        if not parts:
            return "/"
        return "/" + "/".join(parts)


class VirtualFileSystem:
    """Виртуальная файловая система в памяти."""

    def __init__(self) -> None:
        """Инициализировать пустую VFS."""
        self.root = VFSNode("root", True)

    def load_from_directory(self, path: str) -> None:
        """Загрузить директорию с диска в память."""
        if not os.path.isdir(path):
            raise ValueError(
                f"Директория '{path}' не найдена."
            )
        root_name = os.path.basename(path) or "root"
        self.root = VFSNode(root_name, True)
        self._load_recursive(path, self.root)

    def _load_recursive(
        self, disk_path: str, node: VFSNode
    ) -> None:
        """Рекурсивно загрузить содержимое директории."""
        try:
            entries = sorted(os.listdir(disk_path))
        except OSError:
            return
        for entry in entries:
            full_path = os.path.join(disk_path, entry)
            if os.path.isdir(full_path):
                child = VFSNode(entry, True, node)
                node.children[entry] = child
                self._load_recursive(full_path, child)
            else:
                child = VFSNode(entry, False, node)
                child.content = self._read_file(full_path)
                node.children[entry] = child

    @staticmethod
    def _read_file(path: str) -> str:
        """Прочитать содержимое файла."""
        try:
            with open(path, "r", encoding="utf-8") as f:
                return f.read()
        except (OSError, UnicodeDecodeError):
            return ""

    def get_motd(self) -> Optional[str]:
        """Вернуть содержимое motd из корня VFS."""
        motd = self.root.children.get("motd")
        if motd and not motd.is_dir:
            return motd.content
        return None