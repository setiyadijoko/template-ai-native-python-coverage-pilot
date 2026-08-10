from coverage_pilot import Priority, classify_priority


def test_public_package_boundary_classifies_customer_impact() -> None:
    result = classify_priority(severity=3, customer_impact=True)

    assert result is Priority.P2
