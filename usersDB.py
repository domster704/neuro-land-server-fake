import sqlite3
import hashlib
import psycopg2
import os

class DB:
	def __init__(self):
		# self.db = sqlite3.connect('users.db', check_same_thread=False)
		self.db = psycopg2.connect('')
		self.cursor = self.db.cursor()
		self.cursor.execute('''CREATE TABLE IF NOT EXISTS users (
						id INTEGER PRIMARY KEY,
						name TEXT unique,
						password TEXT,
						content TEXT NULLABLE)''')
		self.db.commit()

	@staticmethod
	def hashPassword(password):
		"""Хеширование паролей"""
		hash_password = password.encode()
		return hashlib.md5(hash_password).hexdigest()

	def addUser(self, name, password, content=None):
		"""Добавление пользователя в базу данных"""
		hash_password = self.hashPassword(password)
		try:
			self.cursor.execute("INSERT INTO users (name,password,content) VALUES (?,?,?)", (name, hash_password, content))
		except Exception as e:
			return "Error"
		self.db.commit()
		return "True"

	def authorise(self, name, password):
		"""Вход в аккаунт, смотрим пользователя в базе данных"""
		hash_password = self.hashPassword(password)
		cur = self.cursor.execute('''SELECT password FROM users WHERE name=?''', (name,))
		try:
			if cur.fetchone()[0] == hash_password:
				return True
		except:
			print("User doesn't exist")
			return False

	def getContent(self, name, password):
		"""Получаем контент (последняя введённая ссылка пользователем + цена)"""
		hash_password = self.hashPassword(password)
		try:
			content = self.cursor.execute('''SELECT content FROM users WHERE name=? and password=?''', (name, hash_password)).fetchone()[0]
			return str(content)
		except:
			return "None"

	def changeContent(self, name, password, content):
		"""Меняем контент на новую ссылку и цену"""
		hash_password = self.hashPassword(password)
		try:
			self.cursor.execute('''UPDATE users SET content=? WHERE name=? and password=?''', (content, name, hash_password))
			self.db.commit()
			return "True"
		except:
			return "False"
