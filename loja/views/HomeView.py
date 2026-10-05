from django.shortcuts import render

from loja.models import Favorito, Produto


def home_view(request):
    produto = request.GET.get("produto")
    produtos = Produto.objects.all()
    if produto:
        produtos = produtos.filter(Produto__icontains=produto)

    favoritos_ids = set()
    if request.user.is_authenticated:
        favoritos_ids = set(
            Favorito.objects.filter(usuario=request.user.usuario).values_list('produto_id', flat=True)
        )

    context = {
        "produtos": produtos,
        "favoritos_ids": favoritos_ids,
    }
    return render(request, template_name='home/home.html', context=context, status=200)