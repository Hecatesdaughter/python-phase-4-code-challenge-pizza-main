#!/usr/bin/env python3
from models import db, Restaurant, RestaurantPizza, Pizza
from flask_migrate import Migrate
from flask import Flask, request, make_response
from flask_restful import Api, Resource, reqparse, fields, marshal_with, abort
import os

BASE = 'http://127.0.0.1:5555'
DATABASE = 'sqlite:///app.db'

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

migrate = Migrate(app, db)

api = Api(app)

@app.route("/")
def index():
    return "<h1>Restaurants</h1>"

resource_fields = {
    "id": fields.Integer,
    "name": fields.String,
    "address": fields.String
}



class Restaurants(Resource):
    @app.route("/restaurants")
    def get(self):
        result = Restraurant.query.all()
        return result

    @app.route("/restaurants/<int:restaurant_id>", methods=["GET"])
    @marshal_with(resource_fields)
    def get_restaurant(self, restaurant_id):
        result = Restaurant.query.filter_by(id = restaurant_id).first()
        if  not result:
            abort(404, message = "Could not find restaurant with that id")
        return result

    def delete(self, restaurant_id):
        del restaurants[restaurant_id]
        return '', 204
api.add_resource(Restaurants, "/restaurants")
      

pizza_fields = {
    "id": fields.Integer,
    "name": fields.String,
    "ingredients": fields.String
}

class Pizzas(Resource):
    @app.route("/pizzas")
    def get(self):
        result = Pizza.query.all()
        return result
    @app.route("/pizzas/<int:pizza_id>", methods=["GET"])   
    @marshal_with(pizza_fields)
    def get_pizza(self, pizza_id):
        result = Pizza.query.filter_by(id=pizza_id).first()
        if not result:
            abort(404, message="Could not find pizza with that id")
        return result


restaurant_pizza_fields = {
    "restaurant_id": fields.Integer,
    "pizza_id": fields.Integer
}

class RestaurantPizzas(Resource):
    @marshal_with(restaurant_pizza_fields)
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("restaurant_id", type=int, required=True, help="Restaurant ID is required")
        parser.add_argument("pizza_id", type=int, required=True, help="Pizza ID is required")
        args = parser.parse_args()

        new_restaurant_pizza = RestaurantPizza(restaurant_id=args["restaurant_id"], pizza_id=args["pizza_id"])
        db.session.add(new_restaurant_pizza)
        db.session.commit()

        return new_restaurant_pizza, 201

api.add_resource(RestaurantPizzas, "/restaurant_pizzas")

if __name__ == "__main__":
    app.run(port=5555, debug=True)

