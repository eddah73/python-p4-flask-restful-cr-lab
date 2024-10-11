#!/usr/bin/env python3

from flask import Flask, jsonify, request, make_response
from flask_migrate import Migrate
from flask_restful import Api, Resource
from models import db, Plant

# Initialize the Flask app
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///plants.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = True

# Initialize Flask extensions
migrate = Migrate(app, db)
db.init_app(app)
api = Api(app)

# Resource class for handling all plants
class Plants(Resource):
    def get(self):
        # Retrieve all plants and return as JSON
        response_dict = [n.to_dict() for n in Plant.query.all()]
        response = make_response(
            jsonify(response_dict),
            200,
        )
        return response

    def post(self):
        # Extract data from the request
        data = request.get_json()
        
        # Create a new Plant instance
        new_plant = Plant(
            name=data.get('name'),
            image=data.get('image'),
            price=data.get('price')
        )

        # Add the new plant to the session and commit
        db.session.add(new_plant)
        db.session.commit()

        # Return the new plant data with a success response
        return make_response(new_plant.to_dict(), 201)

# Resource class for handling plant by ID
class PlantByID(Resource):
    def get(self, id):
        # Use session.get to retrieve a plant by ID
        plant = db.session.get(Plant, id)
        if plant:
            response = make_response(
                jsonify(plant.to_dict()),
                200,
            )
        else:
            response = make_response(
                {"error": "Plant not found"},
                404,
            )
        return response

# Register resources with Flask-RESTful
api.add_resource(Plants, '/plants')
api.add_resource(PlantByID, '/plants/<int:id>')

# Run the app
if __name__ == '__main__':
    app.run(port=5555, debug=True)