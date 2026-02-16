@echo off
chcp 65001 >nul
setlocal EnableDelayedExpansion

for /f %%A in ('"prompt $H & echo on & for %%B in (1) do rem"') do set BS=%%A

set USER_COLOR=[92m
set HOST_COLOR=[95m
set PATH_COLOR=[91m
set PROMPT_COLOR=[97m
set RESET=[0m

:input
echo.
echo %PROMPT_COLOR%+--(%USER_COLOR%miss%PROMPT_COLOR%@%HOST_COLOR%her%PROMPT_COLOR%)-[%PATH_COLOR%%cd%%PROMPT_COLOR%]%RESET%
set /p cmd=".%BS% %PROMPT_COLOR%+-->%RESET% "

if "%cmd%"=="" goto input
echo.
call %cmd%
goto input
