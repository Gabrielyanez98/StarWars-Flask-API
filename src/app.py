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
from models import db, User, Favorite, Planets, Characters
#from models import Personn

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
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


# --- ENDPOINTS ---

#Get all users
@app.route('/user', methods=['GET'])
def handle_user():

    user_query = User.query.all()
    results = list(map(lambda item: item.serialize(),user_query))
    print(results)

    return jsonify(results), 200

#Get all planets
@app.route('/planets', methods=['GET'])
def handle_planets():

    planets_query = Planets.query.all()
    results = list(map(lambda item: item.serialize(),planets_query))
    print(results)

    return jsonify(results), 200

#Get one planet
@app.route('/planets/<int:planet_id>', methods=['GET'])
def get_one_planet(planet_id):

    planet_query = Planets.query.filter_by(id=planet_id).first()
    print(planet_query.serialize())

    return jsonify(planet_query.serialize()), 200

#Get all characters
@app.route('/characters', methods=['GET'])
def handle_characters():

    characters_query = Characters.query.all()
    results = list(map(lambda item: item.serialize(),characters_query))
    print(results)

    return jsonify(results), 200

#Get one character
@app.route('/characters/<int:character_id>', methods=['GET'])
def get_one_character(character_id):

    character_query = Characters.query.filter_by(id=character_id).first()
    print(character_query.serialize())

    return jsonify(character_query.serialize()), 200

#Get all favorites

@app.route('user/favorites', methods=['GET'])
def handle_favorites():
          
        favorites_query = Favorite.query.all()
        results = list(map(lambda item: item.serialize(),favorites_query))
        print(results)
    
        return jsonify(results), 200

#Add new favorite planet
@app.route('/favorites/planets', methods=['POST'])
def add_favorite_planet():
    
        request_body = request.get_json()
        print(request_body)
    
        new_favorite = Favorite(
            user_id=request_body["user_id"],
            planet_id=request_body["planet_id"]
        )
    
        db.session.add(new_favorite)
        db.session.commit()
    
        return jsonify(new_favorite.serialize()), 200

#Add new favorite character
@app.route('/favorites/characters', methods=['POST'])
def add_favorite_character():
        
            request_body = request.get_json()
            print(request_body)
        
            new_favorite = Favorite(
                user_id=request_body["user_id"],
                character_id=request_body["character_id"]
            )
        
            db.session.add(new_favorite)
            db.session.commit()
        
            return jsonify(new_favorite.serialize()), 200

#Delete favorite planet
@app.route('/favorites/planets/<int:planet_id>', methods=['DELETE'])
def delete_favorite_planet(planet_id):
        
            favorite_planet = Favorite.query.filter_by(planet_id=planet_id).first()
            db.session.delete(favorite_planet)
            db.session.commit()
        
            return jsonify(favorite_planet.serialize()), 200

#Delete favorite character
@app.route('/favorites/characters/<int:character_id>', methods=['DELETE'])
def delete_favorite_character(character_id):
            
                favorite_character = Favorite.query.filter_by(character_id=character_id).first()
                db.session.delete(favorite_character)
                db.session.commit()
            
                return jsonify(favorite_character.serialize()), 200


# --- /ENDPOINTS ---

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
