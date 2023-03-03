from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from accounts.forms import CustomUserCreationForm, LoginForm

from games.models import PurchaseItem

#Retorna a página da conta do usuário
@login_required
def perfilView(request):
    games = PurchaseItem.objects.filter(
        purchase__user=request.user).exclude(refunded=True)
    return render(request, 'accounts/account.html', {'user': request.user, 'games': games})

#Retorna a página de login de usuário
def loginUserView(request):
    if request.method == "POST":
        form = LoginForm(request, data=request.POST)
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('game-list')
        else:
            return redirect('login')
    else:
        form = LoginForm()
        return render(request, 'accounts/login.html', {'form': form})
    
#Retorna a página de registro de usuário
def registerUserView(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'accounts/register.html', {'form': form})

#Desloga o usuário do sistema
def logoutUserView(request):
    logout(request)
    return redirect('game-list')

