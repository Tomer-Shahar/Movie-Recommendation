import json
import os


def load_recommender(folder_path):
    table = None
    path = folder_path + '\\PearsonDictionary.json'

    if os.path.exists(path):
        with open(path, 'r') as fp:
            table = json.load(fp)

    return table
