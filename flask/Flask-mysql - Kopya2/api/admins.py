from flask import Flask, jsonify, Blueprint, request
from restaurantres.models import Admin
from werkzeug.security import generate_password_hash

apiAdmins = Blueprint("apiAdmins", __name__, url_prefix="/api/admins")

@apiAdmins.route("/")
def admins():
    try:
        allAdmins = Admin.get_all_admins()
        admins = []

        for admin in allAdmins:
            admins.append({
                "id": admin.id,
                "name": admin.name,
                "email": admin.email,
                "password": admin.password,
                "mod": admin.mod
            })

        return jsonify({
            "success": True,
            "data": admins,
            "count": len(admins)
        })

    except Exception as e:
        # print("Error admins: ", e)
        return jsonify({
            "success": False,
            "message": "Beklenmedik bir hata meydana geldi!"
        })

@apiAdmins.route("/addAdmin", methods=["POST"])
def add_admin():
    try:
        name = request.form.get("name")
        email = request.form.get("email")
        password = request.form.get("password")

        if name is None:
            return jsonify({
                "success": False,
                "message": "Name is required"
            })
        if email is None:
            return jsonify({
                "success": False,
                "message": "Email is required"
            })
        if password is None:
            return jsonify({
                "success": False,
                "message": "Password is required"
            })

        password = generate_password_hash(password)

        Admin.add_admin(name, email, password)

        return jsonify({
            "success": True,
            "message": "Admin added successfully"
        })
    except Exception as e:
        print("ERROR in add_admin: ", e)
        return jsonify({
            "success": False,
            "message": "There is an error.."
        })

@apiAdmins.route("/<int:id>", methods=["GET", "DELETE", "PUT"])
def admin(id):
    try:
        admin = Admin.get_admin_by_id(id)

        if admin is None:
            return jsonify({
                "success": False,
                "message": "Admin bulunamadı"
            })

        if request.method == "GET":
            adminObj = {
                "id": admin.id,
                "name": admin.name,
                "email": admin.email,
                "password": admin.password,
                "mod": admin.mod
            }
            # ------------------------------------------------------------------------------------------------
            return jsonify({
                "success": True,
                "data": adminObj
            })
        elif request.method == "DELETE":
            Admin.delete_admin(id)

            return jsonify({
                "success": True,
                "message": "Admin deleted"
            })

        # ------------------------------------------------------------------------------------------------

        elif request.method == "PUT":
            name = request.form.get("name")
            email = request.form.get("email")
            password = request.form.get("password")

            if name is None:
                name = admin.name
            if email is None:
                email = admin.email
            if password is None:
                password = admin.password

            password = generate_password_hash(password)

            Admin.update_admin(id, name, email, password)
            return jsonify({
                "success": True,
                "message": "Admin updated"
            })
    except Exception as e:
        print("ERROR in admin int: ", e)
        return jsonify({
            "success": False,
            "message": "Beklenmedik bir hata meydana geldi!"
        })