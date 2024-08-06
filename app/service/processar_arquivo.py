import re

import pandas as pd
from django.db import transaction

from ..models import Estudio, Filme, Produtor


class CSVProcessError(Exception):
    pass


def processar_csv(caminho_arquivo: str):
    try:
        dados = pd.read_csv(caminho_arquivo, delimiter=';', encoding='latin1')
        dados = dados.fillna('no')
        with transaction.atomic():
            for _, linha in dados.iterrows():
                # Criar ou obter os estúdios e produtores
                objetos_estudio = []
                for nome_estudio in linha['studios'].split(','):
                    objeto_estudio, _ = Estudio.objects.get_or_create(
                        name=nome_estudio.strip())
                    objetos_estudio.append(objeto_estudio)

                objetos_produtor = []
                nomes_produtor = re.split(
                    r',\s*and\s*|,\s*|\s*and\s*', linha['producers'])
                for nome_produtor in nomes_produtor:
                    if nome_produtor:
                        objeto_produtor, _ = Produtor.objects.get_or_create(
                            name=nome_produtor.strip())
                        objetos_produtor.append(objeto_produtor)

                # Criar ou obter o filme
                filme, _ = Filme.objects.get_or_create(
                    title=linha['title'],
                    year=linha['year'],
                    winner='yes' if linha['winner'].strip(
                    ).lower() == 'yes' else 'no'
                )

                # Associar estúdios e produtores ao filme
                filme.studios.set(objetos_estudio)
                filme.producers.set(objetos_produtor)
                filme.save()

    except FileNotFoundError as e:
        raise Exception(f"Arquivo não encontrado: {str(e)}") from e
    except pd.errors.EmptyDataError as e:
        raise Exception(f"Arquivo CSV vazio: {str(e)}") from e
    except pd.errors.ParserError as e:
        raise Exception(f"Erro ao analisar o CSV: {str(e)}") from e
    except Exception as e:
        raise Exception(f"Erro ao processar o CSV: {str(e)}") from e
