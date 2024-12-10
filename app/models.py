from .extension import db

class Pago(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, nullable=False)
    amount = db.Column(db.Float, nullable=False)
    price = db.Column(db.Float, nullable=False)
    id_purchase = db.Column(db.Integer, nullable=False)
    payment_method = db.Column(db.String(50), nullable=False)