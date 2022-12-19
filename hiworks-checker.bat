@echo off

SET BASEDIR=%~dp0
cd "%BASEDIR%" && "%BASEDIR%venv\Scripts\activate.bat" && python3 "%BASEDIR%cli.py" "%~1"