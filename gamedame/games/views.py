import random
from django.shortcuts import redirect, render, get_object_or_404
from django.db.models import Q, Avg
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseBadRequest
from django.core.paginator import Paginator
from django.contrib.auth.models import User
from django.contrib import messages



from .models import CartItem, Game, Purchase, PurchaseItem, Rating

# Retorna a página principal do sistema
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

# Retorna uma página com todos os jogos do sistemma (utiliza o Paginator para criar páginas dentro página)
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

# Retorna a página com os jogos que possuem a palavra-chave pesquisada pelo usuário
def searchGamesView(request):
    search = request.GET.get('search')
    searched_games = []

    if (search):
        searched_games = Game.objects.filter(Q(title__icontains=search))

    context = {
        'searched_games': searched_games
    }

    return render(request, 'games/search-games.html', context)

# Retorna a página de um jogo qualquer
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

# Retorna a página do carrinho de compra
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

# Faz a remoção de um item do carrinho no banco de dados
@login_required
def removecartItemView(request, pk):
    cart_item = get_object_or_404(CartItem, pk=pk, user=request.user)
    cart_item.delete()
    return redirect('cart-view')

# Faz a adição de um item no carrinho
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
def updatecartitemView(request):
    original_game = get_object_or_404(Game, id=request.POST.get('original'))
    new_game = get_object_or_404(Game, id=request.POST.get('new'))

    try:
        cart_item = CartItem.objects.get(user=request.user, game=original_game)
    except CartItem.DoesNotExist:
        return HttpResponseBadRequest('<script>alert("Este jogo não está no carrinho."); window.history.back();</script>')

    # Verifica se o novo jogo já está no carrinho
    if CartItem.objects.filter(user=request.user, game=new_game).exists():
        return HttpResponseBadRequest('<script>alert("Este jogo já está no carrinho."); window.history.back();</script>')

    # Atualiza o item do carrinho com o novo jogo
    cart_item.game = new_game
    cart_item.save()

    return redirect('cart-view')

    
# Realiza a compra do usuário    
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
    
# Faz o reembolso de um jogo
@login_required
def refundGameView(request, game_id):
    # obtém o jogo a ser reembolsado
    game = get_object_or_404(Game, id=game_id)

    # processa o reembolso do jogo
    purchase_items = PurchaseItem.objects.filter(
        game=game, purchase__user=request.user)
    for purchase_item in purchase_items:
        purchase_item.refunded = True
        purchase_item.save()

    return redirect('perfil-view')

# Adiciona uma aviliação a um jogo
@login_required
def add_rating(request, game_id):
    game = get_object_or_404(Game, id=game_id)
    user = request.user
    rating = int(request.POST.get('rating', 0))

    if rating >= 0:
        rating, created = Rating.objects.update_or_create(
            user=user, game=game, defaults={'rating': rating})

    return redirect('game-view', id=game.id)

@login_required
def rating_menu(request):
    ratings = Rating.objects.all()
    return render(request, 'games/rating-menu.html', {'ratings': ratings})

@login_required
def rating_item(request, rating_id):
    rating = get_object_or_404(Rating, pk=rating_id)
    return render(request, 'games/rating.html', {'rating': rating})

@login_required
def delete_rating(request, rating_id):
    rating = get_object_or_404(Rating, id=rating_id)
    rating.delete()
    return redirect('/ratingmenu')

@login_required
def add_rating(request):
    if request.method == 'POST':
        user_username = request.POST.get('user')
        game_title = request.POST.get('game')
        new_rating = request.POST.get('rating')
        try:
            user = User.objects.get(username=user_username)
        except User.DoesNotExist:
            messages.error(request, 'Usuário não encontrado.')
            return redirect('/ratingmenu')

        try:
            game = Game.objects.get(title=game_title)
        except Game.DoesNotExist:
            messages.error(request, 'Jogo não encontrado.')
            return redirect('/ratingmenu')

        rating = Rating(user=user, game=game, rating=new_rating)
        rating.save()

        messages.success(request, 'Avaliação adicionada com sucesso.')
        return redirect('/ratingmenu')
    else:
        return render(request, 'games/add-rating.html')



@login_required
def update_rating_view(request, rating_id):
    rating = get_object_or_404(Rating, id=rating_id)

    user_username = request.POST.get('user')
    game_title = request.POST.get('game')
    new_rating = request.POST.get('rating')

    try:
        user = User.objects.get(username=user_username)
    except User.DoesNotExist:
        messages.error(request, 'Usuário não encontrado.')
        return redirect('/ratingmenu')

    try:
        game = Game.objects.get(title=game_title)
    except Game.DoesNotExist:
        messages.error(request, 'Jogo não encontrado.')
        return redirect('/ratingmenu')

    rating.user = user
    rating.game = game 
    rating.rating = new_rating
    rating.save()

    messages.success(request, 'Avaliação atualizada com sucesso.')
    return redirect('/ratingmenu')

@login_required
def games_menu(request):
    games = Game.objects.all()
    return render(request, 'games/games-menu.html', {'games': games})

@login_required
def game_item(request, game_id):
    game = get_object_or_404(Game, pk=game_id)
    return render(request, 'games/game-item-adm.html', {'game': game})

@login_required
def delete_game(request, game_id):
    game = get_object_or_404(Game, id=game_id)
    game.delete()
    return redirect('/gamesmenu')

@login_required
def update_game_view(request, game_id):
    game = get_object_or_404(Game, id=game_id)

    title = request.POST.get('title')
    description = request.POST.get('description')
    price = request.POST.get('price')
    promotion = request.POST.get('promotion')
    cover_image = request.FILES.get('cover_image')
    release_date = request.POST.get('release_date')

    try:
        if not title:
            messages.error(request, 'O título do jogo é obrigatório.')
            return redirect('/gamesmenu')
        if not description:
            messages.error(request, 'A descrição do jogo é obrigatória.')
            return redirect('/gamesmenu')
        if not price:
            messages.error(request, 'O preço do jogo é obrigatório.')
            return redirect('/gamesmenu')
        if not release_date:
            messages.error(request, 'A data de lançamento do jogo é obrigatória.')
            return redirect('/gamesmenu')

        game.title = title
        game.description = description
        game.price = price
        game.promotion = promotion
        if cover_image:
            game.cover_image = cover_image
        game.release_date = release_date
        game.save()

        messages.success(request, 'Jogo atualizado com sucesso.')
        return redirect('/gamesmenu')
    except ValueError as e:
        messages.error(request, str(e))

@login_required
def add_game(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        price = request.POST.get('price')
        promotion = request.POST.get('promotion')
        image = request.FILES.get('cover_image')
        release_date = request.POST.get('release_date')

        if not title:
            messages.error(request, 'O campo Título é obrigatório.')
            return redirect('/gamesmenu/')
        if not description:
            messages.error(request, 'O campo Descrição é obrigatório.')
            return redirect('/gamesmenu/')
        if not price:
            messages.error(request, 'O campo Preço é obrigatório.')
            return redirect('/gamesmenu/')
        if not image:
            messages.error(request, 'A imagem de capa é obrigatória.')
            return redirect('/gamesmenu/')

        
        game = Game(
            title=title,
            description=description,
            price=price,
            promotion=promotion,
            cover_image=image,
            release_date=release_date
        )
        game.save()

        messages.success(request, 'Jogo adicionado com sucesso.')
        return redirect('/gamesmenu/')
    else:
        return render(request, 'games/add-game.html')
