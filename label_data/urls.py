from django.urls import path
from .views import (
    B01View,
    B02View,
    B03View
)
app_name = 'label_data'

urlpatterns = [
    path("b01/",B01View.as_view(),name='b01'),
    path("b02/",B02View.as_view(),name='b02'),
    path("b03/",B03View.as_view(),name='b03'),
]