from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse

from loja.models.Categoria import Categoria


def list_categoria_view(request, id=None):
    categorias = Categoria.objects.all()
    context = {'categorias': categorias}
    return render(request, template_name='categoria/categoria.html', context=context, status=200)


def create_categoria_view(request):
    if request.method == 'POST':
        nome = request.POST.get('Categoria')
        if nome:
            Categoria.objects.create(Categoria=nome)
            return redirect('categoria')
    return render(request, template_name='categoria/categoria-create.html', status=200)


def edit_categoria_view(request, id=None):
    categoria = get_object_or_404(Categoria, id=id)
    if request.method == 'POST':
        nome = request.POST.get('Categoria')
        if nome:
            categoria.Categoria = nome
            categoria.save()
            return redirect('categoria')
    context = {'categoria': categoria}
    return render(request, template_name='categoria/categoria-edit.html', context=context, status=200)


def delete_categoria_view(request, id=None):
    categoria = get_object_or_404(Categoria, id=id)
    if request.method == 'POST':
        categoria.delete()
        return redirect('categoria')
    context = {'categoria': categoria}
    return render(request, template_name='categoria/categoria-delete.html', context=context, status=200)
