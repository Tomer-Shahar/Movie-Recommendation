import unittest
from random import randint
from Controller.Control import Controller

"""
TENS System Unit Tests

This class performs unit tests on the movie recommendation system. It performs several, simple tests on the functionality
of a user ranking movies and then being added to the system.
"""


class Tester(unittest.TestCase):

    # ToDO: Maybe the list length has to be 20? Check this
    # ToDo: can we init controller not in each function?
    # ToDo: consider randomly generating rankings
    # Todo: Check if user really was added to system

    def setUp(self):
        self.controller = Controller()
        self.controller.start_no_GUI()

    def tearDown(self):
        self.controller = None

    # Test with a valid input if checkUserInput returns "True"
    def test_legal_rank_range(self):
        ranking_list = [2, 5, 3, "", 5, 1, 4, 3, 5, 1.2, 4.2, "", 3.4, 5, 1.3, 1, 2, "", 3, 4]
        self.assertTrue(self.controller.checkUserInput(ranking_list)[0])

    # Verify that a new user was added to the system with a legal ranking liste
    def test_user_added(self):
        top_list = self.controller.get_top_movies_global(10)
        new_user_id = self.controller.add_user(top_list)
        self.assertTrue(self.controller.user_exists(new_user_id))

    # Test with an invalid input if check input returns "False"
    def test_illegal_ranks(self):
        ranking_list = [2, -5, 3, "", 5, 1, 42, 3.4, "", "", "", "", "", 5, 1, 2, "", 3, 4, ""]
        self.assertFalse(self.controller.checkUserInput(ranking_list)[0])

    # Test with an invalid, too short input if checkUserInput returns "False"
    def test_too_few_ranks(self):
        ranking_list = [2, 4, 2, "", "", "", "", "", 4, "", "", "", "", "", "", "", "", "", "", ""]
        self.assertFalse(self.controller.checkUserInput(ranking_list)[0])


if __name__ == "__main__":
    unittest.main()
