from django.urls import path
from .views import A01View
app_name = "basic_data"

urlpatterns = [
    path('a01/',A01View.as_view(),name="a01"),
]