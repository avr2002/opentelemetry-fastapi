from fastapi import status
from fastapi.testclient import TestClient


def test_read_hello(client: TestClient) -> None:
    response = client.get("/hello")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"message": "Hello, World!"}


def test_httpbin(client: TestClient) -> None:
    response = client.get("/httpbin")
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["url"] == "https://httpbin.org/get"


def test_echo(client: TestClient) -> None:
    response = client.post("/echo", json={"message": "Hello, World!"})
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"message": "Hello, World!"}
