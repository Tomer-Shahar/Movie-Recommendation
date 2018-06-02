"""
Created: 28/4/2018
Authors: Nevo Itzhak, Tomer Shahar, Shani Houri, Eyal Arviv

Version: 1.0

Description: A simple collaborative filtering program for recommending movies based off of the movielens database
of 100k ratings.

"""

from Controller.Control import Controller
from TestSuite import Tester

if __name__ == "__main__":
    controller = Controller()
    controller.start()
    """
    for i in range(1, 50):
        print("Test number " + str(i) + ":")
        controller.run_accuracy_test(100)
        print("")
    """



