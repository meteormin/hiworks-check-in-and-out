@echo off

SET BASEDIR=%~dp0
cd "%BASEDIR%\..\" && "%BASEDIR%hiworks-checker.bat" check-work-hour
