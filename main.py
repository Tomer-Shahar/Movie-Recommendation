"""
Created: 28/4/2018
Authors: Nevo Itzhak, Tomer Shahar, Shani Houri, Eyal Arviv

Version: 1.0

Description: A simple collaborative filtering program for recommending movies based off of the movielens database
of 20 million movies.

"""

from Controller.Control import Controller

if __name__ == "__main__":
    controller = Controller()
    controller.start()
    #controller.create_table()
