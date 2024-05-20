from flask import Flask, jsonify, Blueprint, request
from restaurantres.models import Product

apiProducts = Blueprint("apiProducts", __name__, url_prefix="/api/products")

@apiProducts.route("/")
def products():
    try:
        allProducts = Product.get_all_products()
        products = []

        for product in allProducts:
            products.append({"id": product.id, "name": product.name, "price": product.price, "oldPrice": product.oldPrice, "description": product.description, "category_id": product.category_id})
        return jsonify({"success": True, "data": products, "count": len(products)})
    except Exception as e:
        print("Error: in products", e)
        return jsonify({"success": False, "message": "Beklenmedik bir hata meydana geldi!"})
    
#-----------------------------------------------------------------------------------------------------------
       
@apiProducts.route("/addProduct", methods=["POST"])
def add_product():
    try:
        name = request.form.get("name")
        price = request.form.get("price")
        oldPrice = request.form.get("oldPrice")
        description = request.form.get("description")
        category_id = request.form.get("categoryId")

        if name == None:
            return jsonify({"success": False, "message": "Lütfen bir isim giriniz!"})
        if price == None:
            return jsonify({"success": False, "message": "Lütfen bir fiyat giriniz!"})
        if oldPrice == None:
            oldPrice = price
        if description == None:
            return jsonify({"success": False, "message": "Lütfen bir açıklama giriniz!"})
        if category_id == None:
            return jsonify({"success": False, "message": "Lütfen bir kategori id giriniz!"})
        
        Product.add_product(name, price, oldPrice, description, category_id)

        return jsonify({"success": True, "message": "Ürün başarıyla eklendi!"})
    
    except Exception as e:
        print("Error: in add_product", e)
        return jsonify({"success": False, "message": "Beklenmedik bir hata meydana geldi!"})
    
#-----------------------------------------------------------------------------------------------------------
    
@apiProducts.route("/<int:id>", methods=["GET", "DELETE", "PUT"])
def product(id):
    try:
        product = Product.get_product_by_id(id)

        if product is None:
            return jsonify({"success": False, "message": "Product not found"})

        if request.method == "GET":
            productObj = {
                "id": product.id,
                "name": product.name,
                "price": product.price,
                "oldPrice": product.oldPrice,
                "description": product.description,
                "category_id": product.category_id
            }

            return jsonify({"success": True, "data": productObj})
        #-----------------------------------------------------------------------

        elif request.method == "DELETE":
            Product.delete_product(id)

            return jsonify({"success": True, "message": "Product deleted"})
        
        #-----------------------------------------------------------------------

        elif request.method == "PUT":
            name = request.form.get("name")
            price = request.form.get("price")
            oldPrice = request.form.get("oldPrice")
            description = request.form.get("description")
            category_id = request.form.get("categoryId")

            if name is None:
                name = product.name
            if price is None:
                price = product.price
            if oldPrice is None:
                oldPrice = product.oldPrice
            if description is None:
                description = product.description
            if category_id is None:
                category_id = product.category_id

            Product.update_product(id, name, price, oldPrice, description, category_id)
            return jsonify({"success": True, "message": "Product updated"})
        
    except Exception as e:
        print("Error: in product", e)
        return jsonify({"success": False, "message": "Beklenmedik bir hata meydana geldi!"})
