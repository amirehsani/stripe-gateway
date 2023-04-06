from django.urls import path
from .apis import RegisterAPI, ProfileAPI


urlpatterns = [
    path('register/', RegisterAPI.as_view(),name="register"),
    path('profile/', ProfileAPI.as_view(),name="profile"),
]
