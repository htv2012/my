@echo off
rem A directory cd replacement with some Linux-like features:
rem - nav: go to home dir
rem - nav -: go to the previous dir
rem See %localappdata%\southeastwind\nav.json for dir aliases and dirpath

if [%1]==[-l] goto listAndHelp
if [%1]==[--list] goto listAndHelp
if [%1]==[-h] goto listAndHelp
if [%1]==[--help] goto listAndHelp
goto changeDir

:listAndHelp
python %~dpn0.py %*
goto theEnd

:changeDir
python %~dpn0.py %* > %TEMP%/nav_worker.cmd
if not errorlevel 1 (
    call %TEMP%/nav_worker.cmd
    ls -l --color=auto
)
goto theEnd

:theEnd
