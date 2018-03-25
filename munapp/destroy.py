
from app import app, db
from app.models import User, Topic, Comment, Group

db.reflect()
db.drop_all()
db.commit()