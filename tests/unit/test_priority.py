import pytest

from coverage_pilot import Priority, classify_priority


@pytest.mark.parametrize(
    ("severity", "customer_impact", "expected"),
    [
        (1, False, Priority.P1),
        (1, True, Priority.P1),
        (2, False, Priority.P2),
        (2, True, Priority.P1),
        (3, False, Priority.P3),
        (3, True, Priority.P2),
        (4, False, Priority.P4),
        (4, True, Priority.P3),
    ],
)
def test_classifies_literal_priority_matrix(
    severity: int,
    customer_impact: bool,
    expected: Priority,
) -> None:
    assert (
        classify_priority(
            severity=severity,
            customer_impact=customer_impact,
        )
        is expected
    )


@pytest.mark.parametrize("severity", [0, 5])
def test_rejects_severity_outside_supported_range(severity: int) -> None:
    with pytest.raises(ValueError, match="severity must be between 1 and 4"):
        classify_priority(severity=severity, customer_impact=False)
