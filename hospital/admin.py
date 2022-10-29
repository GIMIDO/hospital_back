from django.contrib import admin
from .models import *


admin.site.register(Customer)
admin.site.register(Employee)
admin.site.register(Department)
admin.site.register(Appointment)