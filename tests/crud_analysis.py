import sqlite3
from app import get_db_connection

def login(client):
    with client.session_transaction() as sess:
        sess["user_id"] = 1
        sess["name"] = "Patricio"

def create_fake_analysis():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO analysis (user_id, population, beta, gamma, days, created_at)
        VALUES (?, ?, ?, ?, ?, datetime('now'))
    """, (1, 1000, 0.3, 0.1, 30))
    analysis_id = cur.lastrowid
    conn.commit()
    conn.close()
    return analysis_id

def test_create_analysis(client):
    login(client)

    response = client.post("/analysis/create", data={
        "population": 1000,
        "beta": 0.3,
        "gamma": 0.1,
        "days": 30
    }, follow_redirects=True)

    assert response.status_code == 200
    html = response.data.decode("utf-8")
    assert "Análisis creado" in html


def test_view_analysis(client):
    login(client)
    analysis_id = create_fake_analysis()

    response = client.get(f"/analysis/{analysis_id}")
    html = response.data.decode("utf-8")

    assert response.status_code == 200
    assert "1000" in html
    assert "0.3" in html
    assert "0.1" in html

def test_edit_analysis(client):
    login(client)
    analysis_id = create_fake_analysis()

    response = client.post(
        f"/analysis/{analysis_id}/edit",
        data={
            "population": 2000,
            "beta": 0.5,
            "gamma": 0.2,
            "days": 40
        },
        follow_redirects=True
    )

    html = response.data.decode("utf-8")

    assert response.status_code == 200
    assert "2000" in html
    assert "0.5" in html
    assert "0.2" in html


def test_delete_analysis(client):
    login(client)
    analysis_id = create_fake_analysis()

    response = client.get(f"/analysis/{analysis_id}/delete", follow_redirects=True)
    html = response.data.decode("utf-8")

    assert response.status_code == 200
    assert "Análisis eliminado" in html or "Historial" in html
    conn = get_db_connection()
    row = conn.execute("SELECT * FROM analysis WHERE id = ?", (analysis_id,)).fetchone()
    conn.close()

    assert row is None


def test_history_shows_entries(client):
    login(client)
    analysis_id = create_fake_analysis()

    response = client.get("/history")
    html = response.data.decode("utf-8")

    assert response.status_code == 200
    assert str(analysis_id) in html