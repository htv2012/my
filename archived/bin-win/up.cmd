@echo off

if "%1" == "" (
    echo This script change directory up the chain
    echo Usage: %0 caseInsensitivePartialMatchString
    goto scriptEnd
)

set original=%cd%

:upDirLoop
cd ..

rem Get just the current folder, not the whole path
for %%f in (%cd%) do set currentFolder=%%~nxf

if "%currentFolder%" == "" (
    echo Could not find any parent dir containing "%1"
    cd %original%
    goto scriptEnd
)

rem Is there a partial, case insensitive match with the current folder?
echo %currentFolder% | %windir%\System32\find /i "%1" > nul || goto upDirLoop

:scriptEnd
