from django.urls import path
from .views import RegisterUserView,VerifyUserEmail,LoginUserView

urlpatterns=[
    path('register/',RegisterUserView.as_view(),name='register'),
    path('verify-email/',VerifyUserEmail.as_view(),name='verify'),
    path('login/',LoginUserView.as_view(),name='login')
]