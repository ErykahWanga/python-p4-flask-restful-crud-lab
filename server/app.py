from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_restful import Resource, Api
from flask_cors import CORS
from models import db, Plant



app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

CORS(app)
db.init_app(app)
migrate = Migrate(app, db)
api = Api(app)

class PlantResource(Resource):
    def get(self, id):
        plant = db.session.get(Plant, id)
        if not plant:
            return make_response({'error': 'Plant not found'}, 404)
        return make_response({
            'id': plant.id,
            'name': plant.name,
            'image': plant.image,
            'price': plant.price,
            'is_in_stock': plant.is_in_stock
        }, 200)

    def patch(self, id):
        plant = db.session.get(Plant, id)
        if not plant:
            return make_response({'error': 'Plant not found'}, 404)
        
        data = request.get_json()
        if 'is_in_stock' in data:
            plant.is_in_stock = data['is_in_stock']
        
        try:
            db.session.commit()
            return make_response({
                'id': plant.id,
                'name': plant.name,
                'image': plant.image,
                'price': plant.price,
                'is_in_stock': plant.is_in_stock
            }, 200)
        except Exception as e:
            db.session.rollback()
            return make_response({'errors': [str(e)]}, 422)

    def delete(self, id):
        plant = db.session.get(Plant, id)
        if not plant:
            return make_response({'error': 'Plant not found'}, 404)
        
        db.session.delete(plant)
        db.session.commit()
        return make_response('', 204)

api.add_resource(PlantResource, '/plants/<int:id>')

if __name__ == '__main__':
    app.run(port=5555, debug=True) 