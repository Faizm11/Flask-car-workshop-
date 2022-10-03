
from atexit import register
from cgi import print_exception
from contextlib import redirect_stderr
from socketserver import DatagramRequestHandler
import string
from turtle import color
from unicodedata import name
from wsgiref.validate import validator
from flask import Flask, render_template, request,  redirect, url_for 
from flask_login import login_required, LoginManager, login_user
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_wtf import FlaskForm 
from wtforms import StringField, IntegerField, FloatField, PasswordField
from wtforms.validators import InputRequired, Length
from werkzeug.security import generate_password_hash, check_password_hash
import os 
import flask_login


basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SECRET_KEY'] = 'AYAM'  


app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://root:faiz@localhost/dealer"
db = SQLAlchemy(app)
migrate = Migrate(app,db)
loginmanager = LoginManager() 
loginmanager.init_app(app)
loginmanager.login_message = "Hallo salam dari borjka"


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
    __tablename__ = "type" 
    id = db.Column(db.Integer,primary_key=True, autoincrement  = True) 
    name = db.Column(db.String(100), nullable=False)
    cars_id = db.Column(db.Integer, db.ForeignKey("cars.id"))

class User (db.Model):
    __tablename__ ="users"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    password = db.Column(db.String(233), nullable=False)
    is_activate = db.column(db.Boolean, )

class UsersFormLogin(FlaskForm):
    name = StringField("Nama",validators=[InputRequired(), Length(min=1)])
    p = PasswordField( "Password", validators=[InputRequired(), Length(min=1)])





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

@app.route('/admin/category/cars/<int:id>')
def get_category_by_id(id):
    get_cars = Cars.query.filter(Cars.category_id == id).all()
    return render_template('car_list.html', cars=get_cars, category =Category.query.filter(Category.id==id).first())



@app.route('/admin/category/cars/<int:id>/edit')
@loginmanager.user_loader
@login_required
def edit_cars(id):
    cars_edit = Cars.query.filter(Cars.id == id).first()
    print(cars_edit)
    form = Carsform(cars_edit=cars_edit)
    form.category_id.data=cars_edit.category_id
    form.name_mobil.data = cars_edit.name
    form.colour_mobil.data = cars_edit.colour
    form.price_mobil.data = cars_edit.price
    return render_template ('editcar.html', form=form, id=id)

@app.route('/admin/category/cars/<int:id>/update', methods=['POST'])
def update_category_cars(id):
    if request.method=='POST':
        print('Berhasil')
        print(request.form['category_id'])
        p = Cars.query.filter(Cars.id == id).first()
        p.name = request.form['name_mobil']
        p.colour = request.form['colour_mobil']
        p.price = request.form['price_mobil']
        p.category_id = request.form['category_id']
        db.session.add(p)
        db.session.commit()
        return redirect(f'/admin/category/cars/{id}' )


@app.route('/admin/category/cars/<int:id>/delete')
def delete_car(id):
    car = Cars.query.filter(Cars.id == id).first()
    db.session.delete(car)
    db.session.commit()
    return redirect(f'/admin/category/')


@app.route ('/loginadmin/')
def loginadmin():
    form = UsersFormLogin()
    return render_template('loginusers.html', form=form)

@app.route ('/loginproses/',methods=['POST'])
def loginproses():
    if request.method == 'POST':
        print("oiii")
        name = request.form['name']
        p = request.form['p']
        obj = User.query.filter_by(name= name).first()
        print("Ini user:", obj)
        if not user:
            redirect('/loginuser.html')
        else :
            login_user(obj)
            redirect("/admin/category/")
    print("eror")


@app.route('/admin/regis')
def regis():
    user = UsersFormLogin()
    return render_template('regis.html', user=user)

@app.route('/admin/regis/create', methods=['POST'])
def regis1() :
    if request.method == 'POST':
        name = request.form['name']
        p = request.form['p']
        obj= User()
        obj.name = name
        obj.password =generate_password_hash(p, method="sha256")
        db.session.add(obj)
        db.session.commit()
        return redirect('/loginadmin')


