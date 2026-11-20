import pytest

from orderlab.pricing import subtotal


def test_subtotal_normal_order():
    unit_price = 2_500
    quantity = 4
    expected = 10_000

    actual = subtotal(unit_price, quantity)

    assert actual == expected


def test_subtotal_zero_price():
    unit_price = 0
    quantity = 5
    expected = 0

    actual = subtotal(unit_price, quantity)

    assert actual == expected


def test_subtotal_negative_quantity():
    unit_price = 2_000
    quantity = -3

    with pytest.raises(ValueError):
        subtotal(unit_price, quantity)
