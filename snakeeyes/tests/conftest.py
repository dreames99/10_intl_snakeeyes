import pytest

from snakeeyes.app import create_app

"""
why yield statements?
1. code after yield statement serves as the teardown code, avoiding 
the indirection of registering a teardown callback function
2. ... the part after the “yield” will always be invoked, independently 
from the exception status of the test function which uses the fixture. 
3. https://docs.pytest.org/en/2.9.1/yieldfixture.html
"""

@pytest.yield_fixture(scope='session')
def app():
    """
    Setup our flask test app, this only gets executed once.

    :return: Flask app
    """
    params = {
        'DEBUG': False,
        'TESTING': True,
    }

    _app = create_app(settings_override=params)

    # Establish an application context before running the tests.
    ctx = _app.app_context()
    ctx.push()

    yield _app

    ctx.pop()


@pytest.yield_fixture(scope='function')
def client(app):
    """
    Setup an app client, this gets executed for each test function.

    :param app: Pytest fixture
    :return: Flask app client
    """
    yield app.test_client()
