from django.urls import path,include
from .views import *

urlpatterns = [
    path("verification/",EmailVarification.as_view(),name="verification")

]