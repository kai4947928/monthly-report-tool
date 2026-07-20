import argparse
from unittest.mock import patch

import pytest

from app.main import main, parse_arguments, validate_target_month_argument


@pytest.mark.parametrize("target_month", ["202606", "202612", "202701"])
def test_validate_target_month_argument_accepts_valid_yyyymm(target_month):
    assert validate_target_month_argument(target_month) == target_month


@pytest.mark.parametrize(
    "target_month",
    ["20266", "2026000", "abcdef", "2026-06", "2026/06"],
)
def test_validate_target_month_argument_rejects_invalid_format(target_month):
    with pytest.raises(argparse.ArgumentTypeError, match="6桁のYYYYMM形式"):
        validate_target_month_argument(target_month)


@pytest.mark.parametrize("target_month", ["202600", "202613"])
def test_validate_target_month_argument_rejects_invalid_month(target_month):
    with pytest.raises(argparse.ArgumentTypeError, match="01から12"):
        validate_target_month_argument(target_month)


def test_parse_arguments_requires_target_month():
    with pytest.raises(SystemExit):
        parse_arguments([])


def test_parse_arguments_returns_target_month():
    arguments = parse_arguments(["--target-month", "202606"])

    assert arguments.target_month == "202606"


def test_main_does_not_load_csv_when_target_month_is_invalid():
    with patch("app.main.load_monthly_sales_csv") as load_monthly_sales_csv:
        with pytest.raises(SystemExit):
            main(["--target-month", "202613"])

    load_monthly_sales_csv.assert_not_called()
