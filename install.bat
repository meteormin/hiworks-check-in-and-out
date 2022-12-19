@echo off

SET BASEDIR=%~dp0
IF "-d" "%BASEDIR%/venv" (
  echo "%BASEDIR%/venv is exists"
) ELSE (
  cd "%BASEDIR%" && python3 "-m" "venv" "%BASEDIR%\venv" && "%BASEDIR%\venv\activate.bat" && pip3 "install" "-r" "requirements.txt"
)