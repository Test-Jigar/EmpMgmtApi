import re
from urllib import request
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse
from django.contrib.auth import get_user_model
from .models import Employee, User, Token
from .serializers import UserSerializer, TokenSerializer,EmployeeSerializer
import requests
from django.core.files.storage import default_storage
import secrets


def homePage(request):
    return render(request, 'HomePage.html')

# Create your views here.

@csrf_exempt
def registration(request):
    if request.method=='POST':
        user_data=JSONParser().parse(request)
        temp =  User.objects.filter(email = user_data['email'])
        print(len(temp))
        try:
            user_serializer = UserSerializer(data=user_data)
            if user_serializer.is_valid() and len(temp) == 0:
                user_serializer.save()
                return JsonResponse("Added Successfully", safe=False, status=201)
            else:
                return JsonResponse("Registration Failed", safe=False,status=400)
        except requests.exceptions.RequestException as e:
            return JsonResponse(e, safe=False,status=400)


@csrf_exempt
def login(request):
    if request.method=='POST':
        login_data=JSONParser().parse(request)
        token = secrets.token_hex(16)
        login_data['token'] = token
        temp = User.objects.filter(email = login_data['username'])
        login_serializer=TokenSerializer(data=login_data)
        if login_serializer.is_valid() and len(temp)>0:
            login_serializer.save()
            return JsonResponse({"token":token},safe=False,status=200)
        return JsonResponse("Login Failed",safe=False,status=400)


@csrf_exempt
def logout(request):
    if request.method=='POST':
            token_data=JSONParser().parse(request)
            temp = Token.objects.filter(token = token_data['token'])
            if len(temp)!=0:
                temp.delete()
                return JsonResponse("Logut Successfully", safe=False,status=200)
            else:
                return JsonResponse("Unauthorized User", safe=False,status=403)


@csrf_exempt
def createEmployee(request):
    if request.method=='POST':
        emp_data = JSONParser().parse(request)
        temp = Token.objects.filter(token = emp_data['token'])
        emp = Employee.objects.filter(email = emp_data['email'])
        emp_data.pop("token")
        print(emp_data)
        try:
            emp_serializer = EmployeeSerializer(data=emp_data)
            print("create employee",len(temp),len(emp),emp_serializer.is_valid())
            if len(temp)!=0 and len(emp)==0 and emp_serializer.is_valid():
                    emp_serializer.save()
                    return JsonResponse("Employee Registered Successfully", safe=False,status=200)
            else:
                return JsonResponse("Employee Registration Failed", safe=False,status=422)
        except requests.exceptions.RequestException as e:
            return JsonResponse(e, safe=False,status=422)
    else:
        return JsonResponse("Invalid Request Method", safe=False,status=422)


@csrf_exempt
def getEmployee(request,id=0):
    if request.method=='POST':
        emp_data = JSONParser().parse(request)
        temp = Token.objects.filter(token = emp_data['token'])
        try:
            if len(temp)!=0:
                users = Employee.objects.filter(email = emp_data['email'])
                if users:
                    user_serializer=UserSerializer(users,many=True)
                    return JsonResponse(user_serializer.data, safe=False,status=200)
                else:
                    return JsonResponse("Invalid Request Data", safe=False,status=422)
            else:
                return JsonResponse("Invalid Token", safe=False,status=422)
        except requests.exceptions.RequestException as e:
                    return e
    else:
        return JsonResponse("Invalid Request Method", safe=False,status=422)


@csrf_exempt
def updateEmployee(request,id=0):
    if request.method=='PUT':
        emp_data = JSONParser().parse(request)
        temp = Token.objects.filter(token = emp_data['token'])
        try:
            if len(temp)!=0:
                users = Employee.objects.filter(email = emp_data['email'])
                if users:
                    users.update(firstname=emp_data['firstname'])
                    return JsonResponse("User Data Updated", safe=False,status=200)
                else:
                    return JsonResponse("Invalid Request Data", safe=False,status=400)
            else:
                return JsonResponse("Invalid Token", safe=False,status=400)
        except requests.exceptions.RequestException as e:
                    return e
    else:
        return JsonResponse("Invalid Request Method", safe=False, status=400)


@csrf_exempt
def deleteEmployee(request,id=0):
    if request.method=='POST':
        emp_data = JSONParser().parse(request)
        temp = Token.objects.filter(token = emp_data['token'])
        try:
            if len(temp)!=0:
                users = Employee.objects.filter(email = emp_data['email'])
                print(users,temp,emp_data)
                if users:
                    users.delete()
                    return JsonResponse("User Data Delete", safe=False, status=200)
                else:
                    return JsonResponse("Invalid Request Data", safe=False,status=400)
            else:
                return JsonResponse("Invalid Token", safe=False,status=400)
        except requests.exceptions.RequestException as e:
                    return e
    else:
        return JsonResponse("Invalid Request Method", safe=False,status=400)


