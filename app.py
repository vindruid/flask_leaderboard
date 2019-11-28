import numpy as np 
import pandas as pd # be replaced soon
import os
import datetime as dt

from flask import Flask,render_template,url_for,request,g, flash, redirect
from werkzeug import check_password_hash, generate_password_hash, \
     secure_filename
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import current_user, LoginManager, login_user, logout_user, UserMixin

from forms import LoginForm, RegisterForm
from config import Config

from scorer import Scorer
from sklearn.metrics import mean_squared_error

# PARAMETER

## Upload parameter
UPLOAD_FOLDER = 'submissions'
ALLOWED_EXTENSIONS = {'txt', 'csv', 'names'}

## FLASK configuration
app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 2 * 1024 * 1024 # 16 Megabytes
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SECRET_KEY'] = 'my'
app.config.from_object(Config)

## Database configuration
db = SQLAlchemy(app)
db.app = app
migrate = Migrate(app, db)
login = LoginManager(app)

## Scorer
scorer = Scorer(public_path = './master_key/public_key.csv', 
                private_path = './master_key/private_key.csv', 
                metric = mean_squared_error)

# User Management
@login.user_loader
def load_user(id):
    return User.query.get(int(id))

class User(UserMixin, db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128)) ## Too lazy to make it hash

    def __repr__(self):
        return f'<User {self.username}>'

    def check_password(self, password): ## Too lazy to make it hash
        return self.password_hash == password

class Submission(db.Model):
    __tablename__ = "submission"
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, index=True, default=dt.datetime.now)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    score = db.Column(db.Float)

    def __repr__(self):
        return f'<User ID {self.user_id} score {self.score}>'

db.create_all()

def get_leaderboard(score_min = True, limit = 100):

    if score_min:
        score_agg = "MIN"
        score_sorting = "ASC"

    else:
        score_agg = "MAX"
        score_sorting = "DESC"

    query = f"""
            SELECT
            user.username, 
            {score_agg}(submission.score) as score,
            count(submission.id) as total_submission,
            max(timestamp) as last_sub
            FROM submission 
            LEFT JOIN user 
            ON user.id = submission.user_id
            GROUP BY 1 
            ORDER BY 2 {score_sorting}
            LIMIT {limit}
            """
    df = pd.read_sql(query, 
                    db.session.bind)
    return df

@app.route('/register', methods=['GET', 'POST'])
def register_page():
    u = User(username='halo', password_hash = 'hele')
    registration_status = request.args.get("registration_status", "")
    reg_form = RegisterForm()

    if request.method == 'POST': 
        ### REGISTRATION
        if reg_form.validate_on_submit():
            user = User.query.filter_by(username=reg_form.username.data).first()
            print(user)
            if user is None: # only when user is not registered then proceed
                print("HALOOO")
                u = User(username=reg_form.username.data, password_hash = reg_form.password.data)
                db.session.add(u)
                db.session.commit()
                # flash('Congratulations, you are now a registered user!')
                registration_status = f"Welcome {reg_form.username.data}, Please Login "
                return redirect(url_for('register_page', registration_status = registration_status))
            else:
                registration_status = "USER NAME ALREADY USED"
                return redirect(url_for('register_page', registration_status = registration_status))
        ### LOGIN 
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
    
    submission_status = request.args.get("submission_status", "")

    ## TODO: query leaderboard from database
    # leaderboard = pd.read_csv('dummy_table.csv')
    # leaderboard.sort_values('score', ascending = True, inplace = True) 
    # leaderboard.reset_index(drop = True, inplace = True)
    leaderboard = get_leaderboard(score_min = True, limit = 100)

    if request.method == 'POST': # If upload file / Login
        ### LOGIN 
        if login_form.validate_on_submit():
            print(f'Login requested for user {login_form.username.data}, remember_me={login_form.remember_me.data}')
            user = User.query.filter_by(username=login_form.username.data).first()
            if user is None: # USER is not registered
                print("NO user name")
                return redirect(url_for('home_page'))
            elif user.check_password(login_form.password.data): # Password True
                print('True pass')
                login_user(user, remember=login_form.remember_me.data)
                return redirect(url_for('home_page'))
            else: #WRONG PASSWORD
                print('WRONG PASS')
                return redirect(url_for('home_page'))
            login_user(user, remember=login_form.remember_me.data)
            return redirect(url_for('home_page'))

        ### UPLOAD FILE
        if 'uploadfile' in request.files.keys() and current_user.is_authenticated:
            submission_file = request.files['uploadfile']
            #throw error if extension is not allowed
            if not allowed_file(submission_file.filename):
                raise Exception('Invalid file extension')
            
            if submission_file and allowed_file(submission_file.filename):
                filename = secure_filename(submission_file.filename)
                ## TODO: append userid and date to file to avoid duplicates
                # filename = str(session['user_id']) + '_' + \
                #             str(int(time.time())) + '_' + filename

                fullPath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                submission_file.save(fullPath)
                print(f'SAVED SUBMISSION: {fullPath}')

                ## TODO: doing calculation on saved file
                score = scorer.calculate_score(submission_path = fullPath, submission_type = 'public')

                print(score)
                submission_status = score[0]
                
                return redirect(url_for('home_page', submission_status = submission_status))
            
    return render_template('index.html', 
                        leaderboard = leaderboard,
                        login_form=login_form, 
                        submission_status=submission_status
    )

if __name__ == '__main__':
    app.run(debug=True)