import streamlit as st
import requests
import os
import pickle

st.title('Movie Recommendation System')
movies = pickle.load(open('movie_list.pkl','rb'))
similarity = pickle.load(open('similarity.pkl','rb'))
movie_list = movies['title_x'].values
selected_movie = st.selectbox(
    "Type or select a movie from the dropdown",
    movie_list
)
def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=781a96197d3ef620e98a05bc9bf85cbb".format(movie_id)
    data = requests.get(url)
    data = data.json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w185" + poster_path
    return full_path

def fetch_movie_name_with_index(movies,movie_list):
    list_of_info = []
    for x in movie_list:
        ls = []
        ls.append(movies.iloc[x]['id'])
        ls.append(movies.iloc[x]['title_x'])
        list_of_info.append(ls)
    return list_of_info

def recommend(movie):
    cnt = 0
    movie_index = movies[movies['title_x']==movie].index[0]
    cosine_similarity_theta = similarity[movie_index]
    recommended_movie_list = []
    poster = []
    ls = sorted(list(enumerate(cosine_similarity_theta)),reverse=True,key=lambda x:x[1])
    for x in ls:
        if cnt==6:
            break
        cnt+= 1
        recommended_movie_list.append(x[0])
    lst = fetch_movie_name_with_index(movies,recommended_movie_list)
    lst = lst[1:]
    for i in lst:
        print(i[0])
        path = fetch_poster(int(i[0]))
        poster.append(path)
    return lst,poster


if st.button('Show Recommendation'):
    recommended_movie_names,recommended_movie_posters = recommend(selected_movie)
    col1, col2, col3, col4, col5 = st.columns([1, 1, 1, 1,1])
    with col1:
        st.text(recommended_movie_names[0][1])
        st.image(recommended_movie_posters[0])
    
    with col2:
        st.text(recommended_movie_names[1][1])
        st.image(recommended_movie_posters[1])

    with col3:
        st.text(recommended_movie_names[2][1])
        st.image(recommended_movie_posters[2])

    with col4:
        st.text(recommended_movie_names[3][1])
        st.image(recommended_movie_posters[3])

    with col5:
        st.text(recommended_movie_names[4][1])
        st.image(recommended_movie_posters[4])
