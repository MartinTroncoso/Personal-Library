import random

import requests
from celery import shared_task
from django.utils.timezone import now

from .models import LibroDelDia


@shared_task
def libro_del_dia():
    letras = "abcdefghijklmnopqrstuvwxyz"
    letra_aleatoria = random.choice(letras)

    url = "https://www.googleapis.com/books/v1/volumes"
    params = {
        "q": letra_aleatoria,
        "maxResults": 40,
        "startIndex": random.randint(0, 100),
    }

    response = requests.get(url, params=params)
    data = response.json()

    if "items" not in data:
        return "❌ No books were found"

    libros_validos = [
        item
        for item in data["items"]
        if item.get("accessInfo", {}).get("viewability") != "NO_PAGES"
        and item.get("volumeInfo", {}).get("description") is not None
        and item.get("volumeInfo", {}).get("subtitle") is not None
    ]

    while not libros_validos:
        letra_aleatoria = random.choice(letras.replace(letra_aleatoria, "", 1))
        params["q"] = letra_aleatoria
        response = requests.get(url, params=params)
        data = response.json()
        if "items" not in data:
            return "❌ No books were found"
        
        libros_validos = [
            item
            for item in data["items"]
            if item.get("accessInfo", {}).get("viewability") != "NO_PAGES"
            and item.get("volumeInfo", {}).get("description") is not None
            and item.get("volumeInfo", {}).get("subtitle") is not None
        ]

    if not libros_validos:
        return "❌ No books with visible pages were found"

    LibroDelDia.objects.all().delete()  # Limpiar la tabla antes de guardar un nuevo libro

    libro = random.choice(libros_validos)

    volumeInfo = libro.get("volumeInfo", {})
    accessInfo = libro.get("accessInfo", {})

    # Guardarlo en la base de datos
    LibroDelDia.objects.create(
        titulo=volumeInfo.get("title"),
        subtitulo=volumeInfo.get("subtitle"),
        descripcion=volumeInfo.get("description"),
        autores=", ".join(volumeInfo.get("authors", [])),
        fecha=now(),
        portada=volumeInfo.get("imageLinks", {}).get("thumbnail"),
        visibilidad=accessInfo.get("viewability", "UNKNOWN"),
        link_lectura=volumeInfo.get("infoLink"),
    )

    return f"✅ Book saved: {volumeInfo.get('title')}, description: {volumeInfo.get('description')}, subtitle: {volumeInfo.get('subtitle')}"
