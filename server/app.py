from flask import Flask, jsonify, request
from models import db, Plant

@app.route("/plants", methods=["GET"])
def get_plants():
    plants = Plant.query.all()
    return jsonify([p.to_dict() for p in plants]), 200


@app.route("/plants/<int:id>", methods=["GET"])
def get_plant(id):
    plant = Plant.query.get(id)
    if not plant:
        return jsonify({"error": "Plant not found"}), 404
    return jsonify(plant.to_dict()), 200


@app.route("/plants", methods=["POST"])
def create_plant():
    data = request.get_json()

    plant = Plant(
        name=data["name"],
        image=data["image"],
        price=data["price"]
    )

    db.session.add(plant)
    db.session.commit()

    return jsonify(plant.to_dict()), 201
