from django.urls import path
from . import views
from django.contrib.auth.views import PasswordChangeView
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('login/', views.loginUserView, name = "login"),
    path('register/', views.registerUserView, name = 'signup'),
    path('logout/', views.logoutUserView, name = "logout"),
    path('profile/', views.perfilView, name = 'perfil-view'),
    path('change-password/', PasswordChangeView.as_view(), name='change-password')
]