import difflib
import pandas as pd
import numpy as np
import sklearn
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from scipy.sparse import csr_matrix
from sklearn.neighbors import NearestNeighbors
from sqlalchemy import create_engine

database_url = 'postgresql://zcczqdxovrvwch:0e7ce6d159becf9918fe22b5f706f6ddfc3279a38bf4e03320554b53d82150b4@ec2-23-23-151-191.compute-1.amazonaws.com:5432/d2iap8c27jv8o8'
engine = create_engine(database_url)
placesrating=pd.read_sql('select place_ratings."placeId", place_ratings."userId", place_ratings."rating", places."name", places."activity_type" from place_ratings inner join places on place_ratings."placeId" = places.id ;',engine)

# print(placesrating)
# placesrating = pd.read_sql("place_ratings",engine)
print(placesrating)




def create_matrix(df):
      
    N = len(df['userId'].unique())
    M = len(df['placeId'].unique())
      
    # Map Ids to indices
    user_mapper = dict(zip(np.unique(df["userId"]), list(range(N))))
    place_mapper = dict(zip(np.unique(df["placeId"]), list(range(M))))
  
      
    # Map indices to IDs
    user_inv_mapper = dict(zip(list(range(N)), np.unique(df["userId"])))
    place_inv_mapper = dict(zip(list(range(M)), np.unique(df["placeId"])))
      
    user_index = [user_mapper[i] for i in df['userId']]
    place_index = [place_mapper[i] for i in df['placeId']]
  
    X = csr_matrix((df["rating"], (place_index, user_index)), shape=(M, N))
      
    return X, user_mapper, place_mapper, user_inv_mapper, place_inv_mapper
  
X, user_mapper, place_mapper, user_inv_mapper, place_inv_mapper = create_matrix(placesrating)


#collobarative
#getting similar movies
def find_similar_movies(place_id, X, k, metric='cosine', show_distance=False):
      
    neighbour_ids = []

    place_ind = place_mapper[place_id]
    place_vec = X[place_ind]
    k+=1
    kNN = NearestNeighbors(n_neighbors=k, algorithm="brute", metric=metric)
    kNN.fit(X)
    place_vec = place_vec.reshape(1,-1)
    neighbour = kNN.kneighbors(place_vec, return_distance=show_distance)
    for i in range(0,k):
        n = neighbour.item(i)
        neighbour_ids.append(place_inv_mapper[n])
    neighbour_ids.pop(0)
    return neighbour_ids
  
  

