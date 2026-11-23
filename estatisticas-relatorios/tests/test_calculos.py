from estatisticas.calculos import (
    calcular_taxa_resolucao,
    contar_ocorrencias_por_status,
    contar_ocorrencias_por_tipo,
    contar_ocorrencias_por_dia,
    contar_ocorrencias_por_mes,
    contar_ocorrencias_por_regiao,
    gerar_indicadores_gerais,
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


def test_contagem_ocorrencias_por_regiao():
    ocorrencias = [
        {"regiao": "Asa Norte"},
        {"regiao": "Asa Sul"},
        {"regiao": "Asa Norte"},
        {"regiao": "Taguatinga"},
        {"regiao": "Asa Norte"},
    ]

    resultado = contar_ocorrencias_por_regiao(ocorrencias)

    assert resultado == {
        "Asa Norte": 3,
        "Asa Sul": 1,
        "Taguatinga": 1,
    }


def test_contagem_regiao_lista_vazia():
    resultado = contar_ocorrencias_por_regiao([])

    assert resultado == {}


def test_contagem_regiao_unica():
    ocorrencias = [
        {"regiao": "Asa Norte"},
        {"regiao": "Asa Norte"},
        {"regiao": "Asa Norte"},
    ]

    resultado = contar_ocorrencias_por_regiao(ocorrencias)

    assert resultado == {"Asa Norte": 3}


def test_contagem_regioes_diferentes():
    ocorrencias = [
        {"regiao": "Asa Norte"},
        {"regiao": "Asa Sul"},
        {"regiao": "Taguatinga"},
    ]

    resultado = contar_ocorrencias_por_regiao(ocorrencias)

    assert resultado == {
        "Asa Norte": 1,
        "Asa Sul": 1,
        "Taguatinga": 1,
    }


def test_indicadores_gerais():
    ocorrencias = [
        {"status": "Aberta"},
        {"status": "Resolvida"},
        {"status": "Aberta"},
        {"status": "Em análise"},
        {"status": "Resolvida"},
    ]

    resultado = gerar_indicadores_gerais(ocorrencias)

    assert resultado == {
        "total": 5,
        "por_status": {
            "Aberta": 2,
            "Resolvida": 2,
            "Em análise": 1,
        },
        "resolvidas": 2,
        "taxa_resolucao": 40.0,
    }


def test_indicadores_lista_vazia():
    resultado = gerar_indicadores_gerais([])

    assert resultado == {
        "total": 0,
        "por_status": {},
        "resolvidas": 0,
        "taxa_resolucao": 0.0,
    }


def test_indicadores_todas_resolvidas():
    ocorrencias = [
        {"status": "Resolvida"},
        {"status": "Resolvida"},
    ]

    resultado = gerar_indicadores_gerais(ocorrencias)

    assert resultado["total"] == 2
    assert resultado["resolvidas"] == 2
    assert resultado["taxa_resolucao"] == 100.0


def test_indicadores_nenhuma_resolvida():
    ocorrencias = [
        {"status": "Aberta"},
        {"status": "Em análise"},
    ]

    resultado = gerar_indicadores_gerais(ocorrencias)

    assert resultado["resolvidas"] == 0
    assert resultado["taxa_resolucao"] == 0.0