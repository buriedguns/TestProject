import requests
from .models.user_models import Models


class User:

	def __init__(self, host: str):
		self.host = host
		self.models = Models()

	def get_user(self, token: str):
		"""Method for get user ID"""
		return requests.get(self.host + "/users", headers={"Authorization": "Bearer " + token})

	def register_user(self, body: Models.NewUser):
		"""Method for register new user"""
		return requests.post(self.host + "/register", json=body)

	def login(self, body: Models.LoginUser):
		return requests.post(self.host + "/login", json=body)

	def delete_user(self, user_id: str, token: str):
		return requests.delete(self.host + f"/users/{user_id}", headers={"Authorization": "Bearer " + token})
