# mypy: ignore-errors

import random

import requests
from celery import shared_task
from django.utils.timezone import now

from .models import LibroDelDia


API_URL = "https://www.googleapis.com/books/v1/volumes"
LETTERS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"


@shared_task
def libro_del_dia() -> str:
    MAX_TRIES = 5
    valid_books = []

    for _ in range(MAX_TRIES):
        letra = random.choice(LETTERS)
        params = {
            "q": letra,
            "maxResults": 40,
            "startIndex": random.randint(0, 100),
        }

        response = requests.get(
            API_URL, params=params, timeout=5
        )  # request.get will throw an exception only due to network issues

        try:
            response.raise_for_status()
            data = response.json()
        except requests.exceptions.RequestException as e:
            return f"❌ Error requesting API: {e}"

        items = data.get("items", [])
        if not items:
            continue

        valid_books = [
            item
            for item in items
            if item.get("accessInfo", {}).get("viewability") != "NO_PAGES"
            and item.get("volumeInfo", {}).get("description")
        ]

        if valid_books:
            break

    if not valid_books:
        return "❌ No valid books found after multiple attempts"

    # Delete previous and save new book
    LibroDelDia.objects.all().delete()

    libro = random.choice(valid_books)
    volume = libro.get("volumeInfo", {})
    access = libro.get("accessInfo", {})

    LibroDelDia.objects.create(
        titulo=volume.get("title"),
        subtitulo=volume.get("subtitle"),
        descripcion=volume.get("description"),
        autores=", ".join(volume.get("authors", [])),
        fecha=now(),
        portada=volume.get("imageLinks", {}).get("thumbnail"),
        visibilidad=access.get("viewability", "UNKNOWN"),
        link_lectura=volume.get("infoLink"),
    )

    return f"✅ Book saved: {volume.get('title')}"
