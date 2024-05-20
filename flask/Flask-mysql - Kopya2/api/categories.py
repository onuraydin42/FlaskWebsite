from flask import Flask, jsonify, Blueprint, request
from restaurantres.models import Category

apiCategories = Blueprint("apiCategories", __name__, url_prefix="/api/categories")

@apiCategories.route("/")
def categories():
    try:
        allCategories = Category.get_all_categories()
        categories = []

        for category in allCategories:
            categories.append({"id": category.id, "name": category.name})

        return jsonify({"success": True, "data": categories, "count": len(categories)})
    except Exception as e:
        #print("Error: categories ", e)
        return jsonify({"success": False, "message": "Beklenmedik bir hata meydana geldi!"})
    
@apiCategories.route("/addCategory", methods=["POST"])
def add_category():
    try:
        name = request.form.get("name")

        if name == None:
            return jsonify({"success": False, "message": "Lütfen Kategori İsmi Giriniz"})
        
        Category.add_category(name)

        return jsonify({"success": True, "message": "Kategori başarıyla eklendi"})
    except Exception as e:
        print("ERROR in add_category: ", e)
        return jsonify({"success": False, "message": "Beklenmedik bir hata meydana geldi!"})
    
@apiCategories.route("/<int:id>", methods=["GET", "DELETE", "PUT"])
def category(id):
    try:
        category = Category.get_category_by_id(id)

        if category is None:
            return jsonify({"success": False, "message": "Kategori Bulunamadı"})

        if request.method == "GET":
            categoryObj = {
                "id": category.id,
                "name": category.name,
            }

            return jsonify({"success": True, "data": categoryObj})
        #--------------------------------------------------------------------------------
        elif request.method == "DELETE":
            Category.delete_category(id)

            return jsonify({"success": True, "message": "Kategori Silindi"})
        #--------------------------------------------------------------------------------
        elif request.method == "PUT":
            name = request.form.get("name")

            if name is None:
                name = category.name

            Category.update_category(id, name)

            return jsonify({"success": True, "message": "Kategori Güncellendi"})
        
    except Exception as e:
        print("ERROR in category id : ", e)
        return jsonify({"success": False, "message": "Beklenmedik bir hata meydana geldi!"})