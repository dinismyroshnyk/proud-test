import os
from django.http import JsonResponse
from .models import *
from .utils import *
from .consts import *
import json
from django.views.decorators.csrf import csrf_exempt
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.contrib.auth.hashers import check_password
from django.core.mail import send_mail


@csrf_exempt
def index(request):
    dados = {'mensagem': 'Olá'}
    return JsonResponse(dados, status=OK)


@csrf_exempt
def products(request):
    if request.method == 'GET':
        # obter todos os produtos
        products = Product.objects.all()
        product_list = list(products.values())
        return JsonResponse({'products': product_list}, status=OK)
    elif request.method == 'POST':
        # criar produto
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse(invalid_json_message(), status=BAD_REQUEST)

        validation_error = np_data_validation(data)

        if validation_error:
            return JsonResponse(validation_error, status=BAD_REQUEST)

        try:
            product = Product.objects.create(
                price=data['price'],
                name=data['name'],
                type=data['type'],
                stock=data['stock'],
                description=data['description'],
                exclusivity=data['exclusivity'],
                size=data['size']
            )
        except Exception as e:
            return JsonResponse(internal_server_error_message(str(e)), status=INTERNAL_SERVER_ERROR)

        return JsonResponse({'message': 'Product successfully created', 'product_id': product.id}, status=CREATED)
    else:
        return JsonResponse(invalid_http_method(), status=METHOD_NOT_ALLOWED)


@csrf_exempt
def product(request, product_id):
    if request.method == 'GET':
        product = get_product_by_id(product_id)
        if product is None:
            return JsonResponse(product_not_found_message(product_id), status=NOT_FOUND)
        else:
            product = Product.objects.get(id=product_id)
            product_details = {
                'id': product.id,
                'price': product.price,
                'name': product.name,
                'type': product.type,
                'stock': product.stock,
                'description': product.description,
                'exclusivity': product.exclusivity,
                'size': product.size
            }
            return JsonResponse({'product': product_details}, status=OK)
    elif request.method == 'PUT':
        product = get_product_by_id(product_id)
        if product is None:
            return JsonResponse(product_not_found_message(product_id), status=NOT_FOUND)

        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse(invalid_json_message(), status=BAD_REQUEST)

        validation_error = ep_data_validation(data, product)

        if validation_error:
            return JsonResponse(validation_error, status=BAD_REQUEST)

        try:
            Product.objects.filter(id=product_id).update(
                price=data['price'],
                name=data['name'],
                type=data['type'],
                stock=data['stock'],
                description=data['description'],
                exclusivity=data['exclusivity'],
                size=data['size']
            )
        except Exception as e:
            return JsonResponse(internal_server_error_message(str(e)), status=INTERNAL_SERVER_ERROR)

        return JsonResponse({'message': 'Product successfully updated'}, status=OK)
    elif request.method == 'DELETE':
        product = get_product_by_id(product_id)
        if product is None:
            return JsonResponse(product_not_found_message(product_id), status=NOT_FOUND)

        try:
            product.delete()
        except Exception as e:
            return JsonResponse(internal_server_error_message(str(e)), status=INTERNAL_SERVER_ERROR)

        return JsonResponse({'message': 'Product successfully deleted'}, status=OK)
    else:
        return JsonResponse(invalid_http_method(), status=METHOD_NOT_ALLOWED)


@csrf_exempt
def login(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)

            validation_error = login_data_validation(data)

            if validation_error:
                return JsonResponse(validation_error, status=BAD_REQUEST)

            try:
                user = User.objects.get(email=data['email'])
            except User.DoesNotExist:
                return JsonResponse(invalid_login(), status=BAD_REQUEST)

            if check_password(data['password'], user.password):
                return JsonResponse({"message": "Login successful", "user_uuid": str(user.uuid)}, status=OK)
            else:
                return JsonResponse(invalid_login(), status=BAD_REQUEST)

        except json.JSONDecodeError:
            return JsonResponse(invalid_json_message(), status=BAD_REQUEST)
    else:
        return JsonResponse(invalid_http_method(), status=METHOD_NOT_ALLOWED)


@csrf_exempt
def create_newsletter(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        email = data['email']
        if not email:
            return JsonResponse({"error": "Email is required"}, status=BAD_REQUEST)

        try:
            validate_email(email)
        except ValidationError:
            return JsonResponse(invalid_email(), status=BAD_REQUEST)

        if Newsletter.objects.filter(email=email).exists():
            return JsonResponse({"error": "Email already registered in the newsletter list"}, status=BAD_REQUEST)

        try:
            Newsletter.objects.create(email=email)
            return JsonResponse({"message": "Email successfully registered"}, status=OK)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    else:
        return JsonResponse(invalid_http_method(), status=METHOD_NOT_ALLOWED)


@csrf_exempt
def members(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        subject = data.get('subject')
        message = data.get('message')
        emails_to = data.get('emails_to')  # TODO: TEM DE SER UMA LISTA vinda do front-end

        if not subject or not message:
            return JsonResponse({"error": "Subject, message and email are required"}, status=BAD_REQUEST)

        for email in emails_to:
            try:
                validate_email(email)
            except ValidationError:
                return JsonResponse({"error": "Invalid email format"}, status=BAD_REQUEST)

        try:
            send_mail(
                subject,
                message,
                os.getenv('EMAIL_HOST_USER'),
                emails_to,
                fail_silently=False,
            )
            return JsonResponse({"message": "Email sent successfully"}, status=OK)


        except Exception as e:
            return JsonResponse({"error": str(e)}, status=INTERNAL_SERVER_ERROR)
    elif request.method == 'GET':
        members = User.objects.filter(type=3).values('email')
        members_list = list(members)

        num_members = len(members_list)

        return JsonResponse({"members": {"members_list": members_list, "num_members": num_members}}, status=OK)
    else:
        return JsonResponse(invalid_http_method(), status=METHOD_NOT_ALLOWED)


@csrf_exempt
def member(request, user_id):
    if request.method == 'PUT':
        member = User.objects.get(uuid=user_id)
        if not member:
            return JsonResponse({"error": "Member not found"}, status=NOT_FOUND)

        if member.type == 2:
            if member.request_membership:
                member.type = 3
                member.request_membership = False
                member.save()
                return JsonResponse({"message": "Membership request was successfully accepted"}, status=OK)
            else:
                return JsonResponse({"error": "User did not request a membership"}, status=BAD_REQUEST)
        else:
            return JsonResponse({"error": "User is already a member"}, status=BAD_REQUEST)

    else:
        return JsonResponse(invalid_http_method(), status=METHOD_NOT_ALLOWED)


@csrf_exempt
def member_reject(request, user_id):
    if request.method == 'PUT':
        member = User.objects.get(uuid=user_id)
        if not member:
            return JsonResponse({"error": "Member not found"}, status=NOT_FOUND)

        if member.type == 2:
            if member.request_membership:
                member.request_membership = False
                member.save()
                return JsonResponse({"message": "Membership request was successfully rejected"}, status=OK)
            else:
                return JsonResponse({"error": "User did not request a membership"}, status=BAD_REQUEST)
        else:
            return JsonResponse({"error": "User is already a member"}, status=BAD_REQUEST)

    else:
        return JsonResponse(invalid_http_method(), status=METHOD_NOT_ALLOWED)


@csrf_exempt
def users(request):
    if request.method == 'GET':
        # obter todos os utilizadores
        users = User.objects.all()
        user_list = list(users.values())
        return JsonResponse({'users': user_list}, status=OK)
    elif request.method == 'POST':
        # criar utilizador
        data = json.loads(request.body)

        validation_error = register_data_validation(data)

        if validation_error:
            return JsonResponse(validation_error, status=BAD_REQUEST)

        try:
            user = User.objects.create(
                email=data['email'],
                password=make_password(data['password'])
            )
        except Exception as e:
            return JsonResponse(internal_server_error_message(str(e)), status=INTERNAL_SERVER_ERROR)

        return JsonResponse({'message': 'User successfully created', 'user_uuid': user.uuid}, status=CREATED)
    else:
        return JsonResponse(invalid_http_method(), status=METHOD_NOT_ALLOWED)


@csrf_exempt
def user(request, user_id):

    user = User.objects.get(uuid=user_id)
    if user and user.state:


        if request.method == 'GET':

            return JsonResponse({
                "email": user.email,
                "name": user.name,
                "address": user.address,
                "nationality": user.nationality,
                "phone": user.phone,
                "type": user.type,
                "request_membership": user.request_membership,#TODO: FRONT-END, quando o utilizador tem um pedido de membro (True), deve ser mostrado uma modal para aceitar ou cancelar esse pedido
            }, status=OK)

        elif request.method == 'PUT':
            if user.type == 2:
                user.type = 3
                user.request_membership = False
                user.save()
                return JsonResponse({"message": "User successfully upgraded to member"}, status=OK)
            elif user.type == 3:
                user.type = 2
                user.request_membership = False
                user.save()
                return JsonResponse({"message": "User successfully downgraded to client"}, status=OK)
            else:
                return JsonResponse({"error": "Invalid user type"}, status=BAD_REQUEST)
        else:
            return JsonResponse(invalid_http_method(), status=METHOD_NOT_ALLOWED)
    else:
        return JsonResponse({"error": "User not found"}, status=NOT_FOUND)
@csrf_exempt
def user_cancel(request, user_id):
    user = User.objects.get(uuid=user_id)
    if not user:
        return JsonResponse({"error": "User not found"}, status=NOT_FOUND)

    if request.method == 'PUT':

        if user.state:
            user.state = False
            user.save()
            return JsonResponse({"message": "User successfully deactivated"}, status=OK)
        else:
            return JsonResponse({"message": "User already deactivated"}, status=OK)
    else:
        return JsonResponse(invalid_http_method(), status=METHOD_NOT_ALLOWED)




