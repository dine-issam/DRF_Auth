from django.urls import path
from .views import RegisterUserView,VerifyUserEmail,LoginUserView,TestAuthenticationView

urlpatterns=[
    path('register/',RegisterUserView.as_view(),name='register'),
    path('verify-email/',VerifyUserEmail.as_view(),name='verify'),
    path('login/',LoginUserView.as_view(),name='login'),
    path('profil/',TestAuthenticationView.as_view(),name='granted')
]