@echo off
echo === Тест 1: Запуск без параметров ===
python -m src.main

echo === Тест 2: Минимальная VFS ===
python -m src.main --vfs-path test_vfs_minimal

echo === Тест 3: VFS с несколькими файлами ===
python -m src.main --vfs-path test_vfs_files

echo === Тест 4: Вложенная VFS (3+ уровня) ===
python -m src.main --vfs-path test_vfs_nested

echo === Тест 5: Стартовый скрипт с вложенной VFS ===
python -m src.main --vfs-path test_vfs_nested --script-path scripts/demo_commands.txt

echo === Тест 6: Несуществующая директория VFS ===
python -m src.main --vfs-path nonexistent_dir

echo === Тест 7: Несуществующий стартовый скрипт ===
python -m src.main --script-path scripts/nonexistent.txt