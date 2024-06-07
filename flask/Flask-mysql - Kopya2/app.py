from flask import render_template

from api.users import apiUsers
from api.products import apiProducts
from api.admins import apiAdmins
from api.categories import apiCategories
from api.reservations import apiReservations

from flask_login import LoginManager
from flask_login import login_required
from restaurantres.initialize_db import createDB
from restaurantres.models import User


from restaurantres import createApp
from flask_cors import CORS

app = createApp()
CORS(app)


createDB()

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"


#kayıt kısmı

app.register_blueprint(apiUsers)
app.register_blueprint(apiProducts)
app.register_blueprint(apiAdmins)
app.register_blueprint(apiCategories)
app.register_blueprint(apiReservations)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/index.html")
def index2():
    return render_template("index.html")

@app.route("/base.html")
def base():
    return render_template("base.html")

@app.route("/header.html")
def header():
    return render_template("header.html")

@app.route("/about.html")
def about():
    return render_template("about.html")

@app.route("/reservation.html")
@login_required
def reservation():
    return render_template("reservation.html")

@app.route("/myreservations.html")
@login_required
def myreservations():
    return render_template("myreservations.html")

@app.route("/contact.html")
def contact():
    return render_template("contact.html")

@app.route("/exp.html")
def exp():
    return render_template("exp.html")

@app.route("/menu.html")
def menu():
    return render_template("menu.html")

@app.route("/login.html")
def login():
    return render_template("login.html")

@app.route("/register.html")
def register():
    return render_template("register.html")

@app.route("/dashboard.html")
@login_required
def dashboard():
    return render_template("dashboard.html")


if __name__ == "__main__":
    app.run(debug=True)