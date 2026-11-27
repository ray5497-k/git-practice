import pytest

from orderlab.pricing import final_total, subtotal


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


@pytest.mark.parametrize(
    "price, expected",
    [(49_999, 52_999), (50_000, 50_000), (50_001, 50_001)],
)
def test_shipping_fee_at_free_shipping_limit(price, expected):
    assert final_total(price, 1, 0) == expected


def test_shipping_fee_after_discount():
    assert final_total(30_000, 2, 20) == 51_000


def test_discount_rounds_down_to_whole_won():
    assert final_total(1_505, 1, 10) == 4_355


def test_no_shipping_on_fully_discounted_order():
    assert final_total(9_000, 2, 100) == 0


@pytest.mark.parametrize("discount", [-1, 101])
def test_discount_out_of_range(discount):
    with pytest.raises(ValueError, match="invalid discount"):
        final_total(7_200, 3, discount)
