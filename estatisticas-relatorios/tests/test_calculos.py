from estatisticas.calculos import calcular_taxa_resolucao


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