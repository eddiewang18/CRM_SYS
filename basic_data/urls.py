from django.urls import path
from .views import (A01View,A02View,A03View,
A04View,A05View,cpnyid_shop,
county_area)
app_name = "basic_data"

urlpatterns = [
    path('a01/',A01View.as_view(),name="a01"),
    path('a02/',A02View.as_view(),name="a02"),
    path('a03/',A03View.as_view(),name="a03"),
    path('a04/',A04View.as_view(),name="a04"),
    path('a05/',A05View.as_view(),name="a05"),
    path('county_area/',county_area,name="county_area"),
    path('cpnyid_shop/',cpnyid_shop,name="cpnyid_shop")

]
