@echo off

SET BASEDIR=%~dp0
cd "%BASEDIR%" && "%BASEDIR%/venv/bin/activate.bat" && python3 "%BASEDIR%/cli.py" "%~1"