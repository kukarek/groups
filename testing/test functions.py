from bs4 import BeautifulSoup
import re
import sqlite3
import bybit
import requests
from pybit.unified_trading import HTTP
import hashlib
import hmac
import time
import asyncio

bybit = 'C:\\Users\\Dmitry\\Documents\\softforgroups\\projects\\testing\\spiski\\bybit.txt'
bitget = 'C:\\Users\\Dmitry\\Documents\\softforgroups\\projects\\testing\\spiski\\bitget.txt'
coinex = 'C:\\Users\\Dmitry\\Documents\\softforgroups\\projects\\testing\\spiski\\coinex.txt'

def extract_info(block):
    lines = block.strip().split('\n')
    name = lines[1].strip()
    
    return name
    

def func():

    with open('C:\\Users\\Dmitry\\Documents\\softforgroups\\projects\\testing\\data.txt', 'r', encoding='utf-8') as file:
         text = file.read()


    pattern = r'\b(\w+/\w+)\b'  # Шаблон для поиска строк вида "COMP/USDT"
    matches = re.findall(pattern, text)

    symbols = ""

    for match in matches:
        symbols = symbols + match.replace('/', '') + "\n" # Удаляем слэш из найденных строк

    with open('C:\\Users\\Dmitry\\Documents\\softforgroups\\projects\\testing\\complied.txt', 'w', encoding='utf-8') as file:
         file.write(symbols)

def func2():
    #создание таблицы из трех столбиков монет, каждый столбик - биржа
    #3 столбика повторяющихся названий монет, чтобы видеть в каких биржах они пересекаются

    # Чтение данных из трех файлов
    with open(bybit, 'r', encoding='utf-8') as file1, open(bitget, 'r', encoding='utf-8') as file2, open(coinex, 'r', encoding='utf-8') as file3:
         coins1 = set(file1.read().splitlines())
         coins2 = set(file2.read().splitlines())
         coins3 = set(file3.read().splitlines())

    # Находим пересечения и различия множеств монет
    common_coins = coins1 & coins2 & coins3
    coins_only_in_2 = (coins1 & coins2) - coins3
    coins_only_in_3 = (coins1 & coins3) - coins2
    coins_only_in_1 = (coins2 & coins3) - coins1

    # Создаем таблицу
    table = []

    for coin in common_coins:
        table.append((coin, coin, coin))

    for coin in coins_only_in_2:
        table.append((coin, coin, ""))

    for coin in coins_only_in_3:
        table.append((coin, "", coin))

    for coin in coins_only_in_1:
        table.append(("", coin, coin))
    
    # Вывод таблицы
    print("{:<20} {:<20} {:<20}".format("Exchange 1", "Exchange 2", "Exchange 3"))
    for row in table:
        print("{:<20} {:<20} {:<20}".format(*row))
    
    onecolumn = ""
    for row in table:
        if row[0] == "":
            if row[1] == "":
                onecolumn = onecolumn + row[2] + "\n"
            else:
                onecolumn = onecolumn + row[1] + "\n"
        else:
            onecolumn = onecolumn + row[0] + "\n"

    print(onecolumn)

    return table

def func3():
    
    #занесение списка монет в таблицу

    conn = sqlite3.connect('tokens_table.db')
    cursor = conn.cursor()

    with open('C:\\Users\\Dmitry\\Documents\\softforgroups\\projects\\testing\\1 coloumn.txt', 'r', encoding='utf-8') as file:
         data = file.read()

    list = data.split('\n')
        

    for token in list:
        cursor.execute("INSERT INTO tokens (token_name) VALUES (?)", (token,))
        conn.commit()


    conn.close()

# Замените на свои API ключи Bybit
# API_KEY = "o8q5N3zH1Q431eSpWJ"
# API_SECRET = "xNnQqDdfrK9jp3jWdFwMDycHyXq9jwT5tDnt"


def main():

    print()

if __name__ == '__main__':
    main()
