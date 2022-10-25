from django.urls import path

from . import views

app_name = "encyclopedia"
urlpatterns = [
    path("", views.index, name="index"), 

    path("<str:entry>/", views.page, name="page"),

    path("search", views.search,name="search"),

    path("new",views.new,name="new"),

    path("random_page", views.random_page,name="random_page"),
    
    path('<str:entry>/edit/', views.edit, name="edit")

]
