from tkinter import *
from tkinter.colorchooser import askcolor
from turtle import color
from PIL import ImageTk,Image
from sqlalchemy import true
from server import db
from server import loginManager
from flask_login import UserMixin
import cv2 as cv

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
        return f"User({self.username},{self.password})"

class Parking(db.Model):
    
    def __init__(self):
        super().__init__()
    def __init__(self, input):
        super().__init__()
        self.lat=input['lat']
        self.lon=input['lon']
        self.parkName=input['parkName']
        self.camerIP=input['cameraIP']
       
     
        
    id = db.Column(db.Integer, primary_key = True)
    
    lat = db.Column(db.String(10) , nullable = False)
    lon = db.Column(db.String(10) , nullable = False)
    parkName = db.Column(db.String(20) , nullable = False)
    imagePath = db.Column(db.String(200) , nullable = True)
    camerIP = db.Column(db.String(200) , nullable = True)
    
    places = db.relationship("Place", backref = 'parking', lazy=True)    
    
    def getId():
        return id
    def __repr__(self):
        return f"Parking({self.id}- {self.parkName},'{self.imagePath}')"

class Place(db.Model):
    
    
    id = db.Column(db.Integer, primary_key = True)
    code = db.Column(db.String(20) , nullable = False)
    parking_id = db.Column(db.Integer, db.ForeignKey('parking.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'),nullable=True)
    reserved= db.Column(db.Boolean,default=False)
    
    posx = db.Column(db.Float, nullable = True)
    posy = db.Column(db.Float, nullable = True)
    widthRatio = db.Column(db.Float, nullable = True)
    heightRatio = db.Column(db.Float, nullable = True)
    
    

    def __repr__(self):
        return f"Place({self.code},userId({self.posx},'{self.parking_id}',{self.reserved})"

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
    
    


class Paint(object):

    DEFAULT_PEN_SIZE = 5.0
    DEFAULT_COLOR = 'red'
    IMAGESIZE=(1400,800)
    rects=[]
 
    def __init__(self,imagePath,pid):
        self.root = Tk()
        self.parking=Parking.query.filter_by(id=pid).first()
        self.rowCounter=0
        im=Image.open(imagePath)
        self.image= ImageTk.PhotoImage(im.resize(Paint.IMAGESIZE))
       
        self.insert_down_button = Button(self.root, text='insert below', command=self.insert_down)
        self.insert_down_button.grid(row=0, column=0)

        self.insert_down_button = Button(self.root, text='insert right', command=self.insert_right)
        self.insert_down_button.grid(row=0, column=1)
        
        self.code_label=Label(self.root,text="A")
        self.code_label.grid(row=0,column=2)
        
        self.changeCode_button = Button(self.root, text='next row', command=self.changeCode)
        self.changeCode_button.grid(row=0, column=3)
        
        self.changeCode_button = Button(self.root, text='save', command=self.save)
        self.changeCode_button.grid(row=0, column=4)

        

        
        self.c = Canvas(self.root, bg='white',
                        width=Paint.IMAGESIZE[0],height=Paint.IMAGESIZE[1])
        self.c.grid(row=1,columnspan=20,sticky=N+S+W+E)

        self.root.state('zoomed')
        self.setup()
        
        self.root.mainloop()

    def setup(self):
        self.old_x = None
        self.old_y = None
        self.line_width = 1
        self.color = self.DEFAULT_COLOR
        self.eraser_on = False
        self.active_button = self.insert_down_button
        self.c.bind('<Button-1>', self.selectPostion)
        self.c.bind('<B1-Motion>', self.update)
        self.c.bind('<Button-3>',self.delteRect)
        self.c.bind('<ButtonRelease-1>', self.paint)
        self.c.create_image(0,0,image=self.image,anchor=NW)

   
    def insert_down(self):
        if(len(self.rects)):
            
            rect=self.rects[-1]
            y=rect.y+(rect.hratio*self.image.height())
            self.rowCounter+=1
            code=self.code_label.cget('text')+str(self.rowCounter)
            self.rects.append(placeRect(rect.x,y,rect.wratio,rect.hratio,code))
            current=self.rects[-1]
            width=current.wratio*self.image.width()
            height=current.hratio*self.image.height()
            
            self.rect=self.c.create_rectangle(current.x, current.y, current.x+width, current.y+height,
                                            width=self.line_width,tags="rect"+str(placeRect.count-1))
          
            
    def insert_right(self):
        if(len(self.rects)):
            
            rect=self.rects[-1]
            x=rect.x+(rect.wratio*self.image.width())
            self.rowCounter+=1
            code=self.code_label.cget('text')+str(self.rowCounter)
            self.rects.append(placeRect(x,rect.y,rect.wratio,rect.hratio,code))
            current=self.rects[-1]
            width=current.wratio*self.image.width()
            height=current.hratio*self.image.height()
            
            self.rect=self.c.create_rectangle(current.x, current.y, current.x+width, current.y+height,
                                            width=self.line_width,tags="rect"+str(placeRect.count-1))
      
            
    def changeCode(self):
        text=self.code_label.cget('text')
        self.code_label.config(text= chr(ord(text)+1))
        self.rowCounter=0
        
    def use_brush(self):
        self.activate_button(self.brush_button)

    def choose_color(self):
        self.eraser_on = False
        self.color = askcolor(color=self.color)[1]

    def use_eraser(self):
        self.activate_button(self.eraser_button, eraser_mode=True)

    def activate_button(self, some_button, eraser_mode=False):
        self.active_button.config(relief=RAISED)
        some_button.config(relief=SUNKEN)
        self.active_button = some_button
        self.eraser_on = eraser_mode

    def update(self,event):
        curX, curY = (event.x, event.y)

        # expand rectangle as you drag the mouse
        self.c.coords(self.rect, self.old_x, self.old_y, curX, curY) 
        
    def paint(self, event):
        wratio= (event.x-self.old_x)/ self.image.width()
        hratio= (event.y-self.old_y )/ self.image.height()
     
        self.rowCounter+=1
        code=self.code_label.cget('text')+str(self.rowCounter)
        self.rects.append(placeRect(self.old_x,self.old_y,wratio,hratio,code))
    
    def selectPostion(self,event):
        
        self.old_x=event.x
        self.old_y=event.y
        self.rect=self.c.create_rectangle(self.old_x, self.old_y,self.old_x+ 1,self.old_y+ 1,
                                        
                                        width=self.line_width,tags="rect"+str(placeRect.count))
    def delteRect(self,event):

        for rect in self.rects:
            if (event.x<=(rect.x+(rect.wratio*self.image.width())) 
            and event.x>rect.x
            and event.y>rect.y
            and event.y <= (rect.y+(rect.hratio*self.image.height()))
            ):
                self.c.delete(rect.tag)

                self.rects.remove(rect)
            
            
        if placeRect.count>=1 :
             placeRect.count = placeRect.count-1 
       
       
        
        
    def save(self):
        for rect in self.rects:
            place=Place()
            place.code=rect.code
            place.parking_id=self.parking.id
            place.posx=rect.x
            place.posy=rect.y
            place.heightRatio=rect.hratio
            place.widthRatio=rect.wratio
            db.session.add(place)
        db.session.commit()
  
            
    def reset(self, event):
        self.old_x, self.old_y = None, None
    
class placeRect():
    count=0
    
    def __init__(self,x,y,widthration,Heithration,code) -> None:
        self.x,self.y,self.wratio,self.hratio = (x,y,widthration,Heithration)
        self.tag='rect'+str(placeRect.count)
        self.code=code
        placeRect.count+=1
        