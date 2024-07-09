from microchain import Function


class Sum(Function):
    @property
    def description(self) -> str:
        return "Use this function to compute the sum of two numbers"

    @property
    def example_args(self) -> list[float]:
        return [2, 2]

    def __call__(self, a: float, b: float) -> float:
        return a + b


class Product(Function):
    @property
    def description(self) -> str:
        return "Use this function to compute the product of two numbers"

    @property
    def example_args(self) -> list[int]:
        return [2, 2]

    def __call__(self, a: float, b: float) -> float:
        return a * b


class GreaterThan(Function):
    @property
    def description(self) -> str:
        return (
            "Use this function to assess if one number is greater than the other number"
        )

    @property
    def example_args(self) -> list[float]:
        return [2, 2]

    def __call__(self, a: float, b: float) -> bool:
        return a > b