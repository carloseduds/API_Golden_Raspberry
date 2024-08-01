import os

from django.db.models.signals import post_migrate
from django.dispatch import receiver

from .processar_csv import processar_csv


@receiver(post_migrate)
def checar_arquivo_csv(sender, **kwargs):
    """
    Verifica a existência de um arquivo CSV padrão e o processa se encontrado.
    """
    DEFAULT_CSV_FILE_PATH = os.getenv('CSV_FILE_PATH')
    if DEFAULT_CSV_FILE_PATH and os.path.exists(DEFAULT_CSV_FILE_PATH):
        try:
            processar_csv(DEFAULT_CSV_FILE_PATH)
            print("Arquivo processado com sucesso.")
        except Exception as e:
            print(f"Erro ao processar o arquivo CSV: {str(e)}")
    else:
        print(
            f"Arquivo {DEFAULT_CSV_FILE_PATH} não encontrado. Esperando upload...")
