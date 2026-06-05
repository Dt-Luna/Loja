from django.http import HttpResponse
from loja.models import Produto
from django.shortcuts import render
def home_view(request):
    produto = request.GET.get("produto")
    produtos = Produto.objects.all()
    if produto is not None:
        produtos = produtos.filter(Produto__contains=produto)
    context = {
        "produtos": produtos
        }
    return render(request, template_name='home/home.html', context=context, status=200)