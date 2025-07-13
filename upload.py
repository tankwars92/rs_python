import requests
import argparse
import os
import sys

parser = argparse.ArgumentParser(description="Загрузка видео на RetroShow")
parser.add_argument('--server', required=True, help='Адрес сервера, например: http://retroshow.hoho.ws')
parser.add_argument('--login', required=True, help='Имя пользователя')
parser.add_argument('--password', required=True, help='Пароль пользователя')
parser.add_argument('--video', required=True, help='Путь к видеофайлу')
parser.add_argument('--preview', help='Путь к превью (необязательно)')
parser.add_argument('--title', required=True, help='Название видео')
parser.add_argument('--description', default='', help='Описание видео')

args = parser.parse_args()

if not os.path.isfile(args.video):
    print(f"Видео файл не найден: {args.video}")
    sys.exit(1)

if args.preview and not os.path.isfile(args.preview):
    print(f"Превью файл не найден: {args.preview}")
    sys.exit(1)

BASE_URL = args.server.rstrip('/')
LOGIN_URL = BASE_URL + "/login.php"
UPLOAD_URL = BASE_URL + "/upload.php"

session = requests.Session()

login_data = {
    'login': args.login,
    'pass': args.password
}

print("Входим...")
r = session.post(LOGIN_URL, data=login_data)
if 'Мой канал' not in r.text:
    print("Вход не удался.")
    sys.exit(1)

print("Вход выполнен.")

files = {
    'video': (os.path.basename(args.video), open(args.video, 'rb'), 'video/mp4')
}

if args.preview:
    files['preview'] = (os.path.basename(args.preview), open(args.preview, 'rb'), 'image/jpeg')

data = {
    'title': args.title,
    'description': args.description
}

print("Загружаем видео...")
response = session.post(UPLOAD_URL, data=data, files=files)

files['video'][1].close()
if 'preview' in files:
    files['preview'][1].close()

if "успешно загружено" in response.text.lower():
    print("Видео успешно загружено.")
else:
    print("Видео не загружено.")
    print(response.text)
