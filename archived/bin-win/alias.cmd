@echo off
REM Search DOSKey aliases or display everything

doskey /macros | grep "%1" | sort
