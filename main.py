import sys
from io import BytesIO
# Этот класс поможет нам сделать картинку из потока байт

import requests
from PIL import Image

adress =  'Москва, ул. Ак. Королева, 12'
apteka = 'аптека'

# Пусть наше приложение предполагает запуск:
# python search.py Москва, ул. Ак. Королева, 12
# Тогда запрос к геокодеру формируется следующим образом:
#toponym_to_find = " ".join(sys.argv[1:])

geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"

geocoder_params = {
    "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
    "geocode": adress,
    "format": "json"}

response = requests.get(geocoder_api_server, params=geocoder_params)

if not response:
    # обработка ошибочной ситуации
    pass

# Преобразуем ответ в json-объект
json_response = response.json()
# Получаем первый топоним из ответа геокодера.
toponym = json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
# Координаты центра топонима:
toponym_coodrinates = toponym["Point"]["pos"]
# Долгота и широта:
toponym_longitude, toponym_lattitude = toponym_coodrinates.split(" ")

search_api_server = "https://search-maps.yandex.ru/v1/"
api_key = "dda3ddba-c9ea-4ead-9010-f43fbc15c6e3"

address_ll = f"{toponym_longitude},{toponym_lattitude}"

search_params = {
    "apikey": api_key,
    "text": "аптека",
    "lang": "ru_RU",
    "ll": address_ll,
    "type": "biz"
}

response1 = requests.get(search_api_server, params=search_params)
if not response1:
    #...
    pass
json_response1 = response1.json()

# Получаем первую найденную организацию.
organization = json_response1["features"][1]
# Название организации.
org_name = organization["properties"]["CompanyMetaData"]["name"]
# Адрес организации.
org_address = organization["properties"]["CompanyMetaData"]["address"]

# Получаем координаты ответа.
point1 = organization["geometry"]["coordinates"]
print(point1)
org_point = "{0},{1}".format(point1[0], point1[1])
delta = "0.005"




def spn():
    coords_l = toponym["boundedBy"]["Envelope"]["lowerCorner"].split()
    coords_r = toponym["boundedBy"]["Envelope"]["upperCorner"].split()
    delta = abs((float(coords_l[0]) - float(coords_r[0])) / 1.7)
    delta1 = abs((float(coords_l[1]) - float(coords_r[1])) / 1.7)
    return delta, delta1

delta = spn()


# Собираем параметры для запроса к StaticMapsAPI:
map_params = {
 #   "ll": ",".join([str(point1[0]), str(point1[1])]),
   # "spn": ",".join([str(delta[0]), str(delta[1])]),
    "l": "map",
    "pt": f"{toponym_longitude},{toponym_lattitude},pm2rdm~{org_point},pm2dgl"
}

map_api_server = "http://static-maps.yandex.ru/1.x/"
# ... и выполняем запрос
response = requests.get(map_api_server, params=map_params)

print(response.url)

Image.open(BytesIO(
    response.content)).show()
# Создадим картинку
# и тут же ее покажем встроенным просмотрщиком операционной системы
