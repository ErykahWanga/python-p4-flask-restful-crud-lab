from app import app
from models import db, Plant
import json
import unittest

class TestPlant(unittest.TestCase):
    def setUp(self):
        # Set up test client and database
        self.client = app.test_client()

        with app.app_context():
            db.drop_all()
            db.create_all()

            # Create one test plant
            plant = Plant(
                name="Test Plant",
                image="./images/test.jpg",
                price=9.99,
                is_in_stock=True
            )
            db.session.add(plant)
            db.session.commit()

    def test_plant_by_id_get_route(self):
        '''has a resource available at "/plants/<int:id>".'''
        response = self.client.get('/plants/1')
        assert(response.status_code == 200)

    def test_plant_by_id_get_route_returns_one_plant(self):
        '''returns JSON representing one Plant object at "/plants/<int:id>".'''
        response = self.client.get('/plants/1')
        data = json.loads(response.data.decode())
        assert(type(data) == dict)
        assert(data["id"])

    def test_plant_by_id_patch_route_updates_is_in_stock(self):
        '''returns JSON representing updated Plant object with "is_in_stock" = False at "/plants/<int:id>".'''
        response = self.client.patch(
            '/plants/1',
            json={"is_in_stock": False},
            headers={"Content-Type": "application/json"}
        )
        data = json.loads(response.data.decode())
        assert(data["is_in_stock"] is False)
