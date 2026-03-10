@echo off
setlocal enabledelayedexpansion
title Simple Network Scanner

set /p subnet=Enter subnet (example 192.168.1): 

echo.
echo Scanning %subnet%.0/24
echo -----------------------

for /L %%i in (1,1,254) do (
    ping -n 1 -w 100 %subnet%.%%i >nul
    if !errorlevel! == 0 (
        echo [ONLINE] %subnet%.%%i
    )
)

echo.
echo Scan finished.
pause
