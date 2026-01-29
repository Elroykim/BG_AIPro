@echo off
REM ============================================================
REM BG_AIPro 로컬 환경 셋업 (Windows)
REM
REM 구조:
REM   C:\Git\Elroy Vault\01.Project & Processing\BG_AIPro\  <- 원고 + 자동화
REM   C:\Git\Elroy Vault\01.Project & Processing\AiKim\     <- 배포 전용
REM ============================================================

set "VAULT_PATH=C:\Git\Elroy Vault"
set "WORK_PATH=%VAULT_PATH%\01.Project & Processing"
set "PROJECT_PATH=%WORK_PATH%\BG_AIPro"
set "DEPLOY_PATH=%WORK_PATH%\AiKim"

echo ============================================================
echo  BG_AIPro + AiKim 로컬 환경 셋업
echo ============================================================
echo.

REM 1. 볼트 폴더 확인
if not exist "%VAULT_PATH%" (
    echo [ERROR] 옵시디언 볼트 없음: %VAULT_PATH%
    pause
    exit /b 1
)

REM 2. BG_AIPro 클론
echo [1/4] BG_AIPro 클론...
if exist "%PROJECT_PATH%\.git" (
    echo      이미 존재. pull 실행...
    cd /d "%PROJECT_PATH%"
    git pull origin claude/blog-automation-setup-dGMKc
) else (
    git clone https://github.com/Elroykim/BG_AIPro.git "%PROJECT_PATH%"
    cd /d "%PROJECT_PATH%"
    git checkout claude/blog-automation-setup-dGMKc
)
echo.

REM 3. AiKim 배포 레포 클론
echo [2/4] AiKim 배포 레포 클론...
if exist "%DEPLOY_PATH%\.git" (
    echo      이미 존재. pull 실행...
    cd /d "%DEPLOY_PATH%"
    git pull origin main
) else (
    git clone https://github.com/Elroykim/AiKim.git "%DEPLOY_PATH%"
)
echo.

REM 4. Python 의존성
echo [3/4] Python 의존성 설치...
cd /d "%PROJECT_PATH%"
pip install python-frontmatter python-slugify pydantic pydantic-settings pyyaml httpx markdown rich anthropic
echo.

REM 5. Hugo 확인
echo [4/4] Hugo 확인...
hugo version >nul 2>&1
if errorlevel 1 (
    echo      Hugo 미설치. 설치 명령:
    echo      winget install Hugo.Hugo.Extended
    pause
    exit /b 1
)
hugo version
echo.

echo ============================================================
echo  셋업 완료!
echo ============================================================
echo.
echo  BG_AIPro: %PROJECT_PATH%  (원고 + 자동화 + SEO)
echo  AiKim:    %DEPLOY_PATH%  (배포 전용)
echo.
echo  배포 방법: scripts\deploy.bat 실행
echo.
pause
