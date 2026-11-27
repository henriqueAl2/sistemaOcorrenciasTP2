
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
