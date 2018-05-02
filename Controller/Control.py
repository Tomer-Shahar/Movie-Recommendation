"""

Controller class - manages the flow between the recommendation system and the GUI

"""
from Model.Recommender import Parse
from Model import Writer
from Model import Reader
import os


class Controller:

    def __init__(self):
        print("Initializing GUI and stuff\n")
        self.parser = None

    def start(self):
        #print("Open GUI and do stuff \n")
        cwd = os.getcwd()  # current working directory
        database_folder = cwd + '\\Database\\100k-small'
        #self.parser = Parse(database_folder)
        #self.create_table()
        #self.write_recommender()
        self.load_table()
        self.get_top_movies_global(20)
        self.get_top_x_movies_for_genre('Action', 15)

    def create_table(self):
        self.parser.parse_movieDB_files()

    def write_recommender(self):
        cwd = os.getcwd()  # current working directory
        resource_folder = cwd + '\\Resources'
        Writer.write_recommender(self.parser, resource_folder)

    def load_table(self):
        cwd = os.getcwd()  # current working directory
        resource_folder = cwd + '\\Resources'
        self.parser = Reader.load_recommender(resource_folder)

    # Given a user ID and X, returns a list containing the top X movies for the given user.
    def get_personal_recommendations(self, userID: str, numOfMovies: str):
        top_movies = self.parser.get_top_x_movies_for_user(int(userID), int(numOfMovies))
        print("Predicted score : Movie Title")
        returnedList =[]
        for entry in top_movies:
            print(entry[0], " : ", entry[1].title)
            returnedList.append(entry[1].title)

        return returnedList

    # Given a number X, returns the top X movies by average rating.
    def get_top_movies_global(self, top: int):
        topList = self.parser.get_top_rated_movies_global(int(top))
        print("Movie Title : Score")
        for entry in topList:
            print(entry[0], " : ", entry[1])
        return topList

    def get_top_x_movies_for_genre(self, genre: str, topX: int):
        topList = self.parser.get_top_movies_for_genre(genre, int(topX))
        print("Movie Title : Score")
        for entry in topList:
            print(entry[0], " : ", entry[1])
        return topList


    def add_user(self):
        pass
