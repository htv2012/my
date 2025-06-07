# https://github.com/okken/pytest-check

import pytest_check
import pytest_check as check
from pytest_check import check_func, raises

pytest_check.equal(a, b)
pytest_check.not_equal(a, b)
pytest_check.is_(a, b)
pytest_check.is_not(a, b)
pytest_check.is_true(x)
pytest_check.is_false(x)
pytest_check.is_none(x)
pytest_check.is_not_none(x)
pytest_check.is_in(needle, haystack)
pytest_check.is_not_in(needle, haystack)
pytest_check.is_instance(a, str)
pytest_check.is_not_instance(a, str)
pytest_check.almost_equal
pytest_check.not_almost_equal
pytest_check.greater(a, b)
pytest_check.greater_equal(a, b)
pytest_check.less(a, b)
pytest_check.less_equal(a, b)

@pytest_check.check_func
def check_something():
    pytest_check.equal(1, 1)
    pytest_check.is_true(5)

with pytest_check.raises(AssertionError):
    assert 2 == 3

