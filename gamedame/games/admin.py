from django.contrib import admin

from .models import Game, Purchase, PurchaseItem, CartItem

admin.site.register(Game)
admin.site.register(PurchaseItem)
admin.site.register(Purchase)
admin.site.register(CartItem)
