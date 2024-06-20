# import pandas as pd
# import os

# # Get the absolute path to the directory of the script
# script_dir = os.path.dirname(os.path.abspath(__file__))

# # Specify the relative paths to the CSV files
# books_path = os.path.join(script_dir, '..', 'DataSet', 'Books.csv')
# ratings_path = os.path.join(script_dir, '..', 'DataSet', 'Ratings.csv')

# # Read the CSV files with explicit encoding
# books = pd.read_csv(books_path, encoding='latin-1')
# ratings = pd.read_csv(ratings_path, encoding='latin-1')

# # Merge the two dataframes on the 'ISBN' column
# ratings_with_name = ratings.merge(books, on='ISBN')

# # Convert 'Book-Rating' to numeric, handling errors by setting them to NaN
# ratings_with_name['Book-Rating'] = pd.to_numeric(ratings_with_name['Book-Rating'], errors='coerce').fillna(0)

# # Drop rows with NaN values in 'Book-Rating'
# ratings_with_name = ratings_with_name.dropna(subset=['Book-Rating'])

# # Filter users who have rated more than 50 books
# x = ratings_with_name.groupby('User-ID').count()['Book-Rating'] > 50
# users = x[x].index

# # Filter ratings for users who have rated more than 10 books
# filtered_rating = ratings_with_name[ratings_with_name['User-ID'].isin(users)]

# # Filter books that have received more than 10 ratings
# y = filtered_rating.groupby('Book-Title').count()['Book-Rating'] >= 10
# famous_books = y[y].index

# # Filter final ratings for famous books
# final_ratings = filtered_rating[filtered_rating['Book-Title'].isin(famous_books)]

# # Create a pivot table
# pt = final_ratings.pivot_table(index='Book-Title', columns='User-ID', values='Book-Rating')
# pt.fillna(0, inplace=True)

# # Save the pivot table to a CSV file
# pt.to_csv(os.path.join(script_dir, 'Index.csv'))

# print('indexing Completed')


import pandas as pd
import os

# Get the absolute path to the directory of the script
script_dir = os.path.dirname(os.path.abspath(__file__))

# Specify the relative paths to the CSV files
books_path = os.path.join(script_dir, '..', 'DataSet', 'Books.csv')
ratings_path = os.path.join(script_dir, '..', 'DataSet', 'Ratings.csv')

# Read the CSV files with explicit encoding
books = pd.read_csv(books_path, encoding='latin-1')
ratings = pd.read_csv(ratings_path, encoding='latin-1')

# Merge the two dataframes on the 'ISBN' column
ratings_with_name = ratings.merge(books, on='ISBN')

# Convert 'Book-Rating' to numeric, handling errors by setting them to NaN
ratings_with_name['Book-Rating'] = pd.to_numeric(ratings_with_name['Book-Rating'], errors='coerce').fillna(0)

# Drop rows with NaN values in 'Book-Rating'
ratings_with_name = ratings_with_name.dropna(subset=['Book-Rating'])

# Filter users who have rated more than 50 books
x = ratings_with_name.groupby('User-ID').count()['Book-Rating'] > 50
users = x[x].index

# Filter ratings for users who have rated more than 10 books
filtered_rating = ratings_with_name[ratings_with_name['User-ID'].isin(users)]

# Filter books that have received more than 10 ratings
y = filtered_rating.groupby('Book-Title').count()['Book-Rating'] >= 10
famous_books = y[y].index

# Filter final ratings for famous books
final_ratings = filtered_rating[filtered_rating['Book-Title'].isin(famous_books)]

# Create a pivot table
pt = final_ratings.pivot_table(index='Book-Title', columns='User-ID', values='Book-Rating')
pt.fillna(0, inplace=True)

# Save the pivot table to a pickle file (.pkl)
pt.to_pickle(os.path.join(script_dir, 'Index.pkl'))

print('indexing Completed')
