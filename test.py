from flask_webtest import TestApp
import pytest
from app import app as current_app


@pytest.fixture
def testapp(app):
    return TestApp(app)


_app = None


@pytest.yield_fixture(scope='session')
def app():
    global _app
    if not _app:
        _app = current_app
    with _app.app_context():
        yield _app


class TestFlask(object):

    @pytest.fixture(autouse=True)
    def setup(self, testapp):
        self.testapp = testapp

    def test_comic(self):
        res = self.comic()
        assert res.status_code == 200

    def comic(self):
        return self.testapp.get(
            "/comic",
            expect_errors=True,
        )
