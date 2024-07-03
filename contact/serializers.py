from rest_framework import serializers
from .models import Contact

class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = ["id", "phoneNumber", "email", "linkPrecedence"]

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["emails"] = [contact.email for contact in Contact.objects.filter(linkedId=instance.id)]
        data["phoneNumbers"] = [contact.phoneNumber for contact in Contact.objects.filter(linkedId=instance.id)]
        data["secondaryContactIds"] = [contact.id for contact in Contact.objects.filter(linkedId=instance.id, linkPrecedence="secondary")]
        data["primaryContactId"] = instance.id
        return data


class ContactnewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = '__all__'