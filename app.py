import streamlit as st
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

st.set_page_config(page_title="Movie Recommendation Agent")
st.title("🎬 Movie Recommendation Agent")

@st.cache_data
def load_data():
    df = pd.read_csv("movies.csv")
    df = df.dropna(subset=['Movie', 'Genre'])
    return df

df = load_data()

tfidf = TfidfVectorizer(stop_words='english')
tfidf_matrix = tfidf.fit_transform(df['Genre'])
cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)

movie_list = df['Movie'].tolist()
selected_movie = st.selectbox("🎥 Oka Movie ni select cheyyi", movie_list)

if st.button("Recommend Cheyyi 🔥"):
    idx = df[df['Movie'] == selected_movie].index[0]
    sim_scores = sorted(list(enumerate(cosine_sim[idx])), key=lambda x: x[1], reverse=True)[1:6]
    movie_indices = [i[0] for i in sim_scores]
    
    st.subheader(f"'{selected_movie}' laga unna 5 movies:")
    for i in movie_indices:
        st.write(f"**{df['Movie'].iloc[i]}** - {df['Genre'].iloc[i]}")
