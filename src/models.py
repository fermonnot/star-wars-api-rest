from flask_sqlalchemy import SQLAlchemy
from enum import Enum, unique

db = SQLAlchemy()

class Nature(Enum):
    character = "character"
    planet = "planet"


class Character (db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    height = db.Column(db.String(80), unique=False, nullable=False)

    @classmethod 
    def create(self):
        pass
    
    def serialize(self):
        return {
            "id" : self.id,
            "name": self.name,
            "heigth": self.height
        }



class Planet (db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    population = db.Column(db.String(80), unique=False, nullable=False)

    @classmethod 
    def create(self):
        pass
    
    def serialize(self):
        return {
            "id" : self.id,
            "name": self.name,
            "population": self.population
        }

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)
    favorites = db.relationship("Favorites", backref="user", uselist=True)
    
    
    def __repr__(self):
        return '<User %r>' % self.email

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, its a security breach
        }



class Favorites(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    nature = db.Column(db.Enum(Nature), nullable=False)
    name = db.Column(db.String(50), nullable=False)    

    nature_id = db.Column(db.Integer, nullable=False)
    
    # __table_args__ = (db.UniqueConstraint(), {
    #     "user.id",
    #     "name_favorite"
    # })
   
    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "name": self.name,
            "nature": self.nature.name
        }
    
    


