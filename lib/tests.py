import pytest


def assert_status_with_message(status_code=200, response=None, message=None):
    """
    Check to see if a message is contained within a response.

    :param status_code: Status code that defaults to 200
    :type status_code: int
    :param response: Flask response
    :type response: str
    :param message: String to check for
    :type message: str
    :return: None
    """
    # assert response.status_code == str(status_code)
    assert response.status_code == status_code
    assert message in str(response.data)


class ViewTestMixin(object):
    """
    Automatically load in a session and client, this is common for a lot of
    tests that work w/ views.  See https://docs.pytest.org/en/stable/fixture.html
    """

    @pytest.fixture(autouse=True)
    def set_common_fixtures(self, session, client):
        # def __init__(self, session, client):
        self.session = session
        self.client = client
