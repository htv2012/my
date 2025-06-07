@echo off
file-tools.py cd -o %TEMP%\cdfile_worker.cmd %*
%TEMP%\cdfile_worker.cmd
