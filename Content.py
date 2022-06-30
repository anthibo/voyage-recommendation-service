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
from sqlalchemy import create_engine

#Read data
database_url = 'postgresql://zcczqdxovrvwch:0e7ce6d159becf9918fe22b5f706f6ddfc3279a38bf4e03320554b53d82150b4@ec2-23-23-151-191.compute-1.amazonaws.com:5432/d2iap8c27jv8o8'
engine = create_engine(database_url)

def get_places_ratings():
   placesrating=pd.read_sql('select place_ratings."placeId", place_ratings."userId", place_ratings."rating", places."name", places."activity_type" from place_ratings inner join places on place_ratings."placeId" = places.id ;',engine)
   return placesrating
def get_recommendations(activity, placesrating):
 df = placesrating
 tfidf = TfidfVectorizer(stop_words='english')
 df['activity_type'] = df['activity_type'].fillna('')
 tfidf_matrix = tfidf.fit_transform(df['activity_type'])
 cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)
 indices = pd.Series(df.index,index=df['activity_type']).drop_duplicates()
 idx = indices[activity][0]
    # Get the pairwsie similarity scores of all movies with that movie
 sim_scores = list(enumerate(cosine_sim[idx]))
           # Sort the movies based on the similarity scores
 sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    # Get the scores of the 10 most similar movies
  # Get the scores of the 10 most similar movies
 rec_places=[]
 recom_titles = dict(zip(df.index,df['name']))

 sim_scores = sim_scores[1:10]
 
 places_ids = [i[0] for i in sim_scores]
 for place_id in places_ids:
     rec_places.append({"id":df['placeId'].iloc[place_id], "Places":recom_titles[place_id]})
     
 return (rec_places)

