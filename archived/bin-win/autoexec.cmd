@echo off

REM ------------------------------------------------------------------------------------------------
REM --- Common Setup
REM ------------------------------------------------------------------------------------------------
call fancy_win_prompt.cmd
set DISPLAY=:0.0
set DROPBOXDIR=D:\Dropbox
set PAGER=less

REM vi/vim works best if TERM is unset, or set to cygwin
REM However, in order to get correct tube.py output, we have to unset it
set term=

REM Put cygwin tools before system32 because they are so much better
path C:\cygwin\bin;%PATH%

doskey ahk=start D:\myenv\etc\AutoHotkey.ahk

REM ------------------------------------------------------------------------------------------------
REM --- Development Environment
REM ------------------------------------------------------------------------------------------------
doskey a2x=D:\asciidoc\a2x.py
doskey asciidoc=D:\asciidoc\asciidoc.py $*
doskey diff="C:\Program Files (x86)\Beyond Compare 4\BCompare.exe" $1 $2
doskey find=C:\cygwin\bin\find.exe $*
doskey ipython=d:\anaconda3\Scripts\jupyter-console.exe $*
doskey qtconsole=start /b d:\anaconda3\Scripts\jupyter-qtconsole.exe
doskey scratch=subl %DROPBOXDIR%\src\workspaces\scratch.txt

REM ------------------------------------------------------------------------------------------------
REM --- cd and friends
REM ------------------------------------------------------------------------------------------------
doskey .................=cd ..\..\..\..\..\..\..\..\..\..\..\..\..\..\..\..
doskey ................=cd ..\..\..\..\..\..\..\..\..\..\..\..\..\..\..
doskey ...............=cd ..\..\..\..\..\..\..\..\..\..\..\..\..\..
doskey ..............=cd ..\..\..\..\..\..\..\..\..\..\..\..\..
doskey .............=cd ..\..\..\..\..\..\..\..\..\..\..\..
doskey ............=cd ..\..\..\..\..\..\..\..\..\..\..
doskey ...........=cd ..\..\..\..\..\..\..\..\..\..
doskey ..........=cd ..\..\..\..\..\..\..\..\..
doskey .........=cd ..\..\..\..\..\..\..\..
doskey ........=cd ..\..\..\..\..\..\..
doskey .......=cd ..\..\..\..\..\..
doskey ......=cd ..\..\..\..\..
doskey .....=cd ..\..\..\..
doskey ....=cd ..\..\..\
doskey ...=cd ..\..\
doskey ..=cd ..\
doskey cd=nav.cmd $*
doskey cdb=nav.cmd mybin
doskey cdd=nav Downloads
doskey cdme=nav.cmd myenv
doskey cdp=nav.cmd projects
doskey pushd=nav.cmd -p $*

REM ------------------------------------------------------------------------------------------------
REM --- ls and friends
REM ------------------------------------------------------------------------------------------------
set LS_COLORS=di=1;36:ln=1;35:so=32:pi=33:ex=1;32:bd=34;46:cd=34;43:su=30;41:sg=30;46:tw=30;42:ow=30;43
doskey la=ls --color=auto -A $*
doskey ll=ls --color=auto -l -h $*
doskey lla=ls --color=auto -lA $*
doskey ls=ls --color=auto $*
doskey ltr=ls --color=auto -lGtr $*
doskey lls=ls --color=auto -lShr

REM ------------------------------------------------------------------------------------------------
REM --- Configuration files edit
REM ------------------------------------------------------------------------------------------------
doskey vahk=subl D:\myenv\etc\AutoHotkey.ahk
doskey vbb=subl D:\myenv\bin\autoexec.cmd
doskey vcd=subl %LOCALAPPDATA%\southeastwind\nav.json
doskey vhost=subl /cygdrive/c/Windows/System32/drivers/etc/hosts
doskey vssh=subl C:\cygwin\home\hvu\.ssh\config
