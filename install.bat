@echo off
chcp 65001 >nul
echo =======================================================
echo  Antigravity Codex Desktop Control Skill Installer
echo =======================================================
echo.

set "TARGET_DIR=%USERPROFILE%\.gemini\config\skills\codex-desktop-control"

echo [1/3] 스킬 디렉터리를 생성하는 중... (%TARGET_DIR%)
if not exist "%TARGET_DIR%\scripts" (
    mkdir "%TARGET_DIR%\scripts"
)

echo [2/3] 스킬 및 브릿지 스크립트 파일을 복사하는 중...
copy /Y "%~dp0skills\codex-desktop-control\SKILL.md" "%TARGET_DIR%\SKILL.md" >nul
copy /Y "%~dp0skills\codex-desktop-control\scripts\codex_bridge.py" "%TARGET_DIR%\scripts\codex_bridge.py" >nul

echo [3/3] 설치 완료 검증 중...
if exist "%TARGET_DIR%\SKILL.md" if exist "%TARGET_DIR%\scripts\codex_bridge.py" (
    echo.
    echo =======================================================
    echo  [성공] 스킬이 정상적으로 설치되었습니다!
    echo  Antigravity에서 'Codex 데스크톱에 작업 시켜줘' 등으로
    echo  즉시 사용하실 수 있습니다.
    echo =======================================================
) else (
    echo.
    echo [오류] 파일 복사 중 문제가 발생했습니다. 관리자 권한을 확인해주세요.
)

echo.
pause