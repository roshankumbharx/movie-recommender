import numpy as np
import streamlit as st
import pickle
import pandas as pd
import requests
from pandas.core.apply import reconstruct_func

movies_dict=pickle.load(open('movie_dict.pkl','rb'))
movies=pd.DataFrame(movies_dict)

upper_mat_ind=pickle.load(open('upper_mat_ind.pkl','rb'))
upper_mat_val=pickle.load(open('upper_mat_val.pkl','rb'))

reconstructed_mat=np.zeros((4800,4800))
reconstructed_mat[upper_mat_ind]=upper_mat_val
reconstructed_mat = reconstructed_mat + reconstructed_mat.T - np.diag(reconstructed_mat.diagonal())

def fetch_poster(movie_id):
     response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=3e588d3894440a7f4eaf73f5327ab1a5'.format(movie_id))
     data = response.json()
     return "https://image.tmdb.org/t/p/w500/" + data['poster_path']

def recommend(movie):
    movie_index =  movies[movies['title'] == movie].index[0]
    distances = reconstructed_mat[movie_index]
    movie_list= sorted(list(enumerate(distances)),reverse=True,key=lambda x:x[1])[1:6]

    recommended_movies=[]
    recommended_movies_poster=[]
    for i in movie_list:
        movie_id=movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_movies_poster.append(fetch_poster(movie_id))
    return recommended_movies,recommended_movies_poster


st.title('Movie Recommender System')
selected_movie_name = st.selectbox("Select Movies", movies['title'].values)

try:
    if st.button('Press to Recommend'):
        names, poster = recommend(selected_movie_name)

        col1, col2, col3, col4, col5 = st.columns(5)

        with col1:
            st.text(names[0])
            st.image(poster[0])

        with col2:
            st.text(names[1])
            st.image(poster[1])

        with col3:
            st.text(names[2])
            st.image(poster[2])

        with col4:
            st.text(names[3])
            st.image(poster[3])

        with col5:
            st.text(names[4])
            st.image(poster[4])
except:
    st.text('Error Occured')