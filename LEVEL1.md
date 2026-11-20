# Level 1: 계산 함수, 테스트, Ruff (17쪽까지)

현재 진행 범위는 PDF 15~17쪽이야.
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

`pytest`라는 이름의 새 파일은 만들 필요 없어.
검사할 코드는 `tests/test_pricing.py`에 넣고, pytest는 터미널 명령으로 실행해.

## 계산 함수가 해야 하는 일

`subtotal(unit_price, quantity)`는 두 값을 받아 곱한 정수를 반환해.
가격이나 수량 중 하나라도 음수라면 계산 전에 `ValueError`를 발생시켜.
가격 0은 허용해. `int` 타입 힌트 자체가 실수나 문자열 입력을 막아주는 건 아니야.
현재 과제에 없는 별도의 타입 검사나 할인 기능은 추가하지 않았어.

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
현재 범위는 계산 함수와 테스트 세 개, 로컬 Ruff 검사까지야.
