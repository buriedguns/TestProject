from selenium.webdriver.common.by import By
from utils.constants import UI_HOST


class ProfilePage:

	def __init__(self, driver):
		self.rel_url = '/profile'
		self.host = UI_HOST
		self.driver = driver
		self.delete_button = By.CSS_SELECTOR, "button .pi-trash"

	def check_delete_button(self):
		return self.driver.find_element(*self.delete_button).is_displayed()
