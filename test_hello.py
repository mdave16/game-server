import hello
from webtest import TestApp


def test_says_hello():
    app = TestApp(hello.app)
    hello_response = app.get('/hello')
    assert hello_response.body == b'Hello World!'
    assert hello_response.status == '200 OK'
