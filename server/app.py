
class PlantByID(Resource):

    def get(self, id):
        plant = Plant.query.filter_by(id=id).first()
        if plant:
            return make_response(plant.to_dict(), 200)
        return make_response({"error": "Plant not found"}, 404)

    def patch(self, id):
        plant = Plant.query.filter_by(id=id).first()
        if not plant:
            return make_response({"error": "Plant not found"}, 404)

        data = request.get_json()
        if "is_in_stock" in data:
            plant.is_in_stock = data["is_in_stock"]

        db.session.commit()
        return make_response(plant.to_dict(), 200)

    def delete(self, id):
        plant = Plant.query.filter_by(id=id).first()
        if not plant:
            return make_response({"error": "Plant not found"}, 404)

        db.session.delete(plant)
        db.session.commit()
        return make_response('', 204)
