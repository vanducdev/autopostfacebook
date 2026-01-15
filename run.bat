@echo off
chcp 65001 >nul
title Facebook Auto Post Tool

echo.
echo ========================================
echo    Facebook Auto Post Tool
echo ========================================
echo.

:: Kiểm tra Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python không được cài đặt!
    echo Vui lòng cài đặt Python 3.7+ từ https://python.org
    pause
    exit /b 1
)

:: Kiểm tra và cài đặt dependencies
echo 🔍 Kiểm tra dependencies...
pip show requests >nul 2>&1
if %errorlevel% neq 0 (
    echo 📦 Đang cài đặt dependencies...
    pip install -r requirements.txt
    if %errorlevel% neq 0 (
        echo ❌ Lỗi khi cài đặt dependencies!
        pause
        exit /b 1
    )
)

:: Tạo các thư mục cần thiết
if not exist "input" mkdir input
if not exist "output" mkdir output
if not exist "img" mkdir img

:: Chạy chương trình
echo.
echo 🚀 Khởi động chương trình...
echo.
python main.py

:: Giữ cửa sổ mở khi chương trình kết thúc
echo.
echo Nhấn phím bất kỳ để thoát...
pause >nul
