from django.shortcuts import render
from django.views.generic import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from .models import Employee
from .forms import EmployeeForm
from .mixins import HttpResponseMixin, SerializeMixin
from .utils import is_json
import json


@method_decorator(csrf_exempt, name='dispatch')
class EmployeeCBV(HttpResponseMixin, SerializeMixin, View):
    def get_object_by_id(self, id):
        try:
            emp = Employee.objects.get(id=id)
        except Employee.DoesNotExist:
            emp = None
        return emp

    def get(self, request, *args, **kwargs):
        data = request.body
        valid_data = is_json(data)
        if not valid_data:
            json_data = json.dumps({'msg': "Please provide data in valid format"})
            return self.render_to_httpresponse(json_data, status=400)
        pdata = json.loads(data)
        id = pdata.get('id', None)
        if id is not None:
            emp = self.get_object_by_id(id)
            if emp is None:
                json_data = json.dumps({'msg': "No matched resource found for given id"})
                return self.render_to_httpresponse(json_data, status=400)
            json_data = self.serialize([emp,])
            return self.render_to_httpresponse(json_data)
        qs = Employee.objects.all()
        json_data = self.serialize(qs)
        return self.render_to_httpresponse(json_data)

    def post(self, request, *args, **kwargs):
        data = request.body
        valid_data = is_json(data)
        if not valid_data:
            json_data = json.dumps({'msg': "Please provide data in valid format"})
            return self.render_to_httpresponse(json_data, status=400)
        pdata = json.loads(data)
        form = EmployeeForm(pdata)
        if form.is_valid():
            form.save(commit=True)
            json_data = json.dumps({'msg': 'Resource created successfully'})
            return self.render_to_httpresponse(json_data)
        if form.errors:
            json_data = json.dumps(form.errors)
            return self.render_to_httpresponse(json_data, status=400)

    def put(self, request, *args, **kwargs):
        data = request.body
        valid_data = is_json(data)
        if not valid_data:
            json_data = json.dumps({'msg': "Please provide data in valid format"})
            return self.render_to_httpresponse(json_data, status=400)
        pdata = json.loads(data)
        id = pdata.get('id', None)
        if id is None:
            json_data = json.dumps({'msg': "Id is mandatory to perform updation"})
            return self.render_to_httpresponse(json_data, status=400)
        emp = Employee.objects.get(id=id)
        if emp is None:
            json_data = json.dumps({'msg': "No matched resource found for given id"})
            return self.render_to_httpresponse(json_data, status=400)
        emp_data = {'no': emp.no, 'name': emp.name, 'age': emp.age, 'gender': emp.gender, 'salary': emp.salary, 'address': emp.address}
        emp_data.update(pdata)
        form = EmployeeForm(emp_data, instance=emp)
        if form.is_valid():
            form.save(commit=True)
            json_data = json.dumps({'msg': 'Resource updated successfully'})
            return self.render_to_httpresponse(json_data)
        if form.errors:
            json_data = json.dumps(form.errors)
            return self.render_to_httpresponse(json_data, status=400)

    def delete(self, request, *args, **kwargs):
        data = request.body
        valid_data = is_json(data)
        if not valid_data:
            json_data = json.dumps({'msg': "Please provide data in valid format"})
            return self.render_to_httpresponse(json_data, status=400)
        pdata = json.loads(data)
        id = pdata.get('id', None)
        if id is None:
            json_data = json.dumps({'msg': "Id is mandatory to perform updation"})
            return self.render_to_httpresponse(json_data, status=400)
        emp = Employee.objects.get(id=id)
        if emp is None:
            json_data = json.dumps({'msg': "No matched resource found for given id"})
            return self.render_to_httpresponse(json_data, status=400)
        status, deleted_data = emp.delete()
        if status == 1:
            json_data = json.dumps({'msg': "Resource deleted successfully"})
            return self.render_to_httpresponse(json_data)
        json_data = json.dumps({'msg': "Unable to delete. Try again"})
        return self.render_to_httpresponse(json_data, status=500)
