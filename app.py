import numpy as np 
import pandas as pd
import os
import datetime as dt

from flask import Flask,render_template,url_for,request,g, flash, redirect
from werkzeug.utils import secure_filename
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import current_user, LoginManager, login_user, logout_user, UserMixin
from flask_admin import Admin, AdminIndexView
from flask_admin.contrib.sqla import ModelView
from flask_admin.model import BaseModelView

from sklearn.metrics import mean_absolute_error

from forms import LoginForm, RegisterForm
from config import Config
from scorer import Scorer

# PARAMETER

## Leaderboard parameter
limit_lb = 100 # Number of user showed at leaderboard table
greater_better = False # True if lowest score is the best; False if greatest score is the best
metric = mean_absolute_error #change the metric using sklearn function
scorer = Scorer(public_path = './master_key/public_key.csv', 
                private_path = './master_key/private_key.csv', 
                metric = metric) #change the metric using sklearn function

## Upload parameter
UPLOAD_FOLDER = 'submissions'
ALLOWED_EXTENSIONS = {'csv'} # only accept csv files

## FLASK configuration
app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 2 * 1024 * 1024 # 2 Megabytes
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SECRET_KEY'] = 'my'
app.config.from_object(Config)

## Database configuration
db = SQLAlchemy(app)
db.app = app
migrate = Migrate(app, db)
login = LoginManager(app)

# Database Model
@login.user_loader
def load_user(id):
    return User.query.get(int(id))

class User(UserMixin, db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    password = db.Column(db.String(128)) ## Too lazy to make it hash

    def __repr__(self):
        return self.username

    def check_password(self, password): ## Too lazy to make it hash
        return self.password == password

class Submission(db.Model):
    __tablename__ = "submission"
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, index=True, default=dt.datetime.now)
    submission_type = db.Column(db.String(64))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User')
    score = db.Column(db.Float)

    def __repr__(self):
        return f'<User ID {self.user_id} score {self.score}>'

db.create_all()

# Admin
class MyAdminIndexView(AdminIndexView):
    def is_accessible(self):
        if current_user.is_authenticated:
            return current_user.username == 'admin'
        else:
            False

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('home_page'))

class UserView(ModelView):
    column_list = (User.id, 'username','password')

    def is_accessible(self):
        if current_user.is_authenticated:
            return current_user.username == 'admin'
        else:
            False
    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('home_page'))

class SubmissionView(ModelView):
    column_list = (Submission.id, 'submission_type', 'user_id', 'user',  'timestamp', 'score')

    def is_accessible(self):
        if current_user.is_authenticated:
            return current_user.username == 'admin'
        else:
            False

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('home_page'))

admin = Admin(app, index_view=MyAdminIndexView())
admin.add_view(UserView(User, db.session))
admin.add_view(SubmissionView(Submission, db.session))

# Leader Board
def get_leaderboard(greater_better, limit, submission_type = 'public'):

    if greater_better:
        score_agg = "MAX"
        score_sorting = "DESC"

    else:

        score_agg = "MIN"
        score_sorting = "ASC"

    query = f"""
            SELECT
            user.username, 
            {score_agg}(submission.score) as score,
            count(submission.id) as total_submission,
            max(timestamp) as last_sub
            FROM submission 
            LEFT JOIN user 
            ON user.id = submission.user_id
            WHERE submission_type = '{submission_type}'
            GROUP BY 1 
            ORDER BY 2 {score_sorting}, 4
            LIMIT {limit}
            """
    df = pd.read_sql(query, 
                    db.session.bind)
    return df

# Route
@app.route('/register', methods=['GET', 'POST'])
def register_page():
    registration_status = request.args.get("registration_status", "")
    reg_form = RegisterForm()

    if request.method == 'POST': 
        ### REGISTRATION
        if reg_form.validate_on_submit():
            user = User.query.filter_by(username=reg_form.username.data).first()
            print(user)
            if user is None: # only when user is not registered then proceed
                print("HALOOO")
                u = User(username=reg_form.username.data, password = reg_form.password.data)
                db.session.add(u)
                db.session.commit()
                # flash('Congratulations, you are now a registered user!')
                registration_status = f"Welcome {reg_form.username.data}, Please Login at HOME page"
                return redirect(url_for('register_page', registration_status = registration_status))
            else:
                registration_status = "USER NAME ALREADY USED"
                return redirect(url_for('register_page', registration_status = registration_status))
        else:
            registration_status = "ERROR VALIDATION"
            print("ANEH")
            return redirect(url_for('register_page', registration_status = registration_status))
        
    if request.method == 'GET':
        return render_template('register.html', reg_form = reg_form, registration_status = registration_status)

@app.route('/logout')
def logout():
    logout_user()
    print("log out success")
    return redirect(url_for('home_page'))

def allowed_file(filename):
    # checks if extension in filename is allowed
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def home_page():
    login_form = LoginForm()
    login_status = request.args.get("login_status", "")
    submission_status = request.args.get("submission_status", "")

    leaderboard = get_leaderboard(greater_better = greater_better, limit = limit_lb, submission_type='public')
    leaderboard_private = get_leaderboard(greater_better = greater_better, limit = limit_lb, submission_type='private')

    if request.method == 'POST': # If upload file / Login
        ### LOGIN 
        if login_form.validate_on_submit():
            print(f'Login requested for user {login_form.username.data}, remember_me={login_form.remember_me.data}')
            user = User.query.filter_by(username=login_form.username.data).first()
            if user is None: # USER is not registered
                login_status = "User is not registered / Password does not match"
                return redirect(url_for('home_page', login_status = login_status))
            elif user.check_password(login_form.password.data): # Password True
                print('True pass')
                login_status = ""
                login_user(user, remember=login_form.remember_me.data)
                return redirect(url_for('home_page', login_status = login_status))
            else: #WRONG PASSWORD
                print('WRONG PASS')
                login_status = "User is not registered / Password does not match"
                return redirect(url_for('home_page', login_status = login_status))
            login_status = ""
            login_user(user, remember=login_form.remember_me.data)
            return redirect(url_for('home_page', login_status = login_status))

        ### UPLOAD FILE
        if 'uploadfile' in request.files.keys() and current_user.is_authenticated:
            submission_file = request.files['uploadfile']
            #throw error if extension is not allowed
            if not allowed_file(submission_file.filename):
                raise Exception('Invalid file extension')
            
            if submission_file and allowed_file(submission_file.filename):

                filename = secure_filename(submission_file.filename)

                target_dir = os.path.join(app.config['UPLOAD_FOLDER'], str(current_user.id))
                if not os.path.exists(target_dir):
                    os.makedirs(target_dir)
                
                fullPath = os.path.join(app.config['UPLOAD_FOLDER'], str(current_user.id) , filename)
                submission_file.save(fullPath)

                submission_type = request.form.get('submission_type', "public")
                result = scorer.calculate_score(submission_path = fullPath, submission_type = submission_type)
                submission_status = result[0]
                if submission_status == "SUBMISSION SUCCESS":
                    score = result[1]
                    score = round(score, 3)
                    s = Submission(user_id=current_user.id , score=score, submission_type = submission_type)
                    db.session.add(s)
                    db.session.commit()
                    print(f"submitted {score}")

                    submission_status =  f"SUBMISSION SUCCESS | Score: {round(score,3)}" 
                    
                return redirect(url_for('home_page', submission_status = submission_status))
            
    return render_template('index.html', 
                        leaderboard = leaderboard,
                        leaderboard_private = leaderboard_private,
                        login_form=login_form, 
                        login_status=login_status,
                        submission_status=submission_status
    )

if __name__ == '__main__':
    app.run(debug=True)