from app import db, login
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, nullable=True, primary_key=True)
    name = db.Column(db.String, nullable=True, index=True)
    ashoka_id = db.Column(db.Integer, nullable=True, index=True, unique=True)
    #phone_number=db.Column(db.Integer, nullable=True, index=True)
    ashoka_email = db.Column(db.String, nullable=True, index=True, unique=True)
    flat=db.Column(db.String, nullable=True, index=True)
    room=db.Column(db.Integer, nullable=True, index=True)
    #occupation=db.Column(db.String, nullable=False, index=True)
    #course=db.Column(db.String, nullable=True, index=True)
    #department=db.Column(db.String, nullable=False, index=True)
    password_hash = db.Column(db.String, nullable=True)
    hk_requests = db.relationship('Housekeeping', backref='user', lazy='dynamic' )
    main_requests = db.relationship('Maintenance', backref='user', lazy='dynamic' )
    meal_requests = db.relationship('Mealbooking', backref='user', lazy='dynamic' )
    all_requests = db.relationship('Requests', backref='user', lazy='dynamic' )
    
    def __repr__(self):
        return '<User {}>'.format(self.ashoka_id)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password) 
    
class Mealbooking(db.Model):
    Sr_No = db.Column(db.Integer, primary_key=True)
    ref=db.Column(db.String, nullable= True)
    ashoka_id = db.Column(db.Integer, db.ForeignKey('user.ashoka_id'), nullable=True)
    meal_date = db.Column(db.String, nullable=True)
    name = db.Column(db.String, nullable=True)
    apts_number = db.Column(db.String, nullable=True)
    room_no = db.Column(db.String, nullable=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.now)
    date = db.Column(db.String, index=True)
    time = db.Column(db.String, index=True)
    type = db.Column(db.String, index=True, default='Mealbooking')
    status = db.Column(db.String, index=True, default='Pending')
    #mobile_number = db.Column(db.String(20), nullable=False)
    breakfast = db.Column(db.String, nullable=True)
    lunch = db.Column(db.String, nullable=True)
    snacks = db.Column(db.String, nullable=True)
    dinner = db.Column(db.String, nullable=True)
    remarks = db.Column(db.String, nullable=True)
    
    def __repr__(self):
        return f'Meal(Sr_No={self.Sr_No}, date={self.date})'    


class Housekeeping(UserMixin, db.Model):
    id = db.Column(db.Integer, nullable=True, primary_key=True)
    ref=db.Column(db.Integer, nullable= True)
    name = db.Column(db.String, nullable=True, index=True)
    ashoka_id = db.Column(db.Integer, db.ForeignKey('user.ashoka_id'), nullable=True)
    flat=db.Column(db.String, nullable=True, index=True)
    room=db.Column(db.Integer, nullable=True, index=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.now)
    date=db.Column(db.String, index=True)
    time=db.Column(db.String, index=True)   
    time_slot = db.Column(db.String, nullable=True)
    body = db.Column(db.String, nullable=True)
        
    def __repr__(self):
      return "<Time {}>".format(self.time_slot)
    

class Maintenance(UserMixin, db.Model):
    id = db.Column(db.Integer, nullable=True, primary_key=True)
    ref=db.Column(db.Integer, nullable= True)
    name = db.Column(db.String, nullable=True, index=True)
    ashoka_id = db.Column(db.Integer, db.ForeignKey('user.ashoka_id'), nullable=True)
    flat=db.Column(db.String, nullable=True, index=True)
    room=db.Column(db.Integer, nullable=True, index=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.now)
    time=db.Column(db.String, index=True)
    date=db.Column(db.String, index=True)
    body = db.Column(db.String, nullable=True)

    def __repr__(self):
      return "<Request {}>".format(self.body)
    

class Requests(UserMixin, db.Model):
    id = db.Column(db.Integer, nullable=True, primary_key=True)
    ref=db.Column(db.String, nullable= True)
    name = db.Column(db.String, nullable=True, index=True)
    ashoka_id = db.Column(db.Integer, db.ForeignKey('user.ashoka_id'), nullable=True)
    flat=db.Column(db.String, nullable=True, index=True)
    room=db.Column(db.Integer, nullable=True, index=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.now)
    date=db.Column(db.String, index=True)
    time=db.Column(db.String, index=True)
    type=db.Column(db.String, nullable=True, index=True)
    status=db.Column(db.String, nullable=True, index=True, default='Pending')
    time_slot = db.Column(db.String, nullable=True)
    meal_date = db.Column(db.String, nullable=True)
    breakfast = db.Column(db.String, nullable=True)
    lunch = db.Column(db.String, nullable=True)
    snacks = db.Column(db.String, nullable=True)
    dinner = db.Column(db.String, nullable=True)
    body = db.Column(db.String, nullable=True)

    def __repr__(self):
      return "<Type {}>".format(self.type)


@login.user_loader
def load_user(id):
    return User.query.get(int(id))