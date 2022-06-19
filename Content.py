import numpy as np
import pandas as pd
import sklearn
import random
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.cluster import KMeans
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.decomposition import PCA
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel

#Read data
places=pd.read_csv("Tourism_Datasets2.csv",encoding='windows-1254')

places = places[['City','Activity','Places']]

tfidf = TfidfVectorizer(stop_words='english')
places['Activity'] = places['Activity'].fillna('')
tfidf_matrix = tfidf.fit_transform(places['Activity'])
cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)
indices = pd.Series(places.index, index=places['Places']).drop_duplicates()

def get_recommendations(title):
    # Get the index of the movie that matches the title
    #df2= places[places['City']==city]
    #tfidf_matrix = tfidf.fit_transform(df2['Activity'])
    #cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)
    #indices = pd.Series(df2.index, index=df2['Places']).drop_duplicates()
    idx = indices[title]

    # Get the pairwsie similarity scores of all movies with that movie
    sim_scores = list(enumerate(cosine_sim[idx]))
        
    # Sort the movies based on the similarity scores
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    

    # Get the scores of the 10 most similar movies
    sim_scores = sim_scores[1:10]
    
    # Get the movie indices
    movie_indices = [i[0] for i in sim_scores]

    # Return the top 10 most similar movies
    return places[['Places','Activity']].iloc[movie_indices]
    
get_recommendations('Temple Of Karnak')

