from django.db import IntegrityError
from django.http import JsonResponse
from rest_framework import status

from .models import Filme


def obter_filmes(skip: int = 0, limit: int = 100):
    """
    Retorna uma lista de filmes com paginação.

    Args:
        skip (int): Número de registros para pular.
        limit (int): Número máximo de registros para retornar.

    Returns:
        QuerySet: Lista de filmes.
    """
    try:
        return Filme.objects.all()[skip:skip + limit]
    except Exception as e:
        return JsonResponse({"error": str(e)},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


def criar_filme(filme):
    """
    Cria um novo filme no banco de dados.

    Args:
        filme (dict): Dicionário com os dados do filme a ser criado.

    Returns:
        Filme: Filme criado ou o primeiro filme encontrado com o mesmo título.
    """
    try:
        db_filme = Filme.objects.create(
            title=filme['title'],
            year=filme['year'],
            studios=filme['studios'],
            producers=filme['producers'],
            winner=filme['winner']
        )
    except IntegrityError as e:
        return JsonResponse({"error": str(e)},
                            status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return JsonResponse({"error": str(e)},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    return db_filme


def obter_filme_por_titulo(title: str):
    """
    Obtém um filme pelo título.

    Args:
        title (str): Título do filme.

    Returns:
        Filme: Filme encontrado ou None se não encontrado.
    """
    try:
        return Filme.objects.filter(title=title).first()
    except Exception as e:
        return JsonResponse({"error": str(e)},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
