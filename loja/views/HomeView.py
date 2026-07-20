from loja.models import Produto
from django.shortcuts import render


def home_view(request):
    produto = request.GET.get("produto")
    produtos = Produto.objects.all()
    if produto:
        produtos = produtos.filter(Produto__icontains=produto)
    context = {
        "produtos": produtos
    }
    return render(request, template_name='home/home.html', context=context, status=200)