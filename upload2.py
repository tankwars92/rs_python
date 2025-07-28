#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import os
import sys
import time
from urllib.parse import urljoin, urlparse
import argparse

class RetroShowUploader:
    def __init__(self, base_url="http://retroshow.hoho.ws"):
        self.base_url = base_url.rstrip('/')
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        
    def login(self, username, password):
        print(f"Авторизация пользователя: {username}")
        
        login_url = urljoin(self.base_url, "login.php")
        login_data = {
            'login': username,
            'pass': password,
            'action_login': 'Войти'
        }
        
        try:
            response = self.session.post(login_url, data=login_data, allow_redirects=False)
            
            if response.status_code == 302 and 'index.php' in response.headers.get('Location', ''):
                print("Авторизация успешна!")
                return True
            else:
                print("Ошибка авторизации. Проверьте логин и пароль.")
                return False
                
        except Exception as e:
            print(f"❌ Ошибка при авторизации: {e}")
            return False
    
    def upload_video(self, title, description, video_file_path, is_private=False):
        if not os.path.exists(video_file_path):
            print(f"❌ Файл не найден: {video_file_path}")
            return False
            
        print(f"Загрузка видео: {title}")
        print(f"Файл: {video_file_path}")
        
        print("Шаг 1: Отправка метаданных...")
        step1_url = urljoin(self.base_url, "upload.php?p=1")
        step1_data = {
            'title': title,
            'description': description
        }
        
        try:
            response = self.session.post(step1_url, data=step1_data)
            if response.status_code != 200:
                print(f"❌ Ошибка на шаге 1: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"Ошибка на шаге 1: {e}")
            return False
        
        print("Шаг 2: Загрузка файла...")
        step2_url = urljoin(self.base_url, "upload.php?p=2")
        
        with open(video_file_path, 'rb') as f:
            files = {
                'video': (os.path.basename(video_file_path), f, 'video/mp4')
            }
            
            data = {
                'title': title,
                'description': description,
                'broadcast': 'private' if is_private else 'public'
            }
            
            try:
                print("Загрузка файла (это может занять несколько минут)...")
                response = self.session.post(step2_url, data=data, files=files)
                
                if response.status_code == 200:
                    if "Видео успешно загружено" in response.text:
                        print("Видео успешно загружено!")
                        return True
                    else:
                        print("Ошибка при загрузке видео")

                        if "error" in response.text.lower():
                            print("Детали ошибки:")
                            print(response.text[:500] + "..." if len(response.text) > 500 else response.text)
                        return False
                else:
                    print(f"Ошибка HTTP: {response.status_code}")
                    return False
                    
            except Exception as e:
                print(f"Ошибка при загрузке файла: {e}")
                return False
    
    def upload_video_simple(self, title, description, video_file_path, is_private=False):
        if not os.path.exists(video_file_path):
            print(f"Файл не найден: {video_file_path}")
            return False
            
        print(f"Загрузка видео: {title}")
        print(f"Файл: {video_file_path}")
        
        upload_url = urljoin(self.base_url, "upload.php?p=2")
        
        with open(video_file_path, 'rb') as f:
            files = {
                'video': (os.path.basename(video_file_path), f, 'video/mp4')
            }
            
            data = {
                'title': title,
                'description': description,
                'broadcast': 'private' if is_private else 'public'
            }
            
            try:
                print("Загрузка файла (это может занять несколько минут)...")
                response = self.session.post(upload_url, data=data, files=files)
                
                if response.status_code == 200:
                    if "Видео успешно загружено" in response.text:
                        print("Видео успешно загружено!")
                        return True
                    else:
                        print("Ошибка при загрузке видео")
                        return False
                else:
                    print(f"Ошибка HTTP: {response.status_code}")
                    return False
                    
            except Exception as e:
                print(f"Ошибка при загрузке файла: {e}")
                return False

def main():
    parser = argparse.ArgumentParser(description='RetroShow Video Upload Script')
    parser.add_argument('--url', default='http://retroshow.hoho.ws', help='Базовый URL сайта (по умолчанию: http://retroshow.hoho.ws)')
    parser.add_argument('--username', required=True, help='Имя пользователя')
    parser.add_argument('--password', required=True, help='Пароль')
    parser.add_argument('--title', required=True, help='Название видео')
    parser.add_argument('--description', default='', help='Описание видео')
    parser.add_argument('--file', required=True, help='Путь к файлу видео')
    parser.add_argument('--private', action='store_true', help='Сделать видео приватным')
    parser.add_argument('--simple', action='store_true', help='Использовать упрощенную загрузку')
    
    args = parser.parse_args()
    
    if not os.path.exists(args.file):
        print(f"Файл не найден: {args.file}")
        sys.exit(1)
    к
    uploader = RetroShowUploader(args.url)
    
    if not uploader.login(args.username, args.password):
        print("Не удалось авторизоваться. Проверьте логин и пароль.")
        sys.exit(1)
    
    if args.simple:
        success = uploader.upload_video_simple(args.title, args.description, args.file, args.private)
    else:
        success = uploader.upload_video(args.title, args.description, args.file, args.private)
    
    if success:
        print("Загрузка завершена успешно!")
        sys.exit(0)
    else:
        print("Загрузка не удалась!")
        sys.exit(1)

if __name__ == "__main__":
    main() 
