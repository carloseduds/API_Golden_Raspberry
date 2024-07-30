import os

import pytest
import requests
from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.getenv("BASE_URL")


def teste_obter_produtores_ganhadores():
    """Teste para verificar os intervalos de prêmios dos produtores."""
    response = requests.get(f"{BASE_URL}/vencedores/intervalos/")
    assert response.status_code == 200

    data = response.json()
    assert "min" in data
    assert "max" in data

    for interval in data["min"]:
        assert "producer" in interval
        assert "interval" in interval
        assert "previousWin" in interval
        assert "followingWin" in interval

    for interval in data["max"]:
        assert "producer" in interval
        assert "interval" in interval
        assert "previousWin" in interval
        assert "followingWin" in interval
