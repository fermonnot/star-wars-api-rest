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
from models import db, Character, Planet, Favorites, User
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





@app.route('/character', methods=['GET'])
@app.route('/character/<int:character_id>', methods=['GET'])
def handle_character(character_id = None):
    if request.method == 'GET':
        if character_id is None:

            characters = Character.query.all()
            if characters is None:
                return jsonify ({"Message":"empty list"})
            else:
                return jsonify(list(map(lambda item: item.serialize(), characters))) , 200
        else:
            character = Character.query.get(character_id)
            if character:
                return jsonify(character.serialize())
            
        return jsonify({"message":"not found"}), 404
 


 

@app.route('/character', methods=['POST'])
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
            
            planets = Planet.query.all()
            if planets is None:
                return jsonify ({"Message":"empty list"})
            else:
                return jsonify(list (map(lambda item: item.serialize(), planets))), 200  
        else:
            planet = Planet.query.get(planet_id)
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
        
        new_planet = Planet(name=body["name"],population=body.get("population"))
        db.session.add(new_planet)

        try:
            db.session.commit()
            return jsonify(new_planet.serialize()), 201
        except Exception as error:
            print(error.args)
            db.session.rollback()
            return jsonify ({"message":f"Error {error.args}"}), 500

@app.route('/users', methods=['GET'])
@app.route('/users/<int:user_id>', methods=['GET'])
def handle_user(user_id = None):
    if request.method == 'GET':
        if user_id is None:
            users = User()
            users = users.query.all()

            return jsonify(list(map(lambda item: item.serialize(), users))), 200
        else:
            user = User()
            user = user.query.get(user_id)

            if user:
                return jsonify(user.serialize()), 200
                
        return jsonify({"message": "Not found"}), 404


@app.route("/users/<int:user_id>/favorites", methods=['GET'])
@app.route("/users/<int:user_id>/favorites/<string:nature>/", methods=['GET'])
@app.route("/users/<int:user_id>/favorites/<string:nature>/<int:favorite_id>", methods=['GET'])
def get_favorite(user_id = None, nature = None, favorite_id=None):
    if request.method == 'GET':
        user = User.query.get(user_id)
        if user is None:
            return jsonify({"message": "Error, couldn't find user"}), 404
        elif user is not None:
            if nature is None:
                favorites = Favorites()
                favorites = Favorites.query.all()
                return jsonify(list(map(lambda items: items.serialize(), favorites))), 200
                
            elif nature is not None:    
                if nature != 'character' and nature != 'planet':
                    return jsonify({"message": "Error, bad request"}), 400
                else:
                    if nature == 'character' and favorite_id is None:
                        favorites = Favorites.query.all()
                        favorite_character = filter_character(favorites)
                        return jsonify(favorite_character), 200

                    elif nature == 'character' and favorite_id is not None:
                        favorite = Favorites.query.get(favorite_id)
                        if favorite is None:
                            return jsonify({"message": "Error, couldn't find character"}), 404
                       
                    elif nature == 'planet' and favorite_id is None:
                        favorites = Favorites.query.all()
                        favorite_planet = filter_planet(favorites)
                        return jsonify(favorite_planet), 200

                    elif nature == 'planet' and favorite_id is not None:
                        favorite = Favorites.query.get(favorite_id)
                        if favorite is None:
                            return jsonify({"message": "Error, couldn't find planet"}), 404
                        elif favorite is not None:
                            if favorite.serialize()["nature"] != "planets":
                                return jsonify({"message": "Error, favorite isn't a planet"}), 406
                            else:
                                return jsonify(favorite.serialize()), 200


@app.route("/users/<int:user_id>/favorites", methods=['POST'])
def handle_favorites(user_id = None):
    if request.method == 'POST':
        user = User.query.get(user_id)
        if user is None:
            return jsonify({"message":"Error, couldn't find user"}), 404
        elif user is not None:

            body = request.json
            if body.get("nature") != "character" and body["nature"] != "planet" :
                return jsonify({"message":"Error, bad property"}), 400
            elif body.get("name") is None:
                return jsonify({"message":"Error, bad property"}), 400
            elif body.get("nature_id") is None :
                return jsonify({"message":"Error, bad property"}), 400

            new_favorite = Favorites(name=body.get("name"), nature=body.get("nature"), nature_id=body.get("nature_id"), user_id=user_id)
            
            db.session.add(new_favorite)

            try:
                db.session.commit()
                return jsonify(new_favorite.serialize()), 201
            except Exception as error:
                print(error.args)
                db.session.rollback()
                return jsonify({"message": f"Error {error.args}"}), 500



@app.route("/users/<int:user_id>/favorites/<string:nature>/<int:favorite_id>", methods=['DELETE'])
def delete_favorite(user_id = None, nature = None, favorite_id = None):
    if request.method == 'DELETE':
        user = User.query.get(user_id)
        if user is None:
            return jsonify({"message": "Error, couldn't find user"}), 404
        elif user is not None:
            if nature is None and nature != "character" and nature != "planet":
                return jsonify({"message": "Error, invalid or missing nature"}), 406
            else:
                if favorite_id is None:
                    return jsonify({"message": "Error, missing favorite id"}), 400
                elif favorite_id is not None:
                    deleted_favorite = Favorites.query.get(favorite_id)
                    if deleted_favorite is None:
                        return jsonify({"message": "Error, couldn't find favorite"}), 404
                    elif deleted_favorite is not None:
                        db.session.delete(deleted_favorite)

                        try:
                            db.session.commit()
                            return jsonify([]), 204
                        except Exception as error:
                            print(error.args)
                            db.session.rollback()
                            return jsonify({"message": f"Error {error.args}"})
























# @app.route('/favorites/<int:user_id>', methods=['GET'])
# # @app.route('/favorites/<int:user_id>/<nature>', methods=['GET'])     
# def handle_Favorites(user_id = None):
#     if request.method == 'GET':
#         if user_id is not None:
           
#             favorites = Favorites.query.filter_by(id_user=user_id).all()
        
#             return jsonify(favorites), 200 
    

#         return jsonify ({"message":"Not Found"}), 404
    
#     else:

#         return jsonify ({"message":f"method not accepted"}), 405





# @app.route('/favorites/<int:user_id>/<nature>', methods=['POST'])
# def add_favoites(user_id = None, nature = None):
#     if request.method == 'POST':
#         if user_id is not None and nature is not None:
#             print(user_id, nature)
#             user = User.query.filter_by(id=user_id).first()
#             if user: 
#                 body = request.json
#                 if nature is not None and body['name'] is not None:
#                     new_favorite = Favorites(id_user = user_id, nature=nature, name=body['name'])
#                     db.session.add(new_favorite)
#                     try:
#                         db.session.commit()
#                         return jsonify(new_favorite.serialize()), 201
#                     except Exception as error:
#                         db.session.rollback()
#                         return jsonify({"message":error.args}), 500
#                 print(user.serialize())
#                 return "hola" 
#             else: 
#                 return jsonify ({"message":f"user not Found"}), 404
#     else:
#         return jsonify ({"message":f"method not accepted"}), 405


# @app.route('/favorites', methods=['DELETE'])
# @app.route('/favorites/<int:user_id>/<int:favorite_id>', methods=['DELETE'])
# def delete_favorite(user_id=None):
#     if request.method == 'DELETE':
#         if favorite_id is None:
#             return jsonify({"message":"Not found"}), 400

#         if user_id is not None:
#             delete_favorite = Favorites.query.get(user_id)
            
#             if delete_favorite is None:
#                 return jsonify({"message":"Not found"}), 404
#             else:
#                 db.session.delete(delete_favorite)

#                 try:
#                     db.session.commit()
#                     return jsonify([]), 204
#                 except Exception as error:
#                     print(error.args)
#                     db.session.rollback()
#                     return jsonify({"message":f"Error {error.args}"}),500
        
#     return jsonify([]), 405





# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)

