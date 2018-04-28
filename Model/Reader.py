import os
import pickle


def load_recommender(folder_path):

    path = folder_path + '\\Recommender.pkl'

    if os.path.exists(path):
        with open(path, 'rb') as fp:
            table = pickle.load(fp)
            print("managed to unpickle")
            return table

    else:
        return None
