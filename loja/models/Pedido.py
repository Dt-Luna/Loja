from decimal import Decimal

from django.db import models

from .Carrinho import Carrinho
from .Produto import Produto
from .Usuario import Usuario


class Pedido(models.Model):
    STATUS_CHOICES = (
        ('confirmado', 'Confirmado'),
    )

    usuario = models.ForeignKey(Usuario, related_name='pedidos', on_delete=models.CASCADE)
    carrinho = models.OneToOneField(Carrinho, related_name='pedido', on_delete=models.PROTECT, null=True, blank=True)
    codigo = models.CharField(max_length=20, unique=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='confirmado')
    confirmado_em = models.DateTimeField(auto_now_add=True)
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-confirmado_em']

    @property
    def total(self):
        return sum((item.subtotal for item in self.itens.all()), Decimal('0.00'))

    def save(self, *args, **kwargs):
        if not self.codigo:
            self.codigo = f'PED-{self.usuario_id}-{self.id or 0}'
        super().save(*args, **kwargs)

    def __str__(self):
        return self.codigo


class PedidoItem(models.Model):
    pedido = models.ForeignKey(Pedido, related_name='itens', on_delete=models.CASCADE)
    produto = models.ForeignKey(Produto, on_delete=models.PROTECT)
    quantidade = models.PositiveIntegerField(default=1)
    preco_unitario = models.DecimalField(max_digits=8, decimal_places=2)

    @property
    def subtotal(self):
        return self.preco_unitario * self.quantidade

    def __str__(self):
        return f'{self.produto.Produto} x {self.quantidade}'
