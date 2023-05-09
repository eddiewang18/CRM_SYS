from django.urls import path
from .views import A01View,A02View,A03View,county_area
app_name = "basic_data"

urlpatterns = [
    path('a01/',A01View.as_view(),name="a01"),
    path('a02/',A02View.as_view(),name="a02"),
    path('a03/',A03View.as_view(),name="a03"),
    path('county_area/',county_area,name="county_area")
]
