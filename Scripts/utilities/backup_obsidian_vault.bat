@echo off
REM Obsidian Vault Backup Script
REM Creates timestamped backups of the Obsidian vault with smart exclusions

setlocal enabledelayedexpansion

REM Configuration
set "VAULT_PATH=D:\Github\Obsidian"
set "BACKUP_ROOT=D:\Backups\Obsidian"
set "TIMESTAMP=%date:~-4,4%-%date:~-10,2%-%date:~-7,2%_%time:~0,2%-%time:~3,2%-%time:~6,2%"
set "TIMESTAMP=%TIMESTAMP: =0%"
set "BACKUP_PATH=%BACKUP_ROOT%\Obsidian_%TIMESTAMP%"
set "EXCLUDE_FILE=%~dp0exclude_list.txt"

echo ========================================
echo    Obsidian Vault Backup Script
echo ========================================
echo.
echo Vault Path: %VAULT_PATH%
echo Backup Path: %BACKUP_PATH%
echo Timestamp: %TIMESTAMP%
echo Exclude File: %EXCLUDE_FILE%
echo.

REM Check if vault exists
if not exist "%VAULT_PATH%" (
    echo ERROR: Vault path not found: %VAULT_PATH%
    pause
    exit /b 1
)

REM Check if exclude file exists
if not exist "%EXCLUDE_FILE%" (
    echo WARNING: Exclude file not found: %EXCLUDE_FILE%
    echo Will backup all files (this may be very large)
    echo.
    set /p "CONTINUE=Continue anyway? (y/N): "
    if /i not "!CONTINUE!"=="y" (
        echo Backup cancelled.
        pause
        exit /b 1
    )
)

REM Create backup directory
if not exist "%BACKUP_ROOT%" (
    echo Creating backup root directory...
    mkdir "%BACKUP_ROOT%"
)

echo Creating backup directory...
mkdir "%BACKUP_PATH%"

REM Copy vault contents with exclusions
echo Copying vault contents...
if exist "%EXCLUDE_FILE%" (
    echo Using exclude list: %EXCLUDE_FILE%
    xcopy "%VAULT_PATH%" "%BACKUP_PATH%" /E /I /H /Y /EXCLUDE:"%EXCLUDE_FILE%"
) else (
    echo No exclude list - copying all files
    xcopy "%VAULT_PATH%" "%BACKUP_PATH%" /E /I /H /Y
)

if %errorlevel% equ 0 (
    echo.
    echo ========================================
    echo    Backup completed successfully!
    echo ========================================
    echo.
    echo Backup location: %BACKUP_PATH%
    echo.
    
    REM Create backup info file
    echo Backup created on: %date% %time% > "%BACKUP_PATH%\backup_info.txt"
    echo Vault path: %VAULT_PATH% >> "%BACKUP_PATH%\backup_info.txt"
    echo Backup path: %BACKUP_PATH% >> "%BACKUP_PATH%\backup_info.txt"
    echo Timestamp: %TIMESTAMP% >> "%BACKUP_PATH%\backup_info.txt"
    echo Exclude file used: %EXCLUDE_FILE% >> "%BACKUP_PATH%\backup_info.txt"
    
    REM Calculate backup size
    for /f "tokens=3" %%a in ('dir "%BACKUP_PATH%" /s ^| find "File(s)"') do set "BACKUP_SIZE=%%a"
    echo Backup size: %BACKUP_SIZE% >> "%BACKUP_PATH%\backup_info.txt"
    
    echo Backup info saved to: %BACKUP_PATH%\backup_info.txt
    echo Backup size: %BACKUP_SIZE%
    
    REM Clean up old backups (keep last 5)
    echo.
    echo Cleaning up old backups (keeping last 5)...
    for /f "tokens=*" %%a in ('dir "%BACKUP_ROOT%" /b /ad /o-d ^| findstr "Obsidian_"') do (
        set "BACKUP_DIR=%%a"
        set /a "BACKUP_COUNT+=1"
        if !BACKUP_COUNT! gtr 5 (
            echo Removing old backup: !BACKUP_DIR!
            rmdir /s /q "%BACKUP_ROOT%\!BACKUP_DIR!"
        )
    )
    
) else (
    echo.
    echo ERROR: Backup failed with error code %errorlevel%
    echo Check if you have sufficient disk space and permissions
)

echo.
pause
