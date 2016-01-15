import docker as libdocker
import pytest
import redis
import socket
import time
import uuid


@pytest.fixture(scope='session')
def session_id():
    """Unique session identifier, random string."""
    return str(uuid.uuid4())


@pytest.fixture(scope='session')
def docker():
    """Docker client"""
    return libdocker.Client(version='auto')


@pytest.fixture(scope='session')
def unused_port():
    def factory():
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(('127.0.0.1', 0))
            return s.getsockname()[1]
    return factory


@pytest.yield_fixture(scope='session')
def redis_server(unused_port, session_id, docker):
    docker.pull('redis')
    port = unused_port()
    container = docker.create_container(
        image='redis',
        name='test-redis-{}'.format(session_id),
        ports=[6379],
        detach=True,
        host_config=docker.create_host_config(port_bindings={6379: port})
    )
    try:
        assert docker.start(container=container['Id']) is None

        try:
            # ping redis server, wait for actual starting
            for i in range(100):
                try:
                    redis_cli = redis.StrictRedis(host='127.0.0.1',
                                                  port=port, db=0)
                    redis_cli.get('some_key')
                    break
                except redis.ConnectionError:
                    time.sleep(0.01)

            yield port
        finally:
            docker.kill(container=container['Id'])
    finally:
        docker.remove_container(container['Id'])


@pytest.fixture
def redis_client(redis_server):
    return redis.StrictRedis(host='127.0.0.1',
                             port=redis_server, db=0)


def test_redis(redis_client):
    redis_client.set(b'key', b'value')
    assert redis_client.get(b'key') == b'value'
