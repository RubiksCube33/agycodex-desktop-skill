# PowerShell Installer for Antigravity Codex Desktop Control Skill
$ErrorActionPreference = "Stop"

Write-Host "=======================================================" -ForegroundColor Cyan
Write-Host " Antigravity Codex Desktop Control Skill Installer" -ForegroundColor Cyan
Write-Host "=======================================================" -ForegroundColor Cyan
Write-Host ""

$targetDir = "$HOME\.gemini\config\skills\codex-desktop-control"
$scriptsDir = "$targetDir\scripts"

Write-Host "[1/3] 스킬 디렉터리 확인/생성: $targetDir"
if (-not (Test-Path $scriptsDir)) {
    New-Item -ItemType Directory -Path $scriptsDir -Force | Out-Null
}

Write-Host "[2/3] 스킬 파일 복사 중..."
Copy-Item "$PSScriptRoot\skills\codex-desktop-control\SKILL.md" -Destination "$targetDir\SKILL.md" -Force
Copy-Item "$PSScriptRoot\skills\codex-desktop-control\scripts\codex_bridge.py" -Destination "$scriptsDir\codex_bridge.py" -Force

if ((Test-Path "$targetDir\SKILL.md") -and (Test-Path "$scriptsDir\codex_bridge.py")) {
    Write-Host ""
    Write-Host "=======================================================" -ForegroundColor Green
    Write-Host " [성공] 스킬이 정상적으로 설치되었습니다!" -ForegroundColor Green
    Write-Host " Antigravity에서 자유롭게 Codex 데스크톱 명령을 호출할 수 있습니다." -ForegroundColor Green
    Write-Host "=======================================================" -ForegroundColor Green
} else {
    Write-Host "[오류] 설치 중 문제가 발생했습니다." -ForegroundColor Red
}