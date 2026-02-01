@echo off
rd /s /q objects
md objects
make
python ./createmwa.py
pause
