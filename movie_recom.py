import streamlit as st
import pickle
import pandas as pd
import requests

movies_dict=pickle.load(open('movies_dict.pkl','rb'))
similarity=pickle.load(open('similarity.pkl','rb'))
movies=pd.DataFrame(movies_dict)
st.title("Movie Recommender System")
#function to fetch the poster of the movie
def fetch_poster(movie_id):
       data=requests.get('https://api.themoviedb.org/3/movie/{}?api_key=b1e53fd292f50cdb47bcc66ab7dcabea&language=en-US'.format(movie_id))
       data= data.json() #coverting it into json format
       poster_path = data['poster_path']
       full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
       return full_path
         
       

def recommend(movie):
     movie_index=movies[movies['title']==movie].index[0]
     distances=similarity[movie_index]
     movie_list=sorted(list(enumerate(distances)),reverse= True, key=lambda x:x[1])[1:6]
     recommended_list=[]
     recommend_movie_poster=[] #the recommend_movie_poster ill be appened
     for i in movie_list:
         movie_id=movies.iloc[i[0]].movie_id
         recommended_list.append(movies.iloc[i[0]].title)
         recommend_movie_poster.append(fetch_poster(movie_id))
     return recommended_list,recommend_movie_poster
        #print(movies.iloc[i[0]].title) instead of printing we will append the movies in the list

selected_movie_name = st.selectbox(  #code from documentation of streamlit
    'Search for your movie here',
    movies['title'].values)

st.write('You selected:', selected_movie_name )


if st.button('Recommend'):  
      recommended_list,recommend_movie_poster= recommend(selected_movie_name)  #calling the recommend function here
     
      col1, col2, col3, col4, col5 = st.columns(5)
      with col1:
          st.text(recommended_list[0])
          st.image(recommend_movie_poster[0])
      with col2:
          st.text(recommended_list[1])
          st.image(recommend_movie_poster[1])
      with col3:
          st.text(recommended_list[2])
          st.image(recommend_movie_poster[2])
      with col4:
          st.text(recommended_list[3])
          st.image(recommend_movie_poster[3])
      with col5:
          st.text(recommended_list[4])
          st.image(recommend_movie_poster[4])
    
        

