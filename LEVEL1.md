# Level 1: 계산 함수, 테스트, Ruff, CI (19쪽까지)

이 문서는 PDF 15~19쪽에서 진행한 첫 실습 기록이야. 전체 실습은 [README](README.md)에 있고, 아래의 함수와 테스트 개수는 Level 1 기준이야.
추가로 전달받은 수업 조건은 **같은 기능을 유지하면서 테스트를 직접 설계**하는 거야.
아래 테스트는 PDF의 예제 입력을 그대로 복사하지 않고 구성했어.

## 어떤 파일을 쓰는가

| 파일 | 역할 | 근거 |
| --- | --- | --- |
| `orderlab/__init__.py` | `orderlab` 패키지 준비 | PDF 7쪽 |
| `orderlab/pricing.py` | 가격 × 수량 계산, 음수 입력 거부 | PDF 15쪽 |
| `tests/test_pricing.py` | 정상·0원·음수 테스트 세 개 | PDF 16쪽 + 수업의 직접 설계 조건 |
| `requirements-dev.txt` | 공통 패키지 다섯 개 설치 | PDF 4쪽 |
| `pyproject.toml` | Ruff의 Python 대상 버전, 테스트 경로 설정 | PDF 7쪽은 파일명만 제시. 내용은 이 프로젝트의 최소 설정 |
| `.gitignore` | 가상환경과 생성 파일을 Git에서 제외 | PDF 4쪽의 `.venv/` 제외 조건 반영 |
| `.python-version` | 프로젝트 Python 버전 표시 | 환경 준비를 위한 보조 파일 |
| `.github/workflows/ci.yml` | Push/PR에서 Ruff 검사 두 개와 pytest 실행 | PDF 18쪽 |
| `LEVEL1_RESULTS.txt` | 실제 실패·복구 출력과 원복 확인 기록 | PDF 19쪽의 실습 확인용 |

`pytest`라는 이름의 새 파일은 만들 필요 없어.
검사할 코드는 `tests/test_pricing.py`에 넣고, pytest는 터미널 명령으로 실행해.

## 계산 함수가 해야 하는 일

`subtotal(unit_price, quantity)`는 두 값을 받아 곱한 정수를 반환해.
가격이나 수량 중 하나라도 음수라면 계산 전에 `ValueError`를 발생시켜.
가격 0은 허용해. `int` 타입 힌트 자체가 실수나 문자열 입력을 막아주는 건 아니야.
할인 기능은 다음 단계인 Level 2에서 다룬다.

## 이번 테스트의 설계

| 테스트 함수 | 입력 | 기댓값 | 선택한 이유 |
| --- | --- | --- | --- |
| `test_subtotal_normal_order` | 가격 2,500원, 수량 4개 | `10_000` | 가격만 반환하거나 더하기를 하는 오류를 잡아. 2,500 × 4를 직접 계산한 값과 비교해. |
| `test_subtotal_zero_price` | 가격 0원, 수량 5개 | `0` | 무료 상품도 허용하는지 검사해. 잘못해서 0까지 음수처럼 거부하면 실패해야 해. |
| `test_subtotal_negative_quantity` | 가격 2,000원, 수량 -3개 | `ValueError` | 가격이 정상이어도 음수 수량은 거부해야 해. 가격만 검사하는 구현을 잡을 수 있어. |

정상·0원 테스트는 입력 준비 → 함수 호출 → 결과 비교 순서로 분리했어.
기댓값은 `subtotal()`로 다시 계산하지 않고 상수로 적었어. 검사할 함수로 정답까지 만들면 잘못된 계산을 그대로 믿게 되거든.
음수 테스트는 **예외가 발생해야 통과**해.
이번 세 개에는 음수 가격과 수량 0의 별도 테스트는 포함하지 않았어.

## 1. 정상 실행

새 터미널에서 다음을 실행해.

```bash
cd /Users/bell_h_o_o/Documents/open-source
source .venv/bin/activate
python --version
python -m pytest -q
```

Python은 3.14.x, 테스트 결과는 `3 passed`여야 해.
`pricing.py`만 실행하면 함수 정의만 읽기 때문에 출력이 없어. 테스트가 함수를 호출해주는 구조야.

## 2. pytest를 일부러 실패시키고 복구하기

`tests/test_pricing.py`의 `test_subtotal_normal_order` 안에서 이 줄만 잠깐 바꿔.

```python
# 원래 값
expected = 10_000

# 실패 실습 때만 사용할 값
expected = 10_001
```

두 줄을 동시에 넣는 게 아니라 기존 줄의 숫자를 바꾸는 거야.

```bash
python -m pytest tests/test_pricing.py -q
```

함수의 실제 결과는 `10000`, 잘못 적은 기댓값은 `10001`이라 `AssertionError`가 발생해.
`1 failed, 2 passed`와 해당 테스트의 실패 내용을 확인해.
확인 후 `expected = 10_000`으로 되돌리고 다시 실행해서 `3 passed`로 복구해.
실패 실습은 계산 함수를 틀리게 만드는 단계가 아니라 테스트의 기댓값을 바꾸는 단계야.

## 3. Ruff 검사와 수정 (17쪽)

프로젝트 루트에서 세 명령을 실행해.

```bash
ruff check .
ruff format --check .
python -m pytest -q
```

`ruff check`는 미사용 import나 정의되지 않은 이름 같은 코드 규칙을 검사해.
`ruff format --check`는 포맷을 검사하고, pytest는 실제 실행 결과를 검사해.
하나가 통과했다고 나머지가 통과한 건 아니야.

코드 규칙 위반이나 포맷 문제가 있으면 로컬에서 아래 명령으로 자동 수정할 수 있어.

```bash
ruff check . --fix
ruff format .
```

수정 후 위의 검사 세 개를 다시 실행해. 자동 수정이 모든 문제를 해결하는 건 아니니 남은 메시지는 직접 확인해야 해.


## 4. Ruff 경고 유발과 복구 (19쪽)

`orderlab/pricing.py`에 `import math`를 잠시 추가하고 `ruff check orderlab/pricing.py`를 실행했어.
함수에서 `math`를 쓰지 않으므로 `F401: math imported but unused`가 발생했어.
이번 로그에는 import 뒤 빈 줄 간격 때문에 `I001`도 함께 나왔어.
추가했던 import를 지우고 파일을 원래 내용으로 복구했어.

pytest 실패 실습도 실제 파일의 정상 테스트에서 `expected = 10_000`을 `10_001`로 잠시 바꿔 실행했어.
`assert 10000 == 10001`에서 실패했고 결과는 `1 failed, 2 passed`였어.
그다음 기댓값을 복구한 결과 `3 passed`를 확인했어.
두 파일은 실습 전후 SHA-256이 같아서 실패용 변경이 남아 있지 않아.

실제 명령·종료 코드·전체 실패 출력·복구 결과는 [LEVEL1_RESULTS.txt](LEVEL1_RESULTS.txt)에 있어.
터미널에서 로그를 다시 보려면 프로젝트 루트에서 아래를 실행해.

```bash
cat LEVEL1_RESULTS.txt
```

## 5. CI YAML의 동작 (18쪽)

설정 파일은 `.github/workflows/ci.yml`이야. `.git/workflow`가 아니야.
Push 또는 Pull Request가 발생하면 GitHub의 Ubuntu 실행 환경에서 다음 순서로 진행돼.

1. `Check out code`: 저장소 코드를 가져와.
2. `Set up Python 3.14`: 로컬과 같은 Python 3.14 계열을 준비해.
3. `Install dependencies`: `requirements-dev.txt`의 패키지를 설치해.
4. `Ruff lint`: `ruff check .`로 코드 규칙을 검사해.
5. `Ruff format`: `ruff format --check .`로 포맷을 검사해.
6. `Run unit tests`: `python -m pytest -q`로 테스트 세 개를 실행해.

PDF와 같은 실행 조건·Python 버전·검사 명령을 사용했고, 화면에서 각 단계를 알아보기 쉽도록 이름을 붙였어.
CI에서는 `--fix`나 `ruff format .`으로 코드를 자동 수정하지 않아.
앞 단계가 실패하면 기본 동작상 다음 단계는 건너뛰므로, pytest 실패까지 보려면 Ruff 검사부터 통과해야 해.

## 6. 19쪽 과제와 완료 조건의 현재 상태

| PDF 항목 | 현재 상태 | 확인 내용 |
| --- | --- | --- |
| `subtotal()` 구현 | 완료 | 정상 계산, 0원 허용, 음수 거부 |
| 정상·0·음수 테스트 세 개 작성 | 완료 | 독립 설계한 정상·0원·음수 수량 테스트 |
| Ruff 경고와 pytest 실패 각각 유발 | 완료 | 실제 오류 출력 확인 후 원복 |
| pytest 테스트 세 개 PASS | 완료 | 최종 `3 passed` |
| Ruff 검사 두 개 PASS | 완료 | lint와 format 모두 종료 코드 0 |
| 실패 로그 화면 한 번 확인 | 로컬 로그 확인 완료 | `LEVEL1_RESULTS.txt`에 실제 출력 보관 |
| `ci.yml` Commit 및 Push | 완료 | 커밋 `b9404e5` |
| Actions 결과 초록색 | 통과 | [Python CI 실행](https://github.com/ray5497-k/git-practice/actions/runs/45925633537) |
