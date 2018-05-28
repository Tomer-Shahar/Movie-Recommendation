import unittest
from Controller.Control import Controller


class Tester(unittest.TestCase):
    #ToDO: Maybe the list length has to be 20? Check this
    #ToDo: can we init controller not in each function?
    #ToDo: consider randomly generating rankings

    #Test with a valid input if checkUserInput returns "True"
    def test_legal_rank_range(self):
        controller = Controller()
        controller.start()
        controller.create_table()
        ranking_list = [2,5,3,"",5,1,4,3,5,1,2,"",3,4]
        self.assertTrue(controller.checkUserInput(ranking_list)[0])

    # Test with a valid input if checkUserInput returns "True"
    def test_legal_fraction_ranks(self):
        controller = Controller()
        controller.start()
        controller.create_table()
        ranking_list = [2, 1.5, 3, "", 5, 1.2, 4.2,"", 3.4, 5, 1.3, 2, "", 3, 4]
        self.assertTrue(controller.checkUserInput(ranking_list)[0])

    # Test with an invalid input if check input returns "False"
    def test_illegal_ranks(self):
        controller = Controller()
        controller.start()
        controller.create_table()
        ranking_list = [2,-5,3,"",5,1,42,3.4,5,1,2,"",3,4]
        self.assertFalse(controller.checkUserInput(ranking_list)[0])

    # Test with an invalid, too short input if checkUserInput returns "False"
    def test_too_few_ranks(self):
        controller = Controller()
        controller.start()
        controller.create_table()
        ranking_list = [2,4,2,"","","","","",4]
        self.assertFalse(controller.checkUserInput(ranking_list)[0])

if __name__ == '__main__':
    unittest.main()
