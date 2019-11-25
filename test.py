from app import User, Submission, db

## ADD 
# u = User(username='billy', email='billy@example.com', password_hash = 'hallo')
# db.session.add(u)
# db.session.commit()
# print(u)

# users = User.query.all()
# print(users)

s = Submission(user_id=1, score=0.921)
db.session.add(s)
db.session.commit()

submissions = Submission.query.all()
print(submissions)

# class Submission(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     timestamp = db.Column(db.DateTime, index=True, default=dt.datetime.utcnow)
#     user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
#     score = db.Column(db.Float)
