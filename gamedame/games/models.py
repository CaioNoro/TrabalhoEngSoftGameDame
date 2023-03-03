from django.db import models
from django.contrib.auth import get_user_model

# Modelo que representa o jogo no sistema
class Game(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    promotion = models.DecimalField(
        max_digits=5, decimal_places=2, null=True, blank=True)
    cover_image = models.ImageField(upload_to='static/images')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    copies_sold = models.IntegerField(default=0)
    release_date = models.DateTimeField(null=True)

    def __str__(self):
        return self.title

    def price_with_discount(self):
        return round(self.price * (1 - self.promotion/100), 2)

# Modelo que representa a compra de vários jogos no sistema
class Purchase(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    purchase_date = models.DateTimeField(auto_now_add=True)

# Modelo que representa a compra de um jogo no sistema (tabela auxiliar para o atributo
# multivalorado que representa os jogos comprados de Purchase)
class PurchaseItem(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    purchase = models.ForeignKey(Purchase, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    refunded = models.BooleanField(default=False)

# Modelo que representa o carrinho de compras
class CartItem(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.game.title} ({self.user.username})'
    
# Modelo que representa as avaliacoes dos usuários em relações ao jogos
class Rating(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    rating = models.PositiveSmallIntegerField(default=0)

    def __str__(self):
        return f'{self.rating} - {self.game.title} - ({self.user.username})'
