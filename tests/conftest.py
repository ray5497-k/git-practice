import pytest


@pytest.fixture
def sample_csv(tmp_path):
    path = tmp_path / "orders.csv"
    path.write_text("price,quantity\n3200,3\n8500,2\n", encoding="utf-8")
    return path
