
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


def _contar_por_chave(ocorrencias, obter_chave):
    """
    Conta registros agrupados por uma chave.

    Args:
        ocorrencias: Lista de dicionarios.
        obter_chave: Funcao que extrai a chave de agrupamento.

    Returns:
        Dicionario com as quantidades por chave.
    """
    contagem = {}

    for ocorrencia in ocorrencias:
        chave = obter_chave(ocorrencia)

        if chave not in contagem:
            contagem[chave] = 0

        contagem[chave] += 1

    return contagem


def contar_ocorrencias_por_status(ocorrencias):
    """
    Conta a quantidade de ocorrencias por status.
    """
    return _contar_por_chave(
        ocorrencias,
        lambda ocorrencia: ocorrencia["status"]
    )


def contar_ocorrencias_por_tipo(ocorrencias):
    """
    Conta a quantidade de ocorrencias por tipo.
    """
    return _contar_por_chave(
        ocorrencias,
        lambda ocorrencia: ocorrencia["tipo"]
    )


def contar_ocorrencias_por_dia(ocorrencias):
    """
    Conta ocorrencias por dia, em ordem cronologica.
    """
    contagem = _contar_por_chave(
        ocorrencias,
        lambda ocorrencia: ocorrencia["data"]
    )

    return dict(sorted(contagem.items()))


def contar_ocorrencias_por_mes(ocorrencias):
    """
    Conta ocorrencias por ano e mes, em ordem cronologica.
    """
    contagem = _contar_por_chave(
        ocorrencias,
        lambda ocorrencia: ocorrencia["data"][:7]
    )

    return dict(sorted(contagem.items()))


def contar_ocorrencias_por_regiao(ocorrencias):
    """
    Conta a quantidade de ocorrencias por regiao.

    Args:
        ocorrencias: Lista de dicionarios contendo
                     o campo 'regiao'.

    Returns:
        Dicionario com a quantidade de ocorrencias
        para cada regiao encontrada.
    """
    return _contar_por_chave(
        ocorrencias,
        lambda ocorrencia: ocorrencia["regiao"]
    )