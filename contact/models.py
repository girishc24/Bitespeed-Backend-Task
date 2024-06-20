from django.db import models

class Contact(models.Model):
    CHOICES = [
        ('primary', 'Primary'),
        ('secondary', 'Secondary')
    ]
    phoneNumber = models.CharField(max_length=20, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    linkedId = models.IntegerField(null=True, blank=True)
    linkPrecedence = models.CharField(max_length=10, choices=CHOICES)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)
    deletedAt = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f" {self.phoneNumber} | {self.email}"