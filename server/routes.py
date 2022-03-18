import json
from flask import jsonify, render_template, request
from server import app,bcrypt
from server.models import *
from flask_login import login_user,logout_user,current_user,login_required


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template("index.html")

#user model requests
@app.route('/register', methods=['POST'])
def register():
    if current_user.is_authenticated:
         return {'success':False,
                'message':'user was loged in'}

    #get information
    uname=request.json['username']
    uemail=request.json['email']
    upassword= request.json['password']
    #check if the username was tacken
    user = User.query.filter_by(username=uname).first()
    if(user):
        return {'success':False,
                'message':'user name was tacken'}
    else:
    #check if the email was registered before
        user = User.query.filter_by(email=uemail).first()
        if user:
            return {'success':False,
                'message':'there is user with the same email'}
    #crypt the password
    crypted_pass = bcrypt.generate_password_hash(upassword).decode('utf_8')
    #add the user to the data base
    user = User(username= uname,email=uemail, password=crypted_pass)
    db.session.add(user)
    db.session.commit()
    return {'success':True,
            'message':'success to add user'}

@app.route('/login', methods=['POST'])
def login():
    # if(current_user.is_authenticated):
    #     return {'success':'false',
    #             'message':'user was loged in'}

    #get information
    uname=request.json['username']
    upassword= request.json['password']
    #check if there is user with the user name 
    #and check password
    user = User.query.filter_by(username=uname ).first()
    #the password checked with a ciphered mode for security issues
    if(user and bcrypt.check_password_hash(user.password,upassword)):
        login_user(user)
        return {'success':'true',
                'message':'success to login'}
    else:
            return {'success':'false',
                'message':'user name or password is incorrect'}

@app.route('/logout', methods=['GET', 'POST'])
def logout():
    logout_user()
    return {'success':True,
                'message':'user logedout'}

#parking model routes
@app.route('/parkings', methods=['POST','GET'])
def getAllParkings():
    allParking=Parking.query.all()
    output = []
    for parking in allParking:
        output.append({
        'id': parking.id,
        'lat' : parking.lat,
        'lon' : parking.lon,
        'parkName':parking.parkName,
                     })
    return jsonify(output)

@app.route('/addParking', methods=['POST'])
def addParking():
    #get information
    input = {
        'lat':request.json['lat'],
        'lon': request.json['lon'],
        'parkName': request.json['parkName']
    }
    
   
    #check if there is user with the user name 
    #and check password
    parking = Parking.query.filter_by(lat=input['lat'] , lon=input['lon']).first()
    #the password checked with a ciphered mode for security issues
    if(parking):
         return {'success':'false',
                'message':'Parking already exist'}
    else:
        
        parking= Parking(input)
        db.session.add(parking)
        db.session.commit()
        return {'success':'true',
                'message':'success to add parking'}

@app.route('/Parkings/<qlat>,<qlon>/<qdistance>', methods=['GET'])
def getNearParkings(qlat,qlon,qdistance):
    parks=filter(lambda p: distance(p.lat,qlat,p.lon,qlon)<=float(qdistance),Parking.query.all())
    output=[]
    for p in parks:
      output.append({
          f'{p.id}':str(p)
      })  
    return  jsonify( output)
#places model routes
@app.route('/places/<parkingId>', methods=['POST'])
def getFreePlaces(parkingId):
    places= filter(lambda p: True, Parking.query.get(parkingId).places)
    output = []
    for place in places:
        output.append({
        'id': place.id,
        'code' : place.code,
        'text':str(place)
       
                     })
    return jsonify(output)

@app.route('/reserve/<placeid>', methods=['PUT'])
def reservePlace(placeid):
    input= {
        'userId':request.json['userId']
    }
    place=Place.query.get(placeid)
    if place and not place.reserved:
        place.reserved=True
        place.user_id = input['userId']
        db.session.commit()
        return "true"
    else:
        return "False"
    
@app.route('/unreserve/<placeid>', methods=['PUT'])
def unreservePlace(placeid):
    
    place=Place.query.get(placeid)
    if place and place.reserved:
        place.reserved=False
        place.user_id=None
        db.session.commit()
        return "true"
    else:
        return "False"

@app.route('/addPlaces/<parkingId>', methods=['POST'])
def addPlaces(parkingId):
    
    for jcode in request.json:
        place=Place.query.filter_by(code=jcode,parking_id=parkingId).first()
        if not place:
            db.session.add(Place(code=jcode,parking_id=parkingId))
    db.session.commit()
    return "true"

from math import radians,sin,asin,sqrt,cos

def distance(slat1, slat2, slon1, slon2):
     
    # The math module contains a function named
    # radians which converts from degrees to radians.
    lat1=float(slat1)
    lat2= float(slat2)
    lon1= float(slon1)
    lon2=float(slon2)
    lon1 = radians(lon1)
    lon2 = radians(lon2)
    lat1 = radians(lat1)
    lat2 = radians(lat2)
      
    # Haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
 
    c = 2 * asin(sqrt(a))
    
    # Radius of earth in kilometers. Use 3956 for miles
    r = 6371
      
    # calculate the result
    return(c * r)