import os
from flask_sqlalchemy import SQLAlchemy

database_name = "capstone"
database_path = os.environ.get('DATABASE_URL')

db = SQLAlchemy()

def setup_db(app):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    # migrate = Migrate(app, db)

def db_drop_and_create_all():
    db.drop_all()
    db.create_all()
    db_init_records()

def db_init_records():
    new_album = (Album(title='Your Album',band_id=1))
    new_band = (Band(name='The Beatles',city='Liverpool',state='England'))

    new_album.insert()
    new_band.insert()

class Album(db.Model):
    __tablename__ = 'albums'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    band_id = db.Column(db.Integer)

    def format(self):
        return{
            'id': self.id,
            'title': self.title,
            'band_id': self.band_id
        }
    
    def insert(self):
        db.session.add(self)
        db.session.commit()
    
    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

class Band(db.Model):
    __tablename__ = 'bands'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String)
    state = db.Column(db.String)

    def format(self):
        return{
            'id': self.id,
            'name': self.name,
            'city': self.city,
            'state': self.state
        }
    
    def insert(self):
        db.session.add(self)
        db.session.commit()
    
    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()