@echo off
title HRM Rooster server
cd /d "%~dp0"
where python >nul 2>nul && (python server.py & pause & goto :eof)
where py >nul 2>nul && (py server.py & pause & goto :eof)
echo Python niet gevonden. Installeer Python via https://www.python.org/downloads/ (vink "Add python.exe to PATH" aan).
pause
