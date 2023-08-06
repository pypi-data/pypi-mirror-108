from django.urls import path
from .views import MainHomeView

app_name = 'ex00'
urlpatterns = [
    path('', MainHomeView.as_view(), name='main'),
]
