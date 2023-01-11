@echo off

SET BASEDIR=%~dp0
IF exist "%BASEDIR%venv" (
  echo "%BASEDIR%venv is exists"
  "%BASEDIR%venv\Scripts\activate" && pip "install" "-r" "requirements.txt"
) ELSE (
  cd "%BASEDIR%" && python "-m" "venv" "%BASEDIR%venv"
)

"%BASEDIR%venv\Scripts\activate" && pip "install" "-r" "requirements.txt"