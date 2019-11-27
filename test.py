from app import User, Submission, db
import pandas as pd

## ADD 
# u = User(username='billy', email='billy@example.com', password_hash = 'hallo')
# db.session.add(u)
# db.session.commit()
# print(u)

# users = User.query.all()
# for user in users:
#     print(user.username)
# print(users)

# s = Submission(user_id=2, score=1.021)
# db.session.add(s)
# db.session.commit()

submissions = Submission.query.all()
print(submissions)
print(submissions[0].user_id)
print(pd.DataFrame(submissions))

# df.to_sql(name='submissions', con=db.engine, index=False)

# print(pd.read_sql_table('submissions', db.session.bind))

# print(db.session.bind)


# class Submission(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     timestamp = db.Column(db.DateTime, index=True, default=dt.datetime.utcnow)
#     user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
#     score = db.Column(db.Float)
