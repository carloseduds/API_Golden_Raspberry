from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view

from .service.logs import log_execution
from .service.processar_endpoint import (procesar_upload, processar_filmes,
                                         processar_intervalo)


@log_execution
@csrf_exempt
@api_view(['POST'])
def upload_arquivo(request):
    return procesar_upload(request)


@log_execution
def ler_filmes(request):
    return processar_filmes(request)


@log_execution
def ler_intervalos_premios(request):
    return processar_intervalo()
