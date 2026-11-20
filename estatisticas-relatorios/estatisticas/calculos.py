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


def contar_ocorrencias_por_status(ocorrencias):
    """
    Conta a quantidade de ocorrencias por status.

    Argumentos:
        ocorrencias: Lista de dicionarios contendo
                     o campo 'status'.

    Retorna:
        Dicionario com a quantidade de ocorrencias
        para cada status encontrado.
    """
    contagem = {}

    for ocorrencia in ocorrencias:
        status = ocorrencia["status"]

        if status not in contagem:
            contagem[status] = 0

        contagem[status] += 1

    return contagem