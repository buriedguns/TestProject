from selenium.webdriver.common.by import By
from api.models.user_models import Models
from utils.constants import UI_HOST


class RegistrationPage:

	def __init__(self, driver):
		self.rel_url = '/register'
		self.host = UI_HOST
		self.driver = driver
		self.login_input = By.CSS_SELECTOR, "input#login"
		self.password_input = By.CSS_SELECTOR, "#password input[type=password]"
		self.confirm_password_input = By.CSS_SELECTOR, "#confirm_password input[type=password]"
		self.submit_button = By.CSS_SELECTOR, "button[type='submit']"
		self.models = Models()

	def open_page(self):
		self.driver.get(self.host + self.rel_url)

	def register_user(self, user_model: Models.NewUser):
		self.driver.find_element(*self.login_input).send_keys(user_model.email)
		self.driver.find_element(*self.password_input).send_keys(user_model.password)
		self.driver.find_element(*self.confirm_password_input).send_keys(user_model.confirm_password)
		self.driver.execute_script(f"""document.querySelector("{self.submit_button[1]}").click()""")
