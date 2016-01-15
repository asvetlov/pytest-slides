import pytest


def test_a():
    assert 1 == 1


class TestB:
    def test_b(self):
        assert 'a'.upper() == 'A'

    def test_c(self):
        with pytest.raises(ZeroDivisionError):
            1/0
