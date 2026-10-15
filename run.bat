@echo off
setlocal

set "PROJECT_DIR=%~dp0"
set "RUN_SCRIPT=%PROJECT_DIR%part_08_DOCKER_DEPLOYMENT\run-system.ps1"

if not exist "%RUN_SCRIPT%" (
    echo [ERROR] Khong tim thay: %RUN_SCRIPT%
    pause
    exit /b 1
)

if "%~1"=="" (
    powershell.exe -NoLogo -NoProfile -ExecutionPolicy Bypass -File "%RUN_SCRIPT%" -NoSiem -NoSensor
) else (
    powershell.exe -NoLogo -NoProfile -ExecutionPolicy Bypass -File "%RUN_SCRIPT%" %*
)
set "EXIT_CODE=%ERRORLEVEL%"

if not "%EXIT_CODE%"=="0" (
    echo.
    echo [ERROR] He thong khoi dong khong thanh cong. Exit code: %EXIT_CODE%
    pause
)

exit /b %EXIT_CODE%
