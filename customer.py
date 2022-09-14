from flask import Blueprint, render_template

customer = Blueprint('customer',__name__ ,  template_name='templates')

@customer.route('/')
def view_costome_accounts():
    ...
@customer.route('/')
def edit_costome_accounts():
    ...

 

