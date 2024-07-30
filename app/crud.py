from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from . import models, schemas


def obter_filmes(db: Session, skip: int = 0, limit: int = 100):
    """Retorna uma lista de filmes com paginação.

    Args:
        db (Session): Sessão do banco de dados.
        skip (int): Número de registros para pular.
        limit (int): Número máximo de registros para retornar.

    Returns:
        list: Lista de filmes.
    """
    return db.query(models.Filme).offset(skip).limit(limit).all()


def criar_filme(db: Session, filme: schemas.CriarFilme):
    """Cria um novo filme no banco de dados.

    Args:
        db (Session): Sessão do banco de dados.
        filme (schemas.MovieCreate): Esquema do filme a ser criado.

    Returns:
        models.Filme: Filme criado.
    """
    db_filme = models.Filme(
        title=filme.title,
        year=filme.year,
        studios=filme.studios,
        producers=filme.producers,
        winner=filme.winner
    )
    try:
        db.add(db_filme)
        db.commit()
        db.refresh(db_filme)
    except IntegrityError:
        db.rollback()
        db_filme = db.query(models.Filme).filter(
            models.Filme.title == filme.title).first()
    return db_filme


def obter_filme_por_titulo(db: Session, title: str):
    """Obtém um filme pelo título.

    Args:
        db (Session): Sessão do banco de dados.
        title (str): Título do filme.

    Returns:
        models.Filme: Filme encontrado.
    """
    return db.query(models.Filme).filter(models.Filme.title == title).first()
