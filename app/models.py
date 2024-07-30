from sqlalchemy import Column, Integer, String

from .conexao_banco_dados import Base


class Filme(Base):
    """Modelo que representa um filme no banco de dados."""
    __tablename__ = "filmes"

    id = Column(Integer, primary_key=True, index=True)
    year = Column(Integer, index=True)
    title = Column(String, unique=True, index=True, nullable=False)
    studios = Column(String, index=True)
    producers = Column(String, index=True)
    winner = Column(String, index=True)
