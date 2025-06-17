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
    current_letter = None
    current_count = 0

    while current_url:
        response = session.get(current_url)
        page_animals = extract_letter_counts_from_html(response.text)

        found_russian = False
        for letter in sorted(page_animals):
            count = page_animals[letter]
            found_russian = True
            if letter != current_letter:
                if current_letter is not None:
                    print(f'всего записей на букву "{current_letter}" - {current_count}')
                    animals[current_letter] = current_count
                print(f'Подсчет на букву {letter}')
                current_letter = letter
                current_count = count
            else:
                current_count += count

        if not found_russian:
            if current_letter is not None:
                print(f'всего записей на букву "{current_letter}" - {current_count}')
                animals[current_letter] = current_count
            break

        next_link = BeautifulSoup(response.text, 'html.parser').find('a', string='Следующая страница')
        if next_link and 'href' in next_link.attrs:
            current_url = 'https://ru.wikipedia.org' + next_link['href']
            time.sleep(0.1)
        else:
            if current_letter is not None:
                print(f'всего записей на букву "{current_letter}" - {current_count}')
                animals[current_letter] = current_count
            current_url = None

    write_animals_to_csv(animals, 'beasts.csv')

if __name__ == '__main__':
    parse_animals()
