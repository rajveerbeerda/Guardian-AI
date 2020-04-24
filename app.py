from flask import Flask, request, jsonify, render_template, make_response, redirect, url_for, flash, sessions, session, get_flashed_messages
from firebase_config import firebaseConfig
import variables.guest_details as gd
import variables.other as ov
from get_details import *

import pyrebase
import pandas as pd

app = Flask(__name__)

app.secret_key = "abcdefgh"

firebase=pyrebase.initialize_app(firebaseConfig)
auth=firebase.auth()


@app.route('/', methods=["GET", "POST"])
def index():
    return render_template('index.html')

@app.route('/sign-in', methods=["GET", "POST"])
def signIn():
    if request.method=="POST":
        email = request.form['email']
        password = request.form['password']
        logIn=auth.sign_in_with_email_and_password(email,password)
        print(email, password)

    return render_template('signin.html')

@app.route('/sign-up', methods=["GET", "POST"])
def signUp():
    if request.method=="POST":
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        user = auth.create_user_with_email_and_password(email,password)
        print(name, email, password)
    return render_template('signup.html')

@app.route('/guest', methods=["GET", "POST"])
def guest():
    locations = getAllLocations()
    if request.method=="POST":
        gd.age = request.form["age"]
        gd.gender = request.form["gender"]
        gd.businessman = request.form["businessman"]
        gd.location = request.form["location"]
        return redirect(url_for('crimeDetails', city_name=gd.location, age = gd.age, gender=gd.gender, businessman=gd.businessman))
    return render_template('guest.html', locations = locations)

@app.route('/crime-details/area-<city_name>&age-<age>&gender-<gender>&businessman-<businessman>', methods=['GET', 'POST'])
def crimeDetails(city_name, age, gender, businessman):
    location = city_name
    df = pd.read_csv('data/area.csv')
    df = df[df['location']==location]

    school_count = df['#_schools'].iloc[0]
    park_count = df['#_parks'].iloc[0]
    hospital_count = df['#_hospitals'].iloc[0]
    restaurant_count = df['#_restaurants'].iloc[0]

    school_r = rating(school_count)
    park_r = rating(park_count)
    hospital_r = rating(hospital_count)
    restaurant_r = rating(restaurant_count)

    crimes_reported = 0

    if int(df['safety_index'])!=(-1):
        crimes_reported = 1
        age = age
        gender = gender
        businessman = businessman

        if request.method=="POST":
            if request.form['distance'] == '2.5km':
                ov.distance = 2.5
            elif request.form['distance'] == '5km':
                ov.distance = 5
            elif request.form['distance'] == '10km':
                ov.distance = 10

            return redirect(url_for('safeAreas', city_name=city_name, distance=ov.distance))

        news, crime_count, crime_ages, no_businessman, crimes, age_crimes, most_occ_crime, s = getData(location, int(age))
        if int(age)==0:
            crime_ages = -1

        si = safetyIndex(location)
        if si==0:
            si = 1
        address = getAddress(location)
    else:
        crimes_reported = 0
        age = gd.age
        gender = gd.gender
        businessman = gd.businessman

        news, crime_count, crime_ages, no_businessman, crimes, age_crimes, most_occ_crime, s = -1, -1, -1, -1, -1, -1, -1, -1
        si = -1
        address = getAddress(location)
        # email = session['user_email']
        # print(email)
        # if str(email)!=str(-1):
        #     details = getUserDetails(email)
        #     age = int(details[0])
        #     gender = str(details[1])
        #     businessman = str(details[2])
        #     print(age)
        # else:
        #     age = session['age']
        #     gender = session['gender']
        #     businessman = session['businessman']

    
    return render_template('crime-details.html', crimes_reported=crimes_reported, address=address, location=location, news=news,
                            crime_count=crime_count, crime_ages=crime_ages, no_businessman=no_businessman,
                            businessman=businessman, crimes=crimes, age_crimes=age_crimes,
                            most_occ_crime=most_occ_crime, s=s, si=si,
                            school_r=school_r, restaurant_r=restaurant_r, park_r=park_r, hospital_r=hospital_r)

@app.route('/safe-areas/area-<city_name>&distance-<distance>', methods=['GET', 'POST'])
def safeAreas(city_name, distance):
    src_loc = city_name
    dist = float(distance)
    safe_areas_lst, crime_area = getSafeLocations(src_loc, dist)

    return render_template('safe-areas.html', safe_areas_lst=safe_areas_lst, crime_area=crime_area, l=len(safe_areas_lst), src_loc=src_loc)

@app.route('/about', methods=['GET', 'POST'])
def about():
    return render_template('about.html')

if __name__ == '__main__':
    app.run(debug=True, port=5000)