from .models import db, Pago
import json
from pybreaker import CircuitBreaker, CircuitBreakerError

breaker = CircuitBreaker(fail_max=10, reset_timeout=10)

def add_pagos_service(data):
    from app import Config
    required_fields = ['product_id', 'price', 'payment_method', 'amount', 'id_purchase']
    missing_fields = [field for field in required_fields if field not in data]
    present_fields = {field: data[field] for field in required_fields if field in data}

    if missing_fields:
        return {'error': 'Missing fields', 'present_fields': present_fields}, 400

    try:
        new_payment = Pago(
            product_id=data['product_id'],
            amount=data['amount'],
            price=data['price'],
            id_purchase=data['id_purchase'],
            payment_method=data['payment_method']
        )

        payment_data = {
            'payment_id': new_payment.id,
            'product_id': new_payment.product_id,
            'amount': new_payment.amount,
            'price': new_payment.price,
            'id_purchase': new_payment.id_purchase,
            'payment_method': new_payment.payment_method
        }

        Config.r.set(f"payment:{payment_data['payment_id']}", json.dumps(payment_data), ex=3600)

        db.session.add(new_payment)
        db.session.commit()

        return {'message': 'Payment added successfully'}, 201
    except CircuitBreakerError:
        return {'error': 'Circuito Abierto'}, 500
    except Exception as e:
        db.session.rollback()
        return {'error': str(e)}, 500

def remove_pagos_service(data):
    from app import Config
    if 'payment_id' not in data:
        return {'error': 'Missing fields'}, 400

    try:
        old_payment = Pago.query.get(data['payment_id'])

        if not old_payment:
            return {'error': 'Payment not found'}, 404

        db.session.delete(old_payment)
        db.session.commit()

        return {'message': 'Payment removed successfully'}, 200
    except CircuitBreakerError:
        return {'error': 'Circuito Abierto'}, 500
    except Exception as e:
        db.session.rollback()
        return {'error': str(e)}, 500