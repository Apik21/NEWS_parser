# Autor: Krezub P.N.
# Чтение ленты новостей из яндекс ленты

import requests
import time
import webbrowser
import os
import sys
from random import randint
from bs4 import BeautifulSoup
from PyQt5.QtCore import QCoreApplication
from PyQt5.QtWidgets import (QWidget, QPushButton, QProgressBar, QApplication, QMainWindow)
import gui

class Example(QMainWindow, gui.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.initUI()
        
    def initUI(self):
        self.pushButton_11.clicked.connect(QCoreApplication.instance().quit)
        self.pushButton.clicked.connect(lambda: main(35))
        self.pushButton_4.clicked.connect(lambda: main(39))
        self.pushButton_6.clicked.connect(lambda: main(40))
        self.pushButton_8.clicked.connect(lambda: main(6))
        self.pushButton_10.clicked.connect(lambda: main(172))
        self.pushButton_9.clicked.connect(lambda: main(90))
        self.pushButton_3.clicked.connect(lambda: main(4))
        self.pushButton_5.clicked.connect(lambda: main(44042))
        self.pushButton_7.clicked.connect(lambda: main(99))
        self.pushButton_2.clicked.connect(lambda: main(3218))


def get_html(url, hd):
    headers = [
               {'User-Agent': 'my-app/0.0.1'},
               {'User-Agent': 'my-app/0.0.2'},
               {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'}
              ]
    try:
        r = requests.get(url, headers=headers[hd])
        if r.status_code != 200:
            raise Exception("Агент заблокирован")
    except requests.ConnectionError as e:
        print("OOPS!! Ошибка подключения. Убедитесь, что вы подключены к Интернету. Технические данные, приведены ниже.\n")
        print(str(e))
    except requests.Timeout as e:
        print("OOPS!! Ошибка таймаута")
        print(str(e))
    except Exception as e:
        r = requests.get(url, headers=headers[hd-1])
    return r.text


def write_html(data, flag):
    if flag == 1:
        with open('NEWS.html', 'w', encoding='utf-8') as f:
            f.writelines(
                '<!DOCTYPE html>\n<html lang="ru">\n<head>'
                '<meta http-equiv="Content-Type" content="text/html; charset=utf-8">\n'
                '<title>Новости</title></head>\n<body>\n')
    elif flag == 2:
        with open('NEWS.html', 'a', encoding='utf-8') as f:
            f.writelines('<p><b>' + data['title'] + '</b></p><p>' + data['short_body'] +
                         '</p><a href=' + data['adr'] + ' target="_blank">Читать</a><hr>\n')
    elif flag == 3:
        with open('NEWS.html', 'a', encoding='utf-8') as f:
            f.writelines('\n</body>\n</html>')


def get_page_data(html, url):
    try:
        soup = BeautifulSoup(html, 'lxml')
        ads = soup.find('div', class_='page-content__left').find_all('li', class_='search-item')
    except AttributeError as e:
        get_html(url, 1)
        with open('NEWS.html', 'a', encoding='utf-8') as f:
            f.writelines('<p><b>Ошибка!!! User-Agent заблокирован.</b></p><p>' + str(e) + '</p>\n')
    else:
        for ad in ads:
            try:
                title = ad.find('h2', class_='document__head').text
            except:
                title = 'Заголовок не найден\n'
            try:
                adr = ad.find('h2', class_='document__head').find('a', class_='link link_theme_normal i-bem').get('href')
            except:
                adr = 'Ссылка на страницу не найдена\n'
            try:
                short_body = ad.find('div', class_='document__snippet').text
            except:
                short_body = 'Аннотация новости не найдена\n'
            data = {'title': title, 'short_body': short_body, 'adr': adr}
            write_html(data, 2)


def main(ppp):
    global form
    pb = form.progressBar
    n=2
    pb.setValue(n)
    if ppp == 35:
        url = 'https://news.yandex.ru/yandsearch?rpt=nnews2&geonews=35&grhow=clutop&rel=tm'
    else:
        url = 'https://news.yandex.ru/yandsearch?rpt=nnews2&catnews=' + str(ppp) + '&grhow=clutop&rel=tm'
    page_part = '&p='
    write_html(0, 1)
    pb.setValue(n*7)

    for i in range(6):
        pb.setValue(i*10+n*7)
        url_gen = url + page_part + str(i)
        html = get_html(url_gen, 1)
        get_page_data(html, url_gen)
        time.sleep(randint(3, 5))
        
    write_html(0, 3)
    pb.setValue(n*50)
    file_url = 'file://' + os.getcwd() + '/NEWS.html'
    webbrowser.open(file_url, new=1)
    pb.setValue(0)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    form = Example()
    form.show()
    app.exec()
