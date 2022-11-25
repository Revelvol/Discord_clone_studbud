from django.urls import path
from . import views


urlpatterns = [
    path('',views.getRoutes, name='get-api'),
    path('rooms/',views.getRooms, name='get-room'),

]