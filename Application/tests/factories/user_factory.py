import factory
from Application.models import Usuario


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Usuario

    username = factory.Sequence(
        lambda n: f"user{n}"
    )  # There is no collision between users
    email = factory.LazyAttribute(lambda o: f"{o.username}@example.com")
    password = factory.PostGenerationMethodCall(
        "set_password", "password123"
    )  # Real HASH
