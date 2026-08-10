from coverage_pilot import Priority, classify_priority


def test_operational_signal_sequence_produces_expected_priorities() -> None:
    signals = [(4, False), (3, True), (2, True), (1, False)]

    actual = [
        classify_priority(severity=severity, customer_impact=customer_impact)
        for severity, customer_impact in signals
    ]

    assert actual == [Priority.P4, Priority.P2, Priority.P1, Priority.P1]
