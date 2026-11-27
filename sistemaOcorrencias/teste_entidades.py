"""Suíte de testes unitários para o módulo entidades."""
import pytest
from dominios import (
    CPF,
    Data,
    Email,
    TextoCurto,
    TextoLongo,
    TipoUsuario,
    Senha,
    TipoNotificacao,
)
from entidades import Ocorrencia, Usuario, Alerta, Local, Pesquisa, TipoOcorrencia, TipoNotificacao, Notificacao, AlertaRegiao, Acompanhamento

def test_usuario_valido() -> None:
    """Deve instanciar Usuario corretamente quando todos os domínios são válidos."""
    cpf = CPF("529.982.247-25")
    nome = TextoCurto("Maria Silva")
    email = Email("maria.silva@exemplo.com")
    tipo = TipoUsuario("user")
    senha = Senha("A1b2c3")
    usuario = Usuario(cpf=cpf, nome=nome, email=email, tipo=tipo, senha=senha)

    assert usuario.cpf == cpf
    assert usuario.nome == nome
    assert usuario.email == email
    assert usuario.tipo == tipo
    assert usuario.senha == senha


def test_usuario_rejeita() -> None:
    """Deve lançar TypeError se receber string bruta em vez de objeto de domínio."""
    with pytest.raises(TypeError):
        Usuario(
            cpf="52998224725",  # type: ignore[arg-type]
            nome=TextoCurto("Maria Silva"),
            email=Email("maria.silva@exemplo.com"),
            tipo=TipoUsuario("user"),
            senha=Senha("A1b2c3")
        )


def test_ocorrencia_valida() -> None:
    """Deve instanciar Ocorrencia corretamente com domínios válidos."""
    tipo = TextoCurto("Buraco na via")
    descricao = TextoLongo("Fio eletrico solto na calcada")
    data = Data("26/11/2026")
    localizacao = TextoCurto("Asa Norte Quadra 102")

    ocorrencia = Ocorrencia(
        tipo=tipo,
        descricao=descricao,
        data=data,
        localizacao=localizacao,
    )

    assert ocorrencia.tipo == tipo
    assert ocorrencia.descricao == descricao
    assert ocorrencia.data == data
    assert ocorrencia.localizacao == localizacao


def test_ocorrencia_rejeita() -> None:
    """Deve lançar TypeError se passar TextoCurto onde se espera TextoLongo ou Data."""
    with pytest.raises(TypeError):
        Ocorrencia(
            tipo=TextoCurto("Buraco na via"),
            descricao=TextoCurto("Texto curto no lugar de longo"),  # type: ignore[arg-type]
            data=Data("26/11/2026"),
            localizacao=TextoCurto("Asa Norte Quadra 102"),
        )

def test_local_valido() -> None:
    """Deve instanciar Local corretamente com domínios válidos."""
    nome = TextoCurto("Asa Norte Quadra 102")
    coordenadas = TextoCurto("15.7634 47.8705")

    local = Local(nome=nome, coordenadas=coordenadas)

    assert local.nome == nome
    assert local.coordenadas == coordenadas
    assert local.para_dicionario() == {
        "nome": "Asa Norte Quadra 102",
        "coordenadas": "15.7634 47.8705",
    }


def test_local_rejeita() -> None:
    """Deve lançar TypeError ao passar string bruta em vez de TextoCurto."""
    with pytest.raises(TypeError):
        Local(
            nome="Asa Norte Quadra 102",  # type: ignore[arg-type]
            coordenadas=TextoCurto("15.7634 47.8705"),
        )


def test_tipo_ocorrencia_valido() -> None:
    """Deve instanciar TipoOcorrencia corretamente com domínios válidos."""
    nome = TextoCurto("Buraco na via")
    descricao = TextoLongo("Abertura ou desgaste no asfalto ou calcada")

    tipo_ocorrencia = TipoOcorrencia(nome=nome, descricao=descricao)

    assert tipo_ocorrencia.nome == nome
    assert tipo_ocorrencia.descricao == descricao
    assert tipo_ocorrencia.para_dicionario() == {
        "nome": "Buraco na via",
        "descricao": "Abertura ou desgaste no asfalto ou calcada",
    }


def test_tipo_ocorrencia_rejeita() -> None:
    """Deve lançar TypeError se descricao não for instância de TextoLongo."""
    with pytest.raises(TypeError):
        TipoOcorrencia(
            nome=TextoCurto("Buraco na via"),
            descricao=TextoCurto("Texto curto no lugar de longo"),  # type: ignore[arg-type]
        )
def test_alerta_valido() -> None:
    """Deve instanciar Alerta corretamente com domínios válidos."""
    regiao = TextoCurto("Asa Norte")
    tipo_ocorrencia = TextoCurto("Buraco na via")
    tipo_notificacao = TipoNotificacao("sim")  # Ajuste para valor aceito no seu domínio

    alerta = Alerta(
        regiao=regiao,
        tipo_ocorrencia=tipo_ocorrencia,
        tipo_notificacao=tipo_notificacao,
    )

    assert alerta.regiao == regiao
    assert alerta.tipo_ocorrencia == tipo_ocorrencia
    assert alerta.tipo_notificacao == tipo_notificacao
    assert alerta.para_dicionario() == {
        "regiao": "Asa Norte",
        "tipo_ocorrencia": "Buraco na via",
        "tipo_notificacao": str(tipo_notificacao),
    }


@pytest.mark.parametrize(
    ("regiao", "tipo_ocorrencia", "tipo_notificacao"),
    [
        ("Asa Norte", TextoCurto("Buraco"), TipoNotificacao("sim")),
        (TextoCurto("Asa Norte"), "Buraco", TipoNotificacao("sim")),
        (TextoCurto("Asa Norte"), TextoCurto("Buraco"), "email"),
    ],
)
def test_alerta_rejeita_tipos_invalidos(
    regiao: object,
    tipo_ocorrencia: object,
    tipo_notificacao: object,
) -> None:
    """Deve lançar TypeError se qualquer parâmetro de Alerta não for do domínio esperado."""
    with pytest.raises(TypeError):
        Alerta(
            regiao=regiao,  # type: ignore[arg-type]
            tipo_ocorrencia=tipo_ocorrencia,  # type: ignore[arg-type]
            tipo_notificacao=tipo_notificacao,  # type: ignore[arg-type]
        )


def test_pesquisa_valida() -> None:
    """Deve instanciar Pesquisa corretamente com domínios válidos."""
    termo = TextoCurto("Buraco na via")
    regiao = TextoCurto("Asa Sul")
    data = Data("26/11/2026")

    pesquisa = Pesquisa(termo=termo, regiao=regiao, data=data)

    assert pesquisa.termo == termo
    assert pesquisa.regiao == regiao
    assert pesquisa.data == data
    assert pesquisa.para_dicionario() == {
        "termo": "Buraco na via",
        "regiao": "Asa Sul",
        "data": str(data),
    }


@pytest.mark.parametrize(
    ("termo", "regiao", "data"),
    [
        ("Buraco", TextoCurto("Asa Sul"), Data("26/11/2026")),
        (TextoCurto("Buraco"), "Asa Sul", Data("26/11/2026")),
        (TextoCurto("Buraco"), TextoCurto("Asa Sul"), "26/11/2026"),
    ],
)
def test_pesquisa_rejeita_tipos_invalidos(
    termo: object,
    regiao: object,
    data: object,
) -> None:
    """Deve lançar TypeError se qualquer parâmetro de Pesquisa não for do domínio esperado."""
    with pytest.raises(TypeError):
        Pesquisa(
            termo=termo,  # type: ignore[arg-type]
            regiao=regiao,  # type: ignore[arg-type]
            data=data,  # type: ignore[arg-type]
        )

def test_notificacao_valida() -> None:
    """Deve instanciar Notificacao corretamente com domínios válidos."""
    destinatario = CPF("529.982.247-25")
    mensagem = TextoLongo("Status da ocorrencia alterado para em andamento")
    data_envio = Data("26/11/2026")
    tipo_notificacao = TipoNotificacao("sim")

    notificacao = Notificacao(
        destinatario=destinatario,
        mensagem=mensagem,
        data_envio=data_envio,
        tipo_notificacao=tipo_notificacao,
    )

    assert notificacao.destinatario == destinatario
    assert notificacao.mensagem == mensagem
    assert notificacao.data_envio == data_envio
    assert notificacao.tipo_notificacao == tipo_notificacao
    assert notificacao.para_dicionario() == {
        "destinatario": str(destinatario),
        "mensagem": str(mensagem),
        "data_envio": str(data_envio),
        "tipo_notificacao": str(tipo_notificacao),
    }


@pytest.mark.parametrize(
    ("destinatario", "mensagem", "data_envio", "tipo_notificacao"),
    [
        (
            "52998224725",
            TextoLongo("Ocorrencia atualizada"),
            Data("26/11/2026"),
            TipoNotificacao("sim"),
        ),
        (
            CPF("529.982.247-25"),
            "Ocorrencia atualizada",
            Data("26/11/2026"),
            TipoNotificacao("sim"),
        ),
        (
            CPF("529.982.247-25"),
            TextoLongo("Ocorrencia atualizada"),
            "26/11/2026",
            TipoNotificacao("sim"),
        ),
        (
            CPF("529.982.247-25"),
            TextoLongo("Ocorrencia atualizada"),
            Data("26/11/2026"),
            "sim",
        ),
    ],
)
def test_notificacao_rejeita_tipos_invalidos(
    destinatario: object,
    mensagem: object,
    data_envio: object,
    tipo_notificacao: object,
) -> None:
    """Deve lançar TypeError se qualquer parâmetro de Notificacao não for do domínio esperado."""
    with pytest.raises(TypeError):
        Notificacao(
            destinatario=destinatario,  # type: ignore[arg-type]
            mensagem=mensagem,  # type: ignore[arg-type]
            data_envio=data_envio,  # type: ignore[arg-type]
            tipo_notificacao=tipo_notificacao,  # type: ignore[arg-type]
        )


def test_alerta_regiao_valido() -> None:
    """Deve instanciar AlertaRegiao corretamente com domínios válidos."""
    usuario = CPF("529.982.247-25")
    regiao = TextoCurto("Asa Norte")
    tipo_ocorrencia = TextoCurto("Buraco na via")
    tipo_notificacao = TipoNotificacao("sim")

    alerta_regiao = AlertaRegiao(
        usuario=usuario,
        regiao=regiao,
        tipo_ocorrencia=tipo_ocorrencia,
        tipo_notificacao=tipo_notificacao,
    )

    assert alerta_regiao.usuario == usuario
    assert alerta_regiao.regiao == regiao
    assert alerta_regiao.tipo_ocorrencia == tipo_ocorrencia
    assert alerta_regiao.tipo_notificacao == tipo_notificacao
    assert alerta_regiao.para_dicionario() == {
        "usuario": str(usuario),
        "regiao": "Asa Norte",
        "tipo_ocorrencia": "Buraco na via",
        "tipo_notificacao": "sim",
    }


@pytest.mark.parametrize(
    ("usuario", "regiao", "tipo_ocorrencia", "tipo_notificacao"),
    [
        (
            "529.982.247-25",
            TextoCurto("Asa Norte"),
            TextoCurto("Buraco na via"),
            TipoNotificacao("sim"),
        )]
)
def test_alerta_regiao_rejeita_tipos_invalidos(
    usuario: object,
    regiao: object,
    tipo_ocorrencia: object,
    tipo_notificacao: object,
) -> None:
    """Deve lançar TypeError se qualquer parâmetro de AlertaRegiao não for do domínio esperado."""
    with pytest.raises(TypeError):
        AlertaRegiao(
            usuario=usuario,  # type: ignore[arg-type]
            regiao=regiao,  # type: ignore[arg-type]
            tipo_ocorrencia=tipo_ocorrencia,  # type: ignore[arg-type]
            tipo_notificacao=tipo_notificacao,  # type: ignore[arg-type]
        )

def test_acompanhamento_valido() -> None:
    """Deve instanciar Acompanhamento corretamente com entidades e domínios válidos."""
    usuario = Usuario(
        cpf=CPF("529.982.247-25"),
        nome=TextoCurto("Maria Silva"),
        email=Email("maria.silva@exemplo.com"),
        senha=Senha("A1b2c3"),
        tipo=TipoUsuario("user"),
    )
    ocorrencia = Ocorrencia(
        tipo=TextoCurto("Buraco na via"),
        descricao=TextoLongo("Buraco grande proximo ao meio fio"),
        data=Data("26/11/2026"),
        localizacao=TextoCurto("Asa Norte Quadra 102"),
    )
    notificacao_ativa = TipoNotificacao("sim")

    acompanhamento = Acompanhamento(
        usuario=usuario,
        ocorrencia=ocorrencia,
        notificacao_ativa=notificacao_ativa,
    )

    assert acompanhamento.usuario == usuario
    assert acompanhamento.ocorrencia == ocorrencia
    assert acompanhamento.notificacao_ativa == notificacao_ativa
    assert acompanhamento.para_dicionario() == {
        "usuario": str(usuario.cpf),
        "ocorrencia": str(ocorrencia.tipo),
        "notificacao_ativa": "sim",
    }


@pytest.mark.parametrize(
    ("usuario", "ocorrencia", "notificacao_ativa"),
    [
        (
            "529.982.247-25",
            Ocorrencia(
                tipo=TextoCurto("Buraco na via"),
                descricao=TextoLongo("Buraco grande proximo ao meio fio"),
                data=Data("26/11/2026"),
                localizacao=TextoCurto("Asa Norte Quadra 102"),
            ),
            TipoNotificacao("sim"),
        ),
        (
            Usuario(
                cpf=CPF("529.982.247-25"),
                nome=TextoCurto("Maria Silva"),
                email=Email("maria.silva@exemplo.com"),
                senha=Senha("A1b2c3"),
                tipo=TipoUsuario("user"),
            ),
            "Buraco na via",
            TipoNotificacao("sim"),
        ),
        (
            Usuario(
                cpf=CPF("529.982.247-25"),
                nome=TextoCurto("Maria Silva"),
                email=Email("maria.silva@exemplo.com"),
                senha=Senha("A1b2c3"),
                tipo=TipoUsuario("user"),
            ),
            Ocorrencia(
                tipo=TextoCurto("Buraco na via"),
                descricao=TextoLongo("Buraco grande proximo ao meio fio"),
                data=Data("26/11/2026"),
                localizacao=TextoCurto("Asa Norte Quadra 102"),
            ),
            "sim",
        ),
    ],
)
def test_acompanhamento_rejeita_tipos_invalidos(
    usuario: object,
    ocorrencia: object,
    notificacao_ativa: object,
) -> None:
    """Deve lançar TypeError se qualquer parâmetro de Acompanhamento tiver tipo inválido."""
    with pytest.raises(TypeError):
        Acompanhamento(
            usuario=usuario,  # type: ignore[arg-type]
            ocorrencia=ocorrencia,  # type: ignore[arg-type]
            notificacao_ativa=notificacao_ativa,  # type: ignore[arg-type]
        )