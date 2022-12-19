@echo off

SET BASEDIR=%~dp0
cd "%BASEDIR%" && "%BASEDIR%venv\Scripts\activate.bat" && python "%BASEDIR%cli.py" "%~1"