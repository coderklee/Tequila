from flask import Blueprint, request, jsonify
from helpers import token_required
from models import db, User, Tequila, tequila_schema, tequilas_schema

api = Blueprint('api', __name__, url_prefix='/api')

@api.route('/inventory', methods = ['POST'])
@token_required
def add_to_inventory(current_user_token):
    brand = request.json['brand']
    color = request.json['color']
    region = request.json['region']
    alcohol = request.json['alcohol']
    price = request.json['price']
    user_token = current_user_token.token

    print(f"BIG TESTER: {current_user_token.token}")

    tequila = Tequila(brand, color, region, alcohol, price, user_token=user_token)

    db.session.add(tequila)
    db.session.commit()

    response = tequila_schema.dump(tequila)
    return jsonify(response)

@api.route('/inventory', methods = ['GET'])
@token_required
def get_tequila(current_user_token):
    a_user = current_user_token.token
    tequila = Tequila.query.filter_by(user_token = a_user).all()
    response = tequilas_schema.dump(tequila)
    return jsonify(response)

@api.route('/inventory/<id>', methods = ['POST', 'PUT'])
@token_required
def update_tequila(current_user_token, id):
    tequila = Tequila.query.get(id)
    tequila.brand = request.json['brand']
    tequila.color = request.json['color']
    tequila.region = request.json['region']
    tequila.alcohol = request.json['alcohol']
    tequila.price = request.json['price']
    tequila.user_token = current_user_token.token

    db.session.commit()
    response = tequila_schema.dump(tequila)
    return jsonify(response)

@api.route('/inventory/<id>', methods = ['DELETE'])
@token_required
def delete_tequila(current_user_token, id):
    tequila = Tequila.query.get(id)
    db.session.delete(tequila)
    db.session.commit()
    response = tequila_schema.dump(tequila)
    return jsonify(response)

@api.route('/inventory/<id>', methods = ['GET'])
@token_required
def get_single_tequila(current_user_token, id):
    tequila = Tequila.query.get(id)
    response = tequila_schema.dump(tequila)
    return jsonify(response)