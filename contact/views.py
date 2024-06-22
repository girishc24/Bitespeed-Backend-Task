from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from .services import identify_contact

def welcome(request):
    return  HttpResponse("Welcome BitSpeed Project")

class IdentifyAPIView(APIView):
    def post(self, request):
        email = request.data.get('email')
        phone_number = request.data.get('phoneNumber')
        
        result = identify_contact(email, phone_number)
        
        return Response({"contact": result})
