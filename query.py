from main import Submission, User

subs = Submission.query.all()
print("SUBMISSION: ")
for sub in subs:
    print(sub.user_id, sub.score)

users = User.query.all()
print("USERS: ")
for user in users:
    print(user.username, user.password)