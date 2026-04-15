import pytest
from pydantic import ValidationError

from app.operations.calculation_factory import CalculationFactory
from app.schemas.calculation import CalculationCreate, CalculationType


def test_factory_add():
    assert CalculationFactory.compute(10, 5, CalculationType.Add) == 15


def test_factory_sub():
    assert CalculationFactory.compute(10, 5, CalculationType.Sub) == 5


def test_factory_multiply():
    assert CalculationFactory.compute(10, 5, CalculationType.Multiply) == 50


def test_factory_divide():
    assert CalculationFactory.compute(10, 5, CalculationType.Divide) == 2


def test_factory_divide_by_zero():
    with pytest.raises(ValueError, match="Division by zero is not allowed"):
        CalculationFactory.compute(10, 0, CalculationType.Divide)


def test_calculation_create_valid():
    calc = CalculationCreate(a=4, b=2, type=CalculationType.Add)
    assert calc.a == 4
    assert calc.b == 2
    assert calc.type == CalculationType.Add


def test_calculation_create_invalid_type():
    with pytest.raises(ValidationError):
        CalculationCreate(a=4, b=2, type="Power")


def test_calculation_create_divide_by_zero():
    with pytest.raises(ValidationError):
        CalculationCreate(a=4, b=0, type=CalculationType.Divide)