import requests
from bs4 import BeautifulSoup
import csv
import re
import time

def extract_letter_counts_from_html(html):
    """
    Извлекает количество животных по каждой русской букве из HTML-контента страницы Википедии.
    """
    soup = BeautifulSoup(html, 'html.parser')
    animals = {}
    for group in soup.select('#mw-pages .mw-category-group'):
        letter_tag = group.find('h3')
        if not letter_tag:
            continue
        letter = letter_tag.text.strip()
        if not re.match(r'^[А-ЯЁ]$', letter):
            continue
        count = len(group.select('li'))
        animals[letter] = animals.get(letter, 0) + count
    return animals

def write_animals_to_csv(animals, filename):
    """
    Записывает словарь животных по буквам в CSV-файл.
    """
    with open(filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        for letter in sorted(animals):
            writer.writerow([letter, animals[letter]])

def parse_animals():
    """
    Сохраняет в beasts.csv количество животных на каждую русскую букву алфавита из Википедии.
    """
    base_url = 'https://ru.wikipedia.org/wiki/Категория:Животные_по_алфавиту'
    session = requests.Session()
    session.headers.update({'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})

    animals = {}
    current_url = base_url
    printed_letters = set()

    while current_url:
        response = session.get(current_url)
        page_animals = extract_letter_counts_from_html(response.text)

        found_russian = False
        for letter in sorted(page_animals):
            count = page_animals[letter]
            animals[letter] = animals.get(letter, 0) + count
            if letter not in printed_letters:
                print(f'Подсчет на букву {letter}')
                printed_letters.add(letter)
            found_russian = True

        # Если на странице не найдено ни одной русской буквы — выходим из цикла
        if not found_russian:
            break

        next_link = BeautifulSoup(response.text, 'html.parser').find('a', string='Следующая страница')
        if next_link and 'href' in next_link.attrs:
            current_url = 'https://ru.wikipedia.org' + next_link['href']
            time.sleep(0.1)
        else:
            current_url = None

    for letter in sorted(animals):
        print(f'всего записей на букву "{letter}" - {animals[letter]}')

    write_animals_to_csv(animals, 'beasts.csv')
    print("Подсчет окончен! Данные сохранены в 'beasts.csv' в корневой папке скрипта!")

if __name__ == '__main__':
    parse_animals()



