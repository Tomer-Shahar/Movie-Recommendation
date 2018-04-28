import json
import os


def write_pearson_table(pearsonTable, folder_name):

    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

    savePath = folder_name + "\\Recommender.json"

    with open(savePath, 'w') as fp:
        json.dump(pearsonTable, fp, sort_keys=True, indent=4, ensure_ascii=False)
