from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

PERFIL = (
    (1, "Admin"),
    (2, "Usuario")
)

from .Usuario import Usuario
from .Fabricante import Fabricante
from .Categoria import Categoria
from .Produto import Produto
from .Carrinho import Carrinho, ItemCarrinho
from .Pedido import Pedido, PedidoItem
from .Favorito import Favorito