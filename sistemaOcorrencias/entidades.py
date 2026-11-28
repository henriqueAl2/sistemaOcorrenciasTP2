"""Módulo de implementação das entidades do sistema de ocorrências."""
from dominios import (
    CPF,
    Data,
    Email,
    TextoCurto,
    TextoLongo,
    TipoNotificacao,
    TipoUsuario,
    Senha
)


class Usuario:
    """Representa um usuário (comum ou administrador) do sistema."""

    def __init__(
        self,
        cpf: CPF,
        nome: TextoCurto,
        email: Email,
        tipo: TipoUsuario,
        senha: Senha
    ) -> None:
        if not isinstance(cpf, CPF):
            raise TypeError("cpf deve ser uma instância do domínio CPF.")
        if not isinstance(nome, TextoCurto):
            raise TypeError("nome deve ser uma instância do domínio TextoCurto.")
        if not isinstance(email, Email):
            raise TypeError("email deve ser uma instância do domínio Email.")
        if not isinstance(tipo, TipoUsuario):
            raise TypeError("tipo deve ser uma instância do domínio TipoUsuario.")
        if not isinstance (senha, Senha):
            raise TypeError("senha deve ser uma instância do tipo Senha")

        self.cpf = cpf
        self.nome = nome
        self.email = email
        self.tipo = tipo
        self.senha = senha

    def para_dicionario(self) -> dict[str, str]:
        """Serializa os atributos da entidade para dicionário."""
        return {
            "cpf": str(self.cpf),
            "nome": str(self.nome),
            "email": str(self.email),
            "tipo": str(self.tipo),
            "senha": str(self.senha)
        }

    def __str__(self) -> str:
        return f"{self.nome} ({self.cpf}) - {self.tipo}"


class Ocorrencia:
    """Representa uma ocorrência registrada com localização e data."""

    # pylint: disable=too-many-arguments,too-many-positional-arguments
    def __init__(
        self,
        tipo: TextoCurto,
        descricao: TextoLongo,
        data: Data,
        localizacao: TextoCurto,
        notificacao: TipoNotificacao | None = None,
    ) -> None:
        if not isinstance(tipo, TextoCurto):
            raise TypeError("tipo deve ser uma instância do domínio TextoCurto.")
        if not isinstance(descricao, TextoLongo):
            raise TypeError(
                "descricao deve ser uma instância do domínio TextoLongo."
            )
        if not isinstance(data, Data):
            raise TypeError("data deve ser uma instância do domínio Data.")
        if not isinstance(localizacao, TextoCurto):
            raise TypeError(
                "localizacao deve ser uma instância do domínio TextoCurto."
            )
        if notificacao is not None and not isinstance(
            notificacao, TipoNotificacao
        ):
            raise TypeError(
                "notificacao deve ser uma instância de TipoNotificacao ou None."
            )

        self.tipo = tipo
        self.descricao = descricao
        self.data = data
        self.localizacao = localizacao
        self.notificacao = notificacao

    def para_dicionario(self) -> dict[str, str | None]:
        """Serializa os atributos da ocorrência para dicionário."""
        return {
            "tipo": str(self.tipo),
            "descricao": str(self.descricao),
            "data": str(self.data),
            "localizacao": str(self.localizacao),
            "notificacao": (
                str(self.notificacao) if self.notificacao is not None else None
            ),
        }

    def __str__(self) -> str:
        return f"[{self.data}] {self.tipo} - {self.localizacao}"

class Local:
    """Representa um local geográfico autorizado para registro de ocorrências."""

    def __init__(self, nome: TextoCurto, coordenadas: TextoCurto) -> None:
        if not isinstance(nome, TextoCurto):
            raise TypeError("nome deve ser uma instância do domínio TextoCurto.")
        if not isinstance(coordenadas, TextoCurto):
            raise TypeError(
                "coordenadas deve ser uma instância do domínio TextoCurto."
            )

        self.nome = nome
        self.coordenadas = coordenadas

    def para_dicionario(self) -> dict[str, str]:
        """Serializa os atributos do local para dicionário."""
        return {
            "nome": str(self.nome),
            "coordenadas": str(self.coordenadas),
        }

    def __str__(self) -> str:
        return f"{self.nome} ({self.coordenadas})"


class TipoOcorrencia:
    """Entidade que representa um tipo/categoria de ocorrência cadastrada."""

    def __init__(self, nome: TextoCurto, descricao: TextoLongo) -> None:
        if not isinstance(nome, TextoCurto):
            raise TypeError("nome deve ser uma instância do domínio TextoCurto.")
        if not isinstance(descricao, TextoLongo):
            raise TypeError(
                "descricao deve ser uma instância do domínio TextoLongo."
            )

        self.nome = nome
        self.descricao = descricao

    def para_dicionario(self) -> dict[str, str]:
        """Serializa os atributos do tipo de ocorrência para dicionário."""
        return {
            "nome": str(self.nome),
            "descricao": str(self.descricao),
        }

    def __str__(self) -> str:
        return f"{self.nome}: {self.descricao}"

class Alerta:
    """Representa uma configuração de alerta para notificações de ocorrências."""

    def __init__(
        self,
        regiao: TextoCurto,
        tipo_ocorrencia: TextoCurto,
        tipo_notificacao: TipoNotificacao,
    ) -> None:
        if not isinstance(regiao, TextoCurto):
            raise TypeError(
                "regiao deve ser uma instância do domínio TextoCurto."
            )
        if not isinstance(tipo_ocorrencia, TextoCurto):
            raise TypeError(
                "tipo_ocorrencia deve ser uma instância do domínio TextoCurto."
            )
        if not isinstance(tipo_notificacao, TipoNotificacao):
            raise TypeError(
                "tipo_notificacao deve ser uma instância de TipoNotificacao."
            )

        self.regiao = regiao
        self.tipo_ocorrencia = tipo_ocorrencia
        self.tipo_notificacao = tipo_notificacao

    def para_dicionario(self) -> dict[str, str]:
        """Serializa os atributos do alerta para dicionário."""
        return {
            "regiao": str(self.regiao),
            "tipo_ocorrencia": str(self.tipo_ocorrencia),
            "tipo_notificacao": str(self.tipo_notificacao),
        }

    def __str__(self) -> str:
        return (
            f"Alerta: {self.tipo_ocorrencia} em {self.regiao} "
            f"via {self.tipo_notificacao}"
        )


class Pesquisa:
    """Representa uma pesquisa de ocorrências realizada por um usuário."""

    def __init__(
        self,
        termo: TextoCurto,
        regiao: TextoCurto,
        data: Data,
    ) -> None:
        if not isinstance(termo, TextoCurto):
            raise TypeError("termo deve ser uma instância do domínio TextoCurto.")
        if not isinstance(regiao, TextoCurto):
            raise TypeError(
                "regiao deve ser uma instância do domínio TextoCurto."
            )
        if not isinstance(data, Data):
            raise TypeError("data deve ser uma instância do domínio Data.")

        self.termo = termo
        self.regiao = regiao
        self.data = data

    def para_dicionario(self) -> dict[str, str]:
        """Serializa os atributos da pesquisa para dicionário."""
        return {
            "termo": str(self.termo),
            "regiao": str(self.regiao),
            "data": str(self.data),
        }

    def __str__(self) -> str:
        return f"Pesquisa '{self.termo}' em {self.regiao} ({self.data})"

class Notificacao:
    """Representa uma notificação enviada sobre atualização de ocorrência."""

    def __init__(
        self,
        destinatario: CPF,
        mensagem: TextoLongo,
        data_envio: Data,
        tipo_notificacao: TipoNotificacao,
    ) -> None:
        if not isinstance(destinatario, CPF):
            raise TypeError(
                "destinatario deve ser uma instância do domínio CPF."
            )
        if not isinstance(mensagem, TextoLongo):
            raise TypeError(
                "mensagem deve ser uma instância do domínio TextoLongo."
            )
        if not isinstance(data_envio, Data):
            raise TypeError(
                "data_envio deve ser uma instância do domínio Data."
            )
        if not isinstance(tipo_notificacao, TipoNotificacao):
            raise TypeError(
                "tipo_notificacao deve ser uma instância de TipoNotificacao."
            )

        self.destinatario = destinatario
        self.mensagem = mensagem
        self.data_envio = data_envio
        self.tipo_notificacao = tipo_notificacao

    def para_dicionario(self) -> dict[str, str]:
        """Serializa os atributos da notificação para dicionário."""
        return {
            "destinatario": str(self.destinatario),
            "mensagem": str(self.mensagem),
            "data_envio": str(self.data_envio),
            "tipo_notificacao": str(self.tipo_notificacao),
        }

    def __str__(self) -> str:
        return (
            f"[{self.data_envio}] Para {self.destinatario}: "
            f"{self.mensagem} ({self.tipo_notificacao})"
        )


class AlertaRegiao:
    """Representa um alerta de ocorrência configurado para uma região específica."""

    def __init__(
        self,
        usuario: CPF,
        regiao: TextoCurto,
        tipo_ocorrencia: TextoCurto,
        tipo_notificacao: TipoNotificacao,
    ) -> None:
        if not isinstance(usuario, CPF):
            raise TypeError("usuario deve ser uma instância do domínio CPF.")
        if not isinstance(regiao, TextoCurto):
            raise TypeError(
                "regiao deve ser uma instância do domínio TextoCurto."
            )
        if not isinstance(tipo_ocorrencia, TextoCurto):
            raise TypeError(
                "tipo_ocorrencia deve ser uma instância do domínio TextoCurto."
            )
        if not isinstance(tipo_notificacao, TipoNotificacao):
            raise TypeError(
                "tipo_notificacao deve ser uma instância de TipoNotificacao."
            )

        self.usuario = usuario
        self.regiao = regiao
        self.tipo_ocorrencia = tipo_ocorrencia
        self.tipo_notificacao = tipo_notificacao

    def para_dicionario(self) -> dict[str, str]:
        """Serializa os atributos do alerta de região para dicionário."""
        return {
            "usuario": str(self.usuario),
            "regiao": str(self.regiao),
            "tipo_ocorrencia": str(self.tipo_ocorrencia),
            "tipo_notificacao": str(self.tipo_notificacao),
        }

    def __str__(self) -> str:
        return (
            f"AlertaRegiao ({self.usuario}): {self.tipo_ocorrencia} "
            f"em {self.regiao} ({self.tipo_notificacao})"
        )
class Acompanhamento:
    """Representa o acompanhamento de uma ocorrência específica por um usuário."""

    def __init__(
        self,
        usuario: Usuario,
        ocorrencia: Ocorrencia,
        notificacao_ativa: TipoNotificacao,
    ) -> None:
        if not isinstance(usuario, Usuario):
            raise TypeError(
                "usuario deve ser uma instância da entidade Usuario."
            )
        if not isinstance(ocorrencia, Ocorrencia):
            raise TypeError(
                "ocorrencia deve ser uma instância da entidade Ocorrencia."
            )
        if not isinstance(notificacao_ativa, TipoNotificacao):
            raise TypeError(
                "notificacao_ativa deve ser uma instância de TipoNotificacao."
            )

        self.usuario = usuario
        self.ocorrencia = ocorrencia
        self.notificacao_ativa = notificacao_ativa

    def para_dicionario(self) -> dict[str, str]:
        """Serializa os atributos do acompanhamento para dicionário."""
        return {
            "usuario": str(self.usuario.cpf),
            "ocorrencia": str(self.ocorrencia.tipo),
            "notificacao_ativa": str(self.notificacao_ativa),
        }

    def __str__(self) -> str:
        return (
            f"Acompanhamento: {self.usuario.nome} -> {self.ocorrencia.tipo} "
            f"(notificacao: {self.notificacao_ativa})"
        )