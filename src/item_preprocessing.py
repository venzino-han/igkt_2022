"""
pre-process tag, part 
"""
from collections import defaultdict
import pickle
import numpy as np
import pandas as pd
import config



def tag_to_vector(tags):
    tag_lsit = [0]*188
    if isinstance(tags, float):
        return np.array(tag_lsit)
    tags = tags.split()
    tags = map(int, tags)
    for tag in tags:
        tag_lsit[tag]=1
    return np.array(tag_lsit)



if __name__=="__main__":
    # question_id,bundle_id,correct_answer,part,tags
    ques_path = "data/questions.csv"
    df = pd.read_csv(ques_path)

    df['tag_vector'] = df['tags'].apply(tag_to_vector)
    tag_matrix = df['tag_vector'].tolist()
    tag_matrix = np.stack(tag_matrix, axis=0)
    tag_coo_matrix = np.matmul(tag_matrix, tag_matrix.T)
    print(tag_coo_matrix.sum())

    n_items = config.TOTAL_EXE
    item_tag_coo_matrix = defaultdict(dict)
    for i in range(n_items):
        for j in range(n_items):
            v = tag_coo_matrix[i][j]
            if v != 0:
                item_tag_coo_matrix[i][j]=v    

    with open('./data/tag_coo_matrix.pkl', 'wb') as pick:
        pickle.dump(item_tag_coo_matrix, pick)

    parts = df['part'].tolist()
    item_part_matrix=defaultdict(dict)
    for i in range(n_items):
        for j in range(n_items):
            if parts[i]==parts[j]:
                item_part_matrix[i][j]=1

    with open('./data/part_matrix.pkl', 'wb') as pick:
        pickle.dump(item_part_matrix, pick)
