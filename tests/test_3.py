import asyncio
import pytest


@pytest.yield_fixture
def loop():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(None)

    yield loop

    if not loop.is_closed():
        loop.call_soon(loop.stop)
        loop.run_forever()
        loop.close()


def test_loop(loop):
    fut = asyncio.Future(loop=loop)
    loop.call_soon(fut.set_result, 1)
    ret = loop.run_until_complete(fut)
    assert ret == 1
