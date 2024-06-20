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

# Calculate the number of ratings and average rating
num_rating_df = ratings_with_name.groupby('Book-Title').count()['Book-Rating'].reset_index()
num_rating_df.rename(columns={'Book-Rating': 'num_ratings'}, inplace=True)

# Handle mixed data types in 'Book-Rating' for calculating the average rating
avg_rating_df = ratings_with_name.groupby('Book-Title')['Book-Rating'].apply(lambda x: x.astype(float).mean()).reset_index()
avg_rating_df.rename(columns={'avg_rating': 'Book-Rating'}, inplace=True)

# Merge the dataframes on 'Book-Title'
popular_df = num_rating_df.merge(avg_rating_df, on='Book-Title')

# Filter books with more than 250 ratings
popular_df = popular_df[popular_df['num_ratings'] >= 250].sort_values('Book-Rating', ascending=False).head(50)

# Merge with the 'books' dataframe and drop duplicates
popular_df = popular_df.merge(books, on='Book-Title').drop_duplicates('Book-Title')[['Book-Title', 'Book-Author', 'Image-URL-M', 'num_ratings', 'Book-Rating']]

# Store the popular_df in a CSV file named TopRatedBooks.csv
output_path = os.path.join(script_dir, 'TopRatedBooks.csv')
popular_df.to_csv(output_path, index=False)

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

# # Calculate the number of ratings and average rating
# num_rating_df = ratings_with_name.groupby('Book-Title').count()['Book-Rating'].reset_index()
# num_rating_df.rename(columns={'Book-Rating': 'num_ratings'}, inplace=True)

# # Handle mixed data types in 'Book-Rating' for calculating the average rating
# avg_rating_df = ratings_with_name.groupby('Book-Title')['Book-Rating'].apply(lambda x: x.astype(float).mean()).reset_index()
# avg_rating_df.rename(columns={'avg_rating': 'Book-Rating'}, inplace=True)

# # Merge the dataframes on 'Book-Title'
# popular_df = num_rating_df.merge(avg_rating_df, on='Book-Title')
# print(popular_df)

# # Filter books with more than 250 ratings
# popular_df = popular_df[popular_df['num_ratings'] >= 250].sort_values('Book-Rating', ascending=False).head(50)

# # Merge with the 'books' dataframe and drop duplicates
# popular_df = popular_df.merge(books, on='Book-Title').drop_duplicates('Book-Title')[['Book-Title', 'Book-Author', 'Image-URL-M', 'num_ratings', 'Book-Rating']]

# # Store the popular_df in a Pickle file named TopRatedBooks.pkl
# output_path_pkl = os.path.join(script_dir, 'TopRatedBooks.pkl')
# popular_df.to_pickle(output_path_pkl)

# print(f"TopRatedBooks.pkl has been saved.")
