from pydantic import BaseModel


class BaseFilme(BaseModel):
    """Esquema base para um filme."""
    year: int
    title: str
    studios: str
    producers: str
    winner: str


class CriarFilme(BaseFilme):
    """Esquema para criação de um novo filme, herdando de MovieBase."""
    pass


class Filme(BaseFilme):
    """Esquema para um filme com ID, herdando de MovieBase."""
    id: int

    class Config:
        """Configurações adicionais para Pydantic."""
        orm_mode = True
