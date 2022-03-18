from server import db
from server import loginManager
from flask_login import UserMixin


@loginManager.user_loader
def load_user(userId):
    return User.query.get(int(userId))

#every class represent a table
#every property represent a column
class User(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(20) , unique=True, nullable = False)
    email = db.Column(db.String(120) , unique=True, nullable = False)
    password = db.Column(db.String(50) , nullable = False)
    
    def __repr__(self):
        return f"User({self.userName},{self.email},{self.image})"

class Parking(db.Model):
    
    def __init__(self, input) -> None:
        super().__init__()
        self.lat=input['lat']
        self.lon=input['lon']
        self.parkName=input['parkName']
        
    id = db.Column(db.Integer, primary_key = True)
    lat = db.Column(db.String(10) , nullable = False)
    lon = db.Column(db.String(10) , nullable = False)
    parkName = db.Column(db.String(20) , nullable = False)
    places = db.relationship("Place", backref = 'parking', lazy=True)    
    
    def __repr__(self):
        return f"Parking({self.id}- {self.parkName},'{self.lat}-{self.lon}')"

class Place(db.Model):
    
    
    id = db.Column(db.Integer, primary_key = True)
    code = db.Column(db.String(20) , nullable = False)
    parking_id = db.Column(db.Integer, db.ForeignKey('parking.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'),nullable=True)
    reserved= db.Column(db.Boolean,default=False)
    
    def __repr__(self):
        return f"Place({self.code},userId({self.user_id},'{self.parking_id}',{self.reserved})"

def create():
    db.drop_all()
    db.create_all()


def load_test_data():
    create()
    db.session.add(Parking(lat='11',lon='22',parkName='p1'))   
    db.session.add(Parking(lat='22',lon='33',parkName='p2'))   
    db.session.add(Parking(lat='44',lon='55',parkName='p3'))
    db.session.add(Place(code='A',parking_id=1)) 
    db.session.add(Place(code='B',parking_id=1)) 
    db.session.add(Place(code='C',parking_id=1)) 
    db.session.commit()
    
    print('parkings')
    print(Parking.query.all())
    print('Places')
    print(Place.query.all())
    print('parking1 ')
    print(Parking.query.get(1).places)
    print(Place.query.get(1).parking)    