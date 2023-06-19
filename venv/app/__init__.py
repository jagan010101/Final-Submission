from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_bootstrap import Bootstrap
from flask_mail import Mail
from apscheduler.schedulers.background import BackgroundScheduler

app = Flask(__name__)
app.config.from_object(Config)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
login = LoginManager(app)
login.login_view = 'login'
db = SQLAlchemy(app)
migrate = Migrate(app, db)
bootstrap = Bootstrap(app)

app.config['MAIL_SERVER'] = 'smtp.office365.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'tdiapp@outlook.com'
app.config['MAIL_PASSWORD'] = 'animaltiger12'
mail = Mail(app)


from app.routes import admin_meal, admin_meal_monthly

scheduler = BackgroundScheduler()
scheduler.add_job(admin_meal, 'cron', day_of_week= 'mon-sun', hour = 0, minute = 1, id = 'breakfast_schedule')
scheduler.add_job(admin_meal, 'cron', day_of_week= 'mon-sun', hour = 10, minute = 1, id = 'lunch_schedule')
scheduler.add_job(admin_meal, 'cron', day_of_week= 'mon-sun', hour = 14, minute = 1, id = 'snacks_schedule')
scheduler.add_job(admin_meal, 'cron', day_of_week= 'mon-sun', hour = 17, minute = 1, id = 'dinner_schedule')
scheduler.add_job(admin_meal_monthly, 'cron', day = 1, hour = 0, id = 'monthly_data')
scheduler.start()