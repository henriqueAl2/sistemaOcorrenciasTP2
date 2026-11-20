def calcular_taxa_resolucao(total, resolvidas):
    """
    Calcula o percentual de ocorrencias resolvidas.

    Argumentos:
        total: Quantidade total de ocorrencias.
        resolvidas: Quantidade de ocorrencias resolvidas.

    Retorna:
        Percentual de ocorrencias resolvidas.
    """
    if total == 0:
        return 0.0

    return (resolvidas / total) * 100