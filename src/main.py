"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, Character, Planets, Favorites, User
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
db_url = os.getenv('DATABASE_URL')
# app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)






 

@app.route('/people', methods=['POST'])
def add_new_character():
    if request.method == 'POST':
        body = request.json
        if body.get("name") is None:
            return {"message":"error.propertie bad"}, 400
        
        if body.get("height") is None:
            return {"message":"error.propertie bad"}, 400
        
        new_character = Character(name=body["name"],height=body.get("height"))
        db.session.add(new_character)

        try:
            db.session.commit()
            return jsonify(new_character.serialize()), 201
        except Exception as error:
            print(error.args)
            db.session.rollback()
            return jsonify ({"message":f"Error {error.args}"}), 500


@app.route('/planets', methods=['GET']) 
@app.route('/planets/<int:planet_id>', methods=['GET']) 
def handle_planet(planet_id = None):
    if request.method == 'GET':
        if planet_id is None:
            planets = Planets()
            planets = planets.query.all()
            return jsonify(list (map(lambda item: item.serialize(), planets))), 200  
        else:
            planet = Planet()
            planet = query.get(planet_id)
            if planet:
                return jsonify (planet.serialize())

        return jsonify ({"message":"Not Found"}), 404



@app.route('/planets', methods=['POST'])
def add_new_planet():
    if request.method == 'POST':
        body = request.json
        if body.get("name") is None:
            return {"message":"error.propertie bad"}, 400
        
        if body.get("population") is None:
            return {"message":"error.propertie bad"}, 400
        
        new_planet = Planets(name=body["name"],population=body.get("population"))
        db.session.add(new_planet)

        try:
            db.session.commit()
            return jsonify(new_planet.serialize()), 201
        except Exception as error:
            print(error.args)
            db.session.rollback()
            return jsonify ({"message":f"Error {error.args}"}), 500


@app.route('/favorites/', methods=['GET'])
@app.route('/favorites/<int:user_id>', methods=['GET'])     
def handle_Favorites(user_id = None):
    if request.method == 'GET':
        if user_id is not None:
           
            favorites = Favorites.query.filter_by(id_user=user_id).all()
            print(favorites)
            return jsonify(favorites), 200 
        # else:
        #     favorite = Favorite()
        #     favorite = query.get(user_id)
        #     if planet:
        #         return jsonify (planet.serialize())

        return jsonify ({"message":"Not Found"}), 404
    
    else:

        return jsonify ({"message":f"method not accepted"}), 405





@app.route('/favorites/<int:user_id>/<nature>', methods=['POST'])
def add_favoites(user_id = None, nature = None):
    if request.method == 'POST':
        if user_id is not None and nature is not None:
            print(user_id, nature)
            user = User.query.filter_by(id=user_id).first()
            if user: 
                body = request.json
                if nature is not None and body['name'] is not None:
                    new_favorite = Favorites(id_user = user_id, nature=nature, name=body['name'])
                    db.session.add(new_favorite)
                    try:
                        db.session.commit()
                        return jsonify(new_favorite.serialize()), 201
                    except Exception as error:
                        db.session.rollback()
                        return jsonify({"message":error.args}), 500
                print(user.serialize())
                return "hola" 
            else: 
                return jsonify ({"message":f"user not Found"}), 404
    else:
        return jsonify ({"message":f"method not accepted"}), 405


@app.route('/favorites', methods=['DELETE'])
@app.route('/favorites/<int:user_id>/<int:favorite_id>', methods=['DELETE'])
def delete_favorite(user_id=None):
    if request.method == 'DELETE':
        if user_id is None:
            return jsonify({"message":"Not found"}), 400

        if user_id is not None:
            delete_favorite = Human.query.get(user_id)
            
            if delete_human is None:
                return jsonify({"message":"Not found"}), 404
            else:
                db.session.delete(delete_human)

                try:
                    db.session.commit()
                    return jsonify([]), 204
                except Exception as error:
                    print(error.args)
                    db.session.rollback()
                    return jsonify({"message":f"Error {error.args}"}),500
        
    return jsonify([]), 405





# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)

