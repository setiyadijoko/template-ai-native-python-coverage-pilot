from enum import StrEnum


class Priority(StrEnum):
    P1 = "P1"
    P2 = "P2"
    P3 = "P3"
    P4 = "P4"


def classify_priority(*, severity: int, customer_impact: bool) -> Priority:
    if severity not in range(1, 5):
        raise ValueError("severity must be between 1 and 4")

    level = severity - int(customer_impact)
    return Priority(f"P{max(1, level)}")
