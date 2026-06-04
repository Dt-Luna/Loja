from django.http import HttpResponse
from loja.models import Produto
from datetime import datetime, timedelta
from django.utils import timezone

def list_produto_view(request, id=None):
    produto = request.GET.get('produto')
    destaque = request.GET.get('destaque')
    promocao = request.GET.get('promocao')
    categoria = request.GET.get('categoria')
    fabricante = request.GET.get('fabricante')
    dias = request.GET.get('dias')

    produtos = Produto.objects.all()
    
    if dias is not None:
        now = timezone.now()
        now = now - timedelta(days=int(dias))
        produtos = produtos.filter(criado_em__gte=now)
    # Filtrar os produtos com base nos parâmetros de consulta
    if produto is not None:
        produtos = produtos.filter(Produto__contains=produto)
        # permitir a busca por parte do nome do produto usando o operador __contains
    if promocao is not None:
        produtos = produtos.filter(promocao=promocao)
    if destaque is not None:
        produtos = produtos.filter(destaque=destaque)
    if categoria is not None:
        produtos = produtos.filter(categoria__Categoria=categoria)
    if fabricante is not None:
        produtos = produtos.filter(fabricante__Fabricante=fabricante)
    
    # if destaque is not None:
    #     print(destaque)
    # if promocao is not None:
    #     print(promocao)
    # if categoria is not None:
    #     print(categoria)
    # if fabricante is not None:
    #     print(fabricante)
    # if produto is not None:
    #     print(produto)  

    if id is not None:
        produtos = produtos.filter(id=id)
    print(produtos)
    ids = [produto.id for produto in produtos]
    return HttpResponse('<h1>Produto de id %s!</h1>' % ids)

    