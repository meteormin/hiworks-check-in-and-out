@echo off

SET BASEDIR=%~dp0
IF exist "%BASEDIR%venv" (
  echo "%BASEDIR%venv is exists"
) ELSE (
  cd "%BASEDIR%" && python "-m" "venv" "%BASEDIR%venv" && "%BASEDIR%venv\Scripts\activate" && pip3 "install" "-r" "requirements.txt"
)