from django.contrib import admin
from .models import Autor, Gênero, Livro, LivroInstância, Idioma

# Register your models here.

class LivrosInstânciaInline(admin.TabularInline):
    model = LivroInstância
    extra = 0

# admin.site.register(Livro)
@admin.register(Livro)
class LivroAdmin(admin.ModelAdmin):
    list_display = ('título', 'autor', 'mostrar_gênero')
    inlines = [LivrosInstânciaInline]

# admin.site.register(Autor)
class LivroInline(admin.TabularInline):
    model = Livro
    extra = 0

class AutorAdmin(admin.ModelAdmin):
    list_display = ('nome', 'sobrenome', 'nascimento', 'morte')
    fields = ['nome', 'sobrenome', ('nascimento', 'morte')]
    inlines = [LivroInline]
admin.site.register(Autor, AutorAdmin)


admin.site.register(Gênero)

admin.site.register(Idioma)

# admin.site.register(LivroInstância)
@admin.register(LivroInstância)
class LivroInstânciaAdmin(admin.ModelAdmin):
    list_display = ('livro', 'estado', 'locatário', 'data_de_devolução')
    list_filter = ('estado', 'data_de_devolução')
    fieldsets = (
        (None, {
            'fields': ('livro', 'impressão', 'id')
        }),
        ('Disponibilidade', {
            'fields': ('estado', 'data_de_devolução', 'locatário')
        }),
    )


