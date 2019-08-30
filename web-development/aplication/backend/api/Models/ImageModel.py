from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Image(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    image = db.Column(db.Text)

    def __init__(self, image):
        self.image = image

    def __repr__(self):
        return '<Image %r>' % self.image

