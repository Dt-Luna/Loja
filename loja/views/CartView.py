import uuid

from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils import timezone
from django.utils.http import url_has_allowed_host_and_scheme

from loja.models import Carrinho, Favorito, ItemCarrinho, Pedido, PedidoItem, Produto


def get_or_create_cart(request):
    cart_id = request.session.get('cart_id')
    cart = None
    if cart_id:
        cart = Carrinho.objects.filter(session_key=cart_id).first()

    if cart is None:
        cart = Carrinho.objects.create(session_key=request.session.session_key or f'cart-{uuid.uuid4().hex}')
        request.session['cart_id'] = cart.session_key

    if request.user.is_authenticated:
        usuario = getattr(request.user, 'usuario', None)
        if usuario is not None and cart.usuario_id != usuario.id:
            cart.usuario = usuario
            cart.save(update_fields=['usuario'])

    request.session['cart_id'] = cart.session_key
    return cart


def cart_view(request):
    cart = get_or_create_cart(request)
    itens = cart.itens.select_related('produto').all()
    context = {'cart': cart, 'itens': itens}
    return render(request, template_name='cart/cart.html', context=context, status=200)


def add_to_cart(request, produto_id):
    if request.method != 'POST':
        return redirect('home')

    produto = get_object_or_404(Produto, pk=produto_id)
    cart = get_or_create_cart(request)
    item, created = ItemCarrinho.objects.get_or_create(
        carrinho=cart,
        produto=produto,
        defaults={'preco_unitario': produto.preco}
    )

    if created:
        item.quantidade = 1
    else:
        item.quantidade += 1

    item.preco_unitario = produto.preco
    item.save()
    return redirect('cart')


def update_cart_item(request, item_id):
    if request.method != 'POST':
        return redirect('cart')

    cart = get_or_create_cart(request)
    item = get_object_or_404(ItemCarrinho, pk=item_id)

    if item.carrinho_id != cart.id:
        return redirect('cart')

    acao = request.POST.get('acao', 'increase')
    if acao == 'increase':
        item.quantidade += 1
    elif acao == 'decrease':
        item.quantidade -= 1

    if item.quantidade <= 0:
        item.delete()
    else:
        item.preco_unitario = item.produto.preco
        item.save()

    return redirect('cart')


@login_required(login_url='login')
def checkout_view(request):
    cart = get_or_create_cart(request)

    if cart.status == 'confirmado' and hasattr(cart, 'pedido'):
        return redirect('order_detail', pedido_id=cart.pedido.pk)

    if not cart.itens.exists():
        context = {'cart': cart, 'empty': True}
        return render(request, template_name='cart/checkout.html', context=context, status=200)

    if request.method == 'POST':
        with transaction.atomic():
            pedido = Pedido.objects.create(usuario=request.user.usuario, carrinho=cart)
            for item in cart.itens.select_related('produto'):
                PedidoItem.objects.create(
                    pedido=pedido,
                    produto=item.produto,
                    quantidade=item.quantidade,
                    preco_unitario=item.preco_unitario,
                )

            cart.status = 'confirmado'
            cart.confirmado_em = timezone.now()
            cart.usuario = request.user.usuario
            cart.save(update_fields=['status', 'confirmado_em', 'usuario', 'atualizado_em'])

            request.session['cart_id'] = None
            return redirect('order_detail', pedido_id=pedido.pk)

    context = {'cart': cart, 'itens': cart.itens.select_related('produto').all()}
    return render(request, template_name='cart/checkout.html', context=context, status=200)


@login_required(login_url='login')
def order_detail_view(request, pedido_id):
    pedido = get_object_or_404(Pedido, pk=pedido_id)
    if pedido.usuario_id != request.user.usuario.id:
        return redirect('home')

    context = {'pedido': pedido, 'itens': pedido.itens.select_related('produto').all()}
    return render(request, template_name='cart/order_detail.html', context=context, status=200)


@login_required(login_url='login')
def favoritos_view(request):
    favoritos = Favorito.objects.filter(usuario=request.user.usuario).select_related('produto').all()
    context = {'favoritos': favoritos}
    return render(request, template_name='favoritos/favoritos.html', context=context, status=200)


@login_required(login_url='login')
def toggle_favorito(request, produto_id):
    produto = get_object_or_404(Produto, pk=produto_id)
    favorito = Favorito.objects.filter(usuario=request.user.usuario, produto=produto).first()

    if favorito:
        favorito.delete()
    else:
        Favorito.objects.create(usuario=request.user.usuario, produto=produto)

    next_url = request.POST.get('next') or request.GET.get('next') or request.META.get('HTTP_REFERER') or reverse('home')
    if next_url and url_has_allowed_host_and_scheme(next_url, allowed_hosts={request.get_host()}):
        return redirect(next_url)
    return redirect('home')
