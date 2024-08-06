import pytest
from django.urls import reverse
from rest_framework.test import APIClient

from app.models import Estudio, Filme, Produtor


@pytest.mark.django_db
def test_obter_produtores_ganhadores():
    """Teste para verificar os intervalos de prêmios dos produtores."""

    # Criar estúdios e produtores
    estudio1 = Estudio.objects.create(name='Studio 1')
    estudio2 = Estudio.objects.create(name='Studio 2')
    estudio3 = Estudio.objects.create(name='Studio 3')
    produtor1 = Produtor.objects.create(name='Producer 1')
    produtor2 = Produtor.objects.create(name='Producer 2')

    # Adicionar dados de teste
    filme1 = Filme.objects.create(title='Filme 1', year=2000, winner='yes')
    filme1.studios.add(estudio1)
    filme1.producers.add(produtor1)

    filme2 = Filme.objects.create(title='Filme 2', year=2002, winner='yes')
    filme2.studios.add(estudio2)
    filme2.producers.add(produtor1)

    filme3 = Filme.objects.create(title='Filme 3', year=2004, winner='yes')
    filme3.studios.add(estudio3)
    filme3.producers.add(produtor2)

    client = APIClient()
    url = reverse('ler-intervalos-premios')

    response = client.get(url)
    assert response.status_code == 200

    data = response.json()
    assert "min" in data
    assert "max" in data

    # Verificar detalhes nos intervalos mínimos e máximos
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
