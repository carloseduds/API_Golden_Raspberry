import os
import re
from collections import defaultdict

from django.http import JsonResponse
from dotenv import load_dotenv
from rest_framework import status
from rest_framework.response import Response

from ..models import Filme
from . import crud
from .logs import log_execution
from .processar_arquivo import CSVProcessError, processar_csv

load_dotenv()


@log_execution
def processar_intervalo():
    try:
        filmes = Filme.objects.filter(
            winner="yes").prefetch_related('producers')
        producers_dict = defaultdict(list)

        for filme in filmes:
            for produtor in filme.producers.all():
                producers_dict[produtor.name].append(filme.year)

        intervalos = [
            {
                "producer": produtor,
                "interval": sorted_years[i + 1] - sorted_years[i],
                "previousWin": sorted_years[i],
                "followingWin": sorted_years[i + 1]
            }
            for produtor, years in producers_dict.items() if len(years) > 1
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


@log_execution
def processar_filmes(request):
    """Função para obter uma lista de filmes, incluindo produtores e estúdios."""
    try:
        skip = int(request.GET.get('skip', 0))
        limit = int(request.GET.get('limit', 100))
        filmes = Filme.objects.all().prefetch_related(
            'producers', 'studios')[skip:skip+limit]

        filmes_data = [
            {
                "id": filme.id,
                "titulo": filme.title,
                "ano": filme.year,
                "vencedor": filme.winner,
                "produtores": [produtor.name for produtor in filme.producers.all()],
                "estudios": [estudio.name for estudio in filme.studios.all()]
            }
            for filme in filmes
        ]

        return JsonResponse(filmes_data, safe=False)
    except ValueError as e:
        return JsonResponse({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@log_execution
def procesar_upload(request):
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
    except CSVProcessError as e:
        return JsonResponse({"error": str(e)},
                            status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return JsonResponse({"error": str(e)},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
