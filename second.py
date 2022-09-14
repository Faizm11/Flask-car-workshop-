from flask import Blueprint,   render_template

second = Blueprint("second",__name__, template_folder="template")

@second.route("/")
def home():
    return render_template("second.html")

@second.route("/test")
def test():
    return render_template("test.html")