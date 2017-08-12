import logging

from django.contrib.auth import login, password_validation
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly
from django.views.generic import TemplateView
from rest_framework import status
from rest_framework_jwt.utils import jwt_decode_handler
from .serializers import UserSerializer, ConfirmEmailSerializer, UserInfoSerializer
from .models import User
from utils.utils import HttpResponseNoContent, HttpResponseCreated


#logging.basicConfig(filename='/home/admin_ubuntu/django_projects/express/error.log', level=logging.DEBUG)


class IndexView(TemplateView):
    template_name = 'index.html'
    

@api_view(['POST'])
@permission_classes((AllowAny, ))
def register(request):
    try:
        input_data = {
            'email': request.data['email'],
            'username': request.data['username'],
            'password': request.data['password']
        }

    except Exception as er:
        return JsonResponse({'_error': str(er)}, status=status.HTTP_400_BAD_REQUEST)

    s = UserSerializer(data=input_data)
    if s.is_valid():
        user = s.create(s.validated_data)
        return HttpResponseCreated()
    else:
        return JsonResponse(s.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes((AllowAny, ))
def validate(request):
    try:
        input_data = {
            'email': request.data['email'],
            'confirmation_key': request.data['code']
        }

    except Exception as er:
        return JsonResponse({'_error': str(er)}, status=status.HTTP_400_BAD_REQUEST)

    s = ConfirmEmailSerializer(data=input_data)
    if s.is_valid():
        try:
            email = s.create()
            return HttpResponseCreated()
        except Exception as er:
            return JsonResponse({'_error': str(er)}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return JsonResponse(s.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes((IsAuthenticatedOrReadOnly, ))
def getUserInfo(request):
    try:
        #import ipdb; ipdb.set_trace(context=5)
        #logging.debug('reqiust auth is {} and it`s type {}'.format(request.auth, type(request.auth)))
        instance = User.objects.get_from_auth(request.auth)
        s = UserInfoSerializer(instance)
        return Response(s.data)
    except Exception as er:
        return Response(str(er), status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes((IsAuthenticatedOrReadOnly, ))
def reset_email(request):
    try:
        instance = User.objects.get_from_auth(request.auth)
        instance.send_new_confirmation_key()
        return HttpResponseNoContent()
    except Exception as er:
        return Response(str(er), status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes((IsAuthenticatedOrReadOnly, ))
def set_new_email(request):
    try:
        user = User.objects.get_from_auth(request.auth)
        code = request.data.get('code', None)
        new_email = request.data.get('email', None)
        if code is None:
            return Response('Code may not be null', status=status.HTTP_400_BAD_REQUEST)

        if new_email is None:
            return Response('Email may not be null', status=status.HTTP_400_BAD_REQUEST)

        if user.get_confirmation_key() != code:
            return Response('Confirmation code is spoiled!', status=status.HTTP_400_BAD_REQUEST)

        user.add_confirmed_email(new_email)
        user.set_primary_email(new_email)
        s = UserInfoSerializer(user)
        return Response(s.data)

    except Exception as er:
        return Response(str(er), status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes((IsAuthenticatedOrReadOnly, ))
def send_code_old_email(request):
    try:
        user = User.objects.get_from_auth(request.auth)
        user.send_new_confirmation_key()
        return HttpResponseNoContent()
    except Exception as er:
        return Response(str(er), status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes((IsAuthenticatedOrReadOnly, ))
def check_old_email(request):
    try:
        user = User.objects.get_from_auth(request.auth)
        code = request.data.get('code', None)
        newEmail = request.data.get('newEmail', None)
        if code is None:
            return Response('Code may not be null', status=status.HTTP_400_BAD_REQUEST)

        if newEmail is None:
            return Response('Email may not be null', status=status.HTTP_400_BAD_REQUEST)

        if user.get_confirmation_key() != code:
            return Response('Confirmation code is spoiled!', status=status.HTTP_400_BAD_REQUEST)

        oldEmail = user.confirm_email(code)
        ConfirmationKey = user.add_email_if_not_exists(newEmail)
        # if key is none this email already confirmed - set_primary_email 
        if ConfirmationKey is None:
            user.set_primary_email(newEmail)
        else:
            user.send_new_confirmation_key(newEmail, ConfirmationKey)

        return HttpResponseNoContent()
    except Exception as er:
        return Response(str(er), status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes((IsAuthenticatedOrReadOnly, ))
def check_new_email(request):
    try:
        user = User.objects.get_from_auth(request.auth)
        code = request.data.get('code', None)
        if code is None:
            return Response('Code may not be null', status=status.HTTP_400_BAD_REQUEST)
        
        newEmail = user.confirm_email(code)
        user.set_primary_email(newEmail)
        return HttpResponseNoContent()
    except Exception as er:
        return Response(str(er), status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes((IsAuthenticatedOrReadOnly, ))
def update_password(request):
    try:
        user = User.objects.get_from_auth(request.auth)
        password = request.data.get('password', None)
        if password is None:
            return Response('Password may not be null', status=status.HTTP_400_BAD_REQUEST)
        password_validation.validate_password(password)
        user.update_password(password)
        return HttpResponseNoContent()
    except Exception as er:
        return Response(str(er), status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes((AllowAny, ))
def check_username(request):
    username = request.GET.get('username', None)
    if username is None:
        return JsonResponse({'username': 'Username may not be null'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        user = User.objects.get(username=username)
        return JsonResponse({'username': 'Это имя уже занято'}, status=status.HTTP_400_BAD_REQUEST)
    except:
        return HttpResponseNoContent()

@api_view(['GET'])
@permission_classes((AllowAny, ))
def check_password(request):
    password = request.GET.get('password', None)
    if password is None:
        return JsonResponse({'password': 'Password may not be null'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        password_validation.validate_password(password)
        return HttpResponseNoContent()
    except Exception as er:
        return JsonResponse({'password': str(er)}, status=status.HTTP_400_BAD_REQUEST)











