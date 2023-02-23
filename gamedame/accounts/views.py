from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from accounts.forms import CustomUserCreationForm, LoginForm

from games.models import PurchaseItem

@login_required
def perfilView(request):
    games = PurchaseItem.objects.filter(
        purchase__user=request.user).exclude(refunded=True)
    return render(request, 'accounts/account.html', {'user': request.user, 'games': games})