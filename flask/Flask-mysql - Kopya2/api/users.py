from flask import jsonify, Blueprint, request, redirect
from restaurantres.models import User
from werkzeug.security import generate_password_hash
from flask_login import login_user, logout_user
from flask import redirect
from flask import flash
from flask_login import login_required
from flask import session

apiUsers = Blueprint("apiUser", __name__, url_prefix="/api/users")

@apiUsers.route("/")
def users():
    try:
        allUsers = User.get_all_users()
        users = []

        for user in allUsers:
            users.append({"id": user.id, "username": user.username, "email": user.email, "password": user.password, "activated": user.activated})
        return jsonify({"success": True, "data": users, "count": len(users)})
        #--return redirect("/index.html", code=302)
    except Exception as e:
        #print("Error: ", e)
        return jsonify({"success": False, "message": "Beklenmedik bir hata meydana geldi!"})
    


@apiUsers.route("/<int:id>", methods=["GET", "DELETE", "PUT"])
def user(id):
    try:
        user = User.get_user_by_id(id)

        if user is None:
            return jsonify({"success": False, "message": "User not found"})

        if request.method == "GET":
            userObj = {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "password": user.password,
            }

            return jsonify({"success": True, "data": userObj})
#--------------------------------------------------------------------------------
        elif request.method == "DELETE":
            User.delete_user(id)

            return jsonify({"success": True, "message": "User deleted"})
#--------------------------------------------------------------------------------
        elif request.method == "PUT":
            username = request.form.get("username")
            email = request.form.get("email")
            password = request.form.get("password")



            #Kullanıcı sadece bir verisini güncellemek istiyosa diye
            if username is None:
                username = user.username
            if email is None:
                email = user.email
            if password is None:
                password = user.password

            password = generate_password_hash(password)

            User.update_user(id, username, email, password)
            return jsonify({"success": True, "message": "User updated"})
    except Exception as e:
        # print("ERROR in user: ", e)
        return jsonify({"success": False, "message": "There is an error.."})



@apiUsers.route("/addUser", methods=["POST"])
def addUser():
    try:
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")

        print("USERNAME: ", username)
        print("EMAIL: ", email)
        print("PASSWORD: ", password)

        if username == None or email == None or password == None:
            return jsonify({"success": False, "message": "Missing fields"})
        
        password = generate_password_hash(password)

        User.add_user(username, email, password)

        return redirect("/login.html", code=302)
    except Exception as e:
        print("Error: ", e)
        return jsonify({"success": False, "message": "Beklenmedik bir hata meydana geldi!"})
    

#-------------------------------KULLANICI PROFİLİ PASİF VEYA AKTİF HALE GETİRME-------------------------------------------------

@apiUsers.route("/activate_user", methods=["POST"])
def activateUser():
    try:
        id = request.form.get("id")
        user = User.get_user_by_id(id)
        
        if id is None:
            return jsonify({"success": False, "message": "Kullanıcı bulunamadı!"})
        if user.activated == True:
            return jsonify({"success": False, "message": "Zaten aktif olan kullanıcı!"})
        
        User.activate_user(id)

        return jsonify({"success": True, "message": "Kullanıcı profili aktif edildi!"})
    except Exception as e:
        print("Error in activateUser: ", e)
        return jsonify({"success": False, "message": "Beklenmedik bir hata meydana geldi!"})
    
@apiUsers.route("/deactivate_user", methods=["POST"])
def deactivateUser():
    try:
        id = request.form.get("id")
        user = User.get_user_by_id(id)

        if id is None:
            return jsonify({"success": False, "message": "Kullanıcı bulunamadı!"})
        
        if user.activated == False:
            return jsonify({"success": False, "message": "Zaten pasif olan kullanıcı!"})
        
        User.deactivate_user(id)

        return jsonify({"success": True, "message": "Kullanıcı profili pasif edildi!"})
    
    except Exception as e:
        print("Error in deactivateUser: ", e)
        return jsonify({"success": False, "message": "Beklenmedik bir hata meydana geldi!"})


#-----------------------------------AKTİF-PASİF KULLANICILARIN HEPSİNİ GET-------------------------------------------------------------------------------
    

@apiUsers.route("/deactiveusers", methods=["GET"])
def deactiveUsers():
    try:
        allUsers = User.query.filter_by(activated=False).all()
        users = []

        for user in allUsers:
            users.append({"id": user.id, "username": user.username, "email": user.email, "password": user.password, "activated": user.activated})

        return jsonify({"success": True, "data": users, "count": len(users)})
    except Exception as e:
        #print("Error: ", e)
        return jsonify({"success": False, "message": "Beklenmedik bir hata meydana geldi!"})
    

@apiUsers.route("/activeusers", methods=["GET"])
def activeUsers():
    try:
        allUsers = User.query.filter_by(activated=True).all()
        users = []

        for user in allUsers:
            users.append({"id": user.id, "username": user.username, "email": user.email, "password": user.password, "activated": user.activated})

        return jsonify({"success": True, "data": users, "count": len(users)})
    except Exception as e:
        #print("Error: ", e)
        return jsonify({"success": False, "message": "Beklenmedik bir hata meydana geldi!"})

@apiUsers.route('/login', methods=['POST'])
def login():
    email = request.form.get('email')
    password = request.form.get('password')

    user = User.query.filter_by(email=email).first()
    if user is not None and user.check_password(password):
        login_user(user)
        session['user_id'] = user.id
        return redirect("/api/users/dashboard", code=302)
    
    flash("Email veya parolanızı hatalı girdiniz.Lütfen tekrar deneyin", "error")
    
    return redirect("/login.html", code=302)

@apiUsers.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect("/login.html", code=302)

@apiUsers.route("/dashboard")
@login_required
def dashboard():
    return redirect("/dashboard.html", code=302)
