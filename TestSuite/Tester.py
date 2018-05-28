import unittest
from Controller.Control import Controller


class Tester(unittest.TestCase):

    def test_negative(self):
        self.assertFalse(...)

    def test_accuracy(self, n : int):
        controller = Controller()
        controller.start_no_GUI()
        controller.load_table()
        controller.run_accuracy_test(n)

if __name__ == '__main__':
    C = Controller()

