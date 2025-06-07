@echo off

rem This will start prompt with `User@PC `
set ConEmuPrompt0=$_[$E[m$E[32m$E]9;8;"USERNAME"$E\@$E]9;8;"COMPUTERNAME"$E\$S

rem Followed by colored `Path`
set ConEmuPrompt1=%ConEmuPrompt0%$E[93m$P$E[90m
if NOT "%PROCESSOR_ARCHITECTURE%" == "AMD64" (
  if "%PROCESSOR_ARCHITEW6432%" == "AMD64" if "%PROCESSOR_ARCHITECTURE%" == "x86" (
    rem Use another text color if cmd was run from SysWow64
    set ConEmuPrompt1=%ConEmuPrompt0%$E[93m$P$E[90m
  )
)

rem closing bracket, carriage return and `$` or `>`
rem Spare `$E[90m` was specially added because of GitShowBranch.cmd

rem ====================================================================
rem Am I an admin?
rem ====================================================================
net session >nul 2>&1
if %errorLevel% == 0 (
  set ConEmuPrompt2= admin]$_$E[91m$G
) else (
  set ConEmuPrompt2=]$_$E[90m$G
)

rem Finally reset color and add space
set ConEmuPrompt3=$E[m$S$E]9;12$E\

rem Set new prompt
PROMPT %ConEmuPrompt1%%ConEmuPrompt2%%ConEmuPrompt3%

REM REFERENCE
rem $A   & (Ampersand)
rem $B   | (pipe)
rem $C   ( (Left parenthesis)
rem $D   Current date
rem $E   Escape code (ASCII code 27)
rem $F   ) (Right parenthesis)
rem $G   > (greater-than sign)
rem $H   Backspace (erases previous character)
rem $L   < (less-than sign)
rem $N   Current drive
rem $P   Current drive and path
rem $Q   = (equal sign)
rem $S     (space)
rem $T   Current time
rem $V   Windows version number
rem $_   Carriage return and linefeed
rem $$   $ (dollar sign)

