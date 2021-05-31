# import locale
import sqlite3
import time

from flask import Flask, request
from domofond_parser import get_data_by_link
import random
from usersDB import DB

app = Flask(__name__)
city = {
	"Камчатский край": "1",
	"Марий Эл": "2",
	"Чечня": "3",
	"Оренбургская область": "4",
	"Ямало-Ненецкий АО": "5",
	"Забайкальский край": "6",
	"Ярославская область": "7",
	"Владимирская область": "8",
	"Бурятия": "9",
	"Калмыкия": "10",
	"Белгородская область": "11",
	"Вологодская область": "12",
	"Волгоградская область": "13",
	"Калужская область": "14",
	"Ингушетия": "15",
	"Кабардино-Балкария": "16",
	"Иркутская область": "17",
	"Ивановская область": "18",
	"Астраханская область": "19",
	"Карачаево-Черкесия": "20",
	"Новгородская область": "21",
	"Курганская область": "22",
	"Костромская область": "23",
	"Краснодарский край": "24",
	"Магаданская область": "25",
	"Нижегородская область": "26",
	"Кировская область": "27",
	"Липецкая область": "28",
	"Мурманская область": "29",
	"Курская область": "30",
	"Мордовия": "31",
	"Хакасия": "32",
	"Карелия": "33",
	"Якутия": "34",
	"Татарстан": "35",
	"Адыгея": "36",
	"Омская область": "37",
	"Пензенская область": "38",
	"Псковская область": "39",
	"Северная Осетия": "40",
	"Башкортостан": "41",
	"Пермский край": "42",
	"Ростовская область": "43",
	"Дагестан": "44",
	"Приморский край": "45",
	"Орловская область": "46",
	"Томская область": "47",
	"Тверская область": "48",
	"Удмуртия": "49",
	"Ставропольский край": "50",
	"Ульяновская область": "51",
	"Хабаровский край": "52",
	"Смоленская область": "53",
	"Ханты-Мансийский АО": "54",
	"Челябинская область": "55",
	"Самарская область": "56",
	"Тульская область": "57",
	"Тамбовская область": "58",
	"Тюменская область": "59",
	"Свердловская область": "60",
	"Сахалинская область": "61",
	"Рязанская область": "62",
	"Республика Алтай": "63",
	"Чувашия": "64",
	"Чукотский АО": "65",
	"Брянская область": "66",
	"Еврейская АО": "67",
	"Алтайский край": "68",
	"Калининградская область": "69",
	"Архангельская область": "70",
	"Кемеровская область": "71",
	"Амурская область": "72",
	"Воронежская область": "73",
	"Красноярский край": "74",
	"Ненецкий АО": "75",
	"Тыва": "76",
	"Коми": "77",
	"Новосибирская область": "78",
	"Саратовская область": "79",
	"Ленинградская область": "80",
	"Московская область": "81",
	"Крым": "82",
}
db = DB()

newCity = 1
# locale.setlocale(locale.LC_ALL, ('ru_Ru', 'UTF-8'))


@app.route("/register", methods=["POST", "GET"])
def reg():
	data = request.get_json(force=True)
	data = list(dict(data).values())
	name, password = data
	result = db.addUser(name, password)
	return str(result)


@app.route("/login", methods=["POST", "GET"])
def login():
	data = request.get_json(force=True)
	data = list(dict(data).values())
	print(data)
	name, password = data
	res = str(db.authorise(name, password))
	return res


@app.route("/getContent", methods=["POST", "GET"])
def getCont():
	data = request.get_json(force=True)
	data = list(dict(data).values())
	name, password = data
	return db.getContent(name, password)


@app.route("/changeContent", methods=["POST", "GET"])
def changeCont():
	data = request.get_json(force=True)
	data = list(dict(data).values())
	name, password, content = data
	return db.changeContent(name, password, content)


@app.route("/")
def xd():
	return "<h1>It's a neuroland server</h1>"


# TODO: сделать функцию get_cost_by_data
@app.route("/url", methods=["POST", "GET"])
def get_cost_by_url():
	url = request.get_json(force=True)['0']
	isAll = False
	while not isAll:
		try:
			data = get_data_by_link(url)
			isAll = True
		except Exception as e:
			time.sleep(0.01)
			print(e)
			continue

	randomValue = random.randint(0, 1)
	per = 0
	if randomValue == 0:
		per = data[2] * random.randint(900000, 999999) / 10 ** 6
	elif randomValue == 1:
		per = data[2] * random.randint(1000001, 1100000) / 10 ** 6

	data = list(map(str, data))
	# return str(locale.currency(float(per), grouping=True))
	# Экология, ЖКХ, Соседи, Транспорт
	cityReq = ""
	for i, j in city.items():
		if int(j) == float(data[-1]):
			print(str(round(per)) + ";" + data[3] + ";" + data[5] + ";" + data[6] + ";" + data[10] + ";" + i + ";" + data[0] + ";" + data[1])
			return str(round(per)) + ";" + data[3] + ";" + data[5] + ";" + data[6] + ";" + data[10] + ";" + i + ";" + data[0] + ";" + data[1]


@app.route("/data", methods=["POST", "GET"])
def get_cost_by_data():
	global newCity
	data = request.get_json(force=True)

	data = list(dict(data).values())
	data[-1] = city[data[-1]]
	data = list(map(float, data))

	newData = data[:2]
	newCity = data[-1]

	data = float(dataFromFile(myData=newData))
	randomValue = random.randint(0, 1)
	per = 0
	if randomValue == 0:
		per = data * random.randint(900000, 999999) / 10 ** 6
	elif randomValue == 1:
		per = data * random.randint(1000001, 1100000) / 10 ** 6
	# return str(locale.currency(float(per), grouping=True))
	return str(round(per))


def dataFromFile(myData=None):
	"""Берём площадь и расстояние до городаси и находим похожее в файле"""
	averageValAllCity = 128837.0837521076
	averageVal = [[100284.63630573249, 1.0],
				  [58203.713590604035, 2.0],
				  [282425.3550951849, 3.0],
				  [110334.42100515457, 4.0],
				  [176496.31166666665, 5.0],
				  [53914.357090012316, 6.0],
				  [68679.43703196345, 7.0],
				  [77401.16351744179, 8.0],
				  [51515.21932011339, 9.0],
				  [97175.57515337419, 10.0],
				  [64945.54003115266, 11.0],
				  [62143.29798087144, 12.0],
				  [101107.61060924367, 13.0],
				  [78416.60842696633, 14.0],
				  [387881.61971830984, 16.0],
				  [152134.0473964272, 17.0],
				  [78122.53947019864, 18.0],
				  [134571.91933638454, 19.0],
				  [297928.8786127167, 20.0],
				  [47486.2581289737, 21.0],
				  [30589.857666867123, 22.0],
				  [105703.33562570461, 23.0],
				  [540964.5932053601, 24.0],
				  [52732.72372881358, 25.0],
				  [114742.58231060622, 26.0],
				  [40966.09391727498, 27.0],
				  [56326.492589285685, 28.0],
				  [97194.41276595747, 29.0],
				  [57382.84108565735, 30.0],
				  [89700.37423167852, 31.0],
				  [57804.343139293225, 32.0],
				  [70029.74562500004, 33.0],
				  [247274.28125, 34.0],
				  [167362.29727761404, 35.0],
				  [146735.36594724227, 36.0],
				  [57254.27631447166, 37.0],
				  [34266.639467849214, 39.0],
				  [91210.23669201523, 41.0],
				  [88494.49071969707, 42.0],
				  [379803.05848866515, 43.0],
				  [517635.7795711058, 44.0],
				  [71302.52557585393, 48.0],
				  [72342.00591572122, 49.0],
				  [233034.5388793105, 50.0],
				  [198886.22499999998, 51.0],
				  [37922.27049455155, 53.0],
				  [109593.10617283954, 54.0],
				  [57913.50851251833, 55.0],
				  [132513.55244444456, 56.0],
				  [84597.80306748464, 57.0],
				  [96553.5811059908, 59.0],
				  [90468.32189306355, 60.0],
				  [88825.89177377897, 62.0],
				  [55873.024999999994, 66.0],
				  [96897.41585160198, 68.0],
				  [126488.32323529418, 69.0],
				  [33051.61351888669, 71.0],
				  [121385.68159468443, 73.0],
				  [67860.17822423854, 74.0],
				  [129389.83566502457, 78.0],
				  [320178.97610582865, 80.0],
				  [237478.4814919021, 81.0],
				  ]
	try:
		conn = sqlite3.connect('full.db')
		curs = conn.cursor()
		i = 1
		try:
			while True:
				allRow = list(curs.execute('''SELECT * FROM neuro WHERE id=?''', (i,)).fetchone())
				dictionary = allRow[1:3]
				if myData == dictionary:
					for j in averageVal:
						if j[1] == newCity:
							if allRow[3] + 500000 < j[0] * myData[0]:
								print(allRow[3], j[0], myData[0])
								return myData[0] * j[0]
							print(2)
							return (allRow[3] + myData[0] * j[0]) / 2
				i += 1
		except Exception as e:
			pass
			# print(e)
	except Exception as e:
		pass
		# print(e)
	print(myData[0] * averageValAllCity, 2)
	return myData[0] * averageValAllCity


# db.addUser(name="admin", password="admin", content="test")
# db.printALL()
# print(db.authorise('admin', 'admin'))
# print(db.getContent('admin', 'admin'))
# app.run(port='80', host="0.0.0.0")
