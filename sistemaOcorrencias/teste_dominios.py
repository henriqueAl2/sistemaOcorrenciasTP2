"""Testes unitários para validação dos domínios do sistema."""
from typing import Any
import pytest
from dominios import CPF, Email, Senha, TipoNotificacao, TipoUsuario, TextoCurto, TextoLongo, Data


def test_cpf_valido() -> None:
    """Deve aceitar CPF com 11 dígitos numéricos no formato 000.000.000-00."""
    cpf = CPF("123.456.789-00")
    assert cpf.valor == "123.456.789-00"
    assert str(cpf) == "123.456.789-00"


@pytest.mark.parametrize(
    "entrada_invalida",
    [
        "",                   # String vazia
        "12345678900",        # Apenas números (sem pontos e hífen)
        "123.456.789.00",     # Separadores trocados (ponto no lugar do hífen)
        "123-456-789-00",     # Separadores trocados (hífen no lugar dos pontos)
        "12.345.678-90",      # Fronteira inferior (10 dígitos)
        "123.456.789-000",    # Fronteira superior (12 dígitos)
        "123.456.78a-00",     # Caractere não numérico
        " 123.456.789-00 ",   # Espaços nas extremidades
        None,                 # Valor nulo
        12345678900,          # Tipo inteiro em vez de string
        "123.a46.789-00"      # Letra inserida 
    ],
)

def test_cpf_invalido(entrada_invalida: Any) -> None:
    """Deve lançar ValueError quando o CPF não seguir o formato 000.000.000-00."""
    with pytest.raises(ValueError):
        CPF(entrada_invalida)

def test_senha_valida () -> None:
    """Senha deve aceitar senha com 6 caracteres, 
    incluindo letras (maisculas e minusculas) e digitos numericos. 
    Letra nao pode serguir letra e digito nao pode seguir digito"""
    senha = Senha("A1b2c3")
    assert senha.valor == "A1b2c3"

@pytest.mark.parametrize(
    "entrada_invalida", [
        "",  # String vazia
        "aaaaa",  # Senha menor que 6 digitos
        "aaaaaaaa",  # Senha maior que 8 digitos
        "a1b2c3",  # Senha sem caractere maisculo
        "A1B2C3"   # Senha sem caractere minusculo
        "!1b2c3" #Senha com caractere invalido
    ],
)

def test_senha_invalida(entrada_invalida: Any) -> None:
    """Deve lançar ValueError quando a senha não seguir os critérios de validação."""
    with pytest.raises(ValueError):
        Senha(entrada_invalida)

def test_email_valido () -> None:
    """Parte local pode conter letra, numero, ponto ou hifen. Não pode iniciar ou terminar com ponto ou hifen.
    Ponto ou hifen deve ser seguido por letra ou digito. Comprimento max = 64 caracteres
    Domínio é composto por uma ou mais partes separadas por ponto. Cada parte pode conter letra, digito
    ou hifen. Nao pode iniciar ou terminar com hifen. Comprimento max = 255 caracteres
    Dominio e local separado por @."""
    email = Email("parte-local@dominio.com")
    assert email.valor == "parte-local@dominio.com"

@pytest.mark.parametrize(
    "entrada_invalida", [
        "", #String vazia
        "parte-local.dominio.com", #Email sem @
        "parte-local*@dominio", #Email com caractere invalido
        (64*"parte") + ("@dominio.com"), #Email com parte local muito longa
        "parte" + "@dominio"*255, #Email com dominio muito longo
        "-email@email.com", #Email iniciando com ponto ou hifen
        "email@email.com.", #Email terminando com ponto ou hifen
    ],
)

def test_email_invalido (entrada_invalida: Any) -> None:
    """Lança ValueError quando email não seguir os criterios de validacao"""
    with pytest.raises(ValueError):
        Email(entrada_invalida)

@pytest.mark.parametrize("valor_valido", ["admin", "user"])
def test_tipo_usuario_valido(valor_valido: str) -> None:
    """Deve aceitar exatamente 'admin' ou 'user'."""
    tipo = TipoUsuario(valor_valido)
    assert tipo.valor == valor_valido
    assert str(tipo) == valor_valido


@pytest.mark.parametrize(
    "entrada_invalida",
    ["", "ADMIN", "User", " admin ", "moderador", None, 1],
)
def test_tipo_usuario_invalido(entrada_invalida: Any) -> None:
    """Deve lançar ValueError para valores fora de ('admin', 'user')."""
    with pytest.raises(ValueError):
        TipoUsuario(entrada_invalida)


@pytest.mark.parametrize("valor_valido", ["sim", "nao"])
def test_tipo_notificacao_valido(valor_valido: str) -> None:
    """Deve aceitar exatamente 'sim' ou 'nao'."""
    notif = TipoNotificacao(valor_valido)
    assert notif.valor == valor_valido
    assert str(notif) == valor_valido


@pytest.mark.parametrize(
    "entrada_invalida",
    ["", "SIM", "não", " sim ", "talvez", True, False, None],
)
def test_tipo_notificacao_invalido(entrada_invalida: Any) -> None:
    """Deve lançar ValueError para valores fora de ('sim', 'nao')."""
    with pytest.raises(ValueError):
        TipoNotificacao(entrada_invalida)

@pytest.mark.parametrize(
    "texto_valido",
    [
        "A",
        "Buraco na rua 12, perto da esquina",
        "Texto com virgula, espaco e ponto. Fim",
        "a" * 45,
    ],
)
def test_texto_curto_valido(texto_valido: str) -> None:
    """Deve aceitar textos curtos válidos até 45 caracteres."""
    texto = TextoCurto(texto_valido)
    assert texto.valor == texto_valido
    assert str(texto) == texto_valido


@pytest.mark.parametrize(
    "entrada_invalida",
    [
        "",                          # String vazia
        "a" * 46,                    # Excede limite de 45 caracteres
        ",inicio com virgula",       # Inicia com vírgula
        ".inicio com ponto",         # Inicia com ponto
        " inicio com espaco",        # Inicia com espaço
        "fim com virgula,",          # Termina com vírgula
        "fim com espaco ",           # Termina com espaço
        "virgula,,seguida",          # Vírgula seguida de vírgula
        "virgula,.seguida",          # Vírgula seguida de ponto
        "ponto.,seguido",            # Ponto seguido de vírgula
        "ponto..seguido",            # Ponto seguido de ponto
        "espaco  duplo",             # Espaço não seguido de letra/dígito
        "espaco ,virgula",           # Espaço seguido de vírgula
        "espaco .ponto",             # Espaço seguido de ponto
        "caractere@invalido",        # Caractere fora do conjunto permitido
        None,                        # Tipo inválido
    ],
)
def test_texto_curto_invalido(entrada_invalida: Any) -> None:
    """Deve lançar ValueError para textos curtos inválidos."""
    with pytest.raises(ValueError):
        TextoCurto(entrada_invalida)


def test_texto_longo_limites() -> None:
    """Deve aceitar até 255 caracteres e rejeitar 256."""
    valido = "a" * 255
    texto = TextoLongo(valido)
    assert texto.valor == valido

    with pytest.raises(ValueError):
        TextoLongo("a" * 256)

@pytest.mark.parametrize(
    "data_valida",
    [
        "01/01/2026",  # Limite inferior de ano
        "31/12/2999",  # Limite superior de ano
        "29/02/2028",  # Ano bissexto válido (2028 é divisível por 4)
        "28/02/2026",  # Fevereiro comum válido
        "30/04/2026",  # Mês com 30 dias
        "31/07/2026",  # Mês com 31 dias
    ],
)
def test_data_valida(data_valida: str) -> None:
    """Deve aceitar datas válidas no formato DD/MM/AAAA entre 2026 e 2999."""
    data = Data(data_valida)
    assert data.valor == data_valida
    assert str(data) == data_valida


@pytest.mark.parametrize(
    "entrada_invalida",
    [
        "",            # String vazia
        "2026-05-10",  # Separador inválido (ISO em vez de DD/MM/AAAA)
        "1/05/2026",   # Dia sem zero à esquerda
        "01/5/2026",   # Mês sem zero à esquerda
        "00/05/2026",  # Dia zero
        "32/01/2026",  # Dia maior que 31
        "31/04/2026",  # Abril só tem 30 dias
        "29/02/2026",  # 2026 não é bissexto
        "29/02/2100",  # 2100 não é bissexto (regra secular do calendário)
        "15/00/2026",  # Mês zero
        "15/13/2026",  # Mês maior que 12
        "31/12/2025",  # Ano abaixo de 2026
        "01/01/3000",  # Ano acima de 2999
        "aa/bb/cccc",  # Caracteres não numéricos
        None,          # Tipo inválido
    ],
)
def test_data_invalida(entrada_invalida: Any) -> None:
    """Deve lançar ValueError para datas inválidas."""
    with pytest.raises(ValueError):
        Data(entrada_invalida)