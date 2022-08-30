import requests
import datetime
import json


class VK:

    def __init__(self, access_token, user_id, version='5.131'):
       self.token = access_token
       self.id = user_id
       self.version = version
       self.params = {'access_token': self.token, 'v': self.version}

    def photos(self, owner):
       url = 'https://api.vk.com/method/photos.get'
       params = {'owner_id': owner, 'album_id': 'profile', 'count': ftl, 'photo_sizes': True, 'extended': 1}
       response = requests.get(url, params={**self.params, **params})
       return response.json()


class YandexDisk:

    def __init__(self, token):
        self.token = token

    def urlaa(self, name, url):
        upload_url = 'https://cloud-api.yandex.net/v1/disk/resources/upload'
        headers = {'Content-Type': 'aplication/json', 'Authorization': 'OAuth {}'.format(self.token)}
        params = {"path": "/" + owner + "/" + name + ".jpg", "url": url}
        response = requests.post(upload_url, headers=headers, params=params)

    def mkdir(self, dirname):
        upload_url = 'https://cloud-api.yandex.net/v1/disk/resources'
        headers = {'Content-Type': 'aplication/json', 'Authorization': 'OAuth {}'.format(self.token)}
        params = {"path": dirname}
        response = requests.put(upload_url, headers=headers, params=params)


dict = {}
list1 = []
ftl = input('Какое количество фото надо загрузить? ')
if ftl == '':
    ftl = 5
owner = input('Введите user_id пользователя ВК ')
percent = 0
user_id = ''  # user_id владельца токена ВК
YA_TOKEN = ""  # Токен Яндекса
vk_access_token = ''  # Токен ВКонтакте
ya = YandexDisk(token=YA_TOKEN)
vk = VK(vk_access_token, user_id)


a = vk.photos(owner)
fotocount = a['response']['count']  # колличествоо фоток у пациента
if fotocount > int(ftl):
    fotocount = int(ftl)
for photonumber in range(fotocount):
    timestamp = a['response']['items'][photonumber]['date']  # дата загрузки в ВК в UNIX формате
    dat = (datetime.datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d-%H-%M-%S'))
    likes = a['response']['items'][photonumber]['likes']['count']  # колличество лайков
    maxsize = len(a['response']['items'][photonumber]['sizes'])  # кол-во размеров фотографии
    url = a['response']['items'][photonumber]['sizes'][maxsize - 1]['url']  # ссылка на фотографию

    if str(likes) in dict.keys():  # формируем словарь из имен файлов и ссылки(url)
        dict[str(likes)+'-'+dat] = url
        list1.append({"filename": str(likes)+'-'+dat, "size": maxsize})
    else:
        dict[str(likes)] = url
        list1.append({"filename": str(likes), "size": maxsize})

with open('file_info.txt', 'w') as json_file:
    json.dump(list1, json_file)
ya.mkdir(str(owner))
for i in dict:
    ya.urlaa(i, dict[i])
    percent += 1
    print(str(int(100/fotocount*int(percent))), '%')  # Прогресс бар
print('Загрузка завершена, загружено ',fotocount,' фото.')
