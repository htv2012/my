@echo off

REM whatis: Script to create a dir off workspaces and cd to it

call nav ws > nul
mkdir %*
cd %*
