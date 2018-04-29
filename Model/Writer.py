import os
import pickle


def write_recommender(parser, folder_name):
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

    savePath = folder_name + "\\Recommender.pkl"

    with open(savePath, 'wb') as fp:
        #    json.dump(parser.toDict(), fp, sort_keys=True, indent=4, ensure_ascii=False)
        pickle.dump(parser, fp)
