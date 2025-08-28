@echo off
:: File kịch bản để khởi động toàn bộ hệ thống development
:: Tác giả: Chuyên gia Cao cấp Gemini
:: Ngày: 26/08/2025

echo =======================================================
echo KHOI DONG HE THONG PHAN MEM QUAN LY BAO VE (v1.0)
echo =======================================================

:: Kích hoạt môi trường ảo
echo [1/4] Kich hoat moi truong ao...
call .\\venv\\Scripts\\activate.bat

:: --- Chạy các dịch vụ nền trong cửa sổ riêng ---

:: Chạy Redis Server (Giả sử redis-server.exe nằm trong thư mục con redis/)
:: Anh hãy thay thế ""C:\Users\quanying_zhang\Downloads\Redis-x64-5.0.14.1\redis-server.exe"" bằng đường dẫn thực tế
echo [2/4] Khoi dong Redis Server...
start "Redis Server" ""C:\Users\quanying_zhang\Downloads\Redis-x64-5.0.14.1\redis-server.exe""

:: Chạy Celery Beat (Bộ đếm giờ)
echo [3/4] Khoi dong Celery Beat...
start "Celery Beat" cmd /k "celery -A config beat -l info"

:: Chạy Celery Worker
echo [4/4] Khoi dong Celery Worker...
start "Celery Worker" cmd /k "celery -A config worker -l info -P eventlet"


:: --- Chạy Django Server trong cửa sổ chính ---
echo.
echo >> May chu Django san sang hoat dong! <<
python manage.py runserver