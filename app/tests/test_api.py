import asyncio
from fastapi.testclient import TestClient


from app.main import app
from app.crud import visits as crud_visits


def login(email: str, password: str):
    request_data = {
        "email": email,
        "password": password
    }
    with TestClient(app) as client:
        response = client.post("/app/api/v1/login", data=request_data,
                               headers={"User-Agent": "user-agent"})
    return response


def test_create_url(temp_db):
    test_url = "https://google.com"
    request_data = {"original_url": test_url}

    with TestClient(app) as client:
        response = client.post("/app/api/v1/create-url", json=request_data)
    assert response.json()["hash"] is not None
    assert response.json()["original_url"] == test_url
    assert response.json()["creation_date"] is not None
    assert response.json()["expiration_date"] is not None


def test_register_user(temp_db):
    email = "user1@example.com"
    first_name = "user1first"
    last_name = "user1last"

    request_data = {
        "email": email,
        "first_name": first_name,
        "last_name": last_name,
        "password": "qweRTY123$"
    }

    with TestClient(app) as client:
        response = client.post("/app/api/v1/register", json=request_data,
                               headers={"User-Agent": "user-agent"})

    assert response.status_code == 201
    assert response.json()["email"] == email
    assert response.json()["first_name"] == first_name
    assert response.json()["last_name"] == last_name


def test_login_user(temp_db):
    email = "user1@example.com"
    password = "qweRTY123$"

    response = login(email, password)

    assert response.status_code == 200
    assert response.json()["access_token"] is not None
    assert response.json()["refresh_token"] is not None


def test_login_user_with_invalid_password(temp_db):
    email = "user1@example.com"
    password = "QWErty321$"

    response = login(email, password)

    assert response.status_code == 400
    assert response.json()["detail"] == "Incorrect email or password"


def test_get_user(temp_db):

    email = "user1@example.com"
    password = "qweRTY123$"

    access_token = login(email, password).json()["access_token"]
    token = f"Bearer {access_token}"

    with TestClient(app) as client:
        response = client.get("/app/api/v1/user",
                              headers={"Authorization": token})

    assert response.status_code == 200
    assert response.json()["user_id"] is not None


def test_change_password(temp_db):

    email = "user1@example.com"
    password = "qweRTY123$"

    response = login(email, password)

    access_token = response.json()["access_token"]
    token = f"Bearer {access_token}"
    new_password = "QWErty123$"
    request_data = {"password": new_password}
    with TestClient(app) as client:
        response = client.post("/app/api/v1/change-password",
                               json=request_data,
                               headers={"Authorization": token})
    assert response.status_code == 200

    response = login(email, new_password)

    assert response.json()["access_token"] is not None
    assert response.json()["refresh_token"] is not None


def test_refresh_jwt_token(temp_db):

    email = "user1@example.com"
    password = "QWErty123$"

    def login(email: str, password: str):
        request_data = {
            "email": email,
            "password": password
        }
        with TestClient(app) as client:
            response = client.post("/app/api/v1/login", data=request_data,
                                   headers={"User-Agent": "user-agent"})
        return response

    refresh_token = login(email, password).json()["refresh_token"]
    print(refresh_token)
    request_data = {"refresh_token": refresh_token}
    print(request_data)
    with TestClient(app) as client:
        response = client.post("/app/api/v1/refresh-token", data=request_data,
                               headers={"User-Agent": "user-agent"})
    print(response.json())
    assert response.json()["access_token"] is not None
    assert response.json()["refresh_token"] is not None


def test_create_user_url(temp_db):
    email = "user1@example.com"
    password = "QWErty123$"
    test_url = "https://yandex.ru"
    access_token = login(email, password).json()["access_token"]
    token = f"Bearer {access_token}"

    request_data = {"original_url": test_url}

    with TestClient(app) as client:
        response = client.post("/app/api/v1/create-user-url",
                               json=request_data,
                               headers={"Authorization": token})
    assert response.status_code == 201
    assert response.json()["hash"] is not None
    assert response.json()["original_url"] == test_url
    assert response.json()["creation_date"] is not None
    assert response.json()["expiration_date"] is not None


def test_get_user_urls(temp_db):
    email = "user1@example.com"
    password = "QWErty123$"

    access_token = login(email, password).json()["access_token"]
    token = f"Bearer {access_token}"

    with TestClient(app) as client:
        loop = asyncio.get_event_loop()
        loop.run_until_complete(crud_visits.create_visit(2, "test", "test"))
        response = client.get("/app/api/v1/user-urls",
                              headers={"Authorization": token})
    print(response.json())
    assert response.status_code == 200
    assert response.json()["urls"][0]["visits_count"] == 1
