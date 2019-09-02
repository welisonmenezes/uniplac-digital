from flask_sqlalchemy import SQLAlchemy
from marshmallow import Schema, fields, pre_load, validate
from flask_marshmallow import Marshmallow
import datetime

ma = Marshmallow()
db = SQLAlchemy()
now = datetime.datetime.now()

class Image(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    image = db.Column(db.Text(length=16000000, collation='utf8_bin'), nullable=False)
    created_at = db.Column(db.Date, default=now)
    updated_at = db.Column(db.Date, default=now, onupdate=now)

    def __init__(self, image):
        self.image = image

    def __repr__(self):
        return '<Image %r>' % self.id

class ImageSchema(ma.Schema):
    id = fields.Integer()
    created_at = fields.DateTime()
    updated_at = fields.DateTime()

ConfigurationImage = db.Table('ConfigurationImage',
    db.Column('image_id', db.Integer, db.ForeignKey('image.id')),
    db.Column('configuration_id', db.Integer, db.ForeignKey('configuration.id'))
)

class Configuration(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(45), nullable=False)
    phone = db.Column(db.String(45), nullable=False)
    email = db.Column(db.String(45), nullable=False)
    created_at = db.Column(db.Date, default=now)
    updated_at = db.Column(db.Date, default=now, onupdate=now)
    images = db.relationship('Image', secondary=ConfigurationImage)

    def __init__(self, name, phone, email):
        self.name = name
        self.phone = phone
        self.email = email

    def __repr__(self):
        return '<Configuration %r>' % self.id

class ConfigurationSchema(ma.Schema):
    id = fields.Integer()
    name = fields.String()
    phone = fields.String()
    email = fields.String()
    created_at = fields.DateTime()
    updated_at = fields.DateTime()
    images = fields.Nested(ImageSchema, many=True)


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255), nullable=False)
    content = db.Column(db.Text(), nullable=False)
    genre = db.Column(db.String(15), nullable=False)
    status = db.Column(db.String(15), nullable=False)
    entry_date = db.Column(db.Date, nullable=False)
    departure_date = db.Column(db.Date, nullable=False)
    created_at = db.Column(db.Date, default=now, nullable=False)
    updated_at = db.Column(db.Date, default=now, onupdate=now, nullable=False)
    image_id = db.Column(db.Integer, db.ForeignKey('image.id'), nullable=False)

    def __init__(self, title, description, content, genre, status, entry_date, departure_date, image_id):
        self.title = title
        self.description = description
        self.content = content
        self.genre = genre
        self.status = status
        self.entry_date = entry_date
        self.departure_date = departure_date
        self.image_id = image_id

    def __repr__(self):
        return '<Post %r>' % self.id


class PostSchema(ma.Schema):
    id = fields.Integer()
    title = fields.String()
    description = fields.String()
    content = fields.String()
    genre = fields.String()
    status = fields.String()
    entry_date = fields.DateTime()
    departure_date = fields.DateTime()
    created_at = fields.DateTime()
    updated_at = fields.DateTime()
    image_id = fields.Integer()
