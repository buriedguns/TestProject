import json

import pytest
import jsonschema

from utils.constants import schemas_path


@pytest.mark.user_api_tests
class TestUserApi:

	@pytest.mark.parametrize("case, expected_status", [
		("default", 200),
		("same_email", 400),
		("no_email", 422),
		("no_password", 422),
		("no_confirm_password", 422),
		("different_passwords", 400)
	])
	def test_register_user(self, user_service, case, expected_status, same_email, clear_user):
		"""Проверяем POST /register на позитивные и негативные сценарии"""

		data = user_service.models.NewUser()
		data.gen_data()  # Создаем дефолтное тело запроса

		match case:  # Видоизменяем тело запроса, в зависимости от кейса и добавляем ожидаемый ответ для негативных сценарием
			case "same_email":
				data.email = same_email
				body = data.model_dump()
				expected_response = "Username is taken or pass issue"

			case "no_email":
				body = data.model_dump(exclude={"email"})
				expected_response = [{"loc": ["body", "email"], "msg": "field required", "type": "value_error.missing"}]

			case "no_password":
				body = data.model_dump(exclude={"password"})
				expected_response = [{"loc": ["body", "password"], "msg": "field required", "type": "value_error.missing"}]

			case "no_confirm_password":
				body = data.model_dump(exclude={"confirm_password"})
				expected_response = [{"loc": ["body", "confirm_password"], "msg": "field required", "type": "value_error.missing"}]

			case "different_passwords":
				data.confirm_password = "4321"
				body = data.model_dump()
				expected_response = "Username is taken or pass issue"

			case _:
				body = data.model_dump()
				expected_response = ""

		response = user_service.register_user(body)  # отправляем запрос
		assert response.status_code == expected_status  # проверяем статус код запроса

		if expected_status < 400:
			self.used_email = data.email
			jsonschema.validate(response.json(), json.load(open(schemas_path + "register_user.json")))  # Проверяем ответ по json схеме
			new_user = user_service.models.NewUserResponse(**response.json())  # заворачиваем ответ в модельку для удобства
			assert new_user.email == data.email  # проверяем, что в ответе тот же email, что и в запросе
			response_get_users = user_service.get_user(new_user.token)  # используем токен логина и получения данных о пользователе
			assert response_get_users.status_code == expected_status
			assert response_get_users.json() == new_user.id  # проверяем, что id в GET /users соответствует id в POST /register
			clear_user.token, clear_user.id = new_user.token, new_user.id  # передаем данные о пользователе для очистки после тестов
		else:
			assert response.json()['detail'] == expected_response
