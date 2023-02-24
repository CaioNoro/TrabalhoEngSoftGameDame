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
    path('cart/<int:pk>/remove', views.removecartItemView, name='remove_cart_item'),
    path('cart/<int:game_id>/add', views.addcartItemView, name='add_to_cart'),
    path('purchase/', views.purchaseView, name='purchase'),
    path('refund/<int:game_id>', views.refundGameView, name='refund-game'),
    path('allgames/', views.allGamesView, name = "all_games")
]

# urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
