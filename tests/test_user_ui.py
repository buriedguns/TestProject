import pytest


@pytest.mark.user_ui_tests
class TestUserUI:

	def test_register_user(self, driver, pages, user_service, clear_user):
		"""Проверяем регистрацию пользователя"""
		register_page = pages.register_page
		profile_page = pages.profile_page

		new_user = register_page.models.NewUser()
		new_user.gen_data()
		user_login_model = register_page.models.LoginUser(email=new_user.email, password=new_user.password)

		register_page.open_page()  # открываем страницу с регистрацией
		register_page.register_user(new_user)  # вбиваем данные пользователя
		assert profile_page.check_delete_button()  # проверяем, что перешли на страницу профиля по кнопке со страницы
		assert profile_page.rel_url in profile_page.driver.current_url  # проверяем, что перешли на страницу профиля по URL

		response = user_service.login(user_login_model.model_dump())
		assert response.ok  # проверяем, что можем залогиниться за нового пользователя
		new_user_model = user_service.models.NewUserResponse(**response.json())
		clear_user.id, clear_user.token = new_user_model.id, new_user_model.token  # передаем данные о пользователе для их удаления
