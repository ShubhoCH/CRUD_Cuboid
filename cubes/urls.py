from django.urls import  re_path
from . import  views

urlpatterns = [
    re_path("addUser/", views.addUser),
    re_path("userLogin/", views.loginUser),
    re_path("addCuboid/", views.addCuboid),
    re_path("updateCuboid/", views.updateCuboid),
    re_path("deleteCuboid/", views.deleteCuboid),
    re_path("getAllCuboids/", views.getAllCuboids),
    re_path("getMyCuboids/", views.getMyCuboids)
]
