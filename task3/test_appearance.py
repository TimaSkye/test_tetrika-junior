import unittest
from solution import merge_intervals, cut_intervals_to_lesson, appearance

class TestIntervalFunctions(unittest.TestCase):

    def test_merge_intervals(self):
        """Тест объединения интервалов"""
        test_cases = [
            ([[1, 3], [2, 4]], [[1, 4]]),
            ([[1, 2], [3, 4]], [[1, 2], [3, 4]]),
            ([[1, 5], [2, 3]], [[1, 5]]),
            ([], []),
            ([[5, 6], [1, 2]], [[1, 2], [5, 6]])
        ]
        for input_intervals, expected in test_cases:
            with self.subTest(input=input_intervals):
                result = merge_intervals(input_intervals)
                self.assertEqual(result, expected)

    def test_cut_intervals_to_lesson(self):
        """Тест обрезки интервалов по уроку"""
        test_cases = [
            ([[10, 20], [25, 30]], 15, 25, [[15, 20]]),  # Исправлено: убран нулевой интервал [25,25]
            ([[5, 40]], 10, 30, [[10, 30]]),
            ([[8, 12], [15, 18]], 10, 20, [[10, 12], [15, 18]]),
            ([], 0, 100, []),
            ([[50, 60]], 10, 40, [])
        ]
        for intervals, start, end, expected in test_cases:
            with self.subTest(intervals=intervals, start=start, end=end):
                result = cut_intervals_to_lesson(intervals, start, end)
                self.assertEqual(result, expected)

class TestAppearanceFunction(unittest.TestCase):
    def test_appearance_basic(self):
        """Тест базовых случаев"""
        test_cases = [
            # Полное пересечение
            {
                'lesson': [0, 100],
                'pupil': [[0, 100]],
                'tutor': [[0, 100]],
                'expected': 100
            },
            # Частичное пересечение
            {
                'lesson': [0, 100],
                'pupil': [[0, 50]],
                'tutor': [[50, 100]],
                'expected': 0
            },
            # Несколько интервалов
            {
                'lesson': [0, 100],
                'pupil': [[0, 30], [40, 80]],
                'tutor': [[20, 50], [60, 90]],
                'expected': (30-20) + (50-40) + (80-60)
            }
        ]
        for case in test_cases:
            with self.subTest(case=case):
                intervals = {
                    'lesson': case['lesson'],
                    'pupil': [t for sub in case['pupil'] for t in sub],
                    'tutor': [t for sub in case['tutor'] for t in sub]
                }
                result = appearance(intervals)
                self.assertEqual(result, case['expected'])

    def test_appearance_edge_cases(self):
        """Тест граничных случаев"""
        test_cases = [
            # Интервалы точно на границах урока
            {
                'lesson': [0, 100],
                'pupil': [[0, 100]],
                'tutor': [[0, 100]],
                'expected': 100
            },
            # Интервалы касаются границ
            {
                'lesson': [0, 100],
                'pupil': [[-10, 110]],
                'tutor': [[0, 0], [100, 100]],
                'expected': 0
            }
        ]
        for case in test_cases:
            with self.subTest(case=case):
                intervals = {
                    'lesson': case['lesson'],
                    'pupil': [t for sub in case['pupil'] for t in sub],
                    'tutor': [t for sub in case['tutor'] for t in sub]
                }
                result = appearance(intervals)
                self.assertEqual(result, case['expected'])

    def test_appearance_original_tests(self):
        """Тесты из исходного задания"""
        tests = [
            {
                'intervals': {
                    'lesson': [1594663200, 1594666800],
                    'pupil': [1594663340, 1594663389, 1594663390, 1594663395, 1594663396, 1594666472],
                    'tutor': [1594663290, 1594663430, 1594663443, 1594666473]
                },
                'answer': 3117
            },
            {
                'intervals': {
                    'lesson': [1594702800, 1594706400],
                    'pupil': [1594702789, 1594704500, 1594702807, 1594704542, 1594704512, 1594704513, 1594704564, 1594705150, 1594704581, 1594704582, 1594704734, 1594705009, 1594705095, 1594705096, 1594705106, 1594706480, 1594705158, 1594705773, 1594705849, 1594706480, 1594706500, 1594706875, 1594706502, 1594706503, 1594706524, 1594706524, 1594706579, 1594706641],
                    'tutor': [1594700035, 1594700364, 1594702749, 1594705148, 1594705149, 1594706463]
                },
                'answer': 3577
            },
            {
                'intervals': {
                    'lesson': [1594692000, 1594695600],
                    'pupil': [1594692033, 1594696347],
                    'tutor': [1594692017, 1594692066, 1594692068, 1594696341]
                },
                'answer': 3565
            }
        ]
        for test in tests:
            with self.subTest(test=test):
                result = appearance(test['intervals'])
                self.assertEqual(result, test['answer'])

if __name__ == '__main__':
    unittest.main()
