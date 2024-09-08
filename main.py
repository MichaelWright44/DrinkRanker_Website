from flask import Flask, render_template, jsonify
from config import Config
from database import db, init_db, Drink

app = Flask(__name__)
app.config.from_object(Config)
init_db(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/drinks')
def get_drinks():
    drinks = Drink.query.all()
    return jsonify([
        {
            'name': drink.name,
            'source': drink.source,
            'taste': drink.taste,
            'cost': drink.cost,
            'fun_factor': drink.fun_factor,
            'overall_score': drink.overall_score
        } for drink in drinks
    ])

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
