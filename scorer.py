import pandas as pd 

from sklearn.metrics import mean_squared_error

class Scorer():
    def __init__(self, public_path = './master_key/public_key.csv', 
                private_path = './master_key/private_key.csv', metric = mean_squared_error):
        self.public_path = public_path
        self.private_path = private_path
        self.metric = metric

        self.df_public_key = pd.read_csv(self.public_path)
        self.df_private_key = pd.read_csv(self.private_path)
        
    def calculate_score(self, submission_path, submission_type = 'public'):
        df_submission = pd.read_csv(submission_path)

        if submission_type == 'private':
            df_key = self.df_private_key
        else: 
            df_key = self.df_public_key

        # if input length not same, return None
        if len(df_key) != len(df_submission):
            print(len(df_key), len(df_submission))
            return ("NOT SAME LENGTH", None)
        
        df_merged = df_key.merge(df_submission, how ='inner', 
                                left_on='data_id', right_on='data_id', # adjust `on` columns as params
                                suffixes=('_key', '_submission')) 
        # When submission and key have different index value
        if len(df_key) != len(df_merged):
            return ("NOT SAME INDEX", None)

        # data size is same, time to get score
        y_key = df_merged['prediction_key']
        y_submission = df_merged['prediction_submission']

        if y_submission.isna().sum() > 0:
            return ("SUBMISSION HAS NULL VALUE", None)

        score = self.metric(y_key, y_submission)
        return ("SUBMISSION SUCCESS", score)