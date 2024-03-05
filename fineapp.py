import os
from flask import Flask, render_template 
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
db_path = os.path.join(os.path.dirname(__file__), 'market.db')
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
db = SQLAlchemy(app)

class Item(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(length=30), nullable=False, unique=True)
    price = db.Column(db.Integer(), nullable=False)
    barcode = db.Column(db.String(length=12), nullable=False, unique=True)
    description = db.Column(db.String(length=1024), nullable=False, unique=True)

    def __repr__(self):
        return f'Item {self.name}'

with app.app_context():
    db.create_all()

@app.route('/')
@app.route('/home_page')
def home_page():
    return render_template('home_page.html')

@app.route('/market')

def market_page():
    items = Item.query.all()

    if not items:
        # Add items to the database if it's empty
        phone = Item(name='Phone', barcode='893212299897', price=500, description='A mobile phone')
        laptop = Item(name='Laptop', barcode='123985473165', price=900, description='A laptop computer')
        keyboard = Item(name='Keyboard', barcode='231985128446', price=150, description='A computer keyboard')

        db.session.add_all([phone, laptop, keyboard])
        db.session.commit()

        items = Item.query.all()

    return render_template('market.html', items=items)

if __name__ == '__main__':
    app.run(debug=True)
