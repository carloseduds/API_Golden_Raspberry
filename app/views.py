import os
import re
from collections import defaultdict

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from dotenv import load_dotenv
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from . import crud
from .models import Filme
from .processar_csv import processar_csv

load_dotenv()


@csrf_exempt
@api_view(['POST'])
def upload_arquivo(request):
    """Endpoint para upload de arquivos CSV."""
    try:
        file = request.FILES['file']
        temp_file_path = os.getenv('CSV_TEMP_FILE_PATH')
        if not temp_file_path:
            raise ValueError(
                "CSV_TEMP_FILE_PATH não está definido nas variáveis de ambiente.")

        with open(temp_file_path, "wb") as buffer:
            for chunk in file.chunks():
                buffer.write(chunk)

        processar_csv(temp_file_path)
        os.remove(temp_file_path)

        return Response({"message": "Arquivo processado com sucesso."})
    except KeyError as e:
        return JsonResponse({"error": str(e)},
                            status=status.HTTP_400_BAD_REQUEST)
    except ValueError as e:
        return JsonResponse({"error": str(e)},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    except Exception as e:
        return JsonResponse({"error": str(e)},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


def ler_filmes(request):
    """Endpoint para obter uma lista de filmes."""
    try:
        skip = int(request.GET.get('skip', 0))
        limit = int(request.GET.get('limit', 100))
        filmes = crud.obter_filmes(skip=skip, limit=limit)
        return JsonResponse(list(filmes.values()), safe=False)
    except ValueError as e:
        return JsonResponse({"error": str(e)},
                            status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return JsonResponse({"error": str(e)},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


def ler_intervalos_premios(request):
    """Endpoint para obter intervalos de prêmios entre vitórias."""
    try:
        filmes = Filme.objects.filter(winner="yes")
        producers_dict = defaultdict(list)

        for filme in filmes:
            producers = [producer.strip() for producer in re.split(
                r',\s*and\s*|,\s*|\s*and\s*', filme.producers)]
            for producer in producers:
                producers_dict[producer].append(filme.year)

        intervalos = [
            {
                "producer": producer,
                "interval": sorted_years[i + 1] - sorted_years[i],
                "previousWin": sorted_years[i],
                "followingWin": sorted_years[i + 1]
            }
            for producer, years in producers_dict.items() if len(years) > 1
            for sorted_years in [sorted(years)]
            for i in range(len(sorted_years) - 1)
        ]

        min_intervalo = min(intervalos, key=lambda x: x['interval'])
        max_intervalo = max(intervalos, key=lambda x: x['interval'])

        return JsonResponse({
            "min": [min_intervalo],
            "max": [max_intervalo]
        })
    except Exception as e:
        return JsonResponse({"error": str(e)},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
