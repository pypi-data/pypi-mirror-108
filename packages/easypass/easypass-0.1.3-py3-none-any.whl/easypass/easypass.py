import random

class Password:
	"""
	Генерация пароля
	:param int lenght: Длина пароля
	:param bool lower: Наличие нижнего регистра
	:param bool upper: Наличие верхнего регистра
	:param bool numbers: Наличие цифр
	:param bool symbols: Наличие специальных знаков
	"""
	def __init__(self, length=8, lower=True, upper=True, numbers=True, symbols=False):
		self.length = length
		self.lower = lower
		self.upper = upper
		self.numbers = numbers
		self.symbols = symbols
		if not lower and not upper and not numbers and not symbols:
			raise EasyPassError("Нужно поставить значение True хотя бы на один параметр!")
		else:
			characters = ""
			if self.lower:
				characters += "qwertyuiopasdfghjklzxcvbnm"
			if self.upper:
				characters += "QWERTYUIOPASDFGHJKLZXCVBNM"
			if self.numbers:
				characters += "1234567890"
			if self.symbols:
				characters += "+-=\\|/.,{}!@#$%^&*()`~"

			self.password = ""
			for symbol in range(self.length):
				self.password += random.choice(characters)

	"""Выводит в консоль сгенерированный пароль"""
	def print(self):
		print(self.password)

	"""
	Сохранение пароля в отдельный файл
	:param str path: Путь к файлу
	"""
	def save(self, path=None):
		self.path = path
		if self.path is None or self.path == "":
			raise EasyPassError("Ты не указал путь!")
		else:
			file = open(self.path, "w")
			file.write(self.password)
			file.close()

class Email:
	"""
	Генерация email.
	:param int length1: Длина символов до знака "@"
	:param int length2: Длина символов после знака "@"
	:param bool lower: Наличие нижнего регистра
	:param bool upper: Наличие верхнего регистра
	:param bool numbers: Наличие цифр
	:param str domain: Домен после второй части почты. Точку писать не нужно
	"""
	def __init__(self, length1=7, length2=5, lower=True, upper=True, numbers=True, domain="ru"):
		self.length1 = length1
		self.length2 = length2
		self.lower = lower
		self.upper = upper
		self.numbers = numbers
		self.domain = domain
		if not lower and not upper and not numbers:
			raise EasyPassError("Нужно поставить значение True хотя бы на один параметр!")
		else:
			characters = ""
			if self.lower:
				characters += "qwertyuiopasdfghjklzxcvbnm"
			if self.upper:
				characters += "QWERTYUIOPASDFGHJKLZXCVBNM"
			if self.numbers:
				characters += "1234567890"

			self.email = ""
			for symbol in range(self.length1):
				self.email += random.choice(characters)
			self.email += "@"
			for symbol in range(self.length2):
				self.email += random.choice(characters)
			self.email += f".{self.domain}"

	"""Выводит в консоль сгенерированную почту"""
	def print(self):
		print(self.email)

	"""
	Сохранение почты в отдельный файл
	:param str path: Путь к файлу
	"""
	def save(self, path=None):
		self.path = path
		if self.path is None or self.path == "":
			raise EasyPassError("Ты не указал путь!")
		else:
			file = open(self.path, "w")
			file.write(self.email)
			file.close()

class EasyPassError(Exception):
    def __init__(self, text):
        self.txt = text