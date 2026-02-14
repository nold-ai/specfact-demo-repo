"""Legacy-style example code used for sidecar validation demos."""


def divide(a: float, b: float) -> float:
    # Intentional brownfield bug: no zero guard.
    return a / b


def discount(price: float, pct: float) -> float:
    # Intentional brownfield bug: percent bounds are not validated.
    return price - (price * pct)
