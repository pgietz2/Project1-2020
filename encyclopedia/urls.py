from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:entryname>", views.getentry, name="wiki"),
    path("new/", views.new, name="new"),
    path("edit/<str:entryname>", views.edit, name="edit"),
    path("random/", views.random, name="random")

]
