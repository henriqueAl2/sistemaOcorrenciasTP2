
"""Adaptadores de dados recebidos do backend."""

from email.utils import parsedate_to_datetime


def adaptar_ocorrencias(dados):
    """Converte registros do backend para o formato estatistico."""
    if not isinstance(dados, list):
        raise TypeError("Os dados devem ser uma lista.")

    resultado = []

    for registro in dados:
        if not isinstance(registro, dict):
            raise TypeError("Cada registro deve ser um dicionario.")

        campos = ("Usuario_CPF", "tipo", "status", "data")

        if any(campo not in registro for campo in campos):
            raise ValueError("Registro com campo obrigatorio ausente.")

        data_original = registro["data"]

        if not isinstance(data_original, str):
            raise TypeError("A data deve ser uma string.")

        try:
            data_convertida = parsedate_to_datetime(
                data_original
            ).date().isoformat()
        except (TypeError, ValueError, IndexError) as erro:
            raise ValueError(
                "Data invalida recebida do backend."
            ) from erro

        resultado.append({
            "usuario_id": registro["Usuario_CPF"],
            "tipo": registro["tipo"],
            "status": registro["status"],
            "data": data_convertida,
        })

    return resultado



def _adaptar_campos_textuais(dados, mapeamento):
    """
    Converte campos textuais de registros para nomes padronizados.

    Args:
        dados: Lista de dicionarios de origem.
        mapeamento: Dicionario com os nomes dos campos
                    de origem e destino.

    Returns:
        Lista de dicionarios com os campos padronizados.
    """
    if not isinstance(dados, list):
        raise TypeError("Os dados devem ser uma lista.")

    resultado = []

    for registro in dados:
        if not isinstance(registro, dict):
            raise TypeError(
                "Cada registro deve ser um dicionario."
            )

        registro_adaptado = {}

        for origem, destino in mapeamento.items():
            if origem not in registro:
                raise ValueError(
                    f"Campo obrigatorio ausente: {origem}"
                )

            valor = registro[origem]

            if valor is None:
                raise ValueError(
                    f"O campo {origem} nao pode ser nulo."
                )

            if not isinstance(valor, str):
                raise TypeError(
                    f"O campo {origem} deve ser uma string."
                )

            if not valor.strip():
                raise ValueError(
                    f"O campo {origem} nao pode estar vazio."
                )

            registro_adaptado[destino] = valor

        resultado.append(registro_adaptado)

    return resultado


def adaptar_usuarios(dados):
    """
    Adapta usuarios para o formato das estatisticas.

    Converte CPF em id e tipo em perfil.
    """
    return _adaptar_campos_textuais(
        dados,
        {
            "CPF": "id",
            "tipo": "perfil",
        }
    )


def adaptar_pesquisas(dados):
    """
    Adapta pesquisas para o formato das estatisticas.

    Converte termoPesquisado em termo e
    regiaoConsultada em regiao.
    """
    return _adaptar_campos_textuais(
        dados,
        {
            "termoPesquisado": "termo",
            "regiaoConsultada": "regiao",
        }
    )
