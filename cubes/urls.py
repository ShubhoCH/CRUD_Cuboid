from django.urls import  re_path
from . import  views

urlpatterns = [
    re_path("addUser/", views.addUser),
    re_path("userLogin/", views.loginUser),
    re_path("addCube/", views.addCube),
    re_path("updateCube/", views.updateCube),
    re_path("deleteCube/", views.deleteCube),
    re_path("getAllCubes/", views.getAllCubes),
    re_path("getMyCubes/", views.getMyCubes)
]
