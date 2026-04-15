from app.models.calculation import Calculation
from app.operations.calculation_factory import CalculationFactory
from app.schemas.calculation import CalculationType


def test_create_calculation_record(db_session):
    result = CalculationFactory.compute(8, 2, CalculationType.Divide)

    calculation = Calculation(
        a=8,
        b=2,
        type="Divide",
        result=result
    )

    db_session.add(calculation)
    db_session.commit()
    db_session.refresh(calculation)

    assert calculation.id is not None
    assert calculation.a == 8
    assert calculation.b == 2
    assert calculation.type == "Divide"
    assert calculation.result == 4


def test_saved_calculation_can_be_queried(db_session):
    result = CalculationFactory.compute(3, 7, CalculationType.Add)

    calculation = Calculation(
        a=3,
        b=7,
        type="Add",
        result=result
    )

    db_session.add(calculation)
    db_session.commit()

    saved = db_session.query(Calculation).filter_by(type="Add").first()

    assert saved is not None
    assert saved.result == 10