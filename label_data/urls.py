from django.urls import path
from .views import B01View

app_name = 'label_data'

urlpatterns = [
    path("b01/",B01View.as_view(),name='b01'),
]