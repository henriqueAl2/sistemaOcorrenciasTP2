from datetime import date

class CPF:
    """Implementação da validação e armazenamento do domínio CPF."""

    def __init__(self, valor: str) -> None:
        if not self.eh_valido(valor):
            raise ValueError(
                "CPF inválido: deve conter 11 dígitos no formato 000.000.000-00."
            )
        self.valor = valor

    def eh_valido(self, valor: str) -> bool:
        """Verifica se a string segue exatamente o formato 000.000.000-00."""
        if not isinstance(valor, str) or len(valor) != 14:
            return False

        if valor[3] != "." or valor[7] != "." or valor[11] != "-":
            return False

        apenas_numeros = valor.replace(".", "").replace("-", "")
        return len(apenas_numeros) == 11 and apenas_numeros.isdigit()

    def __str__(self) -> str:
        return self.valor

class Senha:
    """Implementação da validação e armazenamento do domínio Senha."""
    def __init__(self, valor: str) -> None:
        if not self.eh_valido(valor):
            raise ValueError(
                "Senha inválida: deve conter 6 caracteres, " \
                "incluindo letras maiúsculas, minúsculas e dígitos numéricos"
            )
        self.valor = valor

    def eh_valido (self, valor: str) -> bool:
        """Verifica se cumpre os requisitos de validação"""
        if not isinstance(valor, str) or len(valor) != 6:
            return False
        verifica_maiusculo = any(c.isupper() for c in valor)
        verifica_minusculo = any(c.islower() for c in valor)
        verifica_digito = any(c.isdigit() for c in valor)
        if verifica_maiusculo == False:
            return False
        if verifica_minusculo == False:
            return False
        if verifica_digito == False:
            return False
        for i in range(len(valor)-1):
            if valor[i].isalpha() and valor[i+1].isalpha():
                return False
            if valor[i].isdigit() and valor[i+1].isdigit():
                return False      
        return True

    def __str__(self) -> str:
        return self.valor

class Email:
    """Implementação da validação e armazenamento do domínio Email."""

    def __init__(self, valor: str) -> None:
        if not self._eh_valido(valor):
            raise ValueError("E-mail inválido conforme a especificação.")
        self.valor = valor

    def _eh_valido(self, valor: str) -> bool:
        """Valida estrutura geral, parte local e domínio do e-mail."""
        if not isinstance(valor, str) or valor.count("@") != 1:
            return False

        parte_local, dominio = valor.split("@")
        return (
            self._parte_local_valida(parte_local)
            and self._dominio_valido(dominio)
        )

    def _parte_local_valida(self, local: str) -> bool:
        """Valida regras da parte local (antes do @)."""
        if not 1 <= len(local) <= 64:
            return False

        if local[0] in ".-" or local[-1] in ".-":
            return False

        anterior_separador = False
        for char in local:
            if char.isalnum():
                anterior_separador = False
            elif char in ".-":
                if anterior_separador:
                    return False
                anterior_separador = True
            else:
                return False

        return True

    def _dominio_valido(self, dominio: str) -> bool:
        """Valida regras do domínio (depois do @)."""
        if not 1 <= len(dominio) <= 255:
            return False

        partes = dominio.split(".")
        for parte in partes:
            if not parte or parte.startswith("-") or parte.endswith("-"):
                return False
            if not all(char.isalnum() or char == "-" for char in parte):
                return False

        return True

    def __str__(self) -> str:
        return self.valor

    def dominio_valido(self, dominio: str) -> bool:
        """Valida regras do domínio (depois do @)."""
        if not 1 <= len(dominio) <= 255:
            return False

        partes = dominio.split(".")
        for parte in partes:
            if not parte or parte.startswith("-") or parte.endswith("-"):
                return False
            if not all(char.isalnum() or char == "-" for char in parte):
                return False

        return True

    def __str__(self) -> str:
        return self.valor

class TipoUsuario:
    """Implementação da validação do domínio TipoUsuario."""

    VALORES_PERMITIDOS = ("admin", "user")

    def __init__(self, valor: str) -> None:
        if not isinstance(valor, str) or valor not in self.VALORES_PERMITIDOS:
            raise ValueError(
                "Tipo de usuário inválido: deve ser 'admin' ou 'user'."
            )
        self.valor = valor

    def __str__(self) -> str:
        return self.valor

class TipoNotificacao:
    """Implementação da validação do domínio TipoNotificacao."""

    VALORES_PERMITIDOS = ("sim", "nao")

    def __init__(self, valor: str) -> None:
        if not isinstance(valor, str) or valor not in self.VALORES_PERMITIDOS:
            raise ValueError(
                "Tipo de notificação inválido: deve ser 'sim' ou 'nao'."
            )
        self.valor = valor

    def __str__(self) -> str:
        return self.valor

class Texto:
    """Implementação base da validação e armazenamento de domínios de texto."""

    TAMANHO_MAXIMO: int = 0

    def __init__(self, valor: str) -> None:
        if not self._eh_valido(valor):
            raise ValueError(
                f"Texto inválido: deve ter entre 1 e {self.TAMANHO_MAXIMO} caracteres "
                "e respeitar as regras de pontuação e espaçamento."
            )
        self.valor = valor

    def _eh_valido(self, valor: str) -> bool:
        """Verifica tamanho, caracteres permitidos, bordas e sequência."""
        if not isinstance(valor, str):
            return False

        if not 1 <= len(valor) <= self.TAMANHO_MAXIMO:
            return False

        if valor[0] in ",. " or valor[-1] in ",. ":
            return False

        for indice, atual in enumerate(valor):
            if not self._caractere_permitido(atual):
                return False

            if indice < len(valor) - 1:
                proximo = valor[indice + 1]
                if not self._sequencia_valida(atual, proximo):
                    return False

        return True

    @staticmethod
    def _caractere_permitido(caractere: str) -> bool:
        """Verifica se o caractere é letra, dígito, vírgula, ponto ou espaço."""
        return caractere.isalnum() or caractere in ",. "

    @staticmethod
    def _sequencia_valida(atual: str, proximo: str) -> bool:
        """Valida as regras de adjacência entre dois caracteres consecutivos."""
        if atual in ",." and proximo in ",.":
            return False

        if atual == " " and not proximo.isalnum():
            return False

        return True

    def __str__(self) -> str:
        return self.valor


class TextoCurto(Texto):
    """Implementação do domínio TextoCurto (máximo 45 caracteres)."""

    TAMANHO_MAXIMO: int = 45


class TextoLongo(Texto):
    """Implementação do domínio TextoLongo (máximo 255 caracteres)."""

    TAMANHO_MAXIMO: int = 255



class Data:
    """Implementação da validação e armazenamento do domínio Data."""

    def __init__(self, valor: str) -> None:
        if not self._eh_valido(valor):
            raise ValueError(
                "Data inválida: deve estar no formato DD/MM/AAAA entre 2026 e 2999."
            )
        self.valor = valor

    def _eh_valido(self, valor: str) -> bool:
        """Verifica formato DD/MM/AAAA, existência no calendário e intervalo de ano."""
        if not isinstance(valor, str) or len(valor) != 10:
            return False

        if valor[2] != "/" or valor[5] != "/":
            return False

        partes = valor.split("/")
        if not all(parte.isdigit() for parte in partes):
            return False

        dia, mes, ano = int(partes[0]), int(partes[1]), int(partes[2])

        if not 2026 <= ano <= 2999:
            return False

        try:
            date(ano, mes, dia)
        except ValueError:
            return False

        return True

    def __str__(self) -> str:
        return self.valor