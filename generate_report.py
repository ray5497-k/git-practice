from pathlib import Path

from orderlab.csv_report import revenue_from_csv


def generate_report(csv_path: Path, output_dir: Path) -> None:
    revenue = revenue_from_csv(csv_path)
    html = f"""<!doctype html>
<html lang="ko">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>OrderLab 주문 매출 보고서</title>
</head>
<body>
  <main>
    <h1>주문 매출 보고서</h1>
    <p>총매출 <strong>{revenue:,}원</strong></p>
  </main>
</body>
</html>
"""
    output_dir.mkdir(exist_ok=True)
    (output_dir / "index.html").write_text(html, encoding="utf-8")


if __name__ == "__main__":
    generate_report(Path("data/sample_orders.csv"), Path("site"))
