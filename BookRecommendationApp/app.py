import pandas as pd
from flask import Flask, render_template, request
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import os
import re
import pickle

app = Flask(__name__)

# Load the recommendation model
pt = None
similarity_scores = None
books = None

def load_recommendation_model():
    global pt, similarity_scores, books
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # Load the pivot table from Pickle file
    pt_pkl_path = os.path.join(script_dir, '..', 'BookRecommendation', 'Index.pkl')
    with open(pt_pkl_path, 'rb') as file:
        pt = pickle.load(file)

    # Load other necessary data
    similarity_scores = cosine_similarity(pt)

    # Load books DataFrame with ratings from Pickle file
    books_pkl_path = os.path.join(script_dir, '..', 'DataSet', 'BooksWithRatings.pkl')
    with open(books_pkl_path, 'rb') as file:
        books = pickle.load(file)

# Load the recommendation model before the server starts
load_recommendation_model()

def find_closest_match(book_name, available_books):
    pattern = re.compile(f'.*{re.escape(book_name)}.*', flags=re.IGNORECASE)
    matches = [title for title in available_books if pattern.search(title)]
    return matches[0] if matches else None


def recommend(book_name, min_avg_rating=1):
    global pt, similarity_scores, books

    closest_match = find_closest_match(book_name, pt.index)

    if closest_match is not None:
        index = np.where(pt.index == closest_match)[0][0]
        similar_items = sorted(list(enumerate(similarity_scores[index])), key=lambda x: x[1], reverse=True)[1:15]
        data = []
        for i in similar_items:
            item = []
            temp_df = books[books['Book-Title'] == pt.index[i[0]]]
            # Check if the row has a non-null image URL
            if not temp_df['Image-URL-M'].isnull().values.all():
                item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Title'].values))
                item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Author'].values))
                item.extend(list(temp_df.drop_duplicates('Book-Title')['Image-URL-M'].values))
                avg_rating = temp_df['Book-Rating'].mean()

                # Set the average rating to 5 if it is above 5
                avg_rating = 5 if avg_rating > 5 else avg_rating

                # Check if the average rating meets the minimum requirement
                if min_avg_rating is None or (min_avg_rating != '' and avg_rating is not None and avg_rating >= float(min_avg_rating)):
                    item.append(avg_rating)
                    data.append(item)

        # Sort recommendations based on rating (descending order)
        data = sorted(data, key=lambda x: x[3] if x[3] is not None else float('-inf'), reverse=True)

        # Take only the top 10 recommendations
        data = data[:10]

        # Filter out recommendations without images
        data = [item for item in data if item[2]]  # item[2] is the image URL

        return data
    else:
        print(f"No matches found for '{book_name}'.")
        return None



def load_top_rated_books():
    return pd.read_csv(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'TopRatedBooks', 'TopRatedBooks.csv'), encoding='latin-1')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/recommendations', methods=['POST'])
def get_recommendations():
    if request.method == 'POST':
        book_name = request.form['book_name']
        min_avg_rating = request.form.get('min_avg_rating', '1')

        # Check if min_avg_rating is an empty string and set it to '1' if true
        if not min_avg_rating:
            min_avg_rating = '1'

        recommendations = recommend(book_name, min_avg_rating)
        return render_template('index.html', recommendations=recommendations,num_books=len(recommendations))


@app.route('/topratedbooks')
def top_rated_books():
    top_rated_books = load_top_rated_books()
    return render_template('topratedbooks.html', top_rated_books=top_rated_books)

@app.route('/submitfeedback', methods=['POST'])
def submit_feedback():
    if request.method == 'POST':
        # Handle the feedback submission here
        feedback_data = request.form.to_dict()

        # Access the selected relevant books from the feedback data
        selected_books = [key.replace('_checkbox', '') for key, value in feedback_data.items()]

        # Access book details from hidden input fields
        positions = [int(value.split(' ')[0]) for value in feedback_data.values()]

        ground_truth = [0] * 10

        for pos in positions:
            if 0 <= pos < 10:
                ground_truth[pos] = 1

        num_relevant = sum(ground_truth)    
        cumulative_relevant = np.cumsum(ground_truth)
        recall = cumulative_relevant / num_relevant
        precision = cumulative_relevant / np.arange(1, len(ground_truth) + 1)

        num_points = 11
        interp_recall_levels = np.linspace(0, 1, num_points)
        interp_precision_levels = np.interp(interp_recall_levels, recall[::-1], precision[::-1])

        numOfRelevencePerEach = 10 / len(selected_books)

        recommended_books = []  # Array to store recommendations for each selected book

        for book_name in selected_books:
            # Fetch recommendations for each selected book
            recommendations = recommend(book_name, min_avg_rating=1)

            # Check if recommendations are available
            if recommendations is not None:
                # Calculate the number of recommendations to add, considering numOfRelevencePerEach
                num_of_recommendations = min(int(numOfRelevencePerEach), len(recommendations))

                # Extend the recommended_books array with the calculated number of recommendations
                recommended_books.extend(recommendations[:num_of_recommendations])
        print(interp_precision_levels)

        # Pass data to the template
        return render_template(
            'relevanceRecommendations.html',
            recommendations=recommended_books,
            recall=recall.tolist(),  # Convert to a list for JSON serialization
            precision=precision.tolist(),
            interp_precision_levels=interp_precision_levels.tolist()
        )




if __name__ == "__main__":
    app.run(debug=True)


