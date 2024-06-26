from flask import jsonify, Blueprint, request, redirect
from restaurantres.models import Reservation
from flask import render_template
from flask import session
from flask import flash
from datetime import datetime
from restaurantres.models import Reservation

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor



apiReservations = Blueprint("apiReservations", __name__, url_prefix="/api/reservations")

@apiReservations.route("/" , methods=["GET"])
def get_all_reservations():
    try:
        allReservations = Reservation.get_all_reservations()
        reservations = []

        for reservation in allReservations:
            reservations.append({"id": reservation.id, "user_id": reservation.user_id, "phonenumber": reservation.phonenumber, "date": reservation.date, "time": reservation.time, "guests": reservation.guests, "tablenum": reservation.tablenum})
        return jsonify({"success": True, "data": reservations, "count": len(reservations)})
    except Exception as e:
        print("Error: in reservations", e)
        return jsonify({"success": False, "message": "Beklenmedik bir hata meydana geldi!"})
    
#---------------------------------------------------------------------------
    
@apiReservations.route("/addReservation", methods=["POST"])
def add_reservation():
    try:
        user_id = request.form.get("user_id")
        phonenumber = request.form.get("phonenumber")
        date = request.form.get("date")
        time = request.form.get("time")
        guests = request.form.get("guests")
        tablenum = request.form.get("tablenum")
        
        reservation_date = datetime.strptime(date, "%m/%d/%Y")

        if user_id == None:
            return jsonify({"success": False, "message": "Lütfen bir user id giriniz!"})
        if phonenumber == None:
            return jsonify({"success": False, "message": "Lütfen bir telefon numarası giriniz!"})
        if date == None:
            return jsonify({"success": False, "message": "Lütfen bir tarih giriniz!"})
        if time == None:
            return jsonify({"success": False, "message": "Lütfen bir saat giriniz!"})
        if guests == None:
            return jsonify({"success": False, "message": "Lütfen misafir sayısını giriniz!"})
        if tablenum == None:
            return jsonify({"success": False, "message": "Lütfen masa numarasını giriniz!"})
        
        if reservation_date.date() < datetime.now().date():
            flash("Gecmis bir tarih secilemez!")
            return redirect("/reservation.html", code=302)
        
        if Reservation.is_table_reserved(date, time, tablenum):
            flash("Bu masa o gün o saate zaten rezerve edilmis!")
            return redirect("/reservation.html", code=302)
        
        
        Reservation.add_reservation(user_id, phonenumber, date, time, guests, tablenum)
        return redirect("/api/reservations/reserve", code=302)
    
    except Exception as e:
        print("Error: in add_reservation", e)
        return jsonify({"success": False, "message": "Beklenmedik bir hata meydana geldi!"})
    

@apiReservations.route("/<int:id>", methods=["GET", "DELETE", "PUT"])
def reservation(id):
    try:
        reservation = Reservation.get_reservation_by_id(id)

        if reservation is None:
            return jsonify({"success": False, "message": "Reservation not found"})

        if request.method == "GET":
            reservationObj = {
                "id": reservation.id,
                "user_id": reservation.user_id,
                "phonenumber": reservation.phonenumber,
                "date": reservation.date,
                "time": reservation.time,
                "guests": reservation.guests,
                "tablenum": reservation.tablenum
            }
            return jsonify({"success": True, "data": reservationObj})
        
        if request.method == "DELETE":
            deletedReservation = Reservation.delete_reservation(id)
            return jsonify({"success": True, "message": "Reservation deleted", "data": {"id": deletedReservation.id}})
        
        if request.method == "PUT":
            user_id = request.form.get("user_id")
            phonenumber = request.form.get("phonenumber")
            date = request.form.get("date")
            time = request.form.get("time")
            guests = request.form.get("guests")
            tablenum = request.form.get("tablenum")

            if user_id == None:
                return jsonify({"success": False, "message": "Lütfen bir user id giriniz!"})
            if phonenumber == None:
                return jsonify({"success": False, "message": "Lütfen bir telefon numarası giriniz!"})
            if date == None:
                return jsonify({"success": False, "message": "Lütfen bir tarih giriniz!"})
            if time == None:
                return jsonify({"success": False, "message": "Lütfen bir saat giriniz!"})
            if guests == None:
                return jsonify({"success": False, "message": "Lütfen misafir sayısını giriniz!"})
            if tablenum == None:
                return jsonify({"success": False, "message": "Lütfen masa numarasını giriniz!"})
            
            Reservation.update_reservation(id, user_id, phonenumber, date, time, guests, tablenum)
            return jsonify({"success": True, "message": "Reservation updated"})
        
    except Exception as e:
        print("Error: in reservation", e)
        return jsonify({"success": False, "message": "Beklenmedik bir hata meydana geldi!"})
    
    return jsonify({"success": False, "message": "Invalid request method"})


@apiReservations.route("/reserve", methods=["GET"])
def myreservations():
    user_id = session.get('user_id')
    reservations = Reservation.get_reservations_by_user_id(user_id)
    return render_template("/myreservations.html", reservations=reservations)


@apiReservations.route("/rate/<int:id>", methods=["POST"])
def rate_reservation(id):
    rating = request.form.get('rating')
    comment = request.form.get('comment')
    Reservation.update_reservation_rating_comment(id, rating=rating, comment=comment)
    return redirect('/api/reservations/reserve')


    
@apiReservations.route("/price", methods=["GET"])
def get_price():
    price_level = Reservation.determine_price_level()
    price = Reservation.calculate_price(price_level)
    return jsonify({"price": price})

#------- AI TABANLI MASA SEÇME ------------ #

from restaurantres import createApp

app = createApp()

with app.app_context():
    reservations = Reservation.get_all_reservations()

data = pd.DataFrame([(r.guests, r.tablenum) for r in reservations], columns=['guests', 'tablenum'])

X = data[['guests']]
y = data['tablenum']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)


@apiReservations.route("/predicted_tablenum/<int:guests>", methods=["GET"])
def get_predicted_tablenum(guests):
    predict_data = pd.DataFrame([[guests]], columns=['guests'])
    raw_prediction = model.predict(predict_data)
    predicted_tablenum = min(max(1, round(raw_prediction[0])), 35)
    return jsonify(predicted_tablenum=predicted_tablenum)