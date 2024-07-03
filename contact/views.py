from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from .services import identify_contact
from . serializers import *
from rest_framework import status

def welcome(request):
    context={"meeps": "Bitespeed Backend Task"}
    return render(request, 'index.html', context)
    #return  HttpResponse("Welcome BitSpeed Project")

class IdentifyAPIView(APIView):
    def post(self, request):
        email = request.data.get('email')
        phone_number = request.data.get('phoneNumber')
        
        result = identify_contact(email, phone_number)
        
        return Response({"contact": result})


class Contactdetails(APIView):
    def get(self, request):
        contact = Contact.objects.all()
        contact_serializer = ContactnewSerializer(contact, many=True)
        return Response(contact_serializer.data, status=status.HTTP_200_OK)
