import pandas as pd
import numpy as np
from DAO.mongo_client import MongoDBClient

#
# def serialize_data(book_list):
#     for item in book_list:
#         user_dict = item['user'][0]
#         user_dict['_id'] = str(user_dict['_id'])
#         item['_id'] = str(item['_id'])
#         item['user_id'] = str(item['user_id'])
#         item.pop('user')
#         item.update({'user': user_dict})
#     return book_list
#

def get_books_and_users():
    client = MongoDBClient()
    books = client.get_all_books()
    users = client.get_all_users()
    ratings = client.get_all_ratings()
    return users, books,ratings


def get_dataframe(books, users, ratings):
    books_df = pd.DataFrame.from_dict(books)
    users_df = pd.DataFrame.from_dict(users)
    ratings_df = pd.DataFrame.from_dict(ratings)
    return users_df, books_df,ratings_df

def train_model(type):
    users, books, ratings = get_books_and_users()
    users, books, ratings = get_dataframe(books, users, ratings)
    books = preprocess_books(books)
    users = preprocess_users(users)
    ratings,n_users,n_books = preprocess_ratings(ratings,users,books)
    if type == 'popularity':
        return popularitybased(ratings, books)
    if type == 'collaborative':
        print("something else")


def preprocess_books(books):
    # 'ISBN', 'Book-Title', 'Book-Author', 'Year-Of-Publication',
    #        'Publisher', 'Image-URL-S', 'Image-URL-M', 'Image-URL-L
    books.drop(['Image-URL-S', 'Image-URL-M', 'Image-URL-L'], axis=1, inplace=True)
    books.loc[books.ISBN == '0789466953', 'Year-Of-Publication'] = 2000
    books.loc[books.ISBN == '0789466953', 'Book-Author'] = "James Buckley"
    books.loc[books.ISBN == '0789466953', 'Publisher'] = "DK Publishing Inc"
    books.loc[
        books.ISBN == '0789466953', 'Book-Title'] = "DK Readers: Creating the X-Men, How Comic Books Come to Life (Level 4: Proficient Readers)"
    books.loc[books.ISBN == '078946697X', 'Year-Of-Publication'] = 2000
    books.loc[books.ISBN == '078946697X', 'Book-Author'] = "Michael Teitelbaum"
    books.loc[books.ISBN == '078946697X', 'Publisher'] = "DK Publishing Inc"
    books.loc[
        books.ISBN == '078946697X', 'Book-Title'] = "DK Readers: Creating the X-Men, How It All Began (Level 4: Proficient Readers)"
    books.loc[books.ISBN == '2070426769', 'Year-Of-Publication'] = 2003
    books.loc[books.ISBN == '2070426769', 'Book-Author'] = "Jean-Marie Gustave Le ClÃ?Â©zio"
    books.loc[books.ISBN == '2070426769', 'Publisher'] = "Gallimard"
    books.loc[books.ISBN == '2070426769', 'Book-Title'] = "Peuple du ciel, suivi de 'Les Bergers"
    books['Year-Of-Publication'] = pd.to_numeric(books['Year-Of-Publication'], errors='coerce')
    books.loc[(books['Year-Of-Publication'] > 2019) | (books['Year-Of-Publication'] == 0), 'Year-Of-Publication'] = np.NAN
    books['Year-Of-Publication'].fillna(round(books['Year-Of-Publication'].mean()), inplace=True)
    books['Year-Of-Publication'].isnull().sum()
    books['Year-Of-Publication'] = books['Year-Of-Publication'].astype(np.int32)
    books.loc[(books.ISBN == '193169656X'), 'Publisher'] = 'other'
    books.loc[(books.ISBN == '1931696993'), 'Publisher'] = 'other'
    return books

def preprocess_users(users):
    users.loc[(users.Age > 90) | (users.Age < 5), 'Age'] = np.nan
    users.Age = users.Age.fillna(users.Age.mean())
    users.Age = users.Age.astype(np.int32)
    return users

def preprocess_ratings(ratings,users,books):
    n_users = users.shape[0]
    n_books = books.shape[0]
    ratings_new = ratings[ratings.ISBN.isin(books.ISBN)]
    ratings_explicit = ratings_new[ratings_new['Book-Rating'] != 0]
    ratings_implicit = ratings_new[ratings_new['Book-Rating'] == 0]
    return ratings_explicit, n_users, n_books

def popularitybased(ratings_explicit, books):
    ratings_count = pd.DataFrame(ratings_explicit.groupby(['ISBN'])['Book-Rating'].sum())
    res = ratings_count.sort_values('Book-Rating', ascending=False)
    res = res.merge(books, left_index=True, right_on='ISBN')
    res = res.to_dict(orient='records')
    return res
