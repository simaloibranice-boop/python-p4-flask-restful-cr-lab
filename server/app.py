from flask import Flask, jsonify, request
from flask_migrate import Migrate

from models import db, Plant

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)

with app.app_context():
    db.create_all()

    if not Plant.query.first():
        aloe = Plant(
            id=1,
            name="Aloe",
            image="./images/aloe.jpg",
            price=11.50,
        )
        zz_plant = Plant(
            id=2,
            name="ZZ Plant",
            image="./images/zz-plant.jpg",
            price=25.98,
        )
        db.session.add_all([aloe, zz_plant])
        db.session.commit()


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
        price=data["price"],
    )

    db.session.add(plant)
    db.session.commit()

    return jsonify(plant.to_dict()), 201
