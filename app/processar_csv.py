import pandas as pd

from . import crud
from .decorators import log_execution


class CSVProcessError(Exception):
    pass


@log_execution
def processar_csv(file_path: str):
    """
    Processa um arquivo CSV e insere os dados no banco de dados.

    Args:
        file_path (str): Caminho para o arquivo CSV.
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
    except FileNotFoundError as e:
        raise CSVProcessError(f"Arquivo não encontrado: {str(e)}") from e
    except pd.errors.EmptyDataError as e:
        raise CSVProcessError(f"Arquivo CSV vazio: {str(e)}") from e
    except pd.errors.ParserError as e:
        raise CSVProcessError(f"Erro ao analisar o CSV: {str(e)}") from e
    except Exception as e:
        raise CSVProcessError(f"Erro ao processar o CSV: {str(e)}") from e
