import pandas as pd
from django.http import JsonResponse
from rest_framework import status

from . import crud


def processar_csv(file_path: str):
    """
    Processa um arquivo CSV e insere os dados no banco de dados.

    Args:
        file_path (str): Caminho para o arquivo CSV.

    Returns:
        JsonResponse: Mensagem de sucesso ou erro.
    """
    try:
        df = pd.read_csv(file_path, delimiter=';', encoding='latin1')
        df = df.fillna('no')
        for _, row in df.iterrows():
            filme_dados = {
                'title': row['title'],
                'year': row['year'],
                'studios': row['studios'],
                'producers': row['producers'],
                'winner': row['winner']
            }
            filme_existente = crud.obter_filme_por_titulo(filme_dados['title'])
            if filme_existente is None:
                crud.criar_filme(filme_dados)
        return JsonResponse({"message": "Arquivo processado com sucesso."},
                            status=status.HTTP_200_OK)
    except FileNotFoundError as e:
        return JsonResponse({"error": f"Arquivo não encontrado: {str(e)}"},
                            status=status.HTTP_404_NOT_FOUND)
    except pd.errors.EmptyDataError as e:
        return JsonResponse({"error": f"Arquivo CSV vazio: {str(e)}"},
                            status=status.HTTP_400_BAD_REQUEST)
    except pd.errors.ParserError as e:
        return JsonResponse({"error": f"Erro ao analisar o CSV: {str(e)}"},
                            status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return JsonResponse({"error": f"Erro ao processar o CSV: {str(e)}"},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
