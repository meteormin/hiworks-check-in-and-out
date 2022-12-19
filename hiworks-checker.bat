@echo off

SET BASEDIR=%~dp0
cd "%BASEDIR%" && "%BASEDIR%venv\Scripts\activate" && python "%BASEDIR%cli.py" "%~1"