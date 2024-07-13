from flask_sqlalchemy import SQLAlchemy, model
from sqlalchemy.orm import validates

db = SQLAlchemy()


class Restaurant(db.Model):
    __tablename__ = "restaurants"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    address = db.Column(db.String)

    # add relationship
    restaurant_pizzas=db.relationship("RestaurantPizza", backref="restaurants",cascade="all, delete-orphan")

    # add serialization rules
    def details(self):
        return {"id": self.id, "name": self.name, "address": self.address}
    def __repr__(self):
        return f"<Restaurant {self.name}>"


class Pizza(db.Model):
    __tablename__ = "pizzas"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    ingredients = db.Column(db.String)

    # add relationship
    restaurant_pizzas = db.relationship("RestaurantPizza", backref = "pizza", cascade = "all, delete-orphan")

    # add serialization rules
    def details(self):
        return {"id": self.id, "name": self.name, "ingredients": self.ingredients}

    def __repr__(self):
        return f"<Pizza {self.name}, {self.ingredients}>"


class RestaurantPizza(db.Model):
    __tablename__ = "restaurant_pizzas"

    id = db.Column(db.Integer, primary_key=True)
    price = db.Column(db.Integer, nullable=False)
    restaurant_id = db.Column(db.Integer, db.ForeignKey("restaurants.id", ondelete = "CASCADE"), nullable=False)
    pizza_id = db.Column(db.Integer, db.ForeignKey("pizzas.id", ondelete = "CASCADE"), nullable=False)

    # add serialization rules
    def details(self):
        return {"id": self.id, "price": self.price, "restaurant_id": self.restaurant_id, "pizza_id": self.pizza_id}

    # add validation
    def validate(self, key, price):
        if price < 1 or price > 30:
            raise ValueError("Price must be between 1 - 30")
        return price

    def __repr__(self):
        return f"<RestaurantPizza ${self.price}>"

def create_tables():
    with app.app_context():
        db.create_all()  


if __name__ == "__main__":
    create_tables()
