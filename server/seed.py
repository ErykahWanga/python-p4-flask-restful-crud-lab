from app import app
from models import db, Plant

with app.app_context():
    print("🌱 Seeding database...")

    # Clear existing data
    Plant.query.delete()

    # Add new plants
    p1 = Plant(name="Aloe", image="./images/aloe.jpg", price=11.50, is_in_stock=True)
    p2 = Plant(name="Snake Plant", image="./images/snake.jpg", price=15.00, is_in_stock=False)

    db.session.add_all([p1, p2])
    db.session.commit()

    print("✅ Done seeding!")
