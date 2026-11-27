import pytest
from estatisticas.adaptadores import (
    adaptar_ocorrencias,
    adaptar_usuarios,
    adaptar_pesquisas,
)

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



# TESTES DO ADAPTADOR DE USUARIOS

def test_adaptar_usuarios():
    dados = [
        {"CPF": "00123456789", "tipo": "user"},
        {"CPF": "98765432100", "tipo": "admin"},
    ]

    resultado = adaptar_usuarios(dados)

    assert resultado == [
        {"id": "00123456789", "perfil": "user"},
        {"id": "98765432100", "perfil": "admin"},
    ]


def test_adaptar_usuarios_lista_vazia():
    assert adaptar_usuarios([]) == []


def test_adaptar_usuario_campo_ausente():
    dados = [{"CPF": "00123456789"}]

    with pytest.raises(ValueError):
        adaptar_usuarios(dados)


def test_adaptar_usuario_cpf_invalido():
    dados = [{"CPF": None, "tipo": "user"}]

    with pytest.raises(ValueError):
        adaptar_usuarios(dados)


# TESTES DO ADAPTADOR DE PESQUISAS

def test_adaptar_pesquisas():
    dados = [
        {
            "termoPesquisado": "Buraco",
            "regiaoConsultada": "Asa Norte",
        },
        {
            "termoPesquisado": "Iluminacao",
            "regiaoConsultada": "Asa Sul",
        },
    ]

    resultado = adaptar_pesquisas(dados)

    assert resultado == [
        {"termo": "Buraco", "regiao": "Asa Norte"},
        {"termo": "Iluminacao", "regiao": "Asa Sul"},
    ]


def test_adaptar_pesquisas_lista_vazia():
    assert adaptar_pesquisas([]) == []


def test_adaptar_pesquisa_campo_ausente():
    dados = [{"termoPesquisado": "Buraco"}]

    with pytest.raises(ValueError):
        adaptar_pesquisas(dados)


def test_adaptar_pesquisa_regiao_nula():
    dados = [
        {
            "termoPesquisado": "Buraco",
            "regiaoConsultada": None,
        }
    ]

    with pytest.raises(ValueError):
        adaptar_pesquisas(dados)
