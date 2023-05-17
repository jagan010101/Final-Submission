from flask import render_template, flash, redirect, url_for, request
import pandas as pd 
from app import app, db
from app.forms import LogInForm, RegistrationForm, UserDetailsForm, MealForm, EditProfileForm, HouseForm, MaintenanceForm, HouseEditForm, MainEditForm, MealEditForm
from app.models import User, Housekeeping, Maintenance, Requests, Mealbooking
from flask_login import current_user, login_user, logout_user, login_required
from datetime import date, datetime, timedelta
from werkzeug.urls import url_parse
from flask.globals import request
import pandas as pd
from flask_mail import Message
from app import mail

########## Back Space problem ##########
########## Migrations Downgrade Problem ##########
@app.route('/', methods=['GET', 'POST'])
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form=LogInForm()

    if form.validate_on_submit():
            user = User.query.filter_by(ashoka_id=form.ashoka_id.data).first()
            if user is None or not user.check_password(form.password.data):
                flash('Invalid username or password')
                return redirect(url_for('login'))
        
            login_user(user, remember=form.remember_me.data)

            if current_user.ashoka_id == 1000:
                return redirect(url_for('admin'))
            else:
                return redirect(url_for('home'))
            
    else:  
        return render_template('login.html', title='Sign In', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(ashoka_id=form.ashoka_id.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Please Login to Continue')
        return redirect(url_for('login'))
    return render_template('registration.html', title='Register', form=form)


@app.route('/user_details', methods=['GET', 'POST'])
@login_required
def user_details():
    if current_user.ashoka_id == 1000:
        return redirect(url_for('admin'))
    
    if current_user.name != None:
        return redirect(url_for('home'))

    form=UserDetailsForm()
    if form.validate_on_submit():
          current_user.name=form.name.data
          current_user.ashoka_email=form.ashoka_email.data
          current_user.flat=str(form.flat.data) + " " + str(request.form.get('floor'))
          current_user.room=form.room.data
          db.session.commit()
          return redirect(url_for('login'))
    else:
          return render_template('user_details.html', title='Register', form=form)
    
     
@app.route('/admin_home_page Ashoka_University_Off_Campus_Residence TDI_LAKE_GROVE', methods=['GET', 'POST'])
@login_required
def admin():
    if current_user.ashoka_id != 1000:
        logout_user()
        return redirect(url_for('login'))
    
    if request.method == 'POST':
         if request.form.get('admin_action')[0]=='h':
              req=Housekeeping.query.filter_by(id=request.form.get('admin_action')[1:]).first()
              user_req=Requests.query.filter_by(id=req.ref).first()
              user_req.status="Completed"
              db.session.delete(req)
              db.session.commit()
              return redirect(url_for('admin'))
         
         if request.form.get('admin_action')[0]=='m':
              req=Maintenance.query.filter_by(id=request.form.get('admin_action')[1:]).first()
              user_req=Requests.query.filter_by(id=req.ref).first()
              user_req.status="Completed"
              db.session.delete(req)
              db.session.commit()
              return redirect(url_for('admin'))
        
    elif request.method == 'GET':
        hk_req=Housekeeping.query.all()
        hk_req.reverse()
        main_req=Maintenance.query.all()
        main_req.reverse()
        return render_template('admin_home.html', hk_requests=hk_req, main_requests=main_req)
    


@app.route('/admin_home_page Ashoka_University_Off_Campus_Residence TDI_LAKE_GROVE meal_buttons', methods=['GET', 'POST'])
@login_required
def today_meal():

    if current_user.ashoka_id != 1000:
        logout_user()
        return redirect(url_for('login'))
    

#@app.route('/admin_home_page Ashoka_University_Off_Campus_Residence TDI_LAKE_GROVE meal' , methods=['GET', 'POST'])
#@login_required
def admin_meal():
    #if current_user.ashoka_id != 1000:
    #    logout_user()
    #    return redirect(url_for('login'))
    
    from app import app
    app.app_context().push()
    from app import app, db
    from app.models import Mealbooking
    today = datetime.strptime(datetime.now().strftime('%Y-%m-%d'), '%Y-%m-%d').date()
    result = Mealbooking.query.filter_by(meal_date = today).all()
    list_ashoka_id = []
    list_breakfast = []
    list_lunch = []
    list_snacks = []
    list_dinner = []

    for item in result:
        list_ashoka_id+= [item.ashoka_id]
        list_breakfast+= [item.breakfast]
        list_lunch+= [item.lunch]
        list_snacks+= [item.snacks]
        list_dinner+= [item.dinner]
    
    data = {'Ashoka ID': list_ashoka_id,
        'Breakfast': list_breakfast,
        'Lunch': list_lunch,
        'Snacks': list_snacks,
        'Dinner': list_dinner
        }

    df = pd.DataFrame.from_records(data)

    replacement_dict = {'Snacks': 1, 'With Eggs': 1, 'Without Eggs': 1, 'Vegetarian': 1, 'Non - Vegetarian': 1}
    replaced_df = df.replace(replacement_dict)
    breakfast_with_eggs = df['Breakfast'].value_counts().get('With Eggs')
    breakfast_without_eggs = df['Breakfast'].value_counts().get('Without Eggs')
    lunch_vegetarian = df['Lunch'].value_counts().get('Vegetarian')
    lunch_nonvegetarian = df['Lunch'].value_counts().get('Non - Vegetarian')
    snacks = df['Snacks'].value_counts().get('Snacks')
    dinner_vegetarian = df['Dinner'].value_counts().get('Vegetarian')
    dinner_nonvegetarian = df['Dinner'].value_counts().get('Non - Vegetarian')
    data_today = {'Option': ['Vegetarian', 'Non - Vegetarian'],
        'Breakfast': [breakfast_without_eggs, breakfast_with_eggs],
        'Lunch': [lunch_vegetarian, lunch_nonvegetarian],
        'Snacks': [snacks, ''],
        'Dinner': [dinner_vegetarian, dinner_nonvegetarian]
        }
    
    final_today = pd.DataFrame(data_today)

    hour = datetime.now().hour
    if hour < 10:
        prefix = 'breakfast'
    elif hour >= 10 and hour < 14:
        prefix = 'lunch'
    elif hour >= 14 and hour < 17:
        prefix = 'snacks'
    else:
        prefix = 'dinner'

    filename = f'{prefix}_{today}.xlsx'
    final_today.to_excel(r'/Users/jaganathapandiyan/Desktop/Apps/working folder/venv/app/Meal Folder/'+filename, index=False)

    recipient = 'jaganathapandiyan12@gmail.com'
    subject = prefix+'_'+str(today)
    attachment = '/Users/jaganathapandiyan/Desktop/Apps/working folder/venv/app/Meal Folder/'+filename

    msg = Message(subject=subject, sender=app.config['MAIL_USERNAME'], recipients=[recipient])
    with app.open_resource(attachment) as file:
        msg.attach(filename=filename, content_type='application/pdf', data=file.read())
    mail.send(msg)
    
    return 'Email sent successfully.'
      

#@app.route("/process-table", methods=["GET", "POST"])
#def process_table():
#        mainID = request.args.get('mainID')    
#        req = Maintenance.query.filter_by(id = mainID[1:]).first()
#        user_req = Requests.query.filter_by(id = req.ref).first()
#        user_req.status = "Completed"
#        db.session.delete(req)
#        db.session.commit()
#        main_req = Maintenance.query.all()
#        main_req.reverse()
#
#        return(render_template("process-table.html", main_requests=main_req))


@app.route('/edit_profile/<id>', methods=['GET', 'POST'])
@login_required
def edit_profile(id):
    if current_user.ashoka_id == 1000:
        return redirect(url_for('admin'))
    
    if current_user.flat[-2:] == 'GF':
         floor='Ground Floor'
         short_floor='GF'
    elif current_user.flat[-2:] == 'FF':
         floor='First Floor'
         short_floor='FF'
    elif current_user.flat[-2:] == 'SF':
         floor='Second Floor'
         short_floor='SF'
    elif current_user.flat[-2:] == 'TF':
         floor='Third Floor'
         short_floor='TF'
    elif current_user.flat[-6:] == 'Duplex':
         floor='Duplex' 
         short_floor='Duplex'   

    form = EditProfileForm()
    if request.method == 'POST':
        if request.form.get('edit_profile_action') == 'Submit':         
            if form.validate_on_submit():
                current_user.name = form.name.data
                current_user.room = form.room.data
                current_user.ashoka_id = form.ashoka_id.data
                current_user.ashoka_email=form.ashoka_email.data     
                current_user.flat=str(form.flat.data) + " " + str(request.form.get('floor'))
                db.session.commit()
                flash('Your profile has been updated')
                return redirect(url_for('edit_profile', id=current_user.ashoka_id))
            
            else:
                form.name.data = current_user.name
                form.flat.data = current_user.flat[:3]
                form.floor.data = short_floor
                form.ashoka_id.data = current_user.ashoka_id
                form.room.data = current_user.room
                form.ashoka_email.data = current_user.ashoka_email
                return render_template('edit_profile.html', title='Edit Profile', form=form, floor=floor, short_floor=short_floor)
            
        elif request.form.get('edit_profile_action') == 'Cancel':
             return redirect(url_for('home'))
    
    else:
        form.name.data = current_user.name
        form.flat.data = current_user.flat[:3]
        form.floor.data = short_floor
        form.ashoka_id.data = current_user.ashoka_id
        form.room.data = current_user.room
        form.ashoka_email.data = current_user.ashoka_email
        return render_template('edit_profile.html', title='Edit Profile', form=form, floor=floor, short_floor=short_floor)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/home', methods=['GET', 'POST'])
@login_required
def home():
        if current_user.ashoka_id == 1000:
            return redirect(url_for('admin'))

        if current_user.name == None:
             return redirect(url_for('user_details'))
        
        elif request.method == 'POST':
            if request.form.get('home_action') == 'Meal Booking':
               return redirect(url_for('mealbooking'))
            if request.form.get('home_action') == 'Housekeeping':
               return redirect(url_for('housekeeping'))
            if request.form.get('home_action') == 'Maintenance Request':
               return redirect(url_for('maintenance_request'))
            if request.form.get('home_action') == 'Manage Requests':
               return redirect(url_for('manage_requests'))
            
        elif request.method == 'GET':
            return render_template('home.html', title='Home')        
        
@app.route('/mealbooking', methods=['GET', 'POST'])
@login_required      
def mealbooking():
        if current_user.ashoka_id == 1000:
            return redirect(url_for('admin'))
        
        if current_user.name == None:
            return redirect(url_for('user_details'))
        
        form = MealForm()
        today = datetime.strptime(datetime.now().strftime('%Y-%m-%d'), '%Y-%m-%d').date()
        now = datetime.strptime(datetime.now().strftime('%H:%M:%S'),'%H:%M:%S') 

        if request.method == 'POST':
            if request.form.get('mealbooking_action') == 'Submit':
                if form.breakfast.data == None:
                    form.breakfast.data = ''

                if form.lunch.data == None:
                    form.lunch.data = ''

                if form.snacks.data == None:
                    form.snacks.data = ''

                if form.dinner.data == None:
                    form.dinner.data = ''
                    
                if form.validate_on_submit():
                    req=Requests( name = current_user.name, ashoka_id=current_user.ashoka_id, flat = current_user.flat, room = current_user.room, date=datetime.now().strftime('%d-%m-%Y'), time=datetime.now().strftime('%H:%M'), type = "Mealbooking", status = "Pending", meal_date = form.meal_date.data, breakfast = form.breakfast.data, lunch = form.lunch.data, snacks = form.snacks.data, dinner = form.dinner.data, body = form.remarks.data)
                    db.session.add(req)
                    db.session.commit()
                    db.session.add(Mealbooking(ref = req.id, ashoka_id=current_user.ashoka_id, meal_date = form.meal_date.data, name = current_user.name, apts_number = current_user.flat, room_no = current_user.room, date=datetime.now().strftime('%d-%m-%Y'), time=datetime.now().strftime('%H:%M'), breakfast = form.breakfast.data, lunch = form.lunch.data, snacks = form.snacks.data, dinner = form.dinner.data, remarks = form.remarks.data))
                    db.session.commit()
                    flash ("Meal(s) Booked Successfully")
                    return redirect(url_for('home'))
                
                else:
                    if now > datetime.strptime('17:00:00','%H:%M:%S'):
                        tomorrow = datetime.now()+timedelta(1)
                        form.meal_date.data = tomorrow

                    else:    
                        form.meal_date.data=datetime.now().date()

                    return render_template('mealbooking.html', form=form)  
            
            elif request.form.get('mealbooking_action') == 'Cancel':
                return redirect(url_for('home'))
            
            elif request.form.get('mealbooking_action') == 'Menu':
                return render_template ('menu.html')
            
            elif request.form.get('mealbooking_action') == 'Ok':
                return redirect(url_for('home'))

                                                     
        else:
            access = [1, 1, 1, 1]

            if now >= datetime.strptime('10:00:00','%H:%M:%S'):
                access[1] = 0

            if now >= datetime.strptime('14:00:00','%H:%M:%S'):   
                access[2] = 0

            if now >= datetime.strptime('17:00:00','%H:%M:%S'):
                access[3] = 0

            form.access.data = access
            form.today.data = today

            if now > datetime.strptime('17:00:00','%H:%M:%S'):
                form.meal_date.data = datetime.now()+timedelta(1)

            else:    
                form.meal_date.data=datetime.now().date()

        return render_template('mealbooking.html', form=form)
        
     
@app.route('/housekeeping', methods=['GET', 'POST'])
@login_required
def housekeeping():
        form=HouseForm()
        if current_user.ashoka_id == 1000:
            return redirect(url_for('admin'))
         
        if request.method == 'POST':
            if request.form.get('housekeeping_action') == 'Submit':
                if form.validate_on_submit():
                    req=Requests(name=current_user.name, ashoka_id=current_user.ashoka_id, flat=current_user.flat, room=current_user.room, date=datetime.now().strftime('%d-%m-%Y'), time=datetime.now().strftime('%H:%M'), time_slot=form.time_slot.data, body=form.remarks.data, type='Housekeeping')
                    db.session.add(req)
                    db.session.commit()
                    db.session.add(Housekeeping(name=current_user.name, ref=req.id, ashoka_id=current_user.ashoka_id, flat=current_user.flat, room=current_user.room, date=datetime.now().strftime('%d-%m-%Y'), time=datetime.now().strftime('%H:%M'), time_slot=form.time_slot.data, body=form.remarks.data))
                    db.session.commit()
                    flash ("Housekeeping Request Raised Successfully")
                    return redirect(url_for('home'))
                
                else:
                    form.time_slot.data='ASAP'
                    return render_template('housekeeping.html', form=form)
                
            elif request.form.get('housekeeping_action') == 'Cancel':
                return redirect(url_for('home'))
            
            elif request.form.get('housekeeping_action') == 'Ok':
                return redirect(url_for('home'))
        
        else:
            form.time_slot.data='ASAP'
            return render_template('housekeeping.html', form=form)

         
@app.route('/maintenance_request', methods=['GET', 'POST'])
@login_required
def maintenance_request():
        if current_user.ashoka_id == 1000:
            return redirect(url_for('admin'))
         
        form=MaintenanceForm()
        if request.method == 'POST':
            if request.form.get('maintenance_action') == 'Submit':
                if form.validate_on_submit():
                    req=Requests(name=current_user.name, ashoka_id=current_user.ashoka_id, flat=current_user.flat, room=current_user.room, date=datetime.now().strftime('%d-%m-%Y'), time=datetime.now().strftime('%H:%M'), body=form.remarks.data, type='Maintenance')
                    db.session.add(req)
                    db.session.commit()
                    db.session.add(Maintenance(name=current_user.name, ref=req.id, ashoka_id=current_user.ashoka_id, flat=current_user.flat, room=current_user.room, date=datetime.now().strftime('%d-%m-%Y'), time=datetime.now().strftime('%H:%M'), body=form.remarks.data))
                    db.session.commit()
                    flash ('Maintenance Request Raised Successful')
                    return redirect(url_for('home'))
                else:
                    return render_template('maintenance_request.html', form=form)
                
            elif request.form.get('maintenance_action') == 'Cancel':
                return redirect(url_for('home'))
            
        else:
            return render_template('maintenance_request.html', form=form)
               

@app.route('/manage_requests', methods=['GET', 'POST'])
@login_required      
def manage_requests():
        if current_user.ashoka_id == 1000:
            return redirect(url_for('admin'))
         
        if request.method == 'POST':
            req_edit=Requests.query.filter_by(id=request.form.get('manage_req_action')[1:]).first()
            req_type=req_edit.type
            if req_type == 'Housekeeping':
                if request.form.get('manage_req_action')[0] == 'e':
                    return redirect(url_for('housekeeping_edit', id=request.form.get('manage_req_action')[1:]))
                elif request.form.get('manage_req_action')[0] == 'c':
                    db.session.delete(Housekeeping.query.filter_by(ref=req_edit.id).first())
                    req_edit.status='Cancelled'
                    db.session.commit()
                    return redirect(url_for('manage_requests'))

            elif req_type == 'Maintenance':
                if request.form.get('manage_req_action')[0] == 'e':
                    return redirect(url_for('maintenance_edit', id=request.form.get('manage_req_action')[1:]))
                elif request.form.get('manage_req_action')[0] == 'c':
                    db.session.delete(Maintenance.query.filter_by(ref=req_edit.id).first())
                    req_edit.status='Cancelled'
                    db.session.commit()
                    return redirect(url_for('manage_requests'))
                
            elif req_type == 'Mealbooking':
                if request.form.get('manage_req_action')[0] == 'e':
                    return redirect(url_for('mealbooking_edit', id=request.form.get('manage_req_action')[1:]))
                elif request.form.get('manage_req_action')[0] == 'c':
                    db.session.delete(Mealbooking.query.filter_by(ref=req_edit.id).first())
                    req_edit.status='Cancelled'
                    db.session.commit()
                    return redirect(url_for('manage_requests'))   
              
        else:
            requests=Requests.query.filter_by(ashoka_id=current_user.ashoka_id).all()
            requests.reverse()
            today = datetime.strptime(datetime.now().strftime('%Y-%m-%d'), '%Y-%m-%d')
            now=datetime.strptime(datetime.now().strftime('%H:%M:%S'),'%H:%M:%S')
            mealRequests=Requests.query.filter_by(type='Mealbooking', status='Pending', ashoka_id=current_user.ashoka_id).all()

            for mealRequest in mealRequests:
                if today > datetime.strptime(mealRequest.meal_date,'%Y-%m-%d'):
                    mealRequest.status = 'Complete'
                elif today == datetime.strptime(mealRequest.meal_date,'%Y-%m-%d'):
                    if now>=datetime.strptime("17:00:00",'%H:%M:%S'):
                        mealRequest.status = 'Complete'
            
            db.session.commit()
            return render_template('manage_requests_table.html', requests=requests)
         

@app.route('/housekeeping_edit/<id>', methods=['GET', 'POST'])
@login_required
def housekeeping_edit(id):
        if current_user.ashoka_id == 1000:
            return redirect(url_for('admin'))
        
        req_edit=Requests.query.filter_by(id=id).first()
        admin_req_edit=Housekeeping.query.filter_by(ref=req_edit.id).first()
        if current_user.ashoka_id != req_edit.ashoka_id:
             return redirect(url_for('home'))
            
        form=HouseEditForm()
        if request.method == 'POST':
            if request.form.get('action') == 'modify':
                if form.validate_on_submit():         
                    req_edit.body = form.remarks.data
                    req_edit.time_slot = form.time_slot.data
                    admin_req_edit.body = form.remarks.data
                    admin_req_edit.time_slot = form.time_slot.data
                    db.session.commit()
                    return redirect(url_for('manage_requests'))
                
            if request.form.get('action') == 'back':
                return redirect(url_for('manage_requests'))
            
        else:
            form.time_slot.data=req_edit.time_slot
            form.remarks.data=req_edit.body    
            return render_template('housekeeping_edit.html', form=form)
        

@app.route('/maintenance_edit/<id>', methods=['GET', 'POST'])
@login_required
def maintenance_edit(id):
        if current_user.ashoka_id == 1000:
            return redirect(url_for('admin'))
        
        req_edit=Requests.query.filter_by(id=id).first()
        admin_req_edit=Maintenance.query.filter_by(ref=req_edit.id).first()

        if current_user.ashoka_id != req_edit.ashoka_id:
             return redirect(url_for('home'))
            
        form=MainEditForm()
        if request.method == 'POST':
            if request.form.get('action') == 'modify':
                if form.validate_on_submit():         
                    req_edit.body = form.remarks.data
                    admin_req_edit.body = form.remarks.data
                    db.session.commit()
                    return redirect(url_for('manage_requests'))
                
            if request.form.get('action') == 'back':
                return redirect(url_for('manage_requests'))
            
        else:
            form.remarks.data=req_edit.body    
            return render_template('maintenance_edit.html', form=form)
            

@app.route('/mealbooking_edit/<id>', methods=['GET', 'POST'])
@login_required
def mealbooking_edit(id):
        if current_user.ashoka_id == 1000:
            return redirect(url_for('admin'))
        
        req_edit=Requests.query.filter_by(id=id).first()

        if current_user.ashoka_id != req_edit.ashoka_id:
             return redirect(url_for('home'))
        
        breakfast = False
        lunch = False
        snacks = False
        dinner = False
        today = datetime.strptime(datetime.now().strftime('%Y-%m-%d'), '%Y-%m-%d')
        now=datetime.strptime(datetime.now().strftime('%H:%M:%S'),'%H:%M:%S')
        lunch_cutoff=datetime.strptime('10:00:00','%H:%M:%S')
        snacks_cutoff=datetime.strptime('14:00:00','%H:%M:%S')
        dinner_cutoff=datetime.strptime('17:00:00','%H:%M:%S')

        form=MealEditForm()
        if request.method == 'POST':
            if request.form.get('action') == 'modify': 
                if form.breakfast.data != None: 
                    req_edit.breakfast = form.breakfast.data
                if form.lunch.data != None: 
                    req_edit.lunch = form.lunch.data
                if form.snacks.data != None: 
                    req_edit.snacks = form.snacks.data
                if form.dinner.data != None: 
                    req_edit.dinner = form.dinner.data
                req_edit.body = form.remarks.data
                db.session.commit()
                return redirect(url_for('manage_requests'))
                
            if request.form.get('action') == 'back':
                return redirect(url_for('manage_requests'))
            
        else:
            form.meal_date.data=datetime.strptime(req_edit.meal_date,'%Y-%m-%d')
            form.breakfast.data=req_edit.breakfast
            form.lunch.data=req_edit.lunch
            form.snacks.data=req_edit.snacks
            form.dinner.data=req_edit.dinner
            form.remarks.data=req_edit.body

            if today >= form.meal_date.data:
                breakfast = True
            if today > form.meal_date.data:
                lunch = True
            elif today == form.meal_date.data and now >= lunch_cutoff:
                lunch = True
            if today > form.meal_date.data:
                snacks = True
            elif today == form.meal_date.data and now >= snacks_cutoff:
                snacks = True
            if today > form.meal_date.data:
                dinner = True
            elif today == form.meal_date.data and now >= dinner_cutoff:
                dinner = True

            form.breakfast_access.data = breakfast
            form.lunch_access.data = lunch
            form.snacks_access.data = snacks
            form.dinner_access.data = dinner
            form.condition.data = True

            return render_template('mealbooking_edit.html', form=form)
 