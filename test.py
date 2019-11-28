from app import User, Submission, db
import pandas as pd

# ADD 
# u = User(username='billy', password_hash = 'hallo')
# db.session.add(u)
# db.session.commit()
# print(u)

# users = User.query.all()
# for user in users:
#     print(user.username)
# print(users)

# s = Submission(user_id=3, score=1.321)
# db.session.add(s)
# db.session.commit()

s = Submission(user_id=4, score=0.821)
db.session.add(s)
db.session.commit()

# submissions = Submission.query.all()
# print(submissions)
# print(submissions[0].user_id)
# print(pd.DataFrame(submissions))

# df_sub = pd.read_sql_table('submission', db.session.bind)
# df_user =  pd.read_sql_table('user', db.session.bind)
# print(df_sub)
# print(df_user)

# print(df.groupby('user_id', as_index=False).agg({"id" : "count", "timestamp": "last", "score" : "min"}))
# df_sub = df_sub.groupby('user_id', as_index=False).agg({"id" : "count", "score" : "min"})
# df_sub.columns = ['user_id', 'total_submission', 'score']
# df_sub = df_sub.merge(df_user[['id', 'username']], left_on = 'user_id', right_on ='id', how = 'left')
# df_sub = df_sub[['username', 'score', 'total_submission']]
# df_sub = df_sub.sort_values('score', ascending = True)
# print(df_sub)

# DROP TABLE
# db.reflect()
# db.drop_all()

# df_user = pd.read_sql('select * from user limit 2', db.session.bind)
# print(df_user)

# score_agg = "MIN"
# score_sorting = "ASC"
# query = f"""
#                 SELECT
#                 user.username, 
#                 {score_agg}(submission.score) as score,
#                 count(submission.id) as total_submission,
#                 max(timestamp) as last_sub
#                 FROM submission 
#                 LEFT JOIN user 
#                 ON user.id = submission.user_id
#                 GROUP BY 1 
#                 ORDER BY 2 {score_sorting}
#                 LIMIT 100
#                 """
# df = pd.read_sql(query, 
#                 db.session.bind)
# print(df)