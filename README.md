# Flask Leaderboard
Make simple leaderboard for machine learning competition using Flask

# How to Use This Apps
There are two role: admin and user 

Admin is able to: 
- See Public & Private Leaderboard
- Create, read, update, delete (CRUD) Users & Submissions

The Flask Leaderboard repo enable users to:
- See Public Leaderboard 
- Login & Register User
- Public & Private Submission

First, setting up the admin 

## How to Use it As a Admin
- [Clone and Install](#clone-and-install)
- [Insert Master Key](#insert-master-key)
- [Change Scoring Method](#change-scoring-method)
- [Run Flask App](#run-flask-app)
- [Make Admin Account](#make-admin-account)

### Clone and Install
Clone the repo using `git clone https://github.com/vindruid/flask_leaderboard.git` 
<br>
Then install the package with the version `pip install -r requirements.txt`

### Insert Master Key
Put your key inside folder `master_key` with name  `public_key.csv` and `private_key.csv`
<br>
with column `data_id` and `prediction`
<br>
for example 
```
data_id,prediction
1,5
2,4
3,4.1
4,9
5,6.8
```

### Change Scoring Method
open `main.py`
#### change `greater_better` parameter 
```python
greater_better = True
```
if greatest score is the best (i.e. Accuracy, R2 Score) 

```python
greater_better = False
```
if lowest score is the best (i.e. Mean Square Error, log loss)

#### change `metric` parameter
Using [scikit learn metrics](https://scikit-learn.org/stable/modules/classes.html#sklearn-metrics-metrics) 
<br>
for example
```python
from sklearn.metrics import mean_squared_error

metric = mean_squared_error
```
Ensure the metric you choose align with the `greater_better` parameter

### Run Flask App
in your terminal, run `python main.py` <br>
Then you will see a page open in your browser with url `http://localhost:5005/`

### Make Admin account
Go to register page `http://localhost:5005/register` or click register button at the top left <br> 
Then perserve `admin` username, the `password` is up to you. <br>
You can go to `http://localhost:5005/admin` by login with `admin` username. <br>
At that page, you can manage users and submissions (create, read, update, and delete)

*If you forgot your admin password* 
run `python query.py` and it will print all submission and username with password 


## How to Use it As a User
- [Connect to leaderboard](connect-to-leaderboard)
- [Register](#register)
- [Login](#login)
- [Submit](#submit)

### Connect to leaderboard
Go to `http://localhost:5005/`

### Register
Go to register page `http://localhost:5005/register` or click register button at the top left <br> 
Add your `username` and `password` then click register

### Login
Go back to home page `http://localhost:5005/` or click home button <br> 
Put your registered `username` and `password` then login <br> 
If you forget your password, please contact admin or register new account

### Submit
Submission menu will be appeared if you already login <br>
Choose your submission type (`public` or `private`) <br>
Click choose file button and select your file then click upload



