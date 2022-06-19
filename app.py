import json
from flask import Flask, request,jsonify
import difflib
import pandas as pd
import numpy as np
import sklearn
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from scipy.sparse import csr_matrix
from sklearn.neighbors import NearestNeighbors
import Collaborative
from Collaborative import placesrating,create_matrix,find_similar_movies,X
from sqlalchemy import create_engine


app = Flask(__name__)



#read data in sql

#print(placesrating)
#place_titles = dict(zip(placesrating['placeId'], placesrating['name']))
#print('place_titles')
#rint(place_titles)
#place_id=placesrating.max()['placeId']
#print('place id is')
#print(place_id)
#similar_ids = find_similar_movies(place_id, X, k=2)
#place_title = place_titles['name']



  





@app.route('/test', methods=['GET', 'POST'])
def main():
    if(request.method=='GET'):
        place_titles = dict(zip(placesrating['placeId'], placesrating['name']))
        places_ids=placesrating['placeId'][placesrating['rating']==placesrating['rating'].max()].unique()
        place_id=places_ids[0]
        similar_ids = find_similar_movies(place_id, X, k=10)
        rec_places =[]
        print('recommended places are ')
        print(similar_ids)
        for i in similar_ids:
            rec_places.append({"id": i, "name": place_titles[i]})

        # if(user.hasHistory):
        #     content-based code
        #     push data to response
            
        return jsonify({'places': rec_places})


          
    if(request.method=='POST'):
        req_JSON=request.json
        value=req_JSON['value']
        return jsonify({"response":"Hi"})
   

if __name__ == '__main__':
    app.run()