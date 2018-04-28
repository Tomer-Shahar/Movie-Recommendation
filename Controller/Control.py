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
        self.pearsonTable = None

    def start(self):
        print("Open GUI and do stuff \n")
        self.parser = Parse('C:\\Users\\Tomer\\PycharmProjects\\movie-recommendation\\Database\\100k-small')
        #self.create_table()
        #self.write_recommender()
        self.load_table()

    def create_table(self):
        self.pearsonTable = self.parser.create_pearson_table()

    def write_recommender(self):
        cwd = os.getcwd()  # current working directory
        resource_folder = cwd + '\\Resources'
        Writer.write_pearson_table(self.pearsonTable, resource_folder)

    def load_table(self):
        cwd = os.getcwd()  # current working directory
        resource_folder = cwd + '\\Resources'
        self.parser = Reader.load_recommender()
        self.pearsonTable = Reader.load_recommender(resource_folder)

    def get_recommendations(self):


    def add_user(self):
        pass
