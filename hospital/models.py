from django.db import models
from django.utils import timezone


class Customer(models.Model):

    name = models.CharField(max_length=20)

    email = models.EmailField(max_length=255)

    phone = models.CharField(max_length=20, unique=True, null=False, blank=False)

    address = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Department(models.Model):

    name = models.CharField(max_length=20)

    address = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Employee(models.Model):

    ROLE_CHOICES = (
        ('Admin', 'Admin'),
        ('Doctor', 'Doctor'),
        ('Reception', 'Reception'),
    )

    name = models.CharField(max_length=20)

    password = models.CharField(max_length=255)

    email = models.EmailField(max_length=255)

    phone = models.CharField(max_length=20, unique=True, null=False, blank=False)

    address = models.CharField(max_length=255)

    department = models.ForeignKey(Department, on_delete=models.CASCADE)

    role = models.CharField(choices=ROLE_CHOICES, max_length=20, default="Doctor")

    def __str__(self):
        return self.name


class Appointment(models.Model):

    date = models.DateField()

    start = models.TimeField()
    end = models.TimeField()
    
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)

    def __str__(self):
        return "" + self.date.strftime('%m/%d/%Y') + " " + self.start.strftime("%H:%M") + " " + self.end.strftime("%H:%M")
