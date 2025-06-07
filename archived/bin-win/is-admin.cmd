@echo off
C:\Windows\System32\whoami /groups | C:\Windows\System32\find "High Mandatory Level" > nul && echo yes || echo no
