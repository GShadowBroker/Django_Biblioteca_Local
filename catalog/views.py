from django.shortcuts import render, get_object_or_404, redirect
from .models import Gênero, Idioma, Livro, LivroInstância, Autor
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

# Create your views here.

# @login_required ---> to restrict access to logged users on view functions
def index(request):

    num_livros = Livro.objects.all().count()
    num_instâncias = LivroInstância.objects.all().count()
    num_instâncias_disponíveis = LivroInstância.objects.filter(estado__exact='d').count() #Livros disponíveis (estado == 'd')
    num_autores = Autor.objects.all().count()
    num_gêneros = Gênero.objects.all().count()
    num_livros_maionese = Livro.objects.filter(título__icontains='maionese').count()
    num_visitas = request.session.get('num_visitas', 0)

    request.session['num_visitas'] = num_visitas + 1

    context = {
        'num_livros': num_livros,
        'num_instâncias': num_instâncias,
        'num_instâncias_disponíveis': num_instâncias_disponíveis,
        'num_autores': num_autores,
        'num_gêneros': num_gêneros,
        'num_livros_maionese': num_livros_maionese,
        'num_visitas': num_visitas,
    }

    return render(request, 'index.html', context=context) # Context is a python dictionary {} containing the date to insert into the template

# def lista_de_livros(request):
#     lista_de_livros = Livro.objects.all()
#     return render(request, 'lista_de_livros.html', {'lista_de_livros' : lista_de_livros})
class ListaDeLivros(LoginRequiredMixin, generic.ListView):
    model = Livro
    paginate_by = 10
    
class DetalhesDoLivro(LoginRequiredMixin, generic.DetailView):
    model = Livro

class ListaDeAutores(LoginRequiredMixin, generic.ListView):
    model = Autor
    paginate_by = 10

class DetalhesDoAutor(LoginRequiredMixin, generic.DetailView):
    model = Autor

class LivrosEmprestadosAoUsuário(LoginRequiredMixin, generic.ListView):
    model = LivroInstância
    template_name = 'catalog/livroinstância_lista_emprestado_usuário.html'
    paginate_by = 10

    def get_queryset(self):
        return LivroInstância.objects.filter(locatário=self.request.user).filter(estado__exact='e').order_by('data_de_devolução')

class LivrosEmprestados(LoginRequiredMixin, PermissionRequiredMixin, generic.ListView):
    permission_required = 'catalog.can_mark_returned'
    model = LivroInstância
    template_name = 'catalog/livroinstância_lista_emprestado.html'
    paginate_by = 10

    def get_queryset(self):
        return LivroInstância.objects.filter(estado__exact='e').order_by('data_de_devolução')

###############################################################################################################################
from django.contrib.auth.decorators import permission_required
from django.http import HttpResponseRedirect
from django.urls import reverse
from .forms import RenovarLivroForm # Import from forms
import datetime

@permission_required("catalog.can_renew")
def renovar_livro(request, pk):
    livro_instância = get_object_or_404(LivroInstância, pk=pk)

    if request.method == 'POST': # If this is a POST request then process the Form data
        form = RenovarLivroForm(request.POST) # Create a form instance and populate it with data from the request (binding)

        if form.is_valid():
            # process the data in form.cleaned_data as required (here we just write it to the model due_back field)
            # livro_instância.data_de_devolução = form.cleaned_data['data_de_renovação']
            livro_instância.data_de_devolução = form.cleaned_data['data_de_devolução']
            livro_instância.save()

            return HttpResponseRedirect(reverse("todos-emprestados")) # redirect to a new URL (reverse() is the python equivalent to the url tag)

    # If this is a GET (or any other method) create the default form.
    else:
        data_de_renovação_proposta = datetime.date.today() + datetime.timedelta(weeks=3)
        # form = RenovarLivroForm(initial={'data_de_renovação': data_de_renovação_proposta})
        form = RenovarLivroForm(initial={'data_de_devolução': data_de_renovação_proposta})

    context = {
        'form': form,
        'livro_instância': livro_instância,
    }

    return render(request, 'catalog/renovar.html', context)

#######################################################  EDIÇÃO DE AUTORES  ############################################################3

from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

class AutorCreate(PermissionRequiredMixin, CreateView):
    permission_required = 'catalog.can_edit_content'
    model = Autor
    fields = '__all__'
    initial = {'morte': '29/11/2019'}
    template_name_suffix = '_formulário' # o nome padrão do HTML é 'nome_do_meu_modelo'_form.html. template_name_suffix é usado para mudar isso.

class AutorUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = 'catalog.can_edit_content'
    model = Autor
    fields = ['nome','sobrenome','nascimento','morte'] # same as '__all__', but lengthier.
    template_name_suffix = '_formulário'

class AutorDelete(PermissionRequiredMixin, DeleteView):
    permission_required = 'catalog.can_edit_content'
    model = Autor
    success_url = reverse_lazy('autores')
    template_name_suffix = '_confirmar_exclusão'

################## FERRAMENTAS ADMINISTRATIVAS #####################

@permission_required('catalog.can_edit_content')
def ferramentas(request):
    context = {}
    return render(request, 'ferramentas.html', context=context)

############################################ EDIÇÃO LIVROS #############################################################

class LivroCreate(PermissionRequiredMixin, CreateView):
    permission_required = "catalog.can_edit_content"
    model = LivroInstância
    fields = "__all__"
    template_name_suffix = "_formulário"

class LivroUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = "catalog.can_edit_content"
    model = LivroInstância
    fields = "__all__"
    template_name_suffix = "_formulário"

class LivroDelete(PermissionRequiredMixin, DeleteView):
    permission_required = "catalog.can_edit_content"
    model = LivroInstância
    success_url = reverse_lazy('livros')
    template_name_suffix = "_confirmar_exclusão"
