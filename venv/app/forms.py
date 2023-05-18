from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField, DateField, SelectField, TextAreaField, HiddenField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo, NumberRange
from app.models import User
from flask_login import current_user
from datetime import datetime

class LogInForm(FlaskForm):
    ashoka_id=IntegerField('Ashoka ID', validators=[DataRequired()])  
    password=PasswordField('Password', validators=[DataRequired()])
    remember_me=BooleanField('Remember Me')


class RegistrationForm(FlaskForm):
    #ashoka_email = StringField('Ashoka Email ID', validators=[DataRequired(), Email()])
    ashoka_id = IntegerField('Ashoka ID', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_ashoka_id(self, ashoka_id):
        user = User.query.filter_by(ashoka_id=ashoka_id.data).first()
        if user is not None:
            raise ValidationError('Ashoka ID already exists')
        
        if len(str(ashoka_id.data)) != 10:
            raise ValidationError('Enter a valid Ashoka ID')
        
        
class UserDetailsForm(FlaskForm):
    name=StringField('Name', validators=[DataRequired()])
    ashoka_email=StringField('Ashoka Email', validators=[DataRequired(), Email()])    
    flat=IntegerField('Flat Number', validators=[DataRequired()])
    floor=SelectField('Floor', choices=[('GF','Ground Floor'),('FF','First Floor'),('SF','Second Floor'),('TF','Third Floor'),('Duplex','Duplex')],validators=[DataRequired()])
    room=IntegerField('Room Number', validators=[DataRequired()])
    submit=SubmitField('Continue')  

    def validate_ashoka_email(self, ashoka_email):
        user = User.query.filter_by(ashoka_email = (ashoka_email.data).lower()).first()
        if user is not None:
            raise ValidationError('Email already exists')
        
    def validate_flat(self, flat):
        if flat.data < 119 or flat.data > 180:
            raise ValidationError('Enter a flat number from 119 to 180')
        
    def validate_room(self, room):
        if room.data < 1 or room.data > 4:
            raise ValidationError('Please enter a room number from 1 to 4')

        

class EditProfileForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    ashoka_email=StringField('Ashoka Email')
    ashoka_id=IntegerField('Ashoka ID') 
    flat=IntegerField('Flat Number', validators=[DataRequired()])
    floor=SelectField('Floor', choices=[('GF','Ground Floor'),('FF','First Floor'),('SF','Second Floor'),('TF','Third Floor'),('Duplex','Duplex')],validators=[DataRequired()])
    room=IntegerField('Room Number', validators=[DataRequired()])

    def validate_flat(self, flat):
        if flat.data < 119 or flat.data > 180:
            raise ValidationError('Enter a flat number from 119 to 180')
        
    def validate_room(self, room):
        if room.data < 1 or room.data > 4:
            raise ValidationError('Enter a room number from 1 to 4')

    #def validate_ashoka_id(self, ashoka_id):
    #    user = User.query.filter_by(ashoka_id=ashoka_id.data).all()
    #    if current_user in user:
    #        user.remove(current_user)
    #    if len(user)!=0:
    #        raise ValidationError('Ashoka ID already exists')
        
    #def validate_ashoka_email(self, ashoka_email):
    #    user_mail = User.query.filter_by(ashoka_email=ashoka_email.data).all()
    #    if current_user in user_mail:
    #        user_mail.remove(current_user)
    #    if len(user_mail)!=0:
    #        raise ValidationError('Ashoka email already exists')


class MealForm(FlaskForm):
    meal_date = DateField('Date')
    breakfast = SelectField('Breakfast', choices=[('', 'Select an Option'), ('Without Eggs', 'Without Eggs'), ('With Eggs','With Eggs')])
    lunch = SelectField('Lunch', choices=[('', 'Select an Option'), ('Vegetarian', 'Vegetarian'), ('Non - Vegetarian','Non - Vegetarian')])
    snacks = SelectField('Snacks', choices=[('', 'Select an Option'), ('Snacks', 'Yes')])
    dinner = SelectField('Dinner', choices=[('', 'Select an Option'), ('Vegetarian', 'Vegetarian'), ('Non - Vegetarian','Non - Vegetarian')])
    remarks = TextAreaField('Remarks')
    access = HiddenField ("Access")
    today = HiddenField ("Today")

    
    def validate_meal_date(self, meal_date):
        today = datetime.strptime(datetime.now().strftime('%Y-%m-%d'), '%Y-%m-%d').date()
        if self.meal_date.data == None:
            raise ValidationError('Select a valid date')
        elif self.meal_date.data < today:
            raise ValidationError('Cannot book meals for this date')
            

    def validate_breakfast(self, breakfast):
        today = datetime.strptime(datetime.now().strftime('%Y-%m-%d'), '%Y-%m-%d').date()
        if self.meal_date.data == today:
            if breakfast.data != '':
                raise ValidationError('Cutoff time has passed') 
            
    def validate_lunch(self, lunch):
        today = datetime.strptime(datetime.now().strftime('%Y-%m-%d'), '%Y-%m-%d').date()
        time = datetime.strptime(datetime.now().strftime('%H:%M:%S'),'%H:%M:%S')
        if self.meal_date.data == today:
            if time >= datetime.strptime('10:00:00','%H:%M:%S'):
                if lunch.data != '':
                    raise ValidationError('Cutoff time has passed') 
                
    def validate_snacks(self, snacks):
        today = datetime.strptime(datetime.now().strftime('%Y-%m-%d'), '%Y-%m-%d').date()
        time = datetime.strptime(datetime.now().strftime('%H:%M:%S'),'%H:%M:%S')
        if self.meal_date.data == today:
            if time >= datetime.strptime('14:00:00','%H:%M:%S'):
                if snacks.data != '':
                    raise ValidationError('Cutoff time has passed') 
                
    def validate_dinner(self, dinner):
        today = datetime.strptime(datetime.now().strftime('%Y-%m-%d'), '%Y-%m-%d').date()
        time = datetime.strptime(datetime.now().strftime('%H:%M:%S'),'%H:%M:%S')
        if self.meal_date.data == today:
            if time >= datetime.strptime('17:00:00','%H:%M:%S'):
                if dinner.data != '':
                    raise ValidationError('Cutoff time has passed') 
            

class HouseForm(FlaskForm):
    slots=['9 am - 10 am', '10 am - 11 am', '11 am - 12 pm', '12 pm - 1 pm', '1 pm - 2 pm', '3 pm - 4 pm', '4 pm - 5 pm', 'ASAP']
    now_time=datetime.strptime(datetime.now().strftime('%H:%M:%S'),'%H:%M:%S')
    choices=[]
    if now_time >= datetime.strptime('15:45:00','%H:%M:%S'):
        cutoff='ASAP'
    elif now_time >= datetime.strptime('14:45:00','%H:%M:%S'):
        cutoff='4 pm - 5 pm'
    elif now_time >= datetime.strptime('12:45:00','%H:%M:%S'):   
        cutoff='3 pm - 4 pm'
    elif now_time >= datetime.strptime('11:45:00','%H:%M:%S'): 
        cutoff='1 pm - 2 pm'
    elif now_time >= datetime.strptime('10:45:00','%H:%M:%S'):
        cutoff='12 pm - 1 pm'
    elif now_time >= datetime.strptime('09:45:00','%H:%M:%S'):
        cutoff='11 am - 12 pm'
    elif now_time >= datetime.strptime('08:45:00','%H:%M:%S'):
        cutoff='10 am - 11 am'
    else:
        cutoff='9 am - 10 am'

    for i in range(slots.index(cutoff), len(slots)):
        choices+=[(slots[i], slots[i])]

    time_slot=SelectField('Time Slot', choices=choices, validators=[DataRequired()])
    remarks=TextAreaField('Remarks')


class MaintenanceForm(FlaskForm):
    remarks=TextAreaField('Remarks')

    def validate_remarks(self, remarks):
        if remarks.data.strip() == '':
            raise ValidationError('Remarks Field Cannot be Empty') 


class HouseEditForm(FlaskForm):
    slots=['9 am - 10 am', '10 am - 11 am', '11 am - 12 pm', '12 pm - 1 pm', '1 pm - 2 pm', '3 pm - 4 pm', '4 pm - 5 pm']
    now=datetime.now().strftime('%H:%M:%S')
    now_time=datetime.strptime(now,'%H:%M:%S')
    choices=[]

    if now_time >= datetime.strptime('14:45:00','%H:%M:%S'):
        cutoff='4 pm - 5 pm'
    elif now_time >= datetime.strptime('12:45:00','%H:%M:%S'):   
        cutoff='3 pm - 4 pm'
    elif now_time >= datetime.strptime('11:45:00','%H:%M:%S'): 
        cutoff='1 pm - 2 pm'
    elif now_time >= datetime.strptime('10:45:00','%H:%M:%S'):
        cutoff='12 pm - 1 pm'
    elif now_time >= datetime.strptime('09:45:00','%H:%M:%S'):
        cutoff='11 am - 12 pm'
    elif now_time >= datetime.strptime('08:45:00','%H:%M:%S'):
        cutoff='10 am - 11 am'
    else:
        cutoff='9 am - 10 am'

    for i in range(slots.index(cutoff), len(slots)):
        choices+=[(slots[i], slots[i])]

    time_slot=SelectField('Time Slot', choices=choices+[('ASAP','ASAP')], validators=[DataRequired()])
    remarks=TextAreaField('Remarks')

class MainEditForm(FlaskForm):
    remarks=TextAreaField('Remarks')

    def validate_remarks(self, remarks):
        if remarks.data.strip() == '':
            raise ValidationError('Remarks Field Cannot be Empty') 

class MealEditForm(FlaskForm):
    meal_date = DateField('Meal Date', render_kw={'disabled':''})
    breakfast_access = HiddenField('Breakfast Access')
    lunch_access = HiddenField('Lunch Access')
    snacks_access = HiddenField('Snacks Access')
    dinner_access = HiddenField('Dinner Access')
    condition = HiddenField('Condition')
    breakfast = SelectField('Breakfast', choices=[('', 'Select an Option'), ('Without Eggs', 'Without Eggs'), ('With Eggs','With Eggs')])
    lunch = SelectField('Lunch', choices=[('', 'Select an Option'), ('Vegeteraian', 'Vegetarian'), ('Non - Vegetarian','Non - Vegetarian')])
    snacks = SelectField('Snacks', choices=[('', 'Select an Option'), ('Snacks', 'Yes')])
    dinner = SelectField('Dinner', choices=[('', 'Select an Option'), ('Vegeteraian', 'Vegetarian'), ('Non - Vegetarian','Non - Vegetarian')])
    remarks = TextAreaField('Remarks')