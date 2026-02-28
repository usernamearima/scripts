@echo off
setlocal EnableExtensions EnableDelayedExpansion
color 0D
title arima puller

set "LOGFILE=ip_dump.log"
set "IP_SERVICE=https://api.ipify.org"

:: get public ip
for /f "usebackq delims=" %%i in (`
    powershell -NoProfile -Command "try { Invoke-RestMethod -Uri '%IP_SERVICE%' } catch { '' }"
`) do set "PUBLIC_IP=%%i"

if not defined PUBLIC_IP (
    echo [!] Failed to retrieve public IP.
    pause
    exit /b 1
)

echo [+] Public IP detected: %PUBLIC_IP%
echo.

set "TSHARK="

for %%P in (
    "C:\Program Files\Wireshark\tshark.exe"
    "C:\Program Files (x86)\Wireshark\tshark.exe"
) do (
    if exist %%P set "TSHARK=%%P"
)

if not defined TSHARK (
    echo [!] tshark.exe not found.
    start https://www.wireshark.org/download.html
    pause
    exit /b 1
)

echo [+] tshark found:
echo     %TSHARK%
echo.

echo Available interfaces:
"%TSHARK%" -D
echo.

set /p "IFACE=Select interface number: "
if not defined IFACE (
    echo [!] No interface selected.
    pause
    exit /b 1
)

cls
echo ==========================================
echo  stun / udp ip dump
echo ==========================================
echo  Public IP : %PUBLIC_IP%
echo  Interface : %IFACE%
echo  Logging   : %LOGFILE%
echo  Stop with : CTRL+C
echo ==========================================
echo.

"%TSHARK%" ^
 -i %IFACE% ^
 -f "udp" ^
 -Y "stun && stun.type == 0x0101 && stun.att.ipv4 && stun.att.ipv4 != %PUBLIC_IP%" ^
 -T fields ^
 -e stun.att.ipv4 ^
 | tee "%LOGFILE%"
