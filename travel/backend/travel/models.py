from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models

class User(AbstractUser):
    is_admin = models.BooleanField(default=False)
    groups = models.ManyToManyField(Group, related_name="travel_user_groups", blank=True)
    user_permissions = models.ManyToManyField(Permission, related_name="travel_user_permissions", blank=True)

class TravelRequest(models.Model):
    STATUS_PENDING = 'Pending'
    STATUS_APPROVED = 'Approved'
    STATUS_REJECTED = 'Rejected'

    STATUS_CHOICES = [
        (STATUS_PENDING, 'Pending'),
        (STATUS_APPROVED, 'Approved'),
        (STATUS_REJECTED, 'Rejected'),
    ]

    TRANSPORT_FLIGHT = 'Flight'
    TRANSPORT_TRAIN = 'Train'
    TRANSPORT_BUS = 'Bus'
    TRANSPORT_CAR_RENTAL = 'Car Rental'

    TRANSPORTATION_CHOICES = [
        (TRANSPORT_FLIGHT, 'Flight'),
        (TRANSPORT_TRAIN, 'Train'),
        (TRANSPORT_BUS, 'Bus'),
        (TRANSPORT_CAR_RENTAL, 'Car Rental'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    employee_name = models.CharField(max_length=255)
    employee_id = models.CharField(max_length=50)
    department = models.CharField(max_length=100)
    designation = models.CharField(max_length=100)
    contact_number = models.CharField(max_length=20)
    email_id = models.EmailField()
    purpose_of_travel = models.TextField()
    start_point = models.CharField(max_length=255)  # Added Start Point (From)
    destination = models.CharField(max_length=255)  # Destination (To)
    start_date = models.DateField()
    return_date = models.DateField()
    mode_of_transport = models.CharField(max_length=50, choices=TRANSPORTATION_CHOICES, blank=True, null=True)
    preferred_airlines_train = models.CharField(max_length=255, blank=True, null=True)
    accommodation_required = models.BooleanField(default=False)
    meals_requirement = models.CharField(max_length=255, blank=True, null=True)
    emergency_contact_name = models.CharField(max_length=255)
    emergency_contact_number = models.CharField(max_length=20)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_PENDING)
    comments = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.destination} ({self.status})"
