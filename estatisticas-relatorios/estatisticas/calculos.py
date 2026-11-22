def calcular_taxa_resolucao(total, resolvidas):
    """
    Calcula o percentual de ocorrencias resolvidas.

    Args:
        total: Quantidade total de ocorrencias.
        resolvidas: Quantidade de ocorrencias resolvidas.

    Returns:
        Percentual de ocorrencias resolvidas.
    """
    if total == 0:
        return 0.0

    return (resolvidas / total) * 100


def _contar_por_campo(ocorrencias, campo):
    """
    Conta registros agrupados pelo campo informado.

    Args:
        ocorrencias: Lista de dicionarios.
        campo: Nome do campo utilizado no agrupamento.

    Returns:
        Dicionario com a contagem de cada valor.
    """
    contagem = {}

    for ocorrencia in ocorrencias:
        valor = ocorrencia[campo]

        if valor not in contagem:
            contagem[valor] = 0

        contagem[valor] += 1

    return contagem


def contar_ocorrencias_por_status(ocorrencias):
    """
    Conta a quantidade de ocorrencias por status.
    """
    return _contar_por_campo(ocorrencias, "status")


def contar_ocorrencias_por_tipo(ocorrencias):
    """
    Conta a quantidade de ocorrencias por tipo.
    """
    return _contar_por_campo(ocorrencias, "tipo")