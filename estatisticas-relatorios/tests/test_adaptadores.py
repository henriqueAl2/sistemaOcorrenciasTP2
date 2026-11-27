import pytest
from estatisticas.adaptadores import adaptar_ocorrencias


def test_adaptar_ocorrencias():
    dados = [
        {
            "idOcorrencia": 1,
            "Usuario_CPF": "11122233344",
            "tipo": "Buraco na via",
            "status": "Aberta",
            "data": "Fri, 13 Nov 2026 00:00:00 GMT",
        }
    ]

    resultado = adaptar_ocorrencias(dados)

    assert resultado == [
        {
            "usuario_id": "11122233344",
            "tipo": "Buraco na via",
            "status": "Aberta",
            "data": "2026-11-13",
        }
    ]


def test_adaptar_lista_vazia():
    assert adaptar_ocorrencias([]) == []


def test_adaptar_data_invalida():
    dados = [
        {
            "Usuario_CPF": "11122233344",
            "tipo": "Buraco na via",
            "status": "Aberta",
            "data": "data invalida",
        }
    ]

    with pytest.raises(ValueError):
        adaptar_ocorrencias(dados)


def test_adaptar_campo_ausente():
    dados = [
        {
            "tipo": "Buraco na via",
            "status": "Aberta",
            "data": "Fri, 13 Nov 2026 00:00:00 GMT",
        }
    ]

    with pytest.raises(ValueError):
        adaptar_ocorrencias(dados)
