# -*- coding: utf-8 -*-
"""minor_project_book_recommender

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1mVvhwj9NaihSDzyuSVJWoVCkBcZDgLib

# **Book Recommender System**

## Environment Setup and Data Loading
"""

# importing libraries
import pandas as pd
import numpy as np
from collections import Counter
import ast
from google.colab import data_table
from google.colab import drive

# enabling data table formatter
data_table.enable_dataframe_formatter()

# mounting google drive
drive.mount("/content/drive", force_remount=True)

# read the csv file
b = '/content/drive/My Drive/csvfiles/genredata.csv'
books = pd.read_csv(b)

"""## Data Exploration and Preprocessing"""

books.head(1)

books.info()

books.shape

books.columns

# dropping column which is not needed
books.drop('Unnamed: 0',axis=1,inplace=True)

books.isna().sum()

books.isnull().sum()

# some values in the description column have na values so replacing them with custom text
no_desc = "Description not available"
books.fillna(no_desc,inplace=True)

books.duplicated().sum()

books.Num_Ratings.dtype

# data in the following column has data type as object so removing the commas to make it suitable
books['Num_Ratings'] = books['Num_Ratings'].str.replace(',','').astype(int)

"""# **Popularity-Based Book Recommendation**

## Selecting and filtering books
"""

# filter out the books with the most number of ratings from the dataset
popular_books = books[books['Num_Ratings']>=900000]
popular_books.shape

# filter out the top 100 books in descending order refering to the average rating
popular_books = popular_books.sort_values('Avg_Rating',ascending=False).head(100)

# drop any duplicates present in the dataset
popular_books = popular_books.drop_duplicates('Book')[['Book','Author','Description','Avg_Rating','Num_Ratings','URL']]

# filter out the top 50 books from the dataset
popular_books = popular_books.head(50)

popular_books

"""# **Genre-Based Book Recommendation**

## Function for displaying genres
"""

# selecting the 'Genres' column and converting it into a list of commonly appearing genres
unique_genres = books['Genres'].unique()
print(unique_genres)

genres_array = unique_genres

genres_list = [ast.literal_eval(genre_str) for genre_str in genres_array]

flat_genres = [genre for sublist in genres_list for genre in sublist]

def genres():
    genre_counts = Counter(flat_genres)
    top_50_genres = genre_counts.most_common(50)

    num_columns = 10
    column_width = len(top_50_genres) // num_columns

    for i in range(0, len(top_50_genres), column_width):
        columns = top_50_genres[i:i + column_width]
        for genre, count in columns:
            print(f"{genre}".ljust(25), end="")
        print()

"""## Function for recommending books according to the user input"""

# defining recommend function to recommend the user book with the same genre as the user's input
def recommend():
    genres()
    books = pd.read_csv(b)
    user_input = input("\nEnter genres (comma-separated): ")
    user_genres = user_input.split(',')
    books['Num_Ratings'] = books['Num_Ratings'].str.replace(',','').astype(int)

    filtered_books = books[books['Genres'].apply(lambda x: any(genre in x for genre in user_genres))]

    top_num_ratings = filtered_books[filtered_books['Num_Ratings'] >= 900000]

    top_100 = top_num_ratings.sort_values('Avg_Rating', ascending=False).head(100)

    top_no_duplicates = top_100.drop_duplicates('Book')[['Book', 'Author', 'Description', 'Avg_Rating', 'Num_Ratings', 'URL']]

    top_no_duplicates = top_no_duplicates.head(5)

    top_output = top_no_duplicates[['Book', 'Author', 'Description','URL']]

    display(top_output)

# calling the function
recommend()

"""# Code is completed here"""
