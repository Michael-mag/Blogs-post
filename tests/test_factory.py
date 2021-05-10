from my_blog_app import create_app


def test_config():
    assert not create_app().testing
    assert create_app({'TESTING': True}).testing


def test_hello(client):
    response = client.get("/welcome")
    assert response.data == b"Hi...Welcome!"