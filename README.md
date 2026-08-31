# Antigravity Codex Desktop Control Skill (`agycodex-desktop-skill`)

Antigravity(AGY) 에이전트에서 로컬 PC에 실행 중인 **OpenAI Codex Desktop 앱(`ChatGPT.exe` / `codex app`)으로 직접 명령과 프롬프트를 전달하고 제어**하는 전용 브릿지 스킬입니다.

Antigravity와 대화하는 도중, 로컬 Codex Desktop의 **ChatGPT Plus/Pro 구독 혜택(내장 `GPT-Image-2`, 내장 멀티모달 도구 등)**을 종량제 API Key 비용 없이 완전히 자동화하여 호출할 수 있습니다.

---

## 💻 사용을 위해 설치해야 하는 필수 프로그램

이 스킬을 사용하려면 PC에 아래 프로그램들이 준비되어 있어야 합니다:

| 프로그램 | 필수 여부 | 설명 및 준비 사항 |
| :--- | :---: | :--- |
| **Antigravity** | **필수** | 본 스킬을 구동하는 메인 AI 에이전트 (IDE 또는 CLI) |
| **OpenAI Codex Desktop 앱** | **필수** | Windows용 공식 Codex/ChatGPT 데스크톱 애플리케이션 (`ChatGPT.exe`). **ChatGPT Plus/Pro/Team 계정으로 로그인**되어 있어야 합니다. |
| **Codex CLI (`codex.exe`)** | **필수** | Codex Desktop 설치 시 함께 번들되는 CLI 도구 (터미널에서 `codex` 명령 사용 가능 여부 확인) |
| **Python** 또는 **`uv`** | **필수** | Python 3.9 이상 또는 초고속 실행기 `uv` (추천 ⭐) |

---

### 📦 `uv` 설치 방법 (1줄 간편 설치)

`uv`가 아직 설치되어 있지 않다면, 터미널에서 **아래 1줄 명령어를 복사하여 실행**하시면 몇 초 만에 설치가 완료됩니다:

#### 🪟 Windows (PowerShell)
```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```
*(또는 `winget install astral-sh.uv` / `pip install uv`)*

#### 🍎 macOS / 🐧 Linux
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```
*(또는 Homebrew 사용 시 `brew install uv`)*

#### 🔍 설치 확인
터미널을 새로 열고 아래 명령어로 버전이 출력되는지 확인합니다:
```bash
uv --version
```

---

## 🎯 구체적으로 어떤 일을 시킬 수 있나요?

Antigravity에게 평소처럼 자연어로 지시하면, Antigravity가 백그라운드에서 Codex Desktop을 원격 조종하여 아래와 같은 실무 작업들을 수행합니다:

### 1. 🎨 `GPT-Image-2` 기반 고화질 이미지 생성 및 에셋 자동 회수
* **어떤 일인가요?**: 
  OpenAI의 최신 이미지 생성 모델인 **`GPT-Image-2`**를 호출하여 1024×1024부터 2K/4K 해상도의 이미지를 생성하고, 생성된 결과 파일을 현재 내 작업 폴더로 즉시 복사해옵니다.
* **장점**: 
  별도의 OpenAI Platform 종량제 API Key 충전 없이, **기존 ChatGPT Plus/Pro 구독 풀(Pool)**을 활용합니다.
* **실제 지시 예시**:
  * *"Codex 데스크톱에 네온 사이버펑크 도시 야경 2K 해상도로 그려달라고 해줘"*
  * *"Codex로 제품 목업용 세라믹 머그잔 이미지 생성해서 작업 폴더로 가져와줘"*
  * *"방금 Codex가 만든 이미지 현재 폴더에 `banner.png`로 저장해줘"*

---

### 2. 🔀 병렬 작업 분담 및 서브 에이전트 위임 (Multi-Agent Workflow)
* **어떤 일인가요?**: 
  Antigravity가 메인 코딩이나 복잡한 구현을 진행하는 동안, 무거운 탐색·문서화·코드 리뷰 작업을 **Codex Desktop 세션에 비동기 대기열(Queue)로 전달**하여 백그라운드에서 병렬로 처리시킵니다.
* **실제 지시 예시**:
  * *"이 모듈 리팩토링 설계안 검토 작업을 Codex 데스크톱 세션에 넘겨서 분석시켜줘"*
  * *"Codex 데스크톱에 이 API 명세서 초안 작성하도록 대기열에 넣어두고, 우리는 다음 코드 작성하자"*

---

### 3. 💬 데스크톱 세션 자동 생성 및 사이드바 동기화
* **어떤 일인가요?**: 
  터미널을 벗어나지 않고도 Codex Desktop 앱에 **새 대화창(프로젝트 대화 또는 독립 새 대화 `new-chat`)**을 즉시 열고, 생성된 세션이 Codex Desktop 앱의 왼쪽 사이드바에 실시간으로 나타나도록 메타데이터(`source: vscode`)를 동기화합니다.
* **실제 지시 예시**:
  * *"Codex에 프로젝트 없는 새 대화창 하나 열어서 인사 남겨줘"*
  * *"지금 열려 있는 Codex 데스크톱 세션 목록 보여줘"*

---

### 4. 🧹 세션 라이프사이클 및 백그라운드 대기열 관리
* **어떤 일인가요?**: 
  작업이 끝난 세션을 원격으로 영구 삭제(`codex delete`)하거나 아카이브하여 사이드바를 깔끔하게 유지합니다.
* **실제 지시 예시**:
  * *"방금 작업한 Codex 임시 세션 정리해서 삭제해줘"*

---

## 🏗️ 아키텍처 흐름도

```text
[ Antigravity Agent ]
        │
        ▼ (스킬 호출)
[ codex_bridge.py / codex CLI ]
        │
        ▼ (명령을 로컬 대기열에 저장)
[ queue_1.sqlite / state_5.sqlite ]
        │
        ▼ (대기 중인 명령을 실시간으로 가져와 자동 실행)
[ Codex Desktop App (ChatGPT.exe) ] ──▶ (ChatGPT Plus/Pro 구독으로 GPT-Image-2 / 추론 실행)
        │
        ▼ (결과 파일 출력)
[ $CODEX_HOME/generated_images/ ] ──▶ Antigravity가 내 작업 폴더로 자동 회수 (fetch-image)
```

---

## 📦 설치 방법 (Installation)

### 방법 1. 원클릭 자동 설치 (가장 추천 ⭐)
1. 이 레포지토리를 다운로드(또는 Git Clone)합니다.
2. 폴더 안에 있는 **`install.bat` 파일을 더블 클릭**합니다.
3. 자동으로 본인 PC의 `%USERPROFILE%\.gemini\config\skills\codex-desktop-control\` 경로에 스킬이 복사되고 전역 활성화됩니다.

### 방법 2. PowerShell 수동 설치
```powershell
.\install.ps1
```

---

## 🚀 사용 예시

### 🗣️ Antigravity 대화창에서 자연어로 쓰기 (가장 편리함)
스킬이 설치되면 Antigravity가 자동으로 도구를 인식하므로, 평소처럼 대화하시면 됩니다:

* *"Codex 데스크톱에 노을 지는 웅장한 폭포 고화질로 생성하라고 해줘"*
* *"Codex 새 대화 열고 [프롬프트] 실행해줘"*
* *"지금 Codex Desktop에 열린 세션들 확인해줘"*
* *"Codex가 생성한 최신 그림 내 폴더로 가져와줘"*

---

### ⌨️ 터미널에서 브릿지 CLI 직접 호출하기

```bash
# 1. 활성 세션(스레드) 목록 확인
uv run python skills/codex-desktop-control/scripts/codex_bridge.py list -n 5

# 2. 특정 세션에 프롬프트 전송 (데스크톱 앱 화면에 실시간 입력 및 실행됨)
uv run python skills/codex-desktop-control/scripts/codex_bridge.py queue --thread "<세션_UUID>" --message "원하는 지시사항"

# 3. 사이드바에 표시되는 새 세션 생성
uv run python skills/codex-desktop-control/scripts/codex_bridge.py new --prompt "새 대화를 시작합니다."

# 4. 가장 최근에 생성된 이미지 현재 폴더로 가져오기
uv run python skills/codex-desktop-control/scripts/codex_bridge.py fetch-image --dest "./output.png"
```

---

## 🗑️ 제거 방법 (Uninstall)

스킬을 제거하고 싶을 때는 폴더 내 `uninstall.bat`을 실행하거나 아래 명령어를 입력합니다:
```powershell
Remove-Item -Recurse -Force "$HOME\.gemini\config\skills\codex-desktop-control"
```

---

## 📄 라이선스 (License)
MIT License