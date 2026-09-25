@echo off
echo === Тест 1: Запуск без параметров ===
python -m src.main

echo === Тест 2: Запуск с путем к VFS ===
python -m src.main --vfs-path ./mock_vfs

echo === Тест 3: Запуск со стартовым скриптом ===
python -m src.main --script-path scripts/demo_commands.txt