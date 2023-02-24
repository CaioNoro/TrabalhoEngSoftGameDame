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

def allGamesView(request):
    all_games_list = Game.objects.all()
    
    paginator = Paginator(all_games_list, 4)
    page = request.GET.get('page')
    all_games = paginator.get_page(page)
    
    context = {
        'all_games' : all_games,
        'all_games_list' : all_games_list,
    }
    return render(request, 'games/all-games.html', context)

def searchGamesView(request):
    search = request.GET.get('search')
    searched_games = []

    if (search):
        searched_games = Game.objects.filter(Q(title__icontains=search))

    context = {
        'searched_games': searched_games
    }

    return render(request, 'games/search-games.html', context)

@login_required
def gameView(request, id):
    game = get_object_or_404(Game, pk=id)
    has_purchased = PurchaseItem.objects.filter(
        purchase__user=request.user, game=game, refunded=False).exists()
    is_in_cart = CartItem.objects.filter(user=request.user, game=game).exists()

    # Busca todas as avaliações para o jogo e calcula a média das notas
    ratings = Rating.objects.filter(game=game)
    rating_sum = int(ratings.aggregate(avg_rating=Avg('rating'))['avg_rating'] or 0)
    num_ratings = ratings.count()

    # Obtém a avaliação do usuário, se houver
    user_rating = Rating.objects.filter(game=game, user=request.user).first()

    context = {
        'game': game, 
        'has_purchased': has_purchased, 
        'is_in_cart': is_in_cart, 
        'rating_sum': rating_sum,
        'user_rating': user_rating.rating if user_rating else None,
        'num_ratings': num_ratings,
    }      

    return render(request, 'games/game.html', context)

@login_required
def cartView(request):
    user_cart = CartItem.objects.filter(user=request.user)
    cart_items = CartItem.objects.filter(user=request.user)
    total = 0
    for item in cart_items:
        total += item.game.price_with_discount()
    context = {
        'cart_items': user_cart,
        'total': total
    }
    return render(request, 'games/cart.html', context)

@login_required
def removecartItemView(request, pk):
    cart_item = get_object_or_404(CartItem, pk=pk, user=request.user)
    cart_item.delete()
    return redirect('cart-view')

@login_required
def addcartItemView(request, game_id):
    game = get_object_or_404(Game, id=game_id)

    # Verifica se o jogo já está no carrinho
    try:
        cart_item = CartItem.objects.get(user=request.user, game=game)
        return HttpResponseBadRequest('<script>alert("Este jogo já está no carrinho."); window.history.back();</script>')
    except CartItem.DoesNotExist:
        CartItem.objects.create(user=request.user, game=game)
        return redirect('/cart')
    
@login_required
def purchaseView(request):
    user = request.user
    cart_items = CartItem.objects.filter(user=user)

    if cart_items:
        # Cria um objeto Purchase
        purchase = Purchase.objects.create(user=user)

        # Cria objetos PurchaseItem para cada item do carrinho
        for cart_item in cart_items:
            game = cart_item.game
            price = game.price_with_discount()
            PurchaseItem.objects.create(
                game=game, purchase=purchase, price=price)

        # Remove os itens do carrinho
        cart_items.delete()

        return redirect('/')
    else:
        # Se o carrinho está vazio, redireciona de volta para o carrinho
        return redirect('cart')