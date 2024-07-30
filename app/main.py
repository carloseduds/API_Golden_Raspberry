import os
import shutil
from collections import defaultdict

from dotenv import load_dotenv
from fastapi import Depends, FastAPI, File, HTTPException, UploadFile
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .conexao_banco_dados import SessionLocal, engine
from .processar_arquivo import processar_csv

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

load_dotenv()

DEFAULT_CSV_FILE_PATH = os.getenv("CSV_FILE_PATH")


def obter_db():
    """Obtém uma sessão de banco de dados."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.on_event("startup")
def startup_event():
    """Evento de inicialização do aplicativo."""
    if os.path.exists(DEFAULT_CSV_FILE_PATH):
        db = SessionLocal()
        processar_csv(DEFAULT_CSV_FILE_PATH, db)
        db.close()
    else:
        print(
            f"Arquivo {DEFAULT_CSV_FILE_PATH} não encontrado. Esperando upload...")


@app.post("/uploadarquivo/")
async def upload_arquivo(file: UploadFile = File(...),
                         db: Session = Depends(obter_db)):
    """Endpoint para upload de arquivos CSV."""
    try:
        temp_file_path = "tmp/uploaded_file.csv"
        with open(temp_file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        processar_csv(temp_file_path, db)
        os.remove(temp_file_path)

        return {"message": "Arquivo processado com sucesso."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/filmes/", response_model=list[schemas.Filme])
def ler_filmes(skip: int = 0, limit: int = 100,
               db: Session = Depends(obter_db)):
    """Endpoint para obter uma lista de filmes."""
    filmes = crud.obter_filmes(db, skip=skip, limit=limit)
    return filmes


@app.get("/vencedores/intervalos/")
def ler_intervalos_premios(db: Session = Depends(obter_db)):
    """Endpoint para obter intervalos de prêmios entre vitórias."""
    filmes = db.query(models.Filme).filter(models.Filme.winner == "yes").all()
    producers_dict = defaultdict(list)

    for filme in filmes:
        producers = [producer.strip()
                     for producer in filme.producers.split(",")]
        for producer in producers:
            producers_dict[producer].append(filme.year)

    intervalos = [
        {
            "producer": producer,
            "interval": sorted_years[i + 1] - sorted_years[i],
            "previousWin": sorted_years[i],
            "followingWin": sorted_years[i + 1]
        }
        for producer, years in producers_dict.items() if len(years) > 1
        for sorted_years in [sorted(years)]
        for i in range(len(sorted_years) - 1)
    ]

    min_intervalo = min(intervalos, key=lambda x: x['interval'])
    max_intervalo = max(intervalos, key=lambda x: x['interval'])

    return {
        "min": [min_intervalo],
        "max": [max_intervalo]
    }
