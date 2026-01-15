@echo off
chcp 65001 >nul
title Git Setup - Upload to GitHub

echo.
echo ========================================
echo    Git Setup - Upload to GitHub
echo ========================================
echo.

:: Kiểm tra Git
git --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Git chưa được cài đặt!
    echo Vui lòng cài đặt Git từ https://git-scm.com/download/win
    pause
    exit /b 1
)

echo ✅ Git đã sẵn sàng
echo.

:: Khởi tạo Git repository
if not exist ".git" (
    echo 🔄 Khởi tạo Git repository...
    git init
    echo.
)

:: Cấu hình user (chạy lần đầu)
echo ⚙️ Cấu hình thông tin user...
git config user.name "vanducdev"
git config user.email "your-email@example.com"
echo.

:: Add tất cả files
echo 📦 Thêm files vào staging area...
git add .
echo.

:: Commit
echo 💾 Tạo commit...
git commit -m "Initial commit: Facebook Auto Post Tool v1.0.0"
echo.

:: Thêm remote (thay YOUR_REPO_URL bằng URL của bạn)
echo 🔗 Thêm remote repository...
set /p repo_url="Nhập URL repository GitHub của bạn: "
git remote add origin %repo_url%
git branch -M main
echo.

:: Push lên GitHub
echo 🚀 Đẩy code lên GitHub...
git push -u origin main

echo.
echo ✅ Hoàn thành! Project đã được up lên GitHub
echo.
pause
