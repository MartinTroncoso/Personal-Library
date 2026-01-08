from .models import Libro, LibroDelDia


def book_has_been_saved_by_someone(book: Libro | LibroDelDia) -> bool:
    return Libro.objects.filter(
        titulo=book.titulo, subtitulo=book.subtitulo, autores=book.autores
    ).exists()


def book_has_not_been_saved_by_current_user(id: int, book: Libro | LibroDelDia) -> bool:
    return id not in Libro.objects.get(
        titulo=book.titulo, subtitulo=book.subtitulo, autores=book.autores
    ).usuario.values_list("id", flat=True)
