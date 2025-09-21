
from flask import Flask, jsonify, request
from flask_migrate import Migrate
from models import db, Restaurant, Pizza, RestaurantPizza

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)
migrate = Migrate(app, db)

# ---------------- ROUTES ---------------- #

# GET /restaurants
@app.route("/restaurants", methods=["GET"])
def get_restaurants():
    restaurants = Restaurant.query.all()
    return jsonify([r.to_dict() for r in restaurants]), 200

# GET /restaurants/:id
@app.route("/restaurants/<int:id>", methods=["GET"])
def get_restaurant(id):
    restaurant = Restaurant.query.get(id)
    if restaurant:
        data = {
            "id": restaurant.id,
            "name": restaurant.name,
            "address": restaurant.address,
            "restaurant_pizzas": [rp.to_dict() for rp in restaurant.restaurant_pizzas]
        }
        return jsonify(data), 200
    return jsonify({"error": "Restaurant not found"}), 404

# DELETE /restaurants/:id
@app.route("/restaurants/<int:id>", methods=["DELETE"])
def delete_restaurant(id):
    restaurant = Restaurant.query.get(id)
    if not restaurant:
        return jsonify({"error": "Restaurant not found"}), 404
    db.session.delete(restaurant)
    db.session.commit()
    return "", 204

# GET /pizzas
@app.route("/pizzas", methods=["GET"])
def get_pizzas():
    pizzas = Pizza.query.all()
    return jsonify([p.to_dict() for p in pizzas]), 200

# POST /restaurant_pizzas
@app.route("/restaurant_pizzas", methods=["POST"])
def create_restaurant_pizza():
    data = request.get_json()

    try:
        new_rp = RestaurantPizza(
            price=data["price"],
            pizza_id=data["pizza_id"],
            restaurant_id=data["restaurant_id"],
        )
        db.session.add(new_rp)
        db.session.commit()
        return jsonify(new_rp.to_dict()), 201
    except Exception as e:
        return jsonify({"errors": ["validation errors"]}), 400

