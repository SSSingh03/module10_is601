from app.schemas.calculation import CalculationType


class CalculationFactory:
    @staticmethod
    def compute(a: float, b: float, calculation_type: CalculationType) -> float:
        if calculation_type == CalculationType.Add:
            return a + b
        if calculation_type == CalculationType.Sub:
            return a - b
        if calculation_type == CalculationType.Multiply:
            return a * b
        if calculation_type == CalculationType.Divide:
            if b == 0:
                raise ValueError("Division by zero is not allowed")
            return a / b

        raise ValueError(f"Unsupported calculation type: {calculation_type}")