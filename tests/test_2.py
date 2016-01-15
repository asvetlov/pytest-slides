import pytest
import socket


@pytest.fixture
def unique_port():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('127.0.0.1', 0))
        return s.getsockname()[1]


def test_port(unique_port):
    print(unique_port)


@pytest.fixture
def unique_port2():
    def factory():
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(('127.0.0.1', 0))
            return s.getsockname()[1]
    return factory


def test_port2(unique_port2):
    print(unique_port2())
