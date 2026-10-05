from django.urls import path

from loja.views.CartView import add_to_cart, cart_view, order_detail_view, toggle_favorito, update_cart_item

urlpatterns = [
    path('', cart_view, name='cart'),
    path('adicionar/<int:produto_id>/', add_to_cart, name='add_to_cart'),
    path('item/<int:item_id>/atualizar/', update_cart_item, name='update_cart_item'),
    path('pedido/<int:pedido_id>/', order_detail_view, name='order_detail'),
    path('favoritar/<int:produto_id>/', toggle_favorito, name='toggle_favorito'),
]
