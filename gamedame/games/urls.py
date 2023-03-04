from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', views.gameList, name='game-list'),
    path('search/', views.searchGamesView, name="search-games"),
    path('game/<int:id>', views.gameView, name="game-view"),
    path('game/<int:game_id>/add_rating/', views.add_rating, name='add_rating'),
    path('cart/', views.cartView, name="cart-view"),
    path('cart/update', views.updatecartitemView, name="update-cart-item"),
    path('cart/<int:pk>/remove', views.removecartItemView, name='remove_cart_item'),
    path('cart/<int:game_id>/add', views.addcartItemView, name='add_to_cart'),
    path('purchase/', views.purchaseView, name='purchase'),
    path('refund/<int:game_id>', views.refundGameView, name='refund-game'),
    path('allgames/', views.allGamesView, name = "all_games"),
    path('ratingmenu/', views.rating_menu , name = "rating_menu"),
    path('rating/<int:rating_id>', views.rating_item , name = "rating_item"), 
    path('rating/<int:rating_id>/delete/', views.delete_rating, name='delete-rating'),
    path('rating/<int:rating_id>/update/', views.update_rating_view, name='update-rating'),
    path('rating/seach/', views.search_rating_item, name='search-rating-item'),
    path('ratingmenu/add/', views.add_rating, name='add-rating'),
    path('gamesmenu/', views.games_menu, name = "games_menu"),
    path('gamesadm/<int:game_id>', views.game_item , name = "game_item"), 
    path('gamesadm/<int:game_id>/delete/', views.delete_game, name='delete-game'),
    path('gamesadm/<int:game_id>/update/', views.update_game_view, name='update-game'),
    path('gamesadm/add/', views.add_game, name='add-game'),
]