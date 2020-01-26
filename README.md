# Flask Leaderboard
Make simple leaderboard for machine learning competition using Flask

Admin is able to: 
- See Public & Private Leaderboard
- CURD User & Submission

The Flask Leaderboard repo enable users to:
- See Public Leaderboard 
- Login & Register User
- Public & Private Submission

## How to Use it As a Admin
- [Clone and Install](#clone-and-install)
- [Insert Master Key](#insert-master-key)
- [Change Metric score](#change-metric-score)
- [Run Flask App](#run-flask-app)
- [Make Admin account](#make-admin-account)

## How to Use it As a User
- [Register](#register)
- [Login](#login)
- [Submit](#submit)
- [Check Leaderboard](#check-leaderboard)

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

### Change Metric Score
open `app.py`
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
in your terminal, run `python app.py` <br>
Then you will see a page open in your browser with url `http://localhost:5000/` 

### Make Admin account
Go to register page `http://localhost:5000/register` or click register button at the top left <br> 
Then perserve `admin` username, the `password` is up to you.
You can go to `http://localhost:5000/admin` by login with `admin` username. 
At that page, you can manage user and submission (create, read, update, and delete)
