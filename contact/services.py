from .models import Contact
from django.db.models import Q
from django.utils import timezone

def identify_contact(email, phone_number):
    existing_contacts = Contact.objects.filter(
        Q(email=email) | Q(phoneNumber=phone_number),
        linkedId__isnull=True
    ).order_by('createdAt')

    if not existing_contacts.exists():
        new_contact = Contact.objects.create(
            email=email,
            phoneNumber=phone_number,
            linkPrecedence='primary'
        )
        return consolidate_contact_info(new_contact)

    primary_contact = existing_contacts.first()
    
    if len(existing_contacts) > 1 or (email and phone_number and (primary_contact.email != email or primary_contact.phoneNumber != phone_number)):
        secondary_contact = Contact.objects.create(
            email=email,
            phoneNumber=phone_number,
            linkedId=primary_contact,
            linkPrecedence='secondary'
        )
        
        
        Contact.objects.filter(
            id__in=existing_contacts.values_list('id', flat=True)[1:]
        ).update(linkedId=primary_contact, linkPrecedence='secondary')

    return consolidate_contact_info(primary_contact)

def consolidate_contact_info(primary_contact):
    all_contacts = [primary_contact] + list(Contact.objects.filter(linkedId=primary_contact))
    
    emails = list(set(contact.email for contact in all_contacts if contact.email))
    phone_numbers = list(set(contact.phoneNumber for contact in all_contacts if contact.phoneNumber))
    
    secondary_ids = [contact.id for contact in all_contacts if contact.linkPrecedence == 'secondary']

    return {
        "primaryContactId": primary_contact.id,
        "emails": emails,
        "phoneNumbers": phone_numbers,
        "secondaryContactIds": secondary_ids
    }