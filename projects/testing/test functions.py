from bs4 import BeautifulSoup
import re
import sqlite3

bybit = 'C:\\Users\\Dmitry\\Documents\\softforgroups\\projects\\testing\\spiski\\bybit.txt'
bitget = 'C:\\Users\\Dmitry\\Documents\\softforgroups\\projects\\testing\\spiski\\bitget.txt'
coinex = 'C:\\Users\\Dmitry\\Documents\\softforgroups\\projects\\testing\\spiski\\coinex.txt'

def extract_info(block):
    lines = block.strip().split('\n')
    name = lines[1].strip()
    
    return name


def func():
    # Чтение данных из файла
    with open('C:\\Users\\Dmitry\\Documents\\softforgroups\\projects\\testing\\data.txt', 'r', encoding='utf-8') as file:
         data = file.read()

    blocks = re.split(r'\n\d+\n', data)
    # Удаление пустых элементов и первого элемента (пустой)
    blocks = list(filter(lambda x: x.strip() != '', blocks))[1:]

    # Извлечение данных из каждого блока
    coin_info = [extract_info(block) for block in blocks]
    
    names = ""
    # Вывод информации о монетах с парой к USDT
    for name in coin_info:
        names = names + name + '\n'

    with open('C:\\Users\\Dmitry\\Documents\\softforgroups\\projects\\testing\\complied.txt', 'w', encoding='utf-8') as file:
         file.write(names)

def func2():
    
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
    
    return table

def main():
    
    conn = sqlite3.connect('tokens_table.db')
    cursor = conn.cursor()

    with open('C:\\Users\\Dmitry\\Documents\\softforgroups\\projects\\testing\\1 coloumn.txt', 'r', encoding='utf-8') as file:
         data = file.read()

    list = data.split('\n')
        

    for token in list:
        cursor.execute("INSERT INTO tokens (token_name) VALUES (?)", (token,))
        conn.commit()


    conn.close()

    print()

if __name__ == '__main__':
    main()
