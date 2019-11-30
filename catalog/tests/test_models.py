from django.test import TestCase

from catalog.models import Autor

class AuthorModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        Autor.objects.create(nome='Big', sobrenome='Bob')

    def test_first_name_label(self):
        author = Autor.objects.get(id=1)
        field_label = author._meta.get_field('nome').verbose_name
        self.assertEquals(field_label, 'nome')

    def test_date_of_death_label(self):
        author=Autor.objects.get(id=1)
        field_label = author._meta.get_field('nascimento').verbose_name
        self.assertEquals(field_label, 'died')

    def test_first_name_max_length(self):
        author = Autor.objects.get(id=1)
        max_length = author._meta.get_field('nome').max_length
        self.assertEquals(max_length, 100)

    def test_object_name_is_last_name_comma_first_name(self):
        author = Autor.objects.get(id=1)
        expected_object_name = f'{author.nome}, {author.sobrenome}'
        self.assertEquals(expected_object_name, str(author))

    def test_get_absolute_url(self):
        author = Autor.objects.get(id=1)
        # This will also fail if the urlconf is not defined.
        self.assertEquals(author.get_absolute_url(), '/catalog/autor/1')