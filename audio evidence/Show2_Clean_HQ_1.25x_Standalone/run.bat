@echo off
setlocal EnableDelayedExpansion
cd /d "%~dp0"

echo ======================================================================
echo   SHOW2 - CLEAN HQ PITCH 1.25X RESTORATION (STANDALONE)
echo ======================================================================
echo.

:: 1. Check if ffmpeg is available (local folder or PATH)
set "FFMPEG_BIN=ffmpeg"

if exist "%~dp0ffmpeg.exe" (
    set "FFMPEG_BIN=%~dp0ffmpeg.exe"
    goto :FFMPEG_FOUND
)

where ffmpeg >nul 2>&1
if %ERRORLEVEL% equ 0 (
    goto :FFMPEG_FOUND
)

:: 2. FFmpeg not found: prompt user
echo [NOTICE] FFmpeg is required to restore this audio file, but it was
echo          not detected on your system.
echo.
set /p "INSTALL_CHOICE=Would you like to automatically download and install FFmpeg now? (Y/N): "

if /i not "!INSTALL_CHOICE!"=="Y" (
    echo.
    echo [CANCELLED] FFmpeg installation declined.
    echo FFmpeg is required to process this audio. Exiting.
    echo.
    pause
    exit /b 1
)

echo.
echo Installing FFmpeg...

:: Try winget first if available
where winget >nul 2>&1
if %ERRORLEVEL% equ 0 (
    echo Using Windows Package Manager (winget) to install Gyan.FFmpeg...
    winget install --id Gyan.FFmpeg -e --accept-source-agreements --accept-package-agreements
    where ffmpeg >nul 2>&1
    if !ERRORLEVEL! equ 0 (
        goto :FFMPEG_FOUND
    )
)

:: Fallback / direct portable download via PowerShell
echo Downloading portable FFmpeg to this folder...
powershell -NoProfile -Command ^
    "[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12; " ^
    "$zipPath = Join-Path '%~dp0' 'ffmpeg_setup.zip'; " ^
    "$tempDir = Join-Path '%~dp0' 'ffmpeg_temp'; " ^
    "Write-Host 'Downloading FFmpeg zip package...'; " ^
    "Invoke-WebRequest -Uri 'https://github.com/FFmpeg-Builds/FFmpeg-Builds/releases/download/latest/ffmpeg-master-latest-win64-gpl.zip' -OutFile $zipPath; " ^
    "Write-Host 'Extracting ffmpeg.exe...'; " ^
    "Expand-Archive -Path $zipPath -DestinationPath $tempDir -Force; " ^
    "$exe = Get-ChildItem -Path $tempDir -Filter 'ffmpeg.exe' -Recurse | Select-Object -First 1; " ^
    "if ($exe) { Copy-Item -Path $exe.FullName -Destination '%~dp0' -Force }; " ^
    "Remove-Item -Path $tempDir, $zipPath -Recurse -Force; " ^
    "Write-Host 'FFmpeg installed to local folder.'"

if exist "%~dp0ffmpeg.exe" (
    set "FFMPEG_BIN=%~dp0ffmpeg.exe"
    goto :FFMPEG_FOUND
)

echo [ERROR] Automatic installation could not be completed.
echo Please manually install FFmpeg with librubberband and add it to your PATH.
echo.
pause
exit /b 1

:FFMPEG_FOUND
echo.
echo [OK] FFmpeg detected: !FFMPEG_BIN!
echo Processing show2.wav -> show2_CLEAN_HQ_pitch_1.25x.wav ...
echo.

"!FFMPEG_BIN!" -y -i "show2.wav" -af "rubberband=pitch=7.1375:transients=smooth:smoothing=on:pitchq=consistency:window=short:phase=independent,afftdn=nf=-25,highpass=f=200,lowpass=f=4000,acompressor" "show2_CLEAN_HQ_pitch_1.25x.wav"

if %ERRORLEVEL% equ 0 (
    echo.
    echo ======================================================================
    echo [SUCCESS] File created: show2_CLEAN_HQ_pitch_1.25x.wav
    echo ======================================================================
) else (
    echo.
    echo [ERROR] FFmpeg failed during processing.
)

echo.
pause
