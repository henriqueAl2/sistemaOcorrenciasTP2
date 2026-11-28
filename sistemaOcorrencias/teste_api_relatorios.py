from datetime import date, datetime

import admin_reports
from admin_reports import create_app


def _authenticate(client):
    with client.session_transaction() as session:
        session["is_admin"] = True


def test_statistics_api_requires_admin_session():
    client = create_app().test_client()

    response = client.get("/api/statistics/overview")

    assert response.status_code == 401
    assert response.get_json() == {"erro": "Autenticação administrativa necessária."}


def test_reports_api_rejects_invalid_filters():
    client = create_app().test_client()
    _authenticate(client)

    response = client.get("/api/reports/occurrences?start_date=invalid")

    assert response.status_code == 400
    assert "formato AAAA-MM-DD" in response.get_json()["erro"]


def test_statistics_api_returns_dashboard_aggregates(monkeypatch):
    client = create_app().test_client()
    _authenticate(client)
    expected = {
        "total": 1,
        "indicators": {"resolvidas": 1, "taxa_resolucao": 100.0},
        "by_month": [{"mes": "2026-11", "total": 1}],
        "by_type": [{"rotulo": "Buraco", "total": 1}],
        "by_status": [{"rotulo": "Resolvida", "total": 1}],
        "by_local": [{"codigo": 10, "rotulo": "Centro", "total": 1}],
        "total_searches": 2,
        "searches_by_term": [{"rotulo": "Buraco", "total": 2}],
        "searches_by_region": [{"rotulo": "Centro", "total": 2}],
        "total_users": 3,
        "by_profile": [{"rotulo": "user", "total": 2}, {"rotulo": "admin", "total": 1}],
    }
    captured = {}

    def report_data(filters):
        captured.update(filters)
        return expected

    monkeypatch.setattr(admin_reports, "_report_data", report_data)
    response = client.get(
        "/api/statistics/overview?start_date=2026-11-01&tipo=3&local=10"
    )

    assert response.status_code == 200
    payload = response.get_json()
    assert payload["occurrences"]["resolution_rate"] == 100.0
    assert payload["searches"]["total"] == 2
    assert payload["users"]["by_profile"][1]["label"] == "admin"
    assert captured["start_date"] == "2026-11-01"
    assert captured["tipo"] == "3"
    assert captured["local"] == "10"


def test_report_api_serializes_occurrences_without_user_identifiers(monkeypatch):
    client = create_app().test_client()
    _authenticate(client)
    monkeypatch.setattr(admin_reports, "_occurrences", lambda filters: [{
        "id": 5,
        "tipo": "Buraco",
        "descricao": "Calçada danificada",
        "hora": datetime(2026, 11, 13, 9, 30),
        "data": date(2026, 11, 13),
        "status": "Resolvida",
        "local_codigo": 10,
        "endereco": "Centro",
    }])

    response = client.get("/api/reports/occurrences?tipo=3&local=10")

    assert response.status_code == 200
    payload = response.get_json()
    assert payload["total"] == 1
    assert payload["occurrences"][0]["date"] == "2026-11-13T09:30:00"
    assert payload["occurrences"][0]["location"] == {"id": 10, "address": "Centro"}
    assert "cpf" not in payload["occurrences"][0]
