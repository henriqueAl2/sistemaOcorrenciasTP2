from estatisticas.calculos import (
    calcular_taxa_resolucao,
    contar_ocorrencias_por_status,
    contar_ocorrencias_por_tipo,
    contar_ocorrencias_por_dia,
    contar_ocorrencias_por_mes,
)


def test_taxa_resolucao_normal():
    resultado = calcular_taxa_resolucao(20, 5)
    assert resultado == 25.0


def test_taxa_resolucao_zero_ocorrencias():
    resultado = calcular_taxa_resolucao(0, 0)
    assert resultado == 0.0


def test_taxa_resolucao_todas_resolvidas():
    resultado = calcular_taxa_resolucao(10, 10)
    assert resultado == 100.0


def test_taxa_resolucao_nenhuma_resolvida():
    resultado = calcular_taxa_resolucao(10, 0)
    assert resultado == 0.0



def test_contagem_ocorrencias_por_status():
    ocorrencias = [
        {"status": "Aberta"},
        {"status": "Em análise"},
        {"status": "Aberta"},
        {"status": "Resolvida"},
        {"status": "Aberta"},
    ]

    resultado = contar_ocorrencias_por_status(ocorrencias)

    assert resultado == {
        "Aberta": 3,
        "Em análise": 1,
        "Resolvida": 1,
    }


def test_contagem_ocorrencias_lista_vazia():
    resultado = contar_ocorrencias_por_status([])

    assert resultado == {}


def test_contagem_ocorrencias_status_unico():
    ocorrencias = [
        {"status": "Aberta"},
        {"status": "Aberta"},
        {"status": "Aberta"},
    ]

    resultado = contar_ocorrencias_por_status(ocorrencias)

    assert resultado == {"Aberta": 3}


def test_contagem_ocorrencias_status_diferentes():
    ocorrencias = [
        {"status": "Aberta"},
        {"status": "Em análise"},
        {"status": "Resolvida"},
    ]

    resultado = contar_ocorrencias_por_status(ocorrencias)

    assert resultado == {
        "Aberta": 1,
        "Em análise": 1,
        "Resolvida": 1,
    }


def test_contagem_ocorrencias_por_tipo():
    ocorrencias = [
        {"tipo": "Buraco na via"},
        {"tipo": "Iluminação pública"},
        {"tipo": "Buraco na via"},
        {"tipo": "Descarte irregular"},
        {"tipo": "Buraco na via"},
    ]

    resultado = contar_ocorrencias_por_tipo(ocorrencias)

    assert resultado == {
        "Buraco na via": 3,
        "Iluminação pública": 1,
        "Descarte irregular": 1,
    }


def test_contagem_tipo_lista_vazia():
    resultado = contar_ocorrencias_por_tipo([])

    assert resultado == {}


def test_contagem_tipo_unico():
    ocorrencias = [
        {"tipo": "Buraco na via"},
        {"tipo": "Buraco na via"},
        {"tipo": "Buraco na via"},
    ]

    resultado = contar_ocorrencias_por_tipo(ocorrencias)

    assert resultado == {"Buraco na via": 3}


def test_contagem_tipos_diferentes():
    ocorrencias = [
        {"tipo": "Buraco na via"},
        {"tipo": "Iluminação pública"},
        {"tipo": "Descarte irregular"},
    ]

    resultado = contar_ocorrencias_por_tipo(ocorrencias)

    assert resultado == {
        "Buraco na via": 1,
        "Iluminação pública": 1,
        "Descarte irregular": 1,
    }


def test_contagem_ocorrencias_por_dia():
    ocorrencias = [
        {"data": "2026-11-01"},
        {"data": "2026-11-01"},
        {"data": "2026-11-02"},
        {"data": "2026-11-03"},
        {"data": "2026-11-03"},
    ]

    resultado = contar_ocorrencias_por_dia(ocorrencias)

    assert resultado == {
        "2026-11-01": 2,
        "2026-11-02": 1,
        "2026-11-03": 2,
    }


def test_contagem_dia_lista_vazia():
    resultado = contar_ocorrencias_por_dia([])

    assert resultado == {}


def test_contagem_dia_ordenacao():
    ocorrencias = [
        {"data": "2026-11-03"},
        {"data": "2026-11-01"},
        {"data": "2026-11-02"},
    ]

    resultado = contar_ocorrencias_por_dia(ocorrencias)

    assert list(resultado.keys()) == [
        "2026-11-01",
        "2026-11-02",
        "2026-11-03",
    ]


def test_contagem_ocorrencias_por_mes():
    ocorrencias = [
        {"data": "2026-10-01"},
        {"data": "2026-10-15"},
        {"data": "2026-11-01"},
        {"data": "2026-11-03"},
        {"data": "2026-11-05"},
    ]

    resultado = contar_ocorrencias_por_mes(ocorrencias)

    assert resultado == {
        "2026-10": 2,
        "2026-11": 3,
    }


def test_contagem_mes_anos_diferentes():
    ocorrencias = [
        {"data": "2025-11-01"},
        {"data": "2026-11-01"},
        {"data": "2026-11-02"},
    ]

    resultado = contar_ocorrencias_por_mes(ocorrencias)

    assert resultado == {
        "2025-11": 1,
        "2026-11": 2,
    }


def test_contagem_mes_lista_vazia():
    resultado = contar_ocorrencias_por_mes([])

    assert resultado == {}