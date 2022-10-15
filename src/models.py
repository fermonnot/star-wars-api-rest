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
    id_user = db.Column(db.Integer, db.ForeignKey('user.id'))
    nature = db.Column(db.Enum(Nature), nullable=False)
    name = db.Column(db.String(50), nullable=False)    

    # __table_args__ = (db.UniqueConstraint(
    #     "id_user",
    #     "name",
    #     name="unique_favorites_for_user"
    #     ),)

    def serialize(self):
        user= User.query.get(self.user_id)
        return {
            "id" : self.id,
            "name": self.name,
            "nature": self.nature.value,
            "user": user.serialize()
            
        }
    
    


