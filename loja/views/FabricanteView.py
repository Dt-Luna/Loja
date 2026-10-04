from django.shortcuts import render, redirect, get_object_or_404

from loja.models.Fabricante import Fabricante


def list_fabricante_view(request, id=None):
    fabricantes = Fabricante.objects.all()
    context = {'fabricantes': fabricantes}
    return render(request, template_name='fabricante/fabricante.html', context=context, status=200)


def create_fabricante_view(request):
    if request.method == 'POST':
        nome = request.POST.get('Fabricante')
        if nome:
            Fabricante.objects.create(Fabricante=nome)
            return redirect('fabricante')
    return render(request, template_name='fabricante/fabricante-create.html', status=200)


def edit_fabricante_view(request, id=None):
    fabricante = get_object_or_404(Fabricante, id=id)
    if request.method == 'POST':
        nome = request.POST.get('Fabricante')
        if nome:
            fabricante.Fabricante = nome
            fabricante.save()
            return redirect('fabricante')
    context = {'fabricante': fabricante}
    return render(request, template_name='fabricante/fabricante-edit.html', context=context, status=200)


def delete_fabricante_view(request, id=None):
    fabricante = get_object_or_404(Fabricante, id=id)
    if request.method == 'POST':
        fabricante.delete()
        return redirect('fabricante')
    context = {'fabricante': fabricante}
    return render(request, template_name='fabricante/fabricante-delete.html', context=context, status=200)
