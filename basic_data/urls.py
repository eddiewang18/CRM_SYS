from django.urls import path
from .views import (A01View,A02View,A03View,
A04View,A05View,cpnyid_shop,cpnyid_hrgrp,cpny_vipgrp,
county_area,A06View,A07View,A08View,A09View,cpny_prodtype)
app_name = "basic_data"

urlpatterns = [
    path('a01/',A01View.as_view(),name="a01"),
    path('a02/',A02View.as_view(),name="a02"),
    path('a03/',A03View.as_view(),name="a03"),
    path('a04/',A04View.as_view(),name="a04"),
    path('a05/',A05View.as_view(),name="a05"),
    path('a06/',A06View.as_view(),name="a06"),
    path('a07/',A07View.as_view(),name="a07"),
    path('a08/',A08View.as_view(),name="a08"),
    path('a09/',A09View.as_view(),name="a09"),
    path('county_area/',county_area,name="county_area"),
    path('cpnyid_shop/',cpnyid_shop,name="cpnyid_shop"),
    path('cpnyid_hrgrp/',cpnyid_hrgrp,name="cpnyid_hrgrp"),
    path('cpny_vipgrp/',cpny_vipgrp,name="cpny_vipgrp"),
    path('cpny_prodtype/',cpny_prodtype,name="cpny_prodtype"),
]
