from .models import *
from django.core.validators import validate_email
from django.core.exceptions import ValidationError


def get_product_by_id(product_id):
    # para retornar um objeto Product ou None
    try:
        return Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        return None


def bad_request_message(message):
    # response code 400
    return {'error': message}


def invalid_json_message():
    # possivel com response code 400
    return {'error': 'Invalid JSON'}


def product_not_found_message(product_id):
    # response code 404
    return {'error': f'No product found with id {product_id}'}


def invalid_http_method():
    # response code 405
    return {'error': 'Invalid HTTP Method'}


def internal_server_error_message(message):
    return {'error': f'An unexpected error occurred: {message}'}


def np_data_validation(data):
    # new product
    required_fields = ['price', 'name', 'type', 'stock', 'description', 'exclusivity', 'size']
    missing_fields = [field for field in required_fields if field not in data or data.get(field) == ""]

    if missing_fields:
        return {'error': f'Missing fields: {", ".join(missing_fields)}'}

    try:
        type = int(data['type'])
        price = float(data['price'])
        stock = int(data['stock'])
        size = int(data['size'])
    except ValueError:
        return {'error': 'Invalid data type for type, price, stock or size'}

    if price < 0 or stock < 0:
        return {'error': 'Invalid value for price or stock'}

    if type not in [item[0] for item in Product.PRODUCT_TYPES]:
        return {'error': 'Invalid value for type'}

    if size not in [item[0] for item in Product.PRODUCT_SIZES]:
        return {'error': 'Invalid value for size'}

    return None


def ep_data_validation(data, product):
    # edit product
    required_fields = ['price', 'name', 'type', 'stock', 'description', 'exclusivity', 'size']

    for field in required_fields:
        if data.get(field) is None:
            data[field] = getattr(product, field)  # data muda mesmo nas views porque é por referencia e nao por valor

    missing_fields = [field for field in required_fields if field not in data]

    if missing_fields:
        return {'error': f'Missing fields: {", ".join(missing_fields)}'}

    try:
        type = int(data['type'])
        price = float(data['price'])
        stock = int(data['stock'])
        size = int(data['size'])
    except ValueError:
        return {'error': 'Invalid data type for type, price, stock or size'}

    if price < 0 or stock < 0:
        return {'error': 'Invalid value for price or stock'}

    if type not in [item[0] for item in Product.PRODUCT_TYPES]:
        return {'error': 'Invalid value for type'}

    if size not in [item[0] for item in Product.PRODUCT_SIZES]:
        return {'error': 'Invalid value for size'}

    return None


def login_data_validation(data):
    required_fields = ['email', 'password']

    missing_fields = [field for field in required_fields if field not in data]

    if missing_fields:
        return {'error': f'Missing fields: {", ".join(missing_fields)}'}

    return None


def invalid_login():
    return {'error': 'Invalid email or password'}


def invalid_email():
    return {'error': 'Invalid email format'}


def register_data_validation(data):
    required_fields = ['email', 'password']

    missing_fields = [field for field in required_fields if field not in data]

    if missing_fields:
        return {'error': f'Missing fields: {", ".join(missing_fields)}'}

    try:
        validate_email(data['email'])
    except ValidationError:
        return invalid_email()

    return None
