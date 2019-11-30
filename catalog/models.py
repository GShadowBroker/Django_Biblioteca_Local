from django.db import models
from django.urls import reverse
import uuid
from django.contrib.auth.models import User
from datetime import date

# Create your models here.
class Gênero(models.Model):
    nome = models.CharField(max_length=200, help_text='Insira um gênero (ex. Ficção científica).')

    def __str__(self):
        return self.nome

class Idioma(models.Model):
    nome = models.CharField(max_length=100, help_text='Insira o idioma da versão (ex. Francês, Inglês, Japonês).')

    def __str__(self):
        return self.nome

class Livro(models.Model):
    título = models.CharField(max_length=200, help_text='Insira o título.')
    autor = models.ForeignKey('autor', help_text='Insira o autor.', on_delete=models.SET_NULL, null=True)
    resumo = models.TextField(max_length=1000, help_text='Insira a descrição do título.')
    isbn = models.CharField('ISBN', max_length=13, help_text='<a href="http://www.isbn.bn.br/website/" target="_blank">Número do ISBN</a> de 13 caractéres.')
    gênero = models.ManyToManyField(Gênero, help_text='Insira o gênero do livro.')
    data_de_publicação = models.DateField(auto_now_add=True)

    def mostrar_gênero(self):
        """Cria um string pro gênero do livro. Requerido porque
        'gênero' é um campo ManyToMany e portanto não aceito."""
        return ', '.join(gênero.nome for gênero in self.gênero.all()[:3])

    mostrar_gênero.descrição_curta = 'Gênero'

    def __str__(self):
        return self.título

    def get_absolute_url(self):
        return reverse('detalhe-livro', args=[str(self.id)])

    class Meta:
        ordering = ['título', '-data_de_publicação']

class LivroInstância(models.Model):
    id = models.UUIDField(primary_key=True, default = uuid.uuid4, help_text='ID do livro nesta biblioteca.')
    livro = models.ForeignKey('Livro', on_delete=models.SET_NULL, null=True)
    impressão = models.CharField(max_length=200)
    data_de_devolução = models.DateField(null=True, blank=True)
    idioma = models.ManyToManyField(Idioma, help_text="Insira o idioma do livro.")
    locatário = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    @property
    def is_overdue(self):
        if self.data_de_devolução and date.today() > self.data_de_devolução:
            return True
        return False

    ESTADO_EMPRÉSTIMO = (
        ('m', 'Manutenção'),
        ('e', 'Emprestado'),
        ('d', 'Disponível'),
        ('r', 'Reservado'),
    )

    estado = models.CharField(max_length=1, choices=ESTADO_EMPRÉSTIMO, blank=True, default='m', help_text='Disponibilidade do título')

    class Meta:
        ordering = ['data_de_devolução']
        permissions = (("can_mark_returned", "Set book as returned"),("can_renew", "Can set the data_de_devolução"),("can_edit_content", "Can create, update and delete content"),)
    
    def __str__(self):
        return f"{self.id}: {self.livro.título}"

class Autor(models.Model):
    nome = models.CharField(max_length=100)
    sobrenome = models.CharField(max_length=100)
    nascimento = models.DateField(null=True, blank=True)
    morte = models.DateField(null=True, blank=True)

    class Meta:
        ordering = ['sobrenome', 'nome']

    # def get_absolute_url(self):
    #     return reverse('detalhe-autor', args=[{str(self.id)}]) # QUE ISSO SIRVA DE EXEMPLO FDP! PRESTENÇÃO!
    def get_absolute_url(self):
        """Returns the url to access a particular author instance."""
        return reverse('detalhe-autor', args=[str(self.id)])

    def __str__(self):
        return f"{self.sobrenome}, {self.nome}"
