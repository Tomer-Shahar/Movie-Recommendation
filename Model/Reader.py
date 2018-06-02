import os
import pickle


def load_recommender(folder_path):

    path = folder_path + '\\Recommender.pkl'
    if os.path.exists(path):
        with open(path, 'rb') as fp:
            table = pickle.load(fp)
            return table
    else:
        print(path)
        return None
