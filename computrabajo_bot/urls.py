from django.urls import path
from computrabajo_bot.views import ComputrabajoAPIVIew

urlpatterns = [
    path('api/computrabajo/', ComputrabajoAPIVIew.as_view()),
]
