# OrderLab · Python CI/CD 실습

주문 금액을 계산하고 CSV에 적힌 매출을 집계했다. 주문 API는 FastAPI로 만들었고, GitHub Pages에는 CSV로 만든 [매출 보고서](https://ray5497-k.github.io/git-practice/)를 올린다.

| 단계 | 실습 내용 | 확인한 값 |
| --- | --- | --- |
| 1. 소계 | 단가 × 수량 | 2,500원짜리 4개는 10,000원. 0원은 허용하고 음수는 거부한다. |
| 2. 할인과 배송 | 할인 후 금액으로 배송비 계산 | 49,999원은 52,999원, 50,000원부터 무료 배송이다. 전액 할인은 배송비도 0원이다. |
| 3. 매출 집계 | CSV에서 단가와 수량을 곱해 합산 | 빈 CSV는 0원이다. 없는 파일과 수량에 글자를 넣은 파일도 따로 테스트했다. |
| 4. 주문 API | `POST /orders`와 `GET /orders/{id}` | 정상 주문은 201, 조회는 200, 없는 주문은 404, 잘못된 입력은 422다. 응답 JSON도 비교한다. |
| 5. 보고서 | 샘플 주문 3건으로 HTML 생성 | 3,600 × 4 + 5,900 × 2 + 1,800 × 5 = 35,200원 |

## 실행

Python 3.14 환경에서 저장소 루트를 기준으로 실행한다.

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements-dev.txt
ruff check .
ruff format --check .
python -m pytest -q --cov=orderlab --cov-report=term-missing --cov-report=xml
python generate_report.py
```

Windows PowerShell에서는 가상환경을 `.\.venv\Scripts\Activate.ps1`로 활성화한다. 보고서는 `site/index.html`을 열어 확인한다. API 테스트는 `TestClient`를 쓰므로 서버를 따로 켤 필요가 없다.

## 실패 재현과 수정

- **Level 1.** 테스트의 기댓값을 10,000원에서 10,001원으로 바꿨을 때 pytest가 실패했다. 쓰지 않는 `import math`는 Ruff가 F401로 잡았다. 두 변경을 되돌린 [로컬 출력](LEVEL1_RESULTS.txt)과 [첫 CI 성공 기록](https://github.com/ray5497-k/git-practice/actions/runs/45925633537)을 남겼다.
- **Level 2.** 배송비 조건을 `0 < amount <= 50_000`으로 쓰자, 정확히 50,000원인 주문에 배송비 3,000원이 붙었다. [PR의 실패 실행](https://github.com/ray5497-k/git-practice/actions/runs/45925729505)에서 실제 53,000원과 기댓값 50,000원의 차이를 볼 수 있다. 조건을 `0 < amount < 50_000`으로 고치고 같은 테스트를 다시 실행했다.

## CI와 배포

[실습 PR #3](https://github.com/ray5497-k/git-practice/pull/3)에서 커밋별 결과를 확인할 수 있다. Push와 PR에서 Ruff가 통과하면 Ubuntu와 Windows가 각각 같은 테스트를 실행한다. Ubuntu 실행 화면의 Artifacts에서 `coverage-xml`을 내려받으면 `coverage.xml`이 들어 있다.

PR에서는 검사를 통과해도 배포를 건너뛴다. `main`에 병합한 뒤에는 두 OS의 테스트가 모두 성공해야 `deploy`가 시작된다. 이 작업이 샘플 CSV로 HTML을 다시 만들고 Pages에 올린다. [워크플로 설정](.github/workflows/ci.yml) · [실행 기록](https://github.com/ray5497-k/git-practice/actions/workflows/ci.yml?query=branch%3Amain)
