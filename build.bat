@echo off


:-------------------------------------

IF "%PROCESSOR_ARCHITECTURE%" EQU "amd64" (
    >nul 2>&1 "%SYSTEMROOT%\SysWOW64\cacls.exe" "%SYSTEMROOT%\SysWOW64\config\system"
) ELSE (
    >nul 2>&1 "%SYSTEMROOT%\system32\cacls.exe" "%SYSTEMROOT%\system32\config\system"
)

if '%errorlevel%' NEQ '0' (
    echo Requesting administrative privileges...
    goto UACPrompt
) else ( goto gotAdmin )

:UACPrompt
    echo Set UAC = CreateObject^("Shell.Application"^) > "%temp%\getadmin.vbs"
    set params= %*
    echo UAC.ShellExecute "cmd.exe", "/c ""%~s0"" %params:"=""%", "", "runas", 1 >> "%temp%\getadmin.vbs"

    "%temp%\getadmin.vbs"
    del "%temp%\getadmin.vbs"
    exit /B

:gotAdmin
    pushd "%CD%"
    CD /D "%~dp0"
:--------------------------------------    


set PYTHON_PATH=
for /f "delims=" %%p in ('py -c "import sys; print(sys.executable)" 2^>nul') do set PYTHON_PATH=%%p
if not defined PYTHON_PATH for %%p in (python.exe) do set PYTHON_PATH=%%~dp$PATH:p
if not defined PYTHON_PATH if exist "%LOCALAPPDATA%\Programs\Python\Python39\python.exe" set PYTHON_PATH=%LOCALAPPDATA%\Programs\Python\Python39\python.exe
if not defined PYTHON_PATH if exist "C:\Python39\python.exe" set PYTHON_PATH=C:\Python39\python.exe
if not defined PYTHON_PATH (
    echo Error: Python installation not found. Ensure Python is installed and available.
    pause
    exit /b
)

echo Python found at: %PYTHON_PATH%

echo Generating Versioning file...
"%PYTHON_PATH%" update_versioning.py

"%PYTHON_PATH%" -m pipreqs.pipreqs --force
"%PYTHON_PATH%" -m pip install -r requirements.txt
"%PYTHON_PATH%" -m pip install -r requirements.txt --upgrade
"%PYTHON_PATH%" -m PyInstaller main.py --name="VALORANT (RPC)" --icon=favicon.ico --onefile --noconsole --version-file version.txt --add-data "favicon.ico;."

pause