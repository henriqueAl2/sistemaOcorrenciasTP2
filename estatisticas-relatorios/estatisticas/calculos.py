
"""CÁLCULOS SOBRE OCORRÊNCIAS"""

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



""" EVOLUÇÃO TEMPORAL DAS OCORRÊNCIAS """

def contar_ocorrencias_por_dia(ocorrencias):
    """
    Conta ocorrencias agrupadas pela data de registro.

    Args:
        ocorrencias: Lista de dicionarios com o campo
                     'data' no formato AAAA-MM-DD.

    Returns:
        Dicionario ordenado cronologicamente com
        a quantidade de ocorrencias por dia.
    """
    contagem = {}

    for ocorrencia in ocorrencias:
        data = ocorrencia["data"]

        if data not in contagem:
            contagem[data] = 0

        contagem[data] += 1

    return dict(sorted(contagem.items()))


def contar_ocorrencias_por_mes(ocorrencias):
    """
    Conta ocorrencias agrupadas por ano e mes.

    Args:
        ocorrencias: Lista de dicionarios com o campo
                     'data' no formato AAAA-MM-DD.

    Returns:
        Dicionario ordenado cronologicamente com
        a quantidade de ocorrencias por mes.
    """
    contagem = {}

    for ocorrencia in ocorrencias:
        mes = ocorrencia["data"][:7]

        if mes not in contagem:
            contagem[mes] = 0

        contagem[mes] += 1

    return dict(sorted(contagem.items()))