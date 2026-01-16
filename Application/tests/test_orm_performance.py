import pytest
from django.db import connection
from Application.models import Libro
from Application.tests.factories.book_factory import BookFactory
from Application.tests.factories.user_factory import UserFactory


@pytest.mark.django_db
def test_select_related_reduces_queries() -> None:
    user = UserFactory()
    books = BookFactory.create_batch(5, usuario=user)

    # Without optimization
    with connection.cursor():
        # We take how many queries had been executed first
        # connection.queries only works when 'DEBUG = True'
        initial_queries = len(connection.queries)

        books = Libro.objects.all()
        for book in books:
            _ = book.usuario

        queries_without = len(connection.queries) - initial_queries

    # With prefetch_related
    with connection.cursor():
        initial_queries = len(connection.queries)

        books = Libro.objects.prefetch_related("usuario").all()
        for book in books:
            _ = book.usuario

        queries_with = len(connection.queries) - initial_queries

    assert queries_with >= queries_without
