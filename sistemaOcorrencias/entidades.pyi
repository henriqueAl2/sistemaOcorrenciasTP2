from dominios import (
    CPF,
    Data,
    Email,
    TextoCurto,
    TextoLongo,
    TipoUsuario,
    TipoNotificacao,
    Senha
)


class Usuario:
    cpf: CPF
    nome: TextoCurto
    email: Email
    tipo: TipoUsuario
    senha: Senha

    def __init__(
        self,
        cpf: CPF,
        nome: TextoCurto,
        email: Email,
        tipo: TipoUsuario,
        senha: Senha
    ) -> None: ...


class Ocorrencia:
    tipo: TextoCurto
    descricao: TextoLongo
    data: Data
    localizacao: TextoCurto

    def __init__(
        self,
        tipo: TextoCurto,
        descricao: TextoLongo,
        data: Data,
        status: TextoCurto,
    ) -> None: ...

class Local:
    endereco: TextoLongo
    latitude: TextoCurto
    longitude: TextoCurto

    def __init__ (
            self,
            endereco: TextoLongo,
            latitude: TextoCurto,
            longitude: TextoCurto
    ) -> None: ...

class TipoOcorrencia:
    nome: TextoCurto
    descricao: TextoLongo

    def __init__ (
            self,
            nome: TextoCurto,
            descricao: TextoLongo
    ) -> None: ...

class Alerta:
    mensagem: TextoCurto
    tipo: TipoNotificacao

    def __init__ (
            self, 
            mensagem: TextoCurto,
            tipo: TipoNotificacao
    ) -> None: ...

class Pesquisa:
    termoPesquisado: TextoCurto
    regiaoConsultada: TextoCurto

    def __init__ (
            self,
            termoPesquisado: TextoCurto,
            regiaoConsultada: TextoCurto
    ) -> None: ...

class Notificacao:
    mensagem: TextoCurto
    lida: TipoNotificacao

    def __init__ (
            self,
            mensagem: TextoCurto,
            lida: TipoNotificacao
    ) -> None: ...

class AlertaRegiao:
    latitude: TextoCurto
    longitude: TextoCurto
    raio: int

    def __init__ (
            latitude: TextoCurto,
            longitude: TextoCurto,
            raio: int
    ) -> None: ...

class Acompanhamento:
    data: Data

    def __init__ (
            data: Data
    ) -> None: ...