import pytest

import calculator as calc


def test_to_gb_gb():
    assert calc.to_gb(500, "GB") == 500


def test_to_gb_tb():
    assert calc.to_gb(2, "tb") == 2048


@pytest.mark.parametrize("amount,unit", [(0, "GB"), (-5, "GB"), (10, "MB"), ("x", "GB")])
def test_to_gb_invalid(amount, unit):
    with pytest.raises(ValueError):
        calc.to_gb(amount, unit)


def test_sample_500gb():
    r = {x.provider: x.monthly_cost for x in calc.compare(500)}
    assert r == {"AWS S3": 11.50, "Google Cloud": 10.00, "Microsoft Azure": 9.50}


def test_cheapest_is_azure_for_sample():
    assert calc.cheapest(calc.compare(500)).provider == "Microsoft Azure"


def test_sorted_cheapest_first():
    costs = [r.monthly_cost for r in calc.compare(100)]
    assert costs == sorted(costs)


def test_yearly_cost():
    assert calc.compare(500)[0].yearly_cost == 114.0


def test_monthly_cost_invalid():
    with pytest.raises(ValueError):
        calc.monthly_cost(0, 0.02)


def test_cheapest_empty():
    with pytest.raises(ValueError):
        calc.cheapest([])


def test_report_contents():
    text = calc.generate_report(500, calc.compare(500))
    assert "Microsoft Azure is the cheapest" in text
    assert "$9.50" in text
    assert "Illustrative prices only" in text


def test_csv():
    csv = calc.results_to_csv(calc.compare(500))
    assert csv.splitlines()[0].startswith("Provider")
    assert len(csv.splitlines()) == 4
