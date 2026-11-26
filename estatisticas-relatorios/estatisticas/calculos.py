from datetime import date
import re


def calcular_taxa_resolucao(total, resolvidas):
    """
    Calcula o percentual de ocorrencias resolvidas.

    Args:
        total: Quantidade total de ocorrencias.
        resolvidas: Quantidade de ocorrencias resolvidas.

    Returns:
        Percentual de ocorrencias resolvidas.

    Raises:
        TypeError: Se os argumentos nao forem inteiros.
        ValueError: Se as quantidades forem invalidas.
    """

    if type(total) is not int or type(resolvidas) is not int:
        raise TypeError(
            "Total e resolvidas devem ser numeros inteiros."
        )

    if total < 0 or resolvidas < 0:
        raise ValueError(
            "As quantidades nao podem ser negativas."
        )

    if resolvidas > total:
        raise ValueError(
            "Resolvidas nao pode ser maior que o total."
        )

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

    Raises:
        TypeError: Se a estrutura ou o tipo de um valor
                   estiver incorreto.
        ValueError: Se um campo estiver ausente, nulo
                    ou vazio.
    """
    if not isinstance(ocorrencias, list):
        raise TypeError(
            "Os registros devem ser fornecidos em uma lista."
        )

    contagem = {}

    for ocorrencia in ocorrencias:
        if not isinstance(ocorrencia, dict):
            raise TypeError(
                "Cada registro deve ser um dicionario."
            )

        try:
            chave = obter_chave(ocorrencia)
        except KeyError as erro:
            raise ValueError(
                "Registro com campo obrigatorio ausente."
            ) from erro

        if chave is None:
            raise ValueError(
                "O valor do campo nao pode ser nulo."
            )

        if not isinstance(chave, str):
            raise TypeError(
                "O valor do campo deve ser uma string."
            )

        if not chave.strip():
            raise ValueError(
                "O valor do campo nao pode estar vazio."
            )

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



def _validar_data(data):
    """
    Valida uma data no formato AAAA-MM-DD.

    Args:
        data: String contendo uma data.

    Returns:
        A propria data validada.

    Raises:
        TypeError: Se a data possuir tipo incorreto.
        ValueError: Se a data for nula, inexistente
                    ou possuir formato invalido.
    """
    if data is None:
        raise ValueError(
            "A data nao pode ser nula."
        )

    if not isinstance(data, str):
        raise TypeError(
            "A data deve ser uma string."
        )

    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", data):
        raise ValueError(
            "A data deve estar no formato AAAA-MM-DD."
        )

    try:
        ano, mes, dia = map(int, data.split("-"))
        date(ano, mes, dia)
    except ValueError as erro:
        raise ValueError(
            "A data informada nao existe."
        ) from erro

    return data



def contar_ocorrencias_por_dia(ocorrencias):
    """
    Conta ocorrencias por dia, em ordem cronologica.
    """
    contagem = _contar_por_chave(
        ocorrencias,
        lambda ocorrencia: _validar_data(
            ocorrencia["data"]
        )
    )

    return dict(sorted(contagem.items()))



def contar_ocorrencias_por_mes(ocorrencias):
    """
    Conta ocorrencias por ano e mes, em ordem cronologica.
    """
    contagem = _contar_por_chave(
        ocorrencias,
        lambda ocorrencia: _validar_data(
            ocorrencia["data"]
        )[:7]
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


def gerar_indicadores_gerais(ocorrencias):
    """
    Gera indicadores gerais das ocorrencias.

    Args:
        ocorrencias: Lista de dicionarios contendo
                     o campo 'status'.

    Returns:
        Dicionario contendo total, distribuicao
        por status, quantidade resolvida e
        taxa de resolucao.
    """
    total = len(ocorrencias)

    por_status = contar_ocorrencias_por_status(ocorrencias)

    resolvidas = por_status.get("Resolvida", 0)

    taxa = calcular_taxa_resolucao(total, resolvidas)

    return {
        "total": total,
        "por_status": por_status,
        "resolvidas": resolvidas,
        "taxa_resolucao": taxa,
    }



def contar_usuarios_por_perfil(usuarios):
    """
    Conta a quantidade de usuarios por perfil.

    Args:
        usuarios: Lista de dicionarios contendo
                  o campo 'perfil'.

    Returns:
        Dicionario com a quantidade de usuarios
        de cada perfil.
    """
    return _contar_por_chave(
        usuarios,
        lambda usuario: usuario["perfil"]
    )


def contar_usuarios_com_ocorrencias(ocorrencias):
    """
    Conta usuarios distintos que registraram ocorrencias.

    Args:
        ocorrencias: Lista de dicionarios contendo
                     o campo 'usuario_id'.

    Returns:
        Quantidade de usuarios distintos.
    """
    usuarios_distintos = set()

    for ocorrencia in ocorrencias:
        usuarios_distintos.add(ocorrencia["usuario_id"])

    return len(usuarios_distintos)



def contar_pesquisas_por_termo(pesquisas):
    """
    Conta a quantidade de pesquisas por termo.

    Args:
        pesquisas: Lista de dicionarios contendo
                   o campo 'termo'.

    Returns:
        Dicionario com a quantidade de pesquisas
        para cada termo encontrado.
    """
    return _contar_por_chave(
        pesquisas,
        lambda pesquisa: pesquisa["termo"]
    )


def contar_pesquisas_por_regiao(pesquisas):
    """
    Conta a quantidade de pesquisas por regiao.

    Args:
        pesquisas: Lista de dicionarios contendo
                   o campo 'regiao'.

    Returns:
        Dicionario com a quantidade de pesquisas
        para cada regiao consultada.
    """
    return _contar_por_chave(
        pesquisas,
        lambda pesquisa: pesquisa["regiao"]
    )





