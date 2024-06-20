from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Contact
from .serializers import ContactSerializer
from django.db.models import Q


def welcome(request):
    return  HttpResponse("Welcome BitSpeed Project")

class ContactView(APIView):
    def post(self, request):
        data = request.data
        email = data.get("email")
        phone_number = data.get("phoneNumber")

        if not email and not phone_number:
            return Response({"error": "Invalid request"}, status=400)

        
        existing_contacts = Contact.objects.filter(Q(email=email) | Q(phoneNumber=phone_number))

        primary_contact = None
        emails = set()
        phone_numbers = set()
        secondary_contact_ids = set()

        # Determine the primary contact and collect information
        for contact in existing_contacts:
            if contact.linkPrecedence == "primary":
                primary_contact = contact
            elif contact.linkPrecedence == "secondary" and contact.linkedId:
                secondary_contact_ids.add(contact.id)
                
            if contact.email:
                emails.add(contact.email)
            if contact.phoneNumber:
                phone_numbers.add(contact.phoneNumber)

        # If no primary contact found but there are existing contacts, promote one to primary
        if not primary_contact and existing_contacts.exists():
            primary_contact = existing_contacts.first()
            primary_contact.linkPrecedence = "primary"
            primary_contact.save()

        if primary_contact:
            primary_contact_id = primary_contact.id
        else:
            # Create a new primary contact if no existing contacts found
            new_contact = Contact.objects.create(
                email=email,
                phoneNumber=phone_number,
                linkPrecedence="primary"
            )
            primary_contact_id = new_contact.id
            emails.add(email)
            if phone_number:
                phone_numbers.add(phone_number)

        # Link the new email or phone number if not already linked
        if email and email not in emails:
            emails.add(email)
            new_secondary_contact = Contact.objects.create(
                email=email, phoneNumber=None, linkedId=primary_contact_id, linkPrecedence="secondary"
            )
            secondary_contact_ids.add(new_secondary_contact.id)
        if phone_number and phone_number not in phone_numbers:
            phone_numbers.add(phone_number)
            new_secondary_contact = Contact.objects.create(
                email=None, phoneNumber=phone_number, linkedId=primary_contact_id, linkPrecedence="secondary"
            )
            secondary_contact_ids.add(new_secondary_contact.id)

        response_data = {
            "contact": {
                "primaryContactId": primary_contact_id,
                "emails": list(emails),
                "phoneNumbers": list(phone_numbers),
                "secondaryContactIds": list(secondary_contact_ids)
            }
        }

        return Response(response_data, status=status.HTTP_200_OK)
