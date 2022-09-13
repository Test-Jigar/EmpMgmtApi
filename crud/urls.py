from django.urls import path
from . import views

from django.conf.urls.static import static
from django.conf import settings

urlpatterns=[
    path('createEmployee', views.createEmployee),
    path('getEmployee', views.getEmployee),
    path('updateEmployee', views.updateEmployee),
    path('deleteEmployee', views.deleteEmployee),
    path('registration', views.registration),
    path('login', views.login),
    path('logout', views.logout),
    path('', views.homePage)

]