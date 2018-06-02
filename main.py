"""
Created: 28/4/2018
Authors: Nevo Itzhak, Tomer Shahar, Shani Houri, Eyal Arviv

Version: 1.0

Description: A simple collaborative filtering program for recommending movies based off of the movielens database
of 20 million movies.

"""

from Controller.Control import Controller
from TestSuite import Tester

if __name__ == "__main__":
    controller = Controller()
    controller.start_no_GUI()
    for i in range(0, 50):
        controller.run_accuracy_test(100)
        print("")
