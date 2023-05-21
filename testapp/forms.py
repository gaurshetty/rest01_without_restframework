from django import forms
from .models import Employee


class EmployeeForm(forms.ModelForm):
    def clean_salary(self):
        esal = self.cleaned_data['salary']
        if esal < 5000:
            raise forms.ValidationError("Employee salary should be greater than 5000")
        return esal

    class Meta:
        model = Employee
        fields = '__all__'
