from django.db import models

from .Produto import Produto
from .Usuario import Usuario


class Favorito(models.Model):
    usuario = models.ForeignKey(Usuario, related_name='favoritos', on_delete=models.CASCADE)
    produto = models.ForeignKey(Produto, related_name='favoritos', on_delete=models.CASCADE)
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['usuario', 'produto'], name='unique_favorito_por_usuario')
        ]

    def __str__(self):
        return f'{self.usuario} -> {self.produto.Produto}'
