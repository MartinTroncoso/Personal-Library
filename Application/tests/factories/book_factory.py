import factory
from Application.models import Libro
from Application.tests.factories.user_factory import UserFactory


class LibroFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Libro

    title = factory.Faker("sentence", nb_words=3)
    author = factory.Faker("name")
    owner = factory.SubFactory(UserFactory)  # It creates the user automatically
