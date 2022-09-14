
import string
from turtle import color
from unicodedata import name
from flask import Flask, render_template, request,  redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_wtf import FlaskForm 
from wtforms import StringField, IntegerField, FloatField
from wtforms.validators import InputRequired, Length
import os 


basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SECRET_KEY'] = 'AYAM'  


app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://root:faiz@localhost/dealer"
db = SQLAlchemy(app)
migrate = Migrate(app,db)




class Category(db.Model):
    __tablename__ = 'category'
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    name = db.Column(db.String(100), nullable=False)    

    def __repr__(self):
        return self.name

class Categoryform(FlaskForm):
    name = StringField("name_c", validators=[InputRequired(), Length(min=1)])  

class Cars(db.Model):	
    __tablename__   = 'cars'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)      
    colour = db.Column(db.String(255), nullable=False) 
    price   = db.Column(db.Integer, nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey("category.id"))

class Carsform(FlaskForm):	
    name_mobil = StringField("Nama", validators=[InputRequired(), Length(min=1)])    
    colour_mobil = StringField("Warna", validators=[InputRequired(), Length(min=1)])  
    price_mobil  = IntegerField("Harga", validators=[InputRequired()])
    category_id = IntegerField("Category", validators=[InputRequired()])


class Type (db.Model):
    _tablename = "type" 
    id = db.Column(db.Integer,primary_key=True, autoincrement  = True) 
    name = db.Column(db.String(100), nullable=False)
    cars_id = db.Column(db.Integer, db.ForeignKey("cars.id"))


@app.route ('/category')
def home():
    categories = Category.query.all()
    return render_template("index.html", categories=categories)


@app.route ('/admin/category')
def categories():
    categories = Category.query.all()
    return render_template ("categories.html", categories=categories)
    

@app.route('/cars')
def car_list():
    car = Cars.query.all()
    return render_template ("cars.html", car=car)

@app.route('/test')
def base():
    return render_template ("test.html")

@app.route ('/user')
def user():
    return render_template("index.html")

@app.route('/formcat')
def catform():
    form = Categoryform()
    return render_template('catform.html',form=form)

@app.route('/formcat/create', methods=['POST'])
def create():
    if request.method =='POST':
        name = request.form['name']
        obj = Category(name=name)
        db.session.add(obj)
        db.session.commit()
        return redirect('/formcat')

@app.route ('/carform')
def carform():
    form = Carsform()   
    return render_template('carform.html',form=form)

@app.route ('/carform/create', methods=['POST'])
def add():
    if request.method == 'POST':
        name = request.form['name_mobil']
        colour =request.form['colour_mobil']
        price = request.form['price_mobil']
        category_id = request.form['category_id']
        Obj = Cars(name=name, colour=colour, price=price, category_id=category_id)
        db.session.add(Obj)
        db.session.commit()
        return redirect('/carform')

@app.route ('/admin/category/<int:id>')
def get_category_by_id(id):
    get_cars = Cars.query.filter(Cars.category_id == id).all()
    return render_template('car_list.html', cars=get_cars, category =Category.query.filter(Category.id==id).first())