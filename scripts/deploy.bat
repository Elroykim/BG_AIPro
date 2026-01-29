@echo off
REM ============================================================
REM BG_AIPro -> AiKim 배포 스크립트
REM
REM hugo_site/의 콘텐츠를 AiKim 레포에 복사하고 push한다.
REM GitHub Actions가 자동으로 Hugo 빌드 + GitHub Pages 배포.
REM ============================================================

set "VAULT_PATH=C:\Git\Elroy Vault"
set "WORK_PATH=%VAULT_PATH%\01.Project & Processing"
set "PROJECT_PATH=%WORK_PATH%\BG_AIPro"
set "DEPLOY_PATH=%WORK_PATH%\AiKim"
set "HUGO_SRC=%PROJECT_PATH%\hugo_site"

echo ============================================================
echo  BG_AIPro -> AiKim 배포
echo ============================================================
echo.

REM 1. 경로 확인
if not exist "%HUGO_SRC%\hugo.yaml" (
    echo [ERROR] Hugo 사이트 없음: %HUGO_SRC%
    pause
    exit /b 1
)
if not exist "%DEPLOY_PATH%\.git" (
    echo [ERROR] AiKim 레포 없음: %DEPLOY_PATH%
    echo setup_local.bat를 먼저 실행하세요.
    pause
    exit /b 1
)

REM 2. AiKim 레포 최신화
echo [1/4] AiKim 레포 최신화...
cd /d "%DEPLOY_PATH%"
git pull origin main 2>nul
echo.

REM 3. hugo_site 콘텐츠를 AiKim에 동기화
echo [2/4] 콘텐츠 동기화...
REM 핵심 파일들만 동기화 (public/, .git 제외)
robocopy "%HUGO_SRC%\content" "%DEPLOY_PATH%\content" /MIR /NFL /NDL /NJH /NJS
robocopy "%HUGO_SRC%\themes" "%DEPLOY_PATH%\themes" /MIR /NFL /NDL /NJH /NJS
robocopy "%HUGO_SRC%\archetypes" "%DEPLOY_PATH%\archetypes" /MIR /NFL /NDL /NJH /NJS
robocopy "%HUGO_SRC%\.github" "%DEPLOY_PATH%\.github" /MIR /NFL /NDL /NJH /NJS
copy /Y "%HUGO_SRC%\hugo.yaml" "%DEPLOY_PATH%\hugo.yaml" >nul
if exist "%HUGO_SRC%\.gitignore" copy /Y "%HUGO_SRC%\.gitignore" "%DEPLOY_PATH%\.gitignore" >nul
echo      동기화 완료
echo.

REM 4. 커밋 및 푸시
echo [3/4] 커밋...
cd /d "%DEPLOY_PATH%"
git add -A
git diff --cached --quiet
if errorlevel 1 (
    git commit -m "deploy: 콘텐츠 업데이트 %date% %time:~0,5%"
    echo.
    echo [4/4] 푸시...
    git push origin main
    echo.
    echo ============================================================
    echo  배포 완료!
    echo  GitHub Actions가 자동으로 빌드 및 배포합니다.
    echo  확인: https://elroykim.github.io/AiKim/
    echo ============================================================
) else (
    echo      변경사항 없음. 배포 건너뜀.
)
echo.
pause
