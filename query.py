from main import Submission 

subs = Submission.query.all()
for sub in subs:
    print(sub.user_id, sub.score)