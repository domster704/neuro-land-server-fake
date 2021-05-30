import sqlite3
import hashlib
import psycopg2
import os
import pandas as pd
tableName = "users"

class DB:
	def __init__(self):
		self.db = psycopg2.connect(
			database="df566r6v13dd04",
			user="qjgdnhxmbgqdmu",
			password="d298bf18acf28cf8f83bab6f4538518131ffffbd71fcf3ff489c0dcf8b921ace",
			host="ec2-176-34-222-188.eu-west-1.compute.amazonaws.com",
			port="5432"
		)
		self.cursor = self.db.cursor()
		self.cursor.execute(f'''CREATE TABLE IF NOT EXISTS {tableName} (
						name TEXT unique,
						password TEXT,
						content TEXT NOT NULL);''')
		self.cursor.execute("ROLLBACK")
		self.db.commit()

	@staticmethod
	def hashPassword(password):
		"""Хеширование паролей"""
		hash_password = password.encode()
		return hashlib.md5(hash_password).hexdigest()

	def addUser(self, name, password, content=""):
		"""Добавление пользователя в базу данных"""
		hash_password = self.hashPassword(password)
		self.cursor.execute(f"INSERT INTO {tableName} (NAME,PASSWORD,CONTENT) VALUES (%s, %s, %s)", (name, hash_password, content))
		self.db.commit()
		return "True"

	def authorise(self, name, password):
		"""Вход в аккаунт, смотрим пользователя в базе данных"""
		hash_password = self.hashPassword(password)
		self.cursor.execute(f'''SELECT password FROM {tableName} WHERE name=%s''', (name,))
		cur = self.cursor.fetchone()[0]
		try:
			if cur == hash_password:
				return True
		except Exception as e:
			print(e)
			# print("User doesn't exist")
			return False

	def getContent(self, name, password):
		"""Получаем контент (последняя введённая ссылка пользователем + цена)"""
		hash_password = self.hashPassword(password)
		try:
			self.cursor.execute(f'''SELECT content FROM {tableName} WHERE name=%s and password=%s''', (name, hash_password))
			content = self.cursor.fetchone()[0]
			return str(content)
		except Exception as e:
			print(e)
			return "None"

	def changeContent(self, name, password, content):
		"""Меняем контент на новую ссылку и цену"""
		hash_password = self.hashPassword(password)
		try:
			self.cursor.execute(f'''UPDATE {tableName} SET content=%s WHERE name=%s and password=%s''', (content, name, hash_password))
			self.db.commit()
			return "True"
		except Exception as e:
			print(e)
			return "False"

	def printALL(self):
		self.cursor.execute("ROLLBACK")
		self.cursor.execute("SELECT * from users")
		rows = self.cursor.fetchall()
		for row in rows:
			print("name =", row[0])
			print("password =", row[1])
			print("content =", row[2], "\n")
