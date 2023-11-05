import requests
from bs4 import BeautifulSoup
from urllib.parse import unquote

class Executor:

    SEARCH_KEYWORDS = []

    def generate_top_url(self):

        keywords = ""
        for word in self.SEARCH_KEYWORDS:
            keywords += f"%20{word}"

        url = f"https://vk.com/search?c[per_page]=40&c[q]={keywords}&c[section]=communities"

        return url


    def download_html(self, file_path):

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'
        }

        url = self.generate_top_url()

        response = requests.get(url, headers=headers)
        response.raise_for_status()

        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(response.text)

    def read_html(self, file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()

    def remove_before_first_group(self, html):
        start_tag = 'class="groups_row search_row clear_fix"'
        start_index = html.find(start_tag)
        if start_index != -1:
            return html[start_index:]
        else:
            return ''

    def extract_group_strings(self, html):
        soup = BeautifulSoup(html, 'html.parser')
        group_strings = []

        for group_div in soup.find_all('div', class_='groups_row search_row clear_fix'):
            group_strings.append(str(group_div))

        return group_strings



