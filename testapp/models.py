from django.db import models


class Employee(models.Model):
    no = models.IntegerField()
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    gender = models.CharField(max_length=50)
    salary = models.FloatField()
    address = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.__dict__}'

    def __repr__(self):
        return str(self)
    