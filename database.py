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
        Drink(name="Espresso", source="Cafe", taste=4.5, cost=3.5, fun_factor=4.0, overall_score=4.0),
        Drink(name="Latte", source="Coffee Shop", taste=4.2, cost=4.0, fun_factor=3.8, overall_score=4.0),
        Drink(name="Green Tea", source="Cafe", taste=4.0, cost=3.0, fun_factor=3.5, overall_score=3.5),
        Drink(name="Cola", source="Grocery Store", taste=3.8, cost=2.0, fun_factor=4.2, overall_score=3.3),
        Drink(name="Orange Juice", source="Grocery Store", taste=4.3, cost=2.5, fun_factor=3.5, overall_score=3.4),
        Drink(name="Cappuccino", source="Coffee Shop", taste=4.4, cost=3.8, fun_factor=4.0, overall_score=4.1),
        Drink(name="Iced Tea", source="Cafe", taste=3.9, cost=2.8, fun_factor=3.7, overall_score=3.5),
        Drink(name="Smoothie", source="Cafe", taste=4.5, cost=4.5, fun_factor=4.3, overall_score=4.4),
        Drink(name="Hot Chocolate", source="Coffee Shop", taste=4.6, cost=3.5, fun_factor=4.5, overall_score=4.2),
        Drink(name="Lemonade", source="Grocery Store", taste=4.1, cost=2.2, fun_factor=3.8, overall_score=3.4),
        Drink(name="Chai Latte", source="Coffee Shop", taste=4.3, cost=4.0, fun_factor=4.1, overall_score=4.1),
        Drink(name="Americano", source="Cafe", taste=4.0, cost=3.2, fun_factor=3.5, overall_score=3.6),
        Drink(name="Matcha Latte", source="Cafe", taste=4.2, cost=4.2, fun_factor=4.0, overall_score=4.1),
        Drink(name="Fruit Punch", source="Grocery Store", taste=3.9, cost=2.5, fun_factor=4.0, overall_score=3.5),
        Drink(name="Mocha", source="Coffee Shop", taste=4.5, cost=4.0, fun_factor=4.2, overall_score=4.2),
        Drink(name="Coconut Water", source="Grocery Store", taste=3.7, cost=3.0, fun_factor=3.5, overall_score=3.4),
        Drink(name="Bubble Tea", source="Cafe", taste=4.4, cost=4.5, fun_factor=4.7, overall_score=4.5),
        Drink(name="Iced Coffee", source="Coffee Shop", taste=4.1, cost=3.5, fun_factor=3.9, overall_score=3.8),
        Drink(name="Ginger Ale", source="Grocery Store", taste=3.8, cost=2.0, fun_factor=3.6, overall_score=3.1),
        Drink(name="Macchiato", source="Cafe", taste=4.3, cost=3.8, fun_factor=4.0, overall_score=4.0)
    ]
    db.session.add_all(initial_drinks)
    db.session.commit()
