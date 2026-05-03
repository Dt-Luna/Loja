from django.contrib import admin

# Register your models here.
from .models import * #imporata nossos models
admin.site.register(Fabricante, FabricanteAdmin)
admin.site.register(Categoria, CategoriaAdmin)
admin.site.register(Produto, ProdutoAdmin)

class FabricanteAdmin(admin.ModelAdmin):
# Cria um filtro de hierarquia com datas
    date_hierarchy = 'criado_em'

class ProdutoAdmin(admin.ModelAdmin):
# Cria um filtro de hierarquia com datas
    date_hierarchy = 'criado_em'
    list_display = ('Produto', 'destaque', 'promocao', 'msgPromocao', 'preco', 'categoria')
    empty_value_display = 'Vazio'