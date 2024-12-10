from flask import Blueprint, request, jsonify
from tenacity import retry
from tenacity.wait import wait_fixed
from tenacity.stop import stop_after_attempt
from .services import add_pagos_service, remove_pagos_service

pagos = Blueprint('pagos', __name__)

@pagos.route('/pagos/add', methods=['POST'])
@retry(stop=stop_after_attempt(3), wait=wait_fixed(0.5))
def add_pagos():
    data = request.get_json()
    response, status = add_pagos_service(data)
    return jsonify(response), status

@pagos.route('/pagos/remove', methods=['POST'])
@retry(stop=stop_after_attempt(3), wait=wait_fixed(0.5))
def remove_pagos():
    data = request.get_json()
    response, status = remove_pagos_service(data)
    return jsonify(response), status