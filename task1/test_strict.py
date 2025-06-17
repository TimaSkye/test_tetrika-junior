import unittest

from solution import strict


class TestStrictDecorator(unittest.TestCase):
    """Тесты для декоратора strict."""

    @strict
    def func_int_str(self, a: int, b: str):
        """int и str аргументы."""
        return f"{a} {b}"

    @strict
    def func_bool_float(self, flag: bool, value: float):
        """bool и float аргументы."""
        return flag, value

    @strict
    def func_all_types(self, a: bool, b: int, c: float, d: str):
        """Все поддерживаемые типы."""
        return (a, b, c, d)

    def test_correct_types(self):
        """Правильные типы не вызывают ошибок."""
        self.assertEqual(self.func_int_str(10, "test"), "10 test")
        self.assertEqual(self.func_bool_float(True, 3.14), (True, 3.14))
        self.assertEqual(self.func_all_types(False, 5, 2.7, "str"), (False, 5, 2.7, "str"))

    def test_incorrect_types(self):
        """Неправильные типы вызывают TypeError."""
        with self.assertRaises(TypeError):
            self.func_int_str("not int", "test")
        with self.assertRaises(TypeError):
            self.func_int_str(10, 123)
        with self.assertRaises(TypeError):
            self.func_bool_float(1, 3.14)
        with self.assertRaises(TypeError):
            self.func_all_types(False, "5", 2.7, "str")
        with self.assertRaises(TypeError):
            self.func_all_types(False, 5, "2.7", "str")
        with self.assertRaises(TypeError):
            self.func_all_types(False, 5, 2.7, 100)


if __name__ == "__main__":
    unittest.main()
