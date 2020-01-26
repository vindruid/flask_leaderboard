from main import db, User

u = User(username="karjo", password = "karjo")
db.session.add(u)
db.session.commit()