# Git init

name : ray 
date : 2026 0911

---

# OrderLab 공통 실행 환경

`Python_CICD.pdf`의 공통 준비 환경과 Level 1의 15~17쪽까지만 구성했어.
현재 폴더가 프로젝트 루트야. 아래 명령은 전부 여기서 실행하면 돼.

## 맞춰야 하는 조건

- OS: Windows / macOS / Ubuntu
- Python: 3.14.x
- 가상환경: `.venv`
- 패키지: `requirements-dev.txt`에 있는 다섯 개. PDF에 따라 버전 번호는 고정하지 않았어.
- `.venv/`와 이 컴퓨터에 설치한 Python 경로인 `.python/`는 Git에서 제외해뒀어.

## 이 Mac에서 바로 시작

```bash
source .venv/bin/activate
python --version
python -m pip check
```

Python 3.14.x가 나오면 돼. 새 터미널을 열 때마다 가상환경을 다시 활성화해.

현재 설치된 버전은 Python 3.14.4, Ruff 0.17.6, pytest 9.2.0,
pytest-cov 7.1.0, FastAPI 0.165.0, HTTPX 0.28.1이야.
패키지 목록은 PDF 4쪽의 공통 준비 항목 그대로 유지했어.

## 다른 컴퓨터에서 환경 만들기

Python 3.14를 먼저 설치하고, `python --version`이 3.14.x인지 확인해.
아래 `python` 명령이 3.14를 가리켜야 해. venv는 실행한 Python으로 만들어지거든.

```bash
python --version
python -m venv .venv
```

macOS / Linux에서는:

```bash
source .venv/bin/activate
```

Windows PowerShell에서는:

```powershell
.venv\Scripts\Activate.ps1
```

활성화한 뒤 설치하면 돼.

```bash
python --version
python -m pip install -r requirements-dev.txt
```

이미 Conda를 쓴다면 PDF 5쪽처럼 venv 대신 선택할 수 있어. 둘을 동시에 활성화하지 마.

## 공통 검사

```bash
ruff check .
ruff format --check .
python -m pytest -q
```

Level 1 계산 함수와 정상·0원·음수 수량 테스트 세 개를 작성해뒀어.
`python -m pytest -q`를 실행하면 `3 passed`가 나와야 해.
테스트 설계 이유, 파일별 역할과 17쪽까지의 실습 순서는 [LEVEL1.md](LEVEL1.md)에 정리했어.

## 파일 구조

- `orderlab/`: 실제 프로그램. `__init__.py`와 Level 1의 `pricing.py`가 있어.
- `tests/`: Level 1의 `test_pricing.py`가 있어.
- `pyproject.toml`: Python 3.14 대상 Ruff 설정과 테스트 경로만 지정했어. 이 설정값 자체가 PDF에 제시된 건 아니야.

`pricing.py`, 테스트 세 개와 로컬 Ruff 검사까지 진행하는 상태야.
