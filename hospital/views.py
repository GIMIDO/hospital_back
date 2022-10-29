from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics
from django.core.paginator import Paginator
from django.http import HttpResponseForbidden

from .serializers import *
from .authentication import get_access_token, authorise_only, is_not_doctor, is_admin, verify_request_token


pageSize = 1

class CustomerView(APIView):

    @authorise_only
    def get(self, request):
        customers = Customer.objects.all()
        serializer = CustomerSerializer(customers, many=True)

        return Response({"customers": serializer.data})
    
    @is_not_doctor
    def post(self, request):
        customer = request.data.get('customer')
        print(customer)
        
        serializer = CustomerSerializer(data=customer)
        if (serializer.is_valid(raise_exception=True)):
            customer_saved = serializer.save()

        return Response({"success": "Customer {} created successfully".format(customer_saved.name)})

    @is_not_doctor
    def put(self, request, pk):
        savedCustomer = Customer.objects.get(pk=pk)
        customer = request.data.get('customer')
        serializer = CustomerSerializer(instance=savedCustomer, data=customer, partial=True)

        if (serializer.is_valid(raise_exception=True)):
            customer_saved = serializer.save()
        
        return Response({"success": "Customer {} updated successfully".format(customer_saved.name)})
    
    @is_admin
    def delete(self, request, pk):
        customerForDelete = Customer.objects.get(pk=pk)
        customerForDelete.delete()

        return Response({"success": "Customer {} deleted successfully".format(customerForDelete.name)})


class DepartmentView(APIView):

    @authorise_only
    def get(self, request):

        departments = Department.objects.all()
        serializer = DepartmentSerializer(departments, many=True)

        return Response({"departments": serializer.data})
    
    @is_not_doctor
    def post(self, request):

        department = request.data.get('department')
        serializer = DepartmentSerializer(data=department)

        if (serializer.is_valid(raise_exception=True)):
            department_saved = serializer.save()

        return Response({"success": "Department {} created successfully".format(department_saved.name)})

    @is_not_doctor
    def put(self, request, pk):

        savedDepartment = Department.objects.get(pk=pk)
        department = request.data.get('department')
        serializer = DepartmentSerializer(instance=savedDepartment, data=department, partial=True)

        if (serializer.is_valid(raise_exception=True)):
            department_saved = serializer.save()
        
        return Response({"success": "Department {} updated successfully".format(department_saved.name)})
    
    @is_admin
    def delete(self, request, pk):

        departmentForDelete = Department.objects.get(pk=pk)
        departmentForDelete.delete()

        return Response({"success": "Department {} deleted successfully".format(departmentForDelete.name)})


class EmployeeView(APIView):

    @authorise_only
    def get(self, request):

        employees = Employee.objects.all()
        serializer = EmployeeSerializer(employees, many=True)
        ids = Department.objects.all().values_list('id', flat=True)

        return Response({"employees": serializer.data, "ids": ids})

    @is_not_doctor
    def post(self, request):

        employee = request.data.get('employee')
        serializer = EmployeeSerializer(data=employee)

        if (serializer.is_valid(raise_exception=True)):
            employee_saved = serializer.save()

        return Response({"success": "Employee {} created successfully".format(employee_saved.name)})

    @is_not_doctor
    def put(self, request, pk):

        savedEmployee = Employee.objects.get(pk=pk)
        employee = request.data.get('employee')
        serializer = EmployeeSerializer(instance=savedEmployee, data=employee, partial=True)

        if (serializer.is_valid(raise_exception=True)):
            employee_saved = serializer.save()
        
        return Response({"success": "Employee {} updated successfully".format(employee_saved.name)})
    
    @is_admin
    def delete(self, request, pk):

        employeeForDelete = Employee.objects.get(pk=pk)
        employeeForDelete.delete()

        return Response({"success": "Employee {} deleted successfully".format(employeeForDelete.name)})


class AppointmentView(APIView):

    @authorise_only
    def get(self, request):

        appointments = Appointment.objects.all()
        serializer = AppointmentSerializer(appointments, many=True)

        return Response({"appointments": serializer.data, "employeeIds": Employee.objects.all().values_list('id', flat=True), 
        "customerIds": Customer.objects.all().values_list('id', flat=True)})
    
    @is_not_doctor
    def post(self, request):

        appointment = request.data.get('appointment')
        serializer = AppointmentSerializer(data=appointment)

        if (serializer.is_valid(raise_exception=True)):
            appointment_saved = serializer.save()

        return Response({"success": "Appointment {} created successfully".format(appointment_saved)})

    @is_not_doctor
    def put(self, request, pk):

        savedAppointment = Appointment.objects.get(pk=pk)
        appointment = request.data.get('appointment')
        serializer = AppointmentSerializer(instance=savedAppointment, data=appointment, partial=True)

        if (serializer.is_valid(raise_exception=True)):
            appointment_saved = serializer.save()
        
        return Response({"success": "Appointment {} updated successfully".format(appointment_saved)})

    @is_admin
    def delete(self, request, pk):

        appointmentForDelete = Appointment.objects.get(pk=pk)
        appointmentForDelete.delete()

        return Response({"success": "Appointment {} deleted successfully".format(appointmentForDelete)})


class LoginView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        try:
            employee = Employee.objects.get(name=username, password=password)
        except Employee.DoesNotExist:
            return HttpResponseForbidden({"error": "There is no such a person"})
        
        if employee:
            token = get_access_token(employee=employee)
            return Response({"response": token})
        else:
            return HttpResponseForbidden({"error": "There is no such a person"})
    
    def get(self, request, token):
        (role, name) = verify_request_token(token=token)
        if role is None:
            return HttpResponseForbidden()
        else:
            return Response({"role": role, "name": name})