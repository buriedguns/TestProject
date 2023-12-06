from dataclasses import dataclass

import pytest
from selenium import webdriver

from api.user_service import User
from pages.registration_page import RegistrationPage
from pages.profile_page import ProfilePage
from utils.constants import *


@pytest.fixture(scope="session")
def user_service():
	yield User(API_HOST)


@pytest.fixture(scope="session")
def driver():
	driver = webdriver.Chrome()
	driver.implicitly_wait(IMPLICITLY_WAIT)
	driver.maximize_window()
	yield driver
	driver.quit()


@pytest.fixture(scope="session")
def pages(driver):

	@dataclass
	class Pages:
		register_page = RegistrationPage(driver)
		profile_page = ProfilePage(driver)

	yield Pages


@pytest.fixture(scope="class")
def same_email(user_service):
	"""Fixture for creating user before tests for negative scenarios with same email"""
	model = user_service.models.NewUser()
	model.gen_data()
	response = user_service.register_user(model.model_dump())
	if not response.ok:
		raise AssertionError("Can't create user before test")
	new_user_model = user_service.models.NewUserResponse(**response.json())
	yield model.email
	user_service.delete_user(new_user_model.id, new_user_model.token)


@pytest.fixture(scope="class")
def clear_user(user_service):

	@dataclass
	class Data:
		token = ""
		id = ""

	yield Data
	user_service.delete_user(Data.id, Data.token)