import pytest
import requests
from faker import Faker
from constants import HEADERS, BASE_URL

faker = Faker()

@pytest.fixture(scope="session")
def auth_session():
    session = requests.Session()
    session.headers.update(HEADERS)

    response = requests.post(
        f"{BASE_URL}/auth",
        headers=HEADERS,
        json={"username": "admin", "password": "password123"}
    )
    assert response.status_code == 200, "Ошибка авторизации"
    token = response.json().get("token")
    assert token is not None, "В ответе не оказалось токена"

    session.headers.update({"Cookie": f"token={token}"})
    return session

@pytest.fixture
def booking_data():
    return {
        "firstname": faker.first_name(),
        "lastname": faker.last_name(),
        "totalprice": faker.random_int(min=100, max=100000),
        "depositpaid": True,
        "bookingdates": {
            "checkin": "2024-04-05",
            "checkout": "2024-04-08"
        },
        "additionalneeds": "Cigars"
    }

@pytest.fixture
def new_booking_data():
    return {
        "firstname": faker.first_name(),
        "lastname": faker.last_name(),
        "totalprice": faker.random_int(min=100, max=100000),
        "depositpaid": False,
        "bookingdates": {
            "checkin": "2025-04-05",
            "checkout": "2025-04-08"
        },
        "additionalneeds": faker.word()
    }

@pytest.fixture
def patch_booking_data():
    return {
        "firstname": faker.first_name(),
        "additionalneeds": faker.word()
    }



#Написал нейросетью, для уменьшения объема тестов
@pytest.fixture
def create_booking(auth_session, booking_data):
    """Фикстура для создания бронирования и возврата его ID."""
    response = auth_session.post(f"{BASE_URL}/booking", json=booking_data)
    assert response.status_code == 200, "Ошибка при создании брони"
    booking_id = response.json().get("bookingid")
    assert booking_id is not None, "Идентификатор брони не найден"
    yield booking_id  # Возвращаем ID и продолжаем выполнение теста

    # После теста автоматически удаляем бронирование (финализатор)
    delete_response = auth_session.delete(f"{BASE_URL}/booking/{booking_id}")
    assert delete_response.status_code == 201, "Бронь не удалилась"

    response = auth_session.get(f"{BASE_URL}/booking/{booking_id}")
    assert response.status_code == 404, "Бронь не удалилась"


@pytest.fixture
def get_booking(auth_session, create_booking):
    """Фикстура для получения данных бронирования."""
    booking_id = create_booking
    response = auth_session.get(f"{BASE_URL}/booking/{booking_id}")
    assert response.status_code == 200, "Бронь не найдена"
    return response.json()  # Возвращаем данные брони

#Для негативных проверок

@pytest.fixture
def broken_booking_data1():
    return {
        "firstname": '',
    }

@pytest.fixture
def broken_booking_data2():
    return {
        "totalprice": faker.word(),
    }