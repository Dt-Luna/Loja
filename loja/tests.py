from decimal import Decimal

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from loja.models.Categoria import Categoria
from loja.models.Fabricante import Fabricante
from loja.models.Produto import Produto
from loja.models.Carrinho import Carrinho, ItemCarrinho
from loja.models.Pedido import Pedido
from loja.models.Favorito import Favorito


class CartAndCheckoutTests(TestCase):
    def setUp(self):
        self.categoria = Categoria.objects.create(Categoria='Eletrônicos')
        self.fabricante = Fabricante.objects.create(Fabricante='Dell')
        self.produto = Produto.objects.create(
            Produto='Notebook',
            destaque=True,
            promocao=True,
            msgPromocao='Promoção',
            preco=Decimal('1500.00'),
            categoria=self.categoria,
            fabricante=self.fabricante,
        )
        self.user_model = get_user_model()
        self.user = self.user_model.objects.create_user(username='alice', password='senha123')

    def test_add_product_to_empty_cart_and_merge_quantity(self):
        response = self.client.post(reverse('add_to_cart', args=[self.produto.pk]))
        self.assertEqual(response.status_code, 302)

        cart = Carrinho.objects.get(session_key=self.client.session.get('cart_id'))
        self.assertEqual(cart.itens.count(), 1)
        self.assertEqual(cart.itens.first().quantidade, 1)

        response = self.client.post(reverse('add_to_cart', args=[self.produto.pk]))
        self.assertEqual(response.status_code, 302)
        cart.refresh_from_db()
        self.assertEqual(cart.itens.count(), 1)
        self.assertEqual(cart.itens.first().quantidade, 2)

    def test_increase_and_decrease_quantity_updates_totals_and_removes_zero(self):
        cart = Carrinho.objects.create(session_key='cart-1')
        item = ItemCarrinho.objects.create(carrinho=cart, produto=self.produto, quantidade=1, preco_unitario=self.produto.preco)

        session = self.client.session
        session.flush()
        session['cart_id'] = cart.session_key
        session.save()

        self.client.post(reverse('update_cart_item', args=[item.pk]), {'acao': 'increase'})
        item.refresh_from_db()
        self.assertEqual(item.quantidade, 2)
        self.assertEqual(item.subtotal, Decimal('3000.00'))

        self.client.post(reverse('update_cart_item', args=[item.pk]), {'acao': 'decrease'})
        item.refresh_from_db()
        self.assertEqual(item.quantidade, 1)

        self.client.post(reverse('update_cart_item', args=[item.pk]), {'acao': 'decrease'})
        self.assertFalse(ItemCarrinho.objects.filter(pk=item.pk).exists())

    def test_checkout_requires_login_and_records_order(self):
        cart = Carrinho.objects.create(session_key='cart-2')
        ItemCarrinho.objects.create(carrinho=cart, produto=self.produto, quantidade=1, preco_unitario=self.produto.preco)

        session = self.client.session
        session.flush()
        session['cart_id'] = cart.session_key
        session.save()

        response = self.client.get(reverse('checkout'))
        self.assertEqual(response.status_code, 302)
        self.assertIn('login', response.url)

        self.client.force_login(self.user)
        response = self.client.post(reverse('checkout'))
        self.assertEqual(response.status_code, 302)
        cart.refresh_from_db()
        self.assertEqual(cart.status, 'confirmado')
        self.assertTrue(Pedido.objects.filter(usuario=self.user.usuario).exists())
        pedido = Pedido.objects.filter(usuario=self.user.usuario).first()
        self.assertEqual(pedido.itens.count(), 1)
        self.assertEqual(pedido.itens.first().produto, self.produto)
        self.assertEqual(pedido.total, Decimal('1500.00'))

    def test_favorites_require_auth_and_are_private_per_user(self):
        response = self.client.post(reverse('toggle_favorito', args=[self.produto.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertIn('login', response.url)

        self.client.force_login(self.user)
        response = self.client.post(reverse('toggle_favorito', args=[self.produto.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Favorito.objects.filter(usuario=self.user.usuario, produto=self.produto).count(), 1)

        other_user = self.user_model.objects.create_user(username='bob', password='senha123')
        response = self.client.get(reverse('favoritos'))
        self.assertContains(response, self.produto.Produto)

        self.client.force_login(other_user)
        response = self.client.get(reverse('favoritos'))
        self.assertNotContains(response, self.produto.Produto)


class RouteAndTemplateTests(TestCase):
    def test_core_routes_are_registered(self):
        self.assertEqual(reverse('home'), '/')
        self.assertEqual(reverse('produto'), '/produto/')
        self.assertEqual(reverse('cart'), '/carrinho/')
        self.assertEqual(reverse('checkout'), '/checkout/')
        self.assertEqual(reverse('favoritos'), '/favoritos/')
