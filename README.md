# Book Recommendation System

## Project Overview

The Book Recommendation System is designed to provide personalized book recommendations based on user preferences and book ratings. It employs various algorithms such as cosine similarity, TF-IDF, and collaborative filtering to enhance the accuracy of recommendations. The system also includes a web application built using Flask, allowing users to interactively search for recommendations and explore top-rated books.

## Project Structure

The project is organized into several components:

### 1. DataSet

This directory contains the raw data files in CSV format:

- **Books.csv**: Contains information about books such as title, author, and ISBN.
- **Ratings.csv**: Contains user ratings for books.

### 2. BookRecommendation

This directory contains scripts and data related to the recommendation algorithms:

- **Indexing.py**: Indexes the data to optimize search and recommendation algorithms.
- **Recommendations.py**: Contains functions for generating book recommendations based on user input and preferences.

### 3. BookRecommendationApp

This directory contains the Flask web application:

- **app.py**: The main Flask application script that defines routes and handles user requests.
- **templates**: Directory containing HTML templates for the web application.
  - **index.html**: Homepage template for searching and displaying book recommendations.
  - **topratedbooks.html**: Template for displaying top-rated books.
  - **relevanceRecommendations.html**: Template for displaying relevance-based recommendations.
- **static**: Directory for static files like CSS (`styles.css`) for styling the web application.

### 4. TopRatedBooks

This directory handles the generation of top-rated books:

- **TopRatedBooks.py**: Script to filter and process top-rated books based on ratings and user reviews.
- **TopRatedBooks.csv**: CSV file containing top-rated books data.

## Installation

### Install Dependencies

To run the Book Recommendation System, install the required Python dependencies. Open your terminal or command prompt and execute:

```bash
pip install pandas numpy scikit-learn flask
```

### 2. Prepare the Data

Navigate to the DataSet directory:

```bash
cd ir_project/DataSet
```

Run BooksWithRatings.py to generate BooksWithRatings.pkl:

```bash
python BooksWithRatings.py
```

This script processes Books.csv and Ratings.csv, merges them, and cleans the data to create a consolidated dataset with book ratings.

## Index the Data
Navigate to the BookRecommendation directory:

```bash
cd ../BookRecommendation
```
Run Indexing.py to generate Index.pkl:
```bash
python Indexing.py
```
This script builds an index for efficient book recommendation retrieval using algorithms like cosine similarity and TF-IDF.

## Generate Top Rated Books
Navigate to the TopRatedBooks directory:
```bash
cd ../TopRatedBooks
```
Run TopRatedBooks.py to generate TopRatedBooks.pkl:
```bash
python TopRatedBooks.py
```
This script identifies and filters top-rated books based on user ratings and reviews, saving the results in a TopRatedBooks.pkl file.

## Run the Flask Application
Navigate to the BookRecommendationApp directory:
```bash
cd ../BookRecommendationApp
```
Run app.py to start the Flask application:
```bash
python app.py
```
This will start the Flask server, typically on http://127.0.0.1:5000. Open a web browser and go to this URL to interact with the Book Recommendation System.

## Access the Application
Once the Flask application is running, you can access it by opening a web browser and navigating to http://127.0.0.1:5000. Here, you can search for book recommendations, explore top-rated books, and view relevance-based recommendations based on user feedback.
