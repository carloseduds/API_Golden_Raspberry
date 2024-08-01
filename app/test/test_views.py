import pytest
from django.urls import reverse
from rest_framework.test import APIClient

from app.models import Filme


@pytest.mark.django_db
def test_obter_produtores_ganhadores():
    """Teste para verificar os intervalos de prêmios dos produtores."""

    # Adicionar dados de teste
    Filme.objects.create(
        title='Filme 1',
        year=2000,
        studios='Studio 1',
        producers='Producer 1',
        winner='yes'
    )
    Filme.objects.create(
        title='Filme 2',
        year=2002,
        studios='Studio 2',
        producers='Producer 1',
        winner='yes'
    )
    Filme.objects.create(
        title='Filme 3',
        year=2004,
        studios='Studio 3',
        producers='Producer 2',
        winner='yes'
    )

    client = APIClient()
    url = reverse('ler-intervalos-premios')

    response = client.get(url)
    # Adicione esta linha para imprimir a resposta em caso de erro
    print(response.json())
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
