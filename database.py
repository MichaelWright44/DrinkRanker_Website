from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Drink(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    source = db.Column(db.String(50), nullable=False)
    taste = db.Column(db.Float, nullable=False)
    cost = db.Column(db.Float, nullable=False)
    fun_factor = db.Column(db.Float, nullable=False)
    overall_score = db.Column(db.Float, nullable=False)
    image_filename = db.Column(db.String(255))

    def __repr__(self):
        return f'<Drink {self.name}>'

class DrinkSuggestion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    source = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text, nullable=False)
    submitted_by = db.Column(db.String(100), nullable=False)
    status = db.Column(db.String(20), default='pending')

    def __repr__(self):
        return f'<DrinkSuggestion {self.name}>'

def init_db(app):
    db.init_app(app)
    with app.app_context():
        db.create_all()
        if Drink.query.count() == 0:
            add_initial_drinks()

def add_initial_drinks():
    initial_drinks = [
        Drink(name="Espresso", source="Cafe", taste=4.5, cost=3.5, fun_factor=4.0, overall_score=4.0, image_filename=""),
        Drink(name="Latte", source="Coffee Shop", taste=4.2, cost=4.0, fun_factor=3.8, overall_score=4.0, image_filename=""),
        Drink(name="Green Tea", source="Cafe", taste=4.0, cost=3.0, fun_factor=3.5, overall_score=3.5, image_filename=""),
        Drink(name="Cola", source="Grocery Store", taste=3.8, cost=2.0, fun_factor=4.2, overall_score=3.3, image_filename=""),
        Drink(name="Orange Juice", source="Grocery Store", taste=4.3, cost=2.5, fun_factor=3.5, overall_score=3.4, image_filename=""),
    ]
    db.session.add_all(initial_drinks)
    db.session.commit()
