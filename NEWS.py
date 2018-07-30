# Autor: Krezub P.N.
# Чтение ленты новостей из яндекс ленты

import requests
import time
import webbrowser
import os
from random import randint
from bs4 import BeautifulSoup
import tkinter as tk
import tkinter.ttk as ttk


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
    global pb
    n=2
    pb['value']=(n)
    pb.update()
    if ppp == 35:
        url = 'https://news.yandex.ru/yandsearch?rpt=nnews2&geonews=35&grhow=clutop&rel=tm'
    else:
        url = 'https://news.yandex.ru/yandsearch?rpt=nnews2&catnews=' + str(ppp) + '&grhow=clutop&rel=tm'
    page_part = '&p='
    write_html(0, 1)
    pb['value']=(n*7)
    pb.update()

    for i in range(6):
        pb['value']=(i*10+n*7)
        pb.update()
        url_gen = url + page_part + str(i)
        html = get_html(url_gen, 1)
        get_page_data(html, url_gen)
        time.sleep(randint(3, 5))
        
    write_html(0, 3)
    pb['value']=(n*50)
    pb.update()
    file_url = 'file://' + os.getcwd() + '/NEWS.html'
    webbrowser.open(file_url, new=1)
    pb.stop()
    pb.update()


def Exit_ui():
    global root
    root.quit()


if __name__ == '__main__':
    root = tk.Tk()
    root.geometry("190x240+200+200")
    root.maxsize(190, 240)
    root.minsize(190, 240)
    root.configure(background="#333")
    root.title("Новости")

    root.style = ttk.Style()
    root.style.map("Fun.TButton",
        foreground=[('pressed', 'green'), ('active', 'blue')],
        background=[('pressed', '!disabled', 'black'), ('active', 'gray')],
        highlightcolor=[('focus', 'black'), ('!focus', 'gray')]
        )
    pb = ttk.Progressbar(root, length=100, mode='determinate')

    button1 = ttk.Button(root, text="Новости края", style='Fun.TButton', command=lambda: main(35))
    button2 = ttk.Button(root, text="Общество", style='Fun.TButton', command=lambda: main(39))
    button3 = ttk.Button(root, text="Политика", style='Fun.TButton', command=lambda: main(40))
    button4 = ttk.Button(root, text="Экономика", style='Fun.TButton', command=lambda: main(6))
    button5 = ttk.Button(root, text="В Мире", style='Fun.TButton', command=lambda: main(172))
    button10 = ttk.Button(root, text="Спорт", style='Fun.TButton', command=lambda: main(90))
    button7 = ttk.Button(root, text="Технологии", style='Fun.TButton', command=lambda: main(4))
    button8 = ttk.Button(root, text="Наука", style='Fun.TButton', command=lambda: main(44042))
    button9 = ttk.Button(root, text="Авто", style='Fun.TButton', command=lambda: main(99))
    button6 = ttk.Button(root, text="Происшествия", style='Fun.TButton', command=lambda: main(3218))
    button11 = ttk.Button(root, text="Выход", style='Fun.TButton', command=Exit_ui)

    button1.grid(row=0,column=0, sticky='we', padx=5, pady=5)
    button2.grid(row=1,column=0, sticky='we', padx=5, pady=5)
    button3.grid(row=2,column=0, sticky='we', padx=5, pady=5)
    button4.grid(row=3,column=0, sticky='we', padx=5, pady=5)
    button5.grid(row=4,column=0, sticky='we', padx=5, pady=5)
    button6.grid(row=0,column=1, sticky='we', padx=5, pady=5)
    button7.grid(row=1,column=1, sticky='we', padx=5, pady=5)
    button8.grid(row=2,column=1, sticky='we', padx=5, pady=5)
    button9.grid(row=3,column=1, sticky='we', padx=5, pady=5)
    button10.grid(row=4,column=1, sticky='we', padx=5, pady=5)
    pb.grid(row=5,column=0, columnspan=2, sticky='we', padx=5, pady=5)
    button11.grid(row=6,column=0, columnspan=2, sticky='s', pady=15)

    root.mainloop()
