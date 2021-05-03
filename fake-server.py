from flask import Flask, request
from domofond_parser import get_data_by_link
import random

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


@app.route("/")
def xd():
	return "<h1>It's a neuroland server</h1>"


@app.route('/test', methods=["POST", "GET"])
def doit():
	input_json = request.get_json(force=True)
	print(input_json)
	return input_json


@app.route("/")
def root():
	return "hello, it's test response"


# TODO: сделать функцию get_cost_by_data
@app.route("/url", methods=["POST", "GET"])
def get_cost_by_url():
	url = request.get_json(force=True)['data']
	data = get_data_by_link(url)
	print(data)
	randomValue = random.randint(0, 1)
	per = 0
	if randomValue == 0:
		per = data[2] * random.randint(9000000, 9999999) / 10 ** 7
	elif randomValue == 1:
		per = data[2] * random.randint(1000001, 1100000) / 10 ** 7
	return str(per)


@app.route("/data", methods=["POST", "GET"])
def get_cost_by_data():
	data = request.get_json(force=True)

	data = list(dict(data).values())
	data[-1] = 1.0
	data = list(map(float, data))

	newData = data[:2]

	data = float(dataFromFile(myData=newData))
	randomValue = random.randint(0, 1)
	per = 0
	if randomValue == 0:
		per = data * random.randint(9000000, 9999999) / 10 ** 7
	elif randomValue == 1:
		per = data * random.randint(1000001, 1100000) / 10 ** 7
	return str(per)


def dataFromFile(filename='results/obhiy', myData=None):
	isEnd = False
	myDataCopy = myData.copy()
	index = 0
	dictionary = []
	with open(f'{filename}.csv', 'r', encoding='utf-8') as f:
		# index = 0
		# while isEnd or index < 10:
		# 	if index != 0:
		# 		myData = myDataCopy[:-index]
		# 	print(myData, index)
		var = 0
		for i in f:
			index += 1
			if var == 0:
				var += 1
				continue
			# dictionary = list(map(float, [x for x in i.split(',')[:2]])) + list(map(float, [x for x in i.split(',')[3:-1]]))
			try:
				dictionary = list(map(float, [x for x in i.split(',')]))[:2]
			except Exception as e:
				exit()

			# print(myData, "  **  ", dictionary)
			if myData == dictionary:
				return i.split(',')[2]
			# if ' '.join(list(map(str, myData))) in ' '.join(list(map(str, dictionary))):
			# 	print(i)
			# 	isEnd = True
			# 	break
			# index += 1
	return random.randint(4 * 10 ** 5, 1.2 * 10 ** 6)


app.run(host="0.0.0.0", port="80")
