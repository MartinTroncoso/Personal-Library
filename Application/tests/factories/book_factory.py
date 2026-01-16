import factory
from Application.models import Libro


class BookFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Libro

    titulo = factory.Faker("sentence", nb_words=3)
    autores = factory.Faker("name")

    # We use post_generation because it's a ManyToMany relation
    @factory.post_generation
    def usuario(self, create, extracted, **kwargs):  # type: ignore
        if not create:
            return

        if extracted:
            self.usuario.add(extracted)
