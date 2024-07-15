#!/usr/bin/env python3

from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///plants.db"
db = SQLAlchemy(app)

class Plant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    image = db.Column(db.String(200), nullable=False)
    price = db.Column(db.Float, nullable=False)
    is_in_stock = db.Column(db.Boolean, default=True)

@app.route("/plants/<int:id>", methods=["PATCH"])
def update_plant(id):
    plant = Plant.query.get(id)
    if plant is None:
        return jsonify({"error": "Plant not found"}), 404
    data = request.get_json()
    plant.is_in_stock = data["is_in_stock"]
    db.session.commit()
    return jsonify(plant.to_dict())

@app.route("/plants/<int:id>", methods=["DELETE"])
def delete_plant(id):
    plant = Plant.query.get(id)
    if plant is None:
        return jsonify({"error": "Plant not found"}), 404
    db.session.delete(plant)
    db.session.commit()
    return "", 204

if __name__ == "__main__":
    app.run(debug=True, port=5555)