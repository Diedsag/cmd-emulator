@echo off
echo Создание тестовых данных VFS...

rmdir /s /q test_vfs_minimal 2>nul
rmdir /s /q test_vfs_files 2>nul
rmdir /s /q test_vfs_nested 2>nul

mkdir test_vfs_minimal
echo Welcome to minimal VFS > test_vfs_minimal\motd

mkdir test_vfs_files
echo Welcome to files VFS > test_vfs_files\motd
echo Hello World > test_vfs_files\hello.txt
echo Config data > test_vfs_files\config.ini
echo Readme content > test_vfs_files\readme.md

mkdir test_vfs_nested
echo Welcome to nested VFS > test_vfs_nested\motd
mkdir test_vfs_nested\level1
mkdir test_vfs_nested\level1\level2
mkdir test_vfs_nested\level1\level2\level3
echo Deep file > test_vfs_nested\level1\level2\level3\deep.txt
echo Level2 file > test_vfs_nested\level1\level2\file2.txt
echo Level1 file > test_vfs_nested\level1\file1.txt

echo hidden > test_vfs_nested\.hidden

mkdir test_vfs_nested\home
mkdir test_vfs_nested\home\use
mkdir test_vfs_nested\home\use\data
mkdir test_vfs_nested\home\buddy
mkdir test_vfs_nested\home\buddy\info
echo Note > test_vfs_nested\home\buddy\info\note.txt

echo Тестовые данные созданы.