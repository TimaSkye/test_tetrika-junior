import unittest
from unittest.mock import patch, MagicMock
import os
from solution import extract_letter_counts_from_html, write_animals_to_csv, parse_animals

class TestAnimalParser(unittest.TestCase):
    """Тесты для функций парсинга количества животных по буквам."""

    def setUp(self):
        """Устанавливает тестовый HTML для проверки парсинга."""
        self.html = '''
        <div id="mw-pages">
          <div class="mw-category-group">
            <h3>А</h3>
            <ul><li>Акула</li><li>Аист</li></ul>
          </div>
          <div class="mw-category-group">
            <h3>Б</h3>
            <ul><li>Бобр</li></ul>
          </div>
          <div class="mw-category-group">
            <h3>A</h3>
            <ul><li>Ant</li></ul>
          </div>
        </div>
        '''

    def test_extract_letter_counts(self):
        """
        Проверяет, что функция корректно извлекает только русские буквы и их количество.
        """
        result = extract_letter_counts_from_html(self.html)
        self.assertEqual(result, {'А': 2, 'Б': 1})

    def test_csv_file_creation_and_content(self):
        """
        Проверяет, что CSV-файл создаётся и содержит правильные строки.
        """
        animals = {'А': 2, 'Б': 1}
        filename = 'test_beasts.csv'
        if os.path.exists(filename):
            os.remove(filename)
        write_animals_to_csv(animals, filename)
        self.assertTrue(os.path.exists(filename), "CSV-файл не был создан")
        with open(filename, encoding='utf-8') as f:
            lines = [line.strip() for line in f.readlines()]
        self.assertIn('А,2', lines)
        self.assertIn('Б,1', lines)
        os.remove(filename)

class TestParseAnimalsIntegration(unittest.TestCase):
    """
    Интеграционный тест для функции parse_animals с моками сетевых запросов и файловой системы.
    """

    @patch('solution.requests.Session.get')
    @patch('solution.open')
    @patch('solution.csv.writer')
    def test_parse_animals_creates_csv(self, mock_csv_writer, mock_open, mock_get):
        """
        Проверяет, что parse_animals вызывает запись в CSV-файл с правильными данными.
        """
        # Поддельный HTML для двух страниц
        html_page_1 = '''
        <div id="mw-pages">
          <div class="mw-category-group">
            <h3>А</h3>
            <ul><li>Акула</li></ul>
          </div>
          <div class="mw-category-group">
            <h3>Б</h3>
            <ul><li>Бобр</li></ul>
          </div>
        </div>
        <a href="/wiki/next" title="Следующая страница">Следующая страница</a>
        '''
        html_page_2 = '''
        <div id="mw-pages">
          <div class="mw-category-group">
            <h3>А</h3>
            <ul><li>Аист</li></ul>
          </div>
        </div>
        '''

        mock_response_1 = MagicMock()
        mock_response_1.text = html_page_1
        mock_response_2 = MagicMock()
        mock_response_2.text = html_page_2
        mock_get.side_effect = [mock_response_1, mock_response_2]

        written_rows = []
        mock_writer_instance = MagicMock()
        mock_csv_writer.return_value = mock_writer_instance
        mock_writer_instance.writerow.side_effect = lambda row: written_rows.append(row)

        mock_open.return_value.__enter__.return_value = MagicMock()

        parse_animals()

        self.assertIn(['А', 2], written_rows)
        self.assertIn(['Б', 1], written_rows)

if __name__ == '__main__':
    unittest.main()
