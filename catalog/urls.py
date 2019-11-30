from django.contrib import admin
from django.urls import path, include, re_path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    # path('lista_de_livros/', views.lista_de_livros, name="lista_de_livros"),
    path('livros/', views.ListaDeLivros.as_view(), name="livros"),
    re_path(r'^livro/(?P<pk>\d+)$', views.DetalhesDoLivro.as_view(), name="detalhe-livro"),
    path('autores/', views.ListaDeAutores.as_view(), name="autores"),
    re_path(r'^autor/(?P<pk>\d+)$', views.DetalhesDoAutor.as_view(), name="detalhe-autor"),
    path('meuslivros/', views.LivrosEmprestadosAoUsuário.as_view(), name="meus-emprestados"),
    path('livrosemprestados', views.LivrosEmprestados.as_view(), name="todos-emprestados"),
    path('livro/<uuid:pk>/renovar/', views.renovar_livro, name="renovar-livro"),

    path('autor/criar/', views.AutorCreate.as_view(), name="criar-autor"),
    path('autor/<int:pk>/atualizar/', views.AutorUpdate.as_view(), name="atualizar-autor"),
    path('autor/<int:pk>/excluir/', views.AutorDelete.as_view(), name="excluir-autor"),

    path('ferramentas/', views.ferramentas, name="ferramentas"),

    path('livro/criar/', views.LivroCreate.as_view(), name="criar-livro"),
    re_path(r'^livro/(?P<pk>[a-zA-Z0-9-]+)/atualizar/', views.LivroUpdate.as_view(), name="atualizar-livro"), # using regular expressions to find the uuid
    re_path(r'^livro/(?P<pk>[a-zA-Z0-9-]+)/excluir/', views.LivroDelete.as_view(), name="excluir-livro"),

]