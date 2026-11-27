import pytest

from orderlab.csv_report import revenue_from_csv


def test_revenue_adds_all_orders(sample_csv):
    assert revenue_from_csv(sample_csv) == 26_600


@pytest.mark.parametrize("contents", ["", "price,quantity\n"])
def test_csv_without_orders(tmp_path, contents):
    path = tmp_path / "empty.csv"
    path.write_text(contents, encoding="utf-8")

    assert revenue_from_csv(path) == 0


def test_csv_missing_file(tmp_path):
    with pytest.raises(FileNotFoundError):
        revenue_from_csv(tmp_path / "missing.csv")


def test_csv_quantity_is_not_a_number(tmp_path):
    path = tmp_path / "orders.csv"
    path.write_text("price,quantity\n3200,세 개\n", encoding="utf-8")

    with pytest.raises(ValueError):
        revenue_from_csv(path)
