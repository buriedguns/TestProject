from typing import Any

from faker import Faker
from pydantic import BaseModel

f = Faker()


class Models:

	class NewUser(BaseModel):
		email: Any = ""
		password: Any = ""
		confirm_password: Any = ""

		def gen_data(self):
			self.email = f.email()
			self.password = 1234
			self.confirm_password = 1234

	class NewUserResponse(BaseModel):
		token: str
		email: str
		id: int

	class LoginUser(BaseModel):
		email: Any = ""
		password: Any = ""
