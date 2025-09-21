
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates

db = SQLAlchemy()

class Restaurant(db.Model):
    __tablename__ = "restaurants"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    address = db.Column(db.String, nullable=False)

    restaurant_pizzas = db.relationship("RestaurantPizza", back_populates="restaurant", cascade="all, delete-orphan")

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "address": self.address
        }

class Pizza(db.Model):
    __tablename__ = "pizzas"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    ingredients = db.Column(db.String, nullable=False)

    restaurant_pizzas = db.relationship("RestaurantPizza", back_populates="pizza")

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "ingredients": self.ingredients
        }

class RestaurantPizza(db.Model):
    __tablename__ = "restaurant_pizzas"

    id = db.Column(db.Integer, primary_key=True)
    price = db.Column(db.Integer, nullable=False)

    restaurant_id = db.Column(db.Integer, db.ForeignKey("restaurants.id"))
    pizza_id = db.Column(db.Integer, db.ForeignKey("pizzas.id"))

    restaurant = db.relationship("Restaurant", back_populates="restaurant_pizzas")
    pizza = db.relationship("Pizza", back_populates="restaurant_pizzas")

    @validates("price")
    def validate_price(self, key, value):
        if value < 1 or value > 30:
            raise ValueError("Price must be between 1 and 30")
        return value

    def to_dict(self):
        return {
            "id": self.id,
            "price": self.price,
            "pizza_id": self.pizza_id,
            "restaurant_id": self.restaurant_id,
            "pizza": self.pizza.to_dict(),
            "restaurant": self.restaurant.to_dict(),
        }

