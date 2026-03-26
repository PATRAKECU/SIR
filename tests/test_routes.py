def login(client):
    with client.session_transaction() as sess:
        sess["user_id"] = 1
        sess["name"] = "Patricio"

def test_index_redirects_without_login(client):
    response = client.get("/")
    assert response.status_code == 302
    assert "/login" in response.headers["Location"]

def test_index_status_code(client):
    login(client)
    response = client.get("/")
    assert response.status_code == 200

def test_index_contains_title(client):
    login(client)
    response = client.get("/")
    html = response.data.decode("utf-8")
    assert "Modelo SIR" in html