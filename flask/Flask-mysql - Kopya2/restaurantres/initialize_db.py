from restaurantres.models import db
from restaurantres import createApp

def createDB():
    app = createApp()
    with app.app_context():
        db.create_all()