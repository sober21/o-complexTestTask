import unittest

from app.date_logic import render_date


class AppTestCase(unittest.TestCase):
    def setUp(self):
        print("Начало теста")

    def tearDown(self):
        print("Конец теста")

    def test_date_logic(self):
        self.assertEqual(render_date('2024-08-21'), '21 Августа')
        self.assertEqual(render_date('2024-05-12'), '12 Мая')


if __name__ == "__main__":
    unittest.main()
