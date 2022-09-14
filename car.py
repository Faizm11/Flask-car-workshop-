from flask import Blueprint, render_template
from app import categories

cars_blueprint = Blueprint('cars', __name__, template_folder="templates")

@cars_blueprint.route('/cars')
def car_list():
    categories = categories.quaery.all()
    return render_template ("cars.html", categories=categories)

@cars_blueprint.route('/form' )
def add_car():
    return render_template("add_car.html")

@cars_blueprint.route('/')
def edit_car():
    ...

@cars_blueprint.route('/')
def delete_car():
    ...
