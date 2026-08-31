@echo off
chcp 65001 >nul
echo [제거] Codex Desktop Control 스킬을 제거합니다...
set "TARGET_DIR=%USERPROFILE%\.gemini\config\skills\codex-desktop-control"

if exist "%TARGET_DIR%" (
    rmdir /S /Q "%TARGET_DIR%"
    echo 스킬이 성공적으로 제거되었습니다.
) else (
    echo 제거할 스킬 폴더가 존재하지 않습니다.
)
pause