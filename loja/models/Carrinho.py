from decimal import Decimal

from django.db import models

from .Produto import Produto
from .Usuario import Usuario


class Carrinho(models.Model):
    STATUS_CHOICES = (
        ('aberto', 'Aberto'),
        ('confirmado', 'Confirmado'),
    )

    session_key = models.CharField(max_length=255, unique=True, null=True, blank=True)
    usuario = models.ForeignKey(Usuario, null=True, blank=True, on_delete=models.SET_NULL, related_name='carrinhos')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='aberto')
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)
    confirmado_em = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-criado_em']

    @property
    def total(self):
        return sum((item.subtotal for item in self.itens.all()), Decimal('0.00'))

    @property
    def quantidade_total(self):
        return sum(item.quantidade for item in self.itens.all())

    def __str__(self):
        return f'Carrinho {self.id}'


class ItemCarrinho(models.Model):
    carrinho = models.ForeignKey(Carrinho, related_name='itens', on_delete=models.CASCADE)
    produto = models.ForeignKey(Produto, on_delete=models.PROTECT)
    quantidade = models.PositiveIntegerField(default=1)
    preco_unitario = models.DecimalField(max_digits=8, decimal_places=2)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['carrinho', 'produto'], name='unique_item_por_carrinho')
        ]

    @property
    def subtotal(self):
        return self.preco_unitario * self.quantidade

    def __str__(self):
        return f'{self.produto.Produto} ({self.quantidade})'
