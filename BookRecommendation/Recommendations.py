# BookRecommendation/Recommendations.py

import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import os
import re

def load_data():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    pt_csv_path = os.path.join(script_dir, 'Index.csv')
    pt = pd.read_csv(pt_csv_path, index_col='Book-Title')
    return pt

def calculate_similarity(pt):
    similarity_scores = cosine_similarity(pt)
    return similarity_scores

def find_closest_match(book_name, available_books):
    pattern = re.compile(f'.*{re.escape(book_name)}.*', flags=re.IGNORECASE)
    matches = [title for title in available_books if re.match(pattern, title)]
    return matches[0] if matches else None

def recommend(book_name, pt, similarity_scores, books):
    closest_match = find_closest_match(book_name, pt.index)

    if closest_match is not None:
        index = np.where(pt.index == closest_match)[0][0]
        similar_items = sorted(list(enumerate(similarity_scores[index])), key=lambda x: x[1], reverse=True)[1:5]

        data = []
        for i in similar_items:
            item = []
            temp_df = books[books['Book-Title'] == pt.index[i[0]]]
            item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Title'].values))
            item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Author'].values))
            item.extend(list(temp_df.drop_duplicates('Book-Title')['Image-URL-M'].values))
            data.append(item)

        return data
    else:
        print(f"No matches found for '{book_name}'.")
        return None
