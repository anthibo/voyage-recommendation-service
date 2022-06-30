from distutils.sysconfig import PREFIX
import json
from uuid import UUID
from flask import Flask, request,jsonify
import jwt 
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
from sqlalchemy import create_engine, false
import Content
from Content import get_recommendations,get_places_ratings


app = Flask(__name__)






def check(user, placesrating):
  if( (user) in placesrating['userId'].unique()):
    print('salaket')
    result=placesrating[placesrating['userId']==user]
    print('result')
    print(result)

    #result=placesrating[['Place','rating']] [placesrating['user_id']==user]
    places=result.loc[(result['rating'] >3)]
    activity = None
    if len(places) > 0:
        activity=places.groupby(['activity_type'])['rating'].mean().idxmax()
    # activities=places.groupby(['activity_type'])
    print(activity)
    
    #highval=res.Activity.max()
    return activity

JWT_SECRET='VoyageAppGraduationProject2022AnthiboSuhailaFarahMustafaSaieedTeamPlusUltraGGWPCatsVolleyCookingAyHaga'

def get_token(header):
    PREFIX = 'Bearer'
    if not header.startswith(PREFIX):
        raise ValueError('Invalid token')

    return header[len(PREFIX):]

@app.route('/home', methods=['GET', 'POST'])
def main():
    # get user from token then check for history
    if(request.method=='GET'):
        header = request.headers.get('Authorization')
        if not header:
            return {'error': 'EL TOKEN YA SOSO :DDDDDD'}, 403
        token = header[len('Bearer '):]
        print(token)
        
        # decode the token 
        user = jwt.decode(token, JWT_SECRET, algorithms="HS256")
        print(user)
        returned_response = {}
        
        placesrating = get_places_ratings()        
        place_titles = dict(zip(placesrating['placeId'], placesrating['name']))
     
        places_ids=placesrating['placeId'][placesrating['rating']==placesrating['rating'].max()].unique()
        place_id=places_ids[0]
        similar_ids = find_similar_movies(place_id, X, k=10)
        top_rated_places =[]
        for i in similar_ids:
            top_rated_places.append({"id": i, "name": place_titles[i]})
        returned_response['topRatedPlaces'] = top_rated_places
        activity = check(user=UUID(user['id']), placesrating = placesrating)
        suggested_places_flag = False
        if(activity != None):
            suggested_places_flag = True
            suggested_places = get_recommendations(activity, placesrating)
            print(suggested_places)
            returned_response['suggestedPlaces'] = suggested_places
            returned_response['activity'] = activity
        returned_response['suggestedPlacesFlag'] = suggested_places_flag
            
        return returned_response

          
    if(request.method=='POST'):
        req_JSON=request.json
        value=req_JSON['value']
        return jsonify({"response":"Hi"})
   

if __name__ == '__main__':
    app.run()