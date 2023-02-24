import random
from django.shortcuts import redirect, render, get_object_or_404
from django.db.models import Q, Avg
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseBadRequest
from django.core.paginator import Paginator

from .models import CartItem, Game, Purchase, PurchaseItem, Rating

def gameList(request):
    all_games = Game.objects.all()
    
    latest_games = all_games.order_by('-release_date')[:4]
    best_selling_games = all_games.order_by('-copies_sold')[:4]
    games_on_sale = Game.objects.filter(promotion__isnull=False).order_by('-promotion')[:4]
    random_games = random.sample(list(all_games), 3) if all_games.exists() else []

    context = {
        'latest_games': latest_games, 
        'games_on_sale': games_on_sale, 
        'best_selling_games': best_selling_games,
        'random_games' : random_games,
    }
    return render(request, 'games/list.html', context)