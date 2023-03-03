from django.contrib import admin

from .models import Game, Purchase, PurchaseItem, CartItem, Rating

# Modelos que podem se utilizados no menu do administrador
admin.site.register(Game)
admin.site.register(PurchaseItem)
admin.site.register(Purchase)
admin.site.register(CartItem)
admin.site.register(Rating)
