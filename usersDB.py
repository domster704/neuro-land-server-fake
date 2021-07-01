import hashlib

import psycopg2

tableName = "users"


class DB:
	def __init__(self):
		self.db = psycopg2.connect(
			database="d4oed1qeuui5rn",
			user="pgdjwlfyejamox",
			password="6a95b359dbd448d573bf8e0a9786d66fb6f99b42dd0834dc07342cb0490f6102",
			host="ec2-54-155-254-112.eu-west-1.compute.amazonaws.com",
			port="5432"
		)
		# self.db = sqlite3.connect('users.db')
		self.cursor = self.db.cursor()
		self.cursor.execute("ROLLBACK")
		self.cursor.execute(f'''CREATE TABLE IF NOT EXISTS {tableName} (
						id serial unique PRIMARY KEY,
						name TEXT,
						password TEXT,
						content TEXT NOT NULL,
						username TEXT NULL);''')
		self.db.commit()

	@staticmethod
	def hashPassword(password):
		"""Хеширование паролей"""
		hash_password = password.encode()
		return hashlib.md5(hash_password).hexdigest()

	def addUser(self, name, password, content=""):
		"""Добавление пользователя в базу данных"""
		hash_password = self.hashPassword(password)
		self.cursor.execute(f"INSERT INTO {tableName} (NAME,PASSWORD,CONTENT) VALUES (%s, %s, %s)",
							(name, hash_password, content))
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
			self.cursor.execute(f'''SELECT content FROM {tableName} WHERE name=%s and password=%s''',
								(name, hash_password))
			content = self.cursor.fetchone()[0]
			return str(content)
		except Exception as e:
			print(e)
			return "None"

	def changeContent(self, name, password, content):
		"""Меняем контент на новую ссылку и цену"""
		hash_password = self.hashPassword(password)
		try:
			self.cursor.execute(f'''UPDATE {tableName} SET content=%s WHERE name=%s and password=%s''',
								(content, name, hash_password))
			self.db.commit()
			return "True"
		except Exception as e:
			print(e)
			return "False"

	def printALL(self):
		self.cursor.execute("ROLLBACK")
		self.cursor.execute("SELECT * from users")
		rows = self.cursor.fetchall()
		print(rows)


if __name__ == '__main__':
	db = DB()
	# db.cursor.execute(f'delete from {tableName}')
	# db.db.commit()
	db.printALL()
