import sys
from CHATBOT.models import db, User
username = sys.argv[1]

u = User.query.filter_by(username=username).first()
u.is_admin = True
print(u.username)
db.session.commit()
print('done')