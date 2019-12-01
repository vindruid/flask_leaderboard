# Flask Leaderboard
Make simple leaderboard for machine learning competition using Flask

The Flask Leaderboard repo enable users to:
- See Public Leaderboard 
- Login & Register User
- Public & Private Submission

Admin is able to: 
- See Public & Private Leaderboard
- CURD User & Submission

## How to Use it
- [Clone and Install](#clone-and-install)
- [Insert Master Key](#insert-master-key)
- [Change Metric score](#change-metric-score)

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
#### change `score_min` parameter 
```python
score_min = True
```
if lowest score is the best (i.e. Mean Square Error, log loss)
```python
score_min = False
```
if greatest socre is the best (i.e. Accuracy, R2 Score) 

#### change `metric` parameter
Using [scikit learn metrics](https://scikit-learn.org/stable/modules/classes.html#sklearn-metrics-metrics) 
<br>
for example
```python
from sklearn.metrics import mean_squared_error

metric = mean_squared_error
```
Ensure the metric you choose align with the `score_min` parameter
