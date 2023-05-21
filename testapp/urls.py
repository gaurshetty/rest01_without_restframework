from django.urls import path


from . import views
urlpatterns = [
    path('', views.EmployeeCBV.as_view())
]
