import pytest
from constants import BASE_URL
import random
import requests

class TestBookings:
    def test_create_booking(self, auth_session, booking_data):
        # Создаём бронирование
        create_booking = auth_session.post(f"{BASE_URL}/booking", json=booking_data)
        assert create_booking.status_code == 200, "Ошибка при создании брони"

        booking_id = create_booking.json().get("bookingid")
        assert booking_id is not None, "Идентификатор брони не найден в ответе"
        assert create_booking.json()["booking"]["firstname"] == booking_data["firstname"], "Заданное имя не совпадает"
        assert create_booking.json()["booking"]["totalprice"] == booking_data["totalprice"], "Заданная стоимость не совпадает"

        # Проверяем, что бронирование можно получить по ID
        get_booking = auth_session.get(f"{BASE_URL}/booking/{booking_id}")
        assert get_booking.status_code == 200, "Бронь не найдена"
        assert get_booking.json()["lastname"] == booking_data["lastname"], "Заданная фамилия не совпадает"

        # Удаляем бронирование
        deleted_booking = auth_session.delete(f"{BASE_URL}/booking/{booking_id}")
        assert deleted_booking.status_code == 201, "Бронь не удалилась"

        # Проверяем, что бронирование больше недоступно
        get_booking = auth_session.get(f"{BASE_URL}/booking/{booking_id}")
        assert get_booking.status_code == 404, "Бронь не удалилась"

#PATCH
    def test_change_booking(self, auth_session, booking_data, new_booking_data):
        create_booking = auth_session.post(f"{BASE_URL}/booking", json=booking_data)
        assert create_booking.status_code == 200, "Ошибка при создании брони"

        booking_id = create_booking.json().get("bookingid")
        assert booking_id is not None, "Идентификатор брони не найден в ответе"
        assert create_booking.json()["booking"]["firstname"] == booking_data["firstname"], "Заданное имя не совпадает"
        assert create_booking.json()["booking"]["totalprice"] == booking_data[
            "totalprice"], "Заданная стоимость не совпадает"

        get_booking = auth_session.get(f"{BASE_URL}/booking/{booking_id}")
        assert get_booking.status_code == 200, "Бронь не найдена"
        assert get_booking.json()["lastname"] == booking_data["lastname"], "Заданная фамилия не совпадает"

        change_booking = auth_session.put(f"{BASE_URL}/booking/{booking_id}", json=new_booking_data)
        assert change_booking.status_code == 200, "Ошибка при изменении брони"

        get_booking = auth_session.get(f"{BASE_URL}/booking/{booking_id}")
        assert get_booking.status_code == 200, "Бронь не найдена"
        # assert change_booking.json() != create_booking.json(), "JSON при бронировании, и его изменении - идентичны"
        assert get_booking.json()["lastname"] != booking_data["lastname"], "Заданная фамилия совпадает"
        assert get_booking.json()["firstname"] != booking_data["firstname"], "Заданное имя совпадает"
        assert get_booking.json()["totalprice"] != booking_data["totalprice"], "Заданная стоимость совпадает"
        assert get_booking.json()["depositpaid"] != booking_data["depositpaid"], "Заданная депозит совпадает"
        assert get_booking.json()["bookingdates"] != booking_data["bookingdates"], "Заданные даты совпадают"
        assert get_booking.json()["additionalneeds"] != booking_data["additionalneeds"], "Заданные допы совпадают"

        # Удаляем бронирование
        deleted_booking = auth_session.delete(f"{BASE_URL}/booking/{booking_id}")
        assert deleted_booking.status_code == 201, "Бронь не удалилась"

        # Проверяем, что бронирование больше недоступно
        get_booking = auth_session.get(f"{BASE_URL}/booking/{booking_id}")
        assert get_booking.status_code == 404, "Бронь не удалилась"

#PUT
    def test_something_change_booking(self, auth_session, booking_data, patch_booking_data):
        create_booking = auth_session.post(f"{BASE_URL}/booking", json=booking_data)
        assert create_booking.status_code == 200, "Ошибка при создании брони"

        booking_id = create_booking.json().get("bookingid")
        assert booking_id is not None, "Идентификатор брони не найден в ответе"
        assert create_booking.json()["booking"]["firstname"] == booking_data["firstname"], "Заданное имя не совпадает"
        assert create_booking.json()["booking"]["totalprice"] == booking_data[
            "totalprice"], "Заданная стоимость не совпадает"

        get_booking = auth_session.get(f"{BASE_URL}/booking/{booking_id}")
        assert get_booking.status_code == 200, "Бронь не найдена"
        assert get_booking.json()["lastname"] == booking_data["lastname"], "Заданная фамилия не совпадает"

        change_booking = auth_session.patch(f"{BASE_URL}/booking/{booking_id}", json=patch_booking_data)
        assert change_booking.status_code == 200, "Ошибка при изменении брони"

        get_booking = auth_session.get(f"{BASE_URL}/booking/{booking_id}")
        assert get_booking.status_code == 200, "Бронь не найдена"
        # assert change_booking.json() != create_booking.json(), "JSON при бронировании, и его изменении - идентичны"
        assert get_booking.json()["lastname"] == booking_data["lastname"], "Заданная фамилия НЕ совпадает(в patch не обновляли)"
        assert get_booking.json()["firstname"] != booking_data["firstname"], "Заданное имя совпадает"
        assert get_booking.json()["totalprice"] == booking_data["totalprice"], "Заданная стоимость НЕ совпадает(в patch не обновляли)"
        assert get_booking.json()["depositpaid"] == booking_data["depositpaid"], "Заданная депозит НЕ совпадает(в patch не обновляли)"
        assert get_booking.json()["bookingdates"] == booking_data["bookingdates"], "Заданные даты НЕ совпадают(в patch не обновляли)"
        assert get_booking.json()["additionalneeds"] != booking_data["additionalneeds"], "Заданные допы совпадают"

        # Удаляем бронирование
        deleted_booking = auth_session.delete(f"{BASE_URL}/booking/{booking_id}")
        assert deleted_booking.status_code == 201, "Бронь не удалилась"

        # Проверяем, что бронирование больше недоступно
        get_booking = auth_session.get(f"{BASE_URL}/booking/{booking_id}")
        assert get_booking.status_code == 404, "Бронь не удалилась"

#Негативные тесты

    # firstname = '' (Fail)
    def test_negative1(self, auth_session, booking_data, create_booking, get_booking, broken_booking_data1):
        #Бронирование сделано в фикстуре create_booking, получили id бронирования
        new_booking = get_booking #Сохраняем в переменной new_booking json с бронью
        assert new_booking["lastname"] == booking_data["lastname"], "Заданное фамилия не совпадает"
        assert new_booking["firstname"] == booking_data["firstname"], "Заданное имя не совпадает"
        assert new_booking["totalprice"] == booking_data["totalprice"], "Заданная стоимость не совпадает"
        assert new_booking["depositpaid"] == booking_data["depositpaid"], "Депозит не совпадает"
        assert new_booking["bookingdates"] == booking_data["bookingdates"], "Заданные даты не совпадает"
        assert new_booking["additionalneeds"] == booking_data["additionalneeds"], "Заданные допы не совпадают"

        booking_id = create_booking # Получаем id бронирования
        change_response = auth_session.patch(f'{BASE_URL}/booking/{booking_id}', json=broken_booking_data1) #Патчим бронирование не валидными данными
        data = change_response.json()
        assert change_response.status_code == 400

        get_booking = auth_session.get(f"{BASE_URL}/booking/{booking_id}")
        # assert new_booking == get_booking.json()
        assert new_booking['firstname'] == get_booking.json()['firstname']

#totalprice = str (Fail)
    def test_negative2(self, auth_session, booking_data, create_booking, get_booking, broken_booking_data2):
        #Бронирование сделано в фикстуре create_booking, получили id бронирования
        new_booking = get_booking #Сохраняем в переменной new_booking json с бронью
        assert new_booking["lastname"] == booking_data["lastname"], "Заданное фамилия не совпадает"
        assert new_booking["firstname"] == booking_data["firstname"], "Заданное имя не совпадает"
        assert new_booking["totalprice"] == booking_data["totalprice"], "Заданная стоимость не совпадает"
        assert new_booking["depositpaid"] == booking_data["depositpaid"], "Депозит не совпадает"
        assert new_booking["bookingdates"] == booking_data["bookingdates"], "Заданные даты не совпадает"
        assert new_booking["additionalneeds"] == booking_data["additionalneeds"], "Заданные допы не совпадают"

        booking_id = create_booking # Получаем id бронирования
        change_response = auth_session.patch(f'{BASE_URL}/booking/{booking_id}', json=broken_booking_data2)
        #Патчим бронирование не валидными данными
        data = change_response.json()
        assert change_response.status_code == 400

        get_booking = auth_session.get(f"{BASE_URL}/booking/{booking_id}")
        # assert new_booking == get_booking.json()
        assert new_booking['totalprice'] == get_booking.json()['totalprice']

#booking_id = random_number (?)
    def test_negative3(self, auth_session, booking_data, create_booking, get_booking):
        #Бронирование сделано в фикстуре create_booking, получили id бронирования
        random_id = (10000, 100000)
        num1 = 0
        num2 = 10

        while num1 < num2:
            random_id = random.randint(*random_id)
            get_booking = auth_session.get(f"{BASE_URL}/booking/{random_id}")
            if get_booking.status_code == 200:
                num1 += 1
            else:
                change_response = auth_session.patch(f'{BASE_URL}/booking/{random_id}', json=booking_data)
                # Пытаемся изменить несуществующий, рандомный id (get - 404 (+), patch - 405?)
                assert change_response.status_code == 404

# Удаление без авторизации (PASS)
    def test_negative4(self, auth_session, booking_data, create_booking, get_booking):
        #Бронирование сделано в фикстуре create_booking, получили id бронирования
        new_booking = get_booking #Сохраняем в переменной new_booking json с бронью
        assert new_booking["lastname"] == booking_data["lastname"], "Заданное фамилия не совпадает"
        assert new_booking["firstname"] == booking_data["firstname"], "Заданное имя не совпадает"
        assert new_booking["totalprice"] == booking_data["totalprice"], "Заданная стоимость не совпадает"
        assert new_booking["depositpaid"] == booking_data["depositpaid"], "Депозит не совпадает"
        assert new_booking["bookingdates"] == booking_data["bookingdates"], "Заданные даты не совпадает"
        assert new_booking["additionalneeds"] == booking_data["additionalneeds"], "Заданные допы не совпадают"

        booking_id = create_booking # Получаем id бронирования
        del_response = requests.delete(f'{BASE_URL}/booking/{booking_id}')
        #Удаляем бронирование без авторизации
        assert del_response.status_code == 403

        get_booking = auth_session.get(f"{BASE_URL}/booking/{booking_id}")
        assert get_booking.status_code != 404, "Бронь удалилась"

#Empty data (PASS)
    def test_negative5(self, auth_session, booking_data, create_booking, get_booking):
        #Бронирование сделано в фикстуре create_booking, получили id бронирования
        new_booking = get_booking #Сохраняем в переменной new_booking json с бронью
        assert new_booking["lastname"] == booking_data["lastname"], "Заданное фамилия не совпадает"
        assert new_booking["firstname"] == booking_data["firstname"], "Заданное имя не совпадает"
        assert new_booking["totalprice"] == booking_data["totalprice"], "Заданная стоимость не совпадает"
        assert new_booking["depositpaid"] == booking_data["depositpaid"], "Депозит не совпадает"
        assert new_booking["bookingdates"] == booking_data["bookingdates"], "Заданные даты не совпадает"
        assert new_booking["additionalneeds"] == booking_data["additionalneeds"], "Заданные допы не совпадают"

        empty_data = ''
        booking_id = create_booking # Получаем id бронирования
        change_response = auth_session.patch(f'{BASE_URL}/booking/{booking_id}', json=empty_data)
        #Патчим json пустыми данными
        assert change_response.status_code == 400

        # get_booking = auth_session.get(f"{BASE_URL}/booking/{booking_id}")
        # assert new_booking == get_booking.json()