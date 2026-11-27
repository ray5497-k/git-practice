from generate_report import generate_report


def test_report_shows_total_revenue(tmp_path):
    orders = tmp_path / "orders.csv"
    orders.write_text("price,quantity\n1600,2\n4900,3\n", encoding="utf-8")
    site = tmp_path / "site"

    generate_report(orders, site)

    html = (site / "index.html").read_text(encoding="utf-8")
    assert "17,900원" in html
