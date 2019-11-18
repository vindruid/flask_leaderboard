import numpy as np 
import pandas as pd # be replaced soon
import os

from flask import Flask,render_template,url_for,request,g, flash, redirect
from werkzeug import check_password_hash, generate_password_hash, \
     secure_filename
import sqlite3

from forms import LoginForm

DATABASE = '/path/to/database.db'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

UPLOAD_FOLDER = 'submissions'
ALLOWED_EXTENSIONS = {'txt', 'csv', 'names'}

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 2 * 1024 * 1024 # 16 Megabytes
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SECRET_KEY'] = 'my'

def allowed_file(filename):
    # checks if extension in filename is allowed
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/register', methods=['GET', 'POST'])
def register_page():
    if request.method == 'POST': 
        # load and insert user data
        print(1231)
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm()
    if login_form.validate_on_submit():
        print('Login requested for user {}, remember_me={}'.format(
            login_form.username.data, login_form.remember_me.data))
        return redirect('/')
    return render_template('login.html', title='Sign In', login_form=login_form)

@app.route('/', methods=['GET', 'POST'])
def home_page():
    login_form = LoginForm()

    ## TODO: query leaderboard from database
    leaderboard = pd.read_csv('dummy_table.csv')
    leaderboard.sort_values('score', ascending = True, inplace = True) 
    leaderboard.reset_index(drop = True, inplace = True)

    if request.method == 'POST': # If upload file / Login

        ### LOGIN 
        if login_form.validate_on_submit():
            print(f'Login requested for user {login_form.username.data}, remember_me={login_form.remember_me.data}')
            return redirect('/')

        ### UPLOAD FILE
        if 'uploadfile' in request.files.keys(): 
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
            
    return render_template('index.html', 
                        leaderboard = leaderboard,
                        login_form=login_form
    )

if __name__ == '__main__':
	app.run(debug=True)