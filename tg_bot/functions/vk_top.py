import requests
from bs4 import BeautifulSoup
import os

#просто показывает место в топе обеих групп в вк

def download_html(url, file_path):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'
    }

    response = requests.get(url, headers=headers)
    response.raise_for_status()

    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(response.text)

def read_html(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

def remove_before_first_group(html):
    start_tag = 'class="groups_row search_row clear_fix"'
    start_index = html.find(start_tag)
    if start_index != -1:
        return html[start_index:]
    else:
        return ''

def extract_group_strings(html):
    soup = BeautifulSoup(html, 'html.parser')
    group_strings = []

    for group_div in soup.find_all('div', class_='groups_row search_row clear_fix'):
        group_strings.append(str(group_div))

    return group_strings


def Get_top(url, group_id):
    top = 0
    file_path = 'tg_bot/functions/html_page.html'  # Имя файла, куда будет сохранена HTML страница
    try:
        download_html(url, file_path)
        html = read_html(file_path)
        cleaned_html = remove_before_first_group(html)
        group_strings = extract_group_strings(cleaned_html)
        a = len(group_strings)
        for i in range(a):
                          
            if group_strings[i].find(group_id) != -1:
                top = i+1

    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except Exception as err:
        print(f"An error occurred: {err}")

    if os.path.exists(file_path):
        os.remove(file_path)
        
    if(top == 0):
        return 40
    else:
        return top

def main():
    print(Get_top())

if __name__ == "__main__":
    main()
