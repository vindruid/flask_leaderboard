from app import User, db

## ADD 
u = User(username='billy', email='billy@example.com', password_hash = 'hallo')
db.session.add(u)
db.session.commit()
print(u)

users = User.query.all()
print(users)

