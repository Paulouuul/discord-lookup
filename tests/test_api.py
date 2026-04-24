import pytest
from fastapi.testclient import TestClient
from api.main import app

client = TestClient(app)


class TestAPI:
    """Testes para a API"""
    
    def test_health_check(self):
        """Testa endpoint /health"""
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json()["status"] == "ok"
    
    def test_get_user_success(self):
        """Testa busca de usuário com sucesso"""
        user_id = "561973026711797792"
        response = client.get(f"/users/{user_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == user_id
        assert "username" in data
    
    def test_get_user_not_found(self):
        """Testa usuário não encontrado"""
        response = client.get("/users/999999999999999999")
        assert response.status_code == 404
    
    def test_batch_success(self):
        """Testa batch com sucesso"""
        response = client.post(
            "/users/batch",
            json={"user_ids": ["561973026711797792", "563529796768759840"]}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["total"] == 2
        assert data["success_count"] == 2
    
    def test_batch_with_invalid_id(self):
        """Testa batch com ID inválido"""
        response = client.post(
            "/users/batch",
            json={"user_ids": ["invalid_id"]}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["success_count"] == 0
        assert data["error_count"] == 1
    
    def test_batch_empty_request(self):
        """Testa batch com lista vazia"""
        response = client.post("/users/batch", json={"user_ids": []})
        assert response.status_code == 200
        data = response.json()
        assert data["total"] == 0

    def test_invalid_accept_header(self):
        """Testa Accept header inválido (deve retornar JSON)"""
        response = client.get(
            "/users/561973026711797792",
            headers={"Accept": "application/invalid"}
        )
        assert response.status_code == 200
        assert response.headers["content-type"] == "application/json"