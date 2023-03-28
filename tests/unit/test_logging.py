"""Test the import of logging"""

from simqle.logging import simqle_filter, ignore_simqle_filter


def test_import():
    from simqle.logging import RECOMMENDED_LOG_FORMAT


def test_simqle_filter():

    record = {"extra": {"simqle": True}}
    assert simqle_filter(record)

    record = {"extra": {"something_else": True}}
    assert not simqle_filter(record)


def test_ignore_simqle_filter():

    record = {"extra": {"simqle": True}}
    assert not ignore_simqle_filter(record)

    record = {"extra": {"something_else": True}}
    assert ignore_simqle_filter(record)



