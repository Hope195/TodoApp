from task import db, login_manager
from task import bcrypt
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model,UserMixin):
    id=db.Column(db.Integer(),primary_key=True)
    username=db.Column(db.String(length=30),nullable=False,unique=True)
    email=db.Column(db.String(length=50),nullable=False,unique=True)
    password_hash=db.Column(db.String(length=60),nullable=False)
    tasks=db.relationship('Tasks',backref='user',lazy = "dynamic")

    @property
    def password(self):
        return self.password 

    @password.setter
    def password(self,plain_text_password):
        self.password_hash=bcrypt.generate_password_hash(plain_text_password).decode('utf-8')

    def check_password_correction(self,attempted_password):
        return bcrypt.check_password_hash(self.password_hash,attempted_password)


class Tasks(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task_name=db.Column(db.String(length=100),nullable=False)
    date_to_be_completed=db.Column(db.String(length=20),nullable=False)
    week_no=db.Column(db.String(length=4),nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'),
        nullable=False)


