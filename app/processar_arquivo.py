import pandas as pd
from sqlalchemy.orm import Session

from . import crud, schemas


def processar_csv(file_path: str, db: Session):
    """Processa um arquivo CSV e insere os dados no banco de dados.

    Args:
        file_path (str): Caminho para o arquivo CSV.
        db (Session): Sessão do banco de dados.
    """
    try:
        df = pd.read_csv(file_path, delimiter=';', encoding='latin1')
        df = df.fillna('no')
        for _, row in df.iterrows():
            filmes_dados = schemas.CriarFilme(
                title=row['title'],
                year=row['year'],
                studios=row['studios'],
                producers=row['producers'],
                winner=row['winner']
            )
            filme_existente = crud.obter_filme_por_titulo(
                db, title=filmes_dados.title)
            if filme_existente is None:
                crud.criar_filme(db, filmes_dados)
        db.commit()
    except Exception as e:
        print(f"Erro ao processar o arquivo CSV: {e}")
        raise
