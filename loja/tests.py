from django.test import TestCase
from django.urls import reverse

from loja.models.Categoria import Categoria
from loja.models.Fabricante import Fabricante


class CategoriaCrudTests(TestCase):
    def test_categoria_create_and_list(self):
        response = self.client.post(reverse('create_categoria'), {'Categoria': 'Eletrônicos'})

        self.assertRedirects(response, reverse('categoria'))
        self.assertTrue(Categoria.objects.filter(Categoria='Eletrônicos').exists())

        list_response = self.client.get(reverse('categoria'))
        self.assertContains(list_response, 'Eletrônicos')


class FabricanteCrudTests(TestCase):
    def test_fabricante_create_and_list(self):
        response = self.client.post(reverse('create_fabricante'), {'Fabricante': 'Dell'})

        self.assertRedirects(response, reverse('fabricante'))
        self.assertTrue(Fabricante.objects.filter(Fabricante='Dell').exists())
