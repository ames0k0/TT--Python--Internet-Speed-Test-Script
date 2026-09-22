# Скрипт-замерятель скорости интернета

> Зависимости: Python 3.12.3

```
>>> python3 main.py -h
usage: python3 main.py -[u]rl -[c]ount

options:
  -h, --help            show this help message and exit
  -u URL, --url URL     Адрес, куда стучаться
  -c {10,15,20,25,30,35,40,45,50}, --count {10,15,20,25,30,35,40,45,50}
                        Количество последовательных запросов к этому адресу

epilog: python3 main.py -u https://raw.githubusercontent.com/cat-milk/Anime-Girls-Holding-Programming-Books/refs/heads/master/Python/Tohru-Dragon_Maid_Beginning_Python.jpg -c 50
```

Пример
```
>>> python3 main.py -u https://raw.githubusercontent.com/cat-milk/Anime-Girls-Holding-Programming-Books/refs/heads/master/Python/Tohru-Dragon_Maid_Beginning_Python.jpg
Среднее время запроса: 0.15 /с
Объем скачанных данных: 23.32 /мб
Скорость: 159.42 мб/с
```
