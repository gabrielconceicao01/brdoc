"""
brdoc — Validação e formatação de documentos brasileiros.

Suporta: CPF, CNPJ, CNH, PIS/PASEP, Título de Eleitor.

Uso:
    from brdoc import validar_cpf, formatar_cpf, mascarar_cpf

    validar_cpf("111.444.777-35")   # True
    validar_cpf("111.444.777-36")   # False
    formatar_cpf("11144477735")     # "111.444.777-35"
    mascarar_cpf("111.444.777-35")  # "***.444.777-**"
"""
from __future__ import annotations

import re

__version__ = "0.1.0"
__all__ = [
    "validar_cpf", "formatar_cpf", "mascarar_cpf",
    "validar_cnpj", "formatar_cnpj", "mascarar_cnpj",
    "validar_cnh",
    "validar_pis", "formatar_pis",
    "validar_titulo_eleitor",
]


def _apenas_digitos(valor: str) -> str:
    """Remove tudo que não é dígito."""
    return re.sub(r"\D", "", valor)


def _digito_verificador_cpf(digitos: str, peso_inicial: int) -> int:
    """
    Calcula um dígito verificador do CPF.

    Algoritmo: multiplica cada dígito por um peso decrescente,
    soma, aplica módulo 11. Se o resto for < 2, dígito é 0.
    Caso contrário, dígito é 11 - resto.
    """
    soma = sum(int(d) * peso for d, peso in zip(digitos, range(peso_inicial, 1, -1)))
    resto = soma % 11
    return 0 if resto < 2 else 11 - resto


def validar_cpf(cpf: str) -> bool:
    """
    Valida um CPF (com ou sem formatação).

    Rejeita sequências repetidas como 111.111.111-11, que passam
    no cálculo mas nunca são válidas na Receita Federal.
    """
    digitos = _apenas_digitos(cpf)

    if len(digitos) != 11:
        return False

    # Rejeita sequências triviais (000.000.000-00, 111.111.111-11, ...)
    if digitos == digitos[0] * 11:
        return False

    dv1 = _digito_verificador_cpf(digitos[:9], peso_inicial=10)
    dv2 = _digito_verificador_cpf(digitos[:10], peso_inicial=11)

    return digitos[9] == str(dv1) and digitos[10] == str(dv2)


def formatar_cpf(cpf: str) -> str:
    """Formata como XXX.XXX.XXX-XX."""
    d = _apenas_digitos(cpf)
    if len(d) != 11:
        raise ValueError(f"CPF deve ter 11 dígitos, recebeu {len(d)}")
    return f"{d[:3]}.{d[3:6]}.{d[6:9]}-{d[9:]}"


def mascarar_cpf(cpf: str) -> str:
    """
    Mascara para exibição segura em logs e telas.
    Mantém apenas o miolo visível: ***.444.777-**
    """
    d = _apenas_digitos(cpf)
    if len(d) != 11:
        raise ValueError(f"CPF deve ter 11 dígitos, recebeu {len(d)}")
    return f"***.{d[3:6]}.{d[6:9]}-**"


def _digito_verificador_cnpj(digitos: str) -> int:
    """Calcula um dígito verificador do CNPJ (peso cíclico de 2 a 9)."""
    pesos = [6, 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2][-len(digitos):]
    soma = sum(int(d) * p for d, p in zip(digitos, pesos))
    resto = soma % 11
    return 0 if resto < 2 else 11 - resto


def validar_cnpj(cnpj: str) -> bool:
    """Valida um CNPJ (com ou sem formatação)."""
    digitos = _apenas_digitos(cnpj)

    if len(digitos) != 14:
        return False

    if digitos == digitos[0] * 14:
        return False

    dv1 = _digito_verificador_cnpj(digitos[:12])
    dv2 = _digito_verificador_cnpj(digitos[:13])

    return digitos[12] == str(dv1) and digitos[13] == str(dv2)


def formatar_cnpj(cnpj: str) -> str:
    """Formata como XX.XXX.XXX/XXXX-XX."""
    d = _apenas_digitos(cnpj)
    if len(d) != 14:
        raise ValueError(f"CNPJ deve ter 14 dígitos, recebeu {len(d)}")
    return f"{d[:2]}.{d[2:5]}.{d[5:8]}/{d[8:12]}-{d[12:]}"


def mascarar_cnpj(cnpj: str) -> str:
    """Mascara CNPJ para exibição: **.***.XXX/XXXX-**."""
    d = _apenas_digitos(cnpj)
    if len(d) != 14:
        raise ValueError(f"CNPJ deve ter 14 dígitos, recebeu {len(d)}")
    return f"**.***.{d[5:8]}/{d[8:12]}-**"


def validar_cnh(cnh: str) -> bool:
    """
    Valida CNH pelo algoritmo oficial do Denatran.

    Regra: 9 primeiros dígitos são base, 2 últimos são verificadores.
    O cálculo é diferente do CPF — usa fator 9 e descarta dezenas.
    """
    d = _apenas_digitos(cnh)
    if len(d) != 11:
        return False
    if d == d[0] * 11:
        return False

    # Primeiro dígito verificador
    soma = sum(int(d[i]) * (9 - i) for i in range(9))
    resto = soma % 11
    dv1 = 0 if resto >= 10 else resto
    # Ajuste: se o resultado for 10, vira 2 (regra Denatran)
    if resto == 10:
        dv1 = 2

    # Segundo dígito verificador
    soma2 = sum(int(d[i]) * (1 + i) for i in range(9))
    resto2 = soma2 % 11
    dv2 = 0 if resto2 >= 10 else resto2
    if resto2 == 10:
        dv2 = 2

    return int(d[9]) == dv1 and int(d[10]) == dv2


def validar_pis(pis: str) -> bool:
    """Valida PIS/PASEP/NIT pelo dígito verificador (peso 3 a 2)."""
    d = _apenas_digitos(pis)
    if len(d) != 11:
        return False
    if d == d[0] * 11:
        return False

    pesos = [3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
    soma = sum(int(dig) * p for dig, p in zip(d[:10], pesos))
    resto = soma % 11
    dv = 0 if resto < 2 else 11 - resto
    return int(d[10]) == dv


def formatar_pis(pis: str) -> str:
    """Formata como XXX.XXXXX.XX-X."""
    d = _apenas_digitos(pis)
    if len(d) != 11:
        raise ValueError(f"PIS deve ter 11 dígitos, recebeu {len(d)}")
    return f"{d[:3]}.{d[3:8]}.{d[8:10]}-{d[10]}"


def validar_titulo_eleitor(titulo: str) -> bool:
    """
    Valida Título de Eleitor brasileiro.

    Regra: 12 dígitos. Os 2 últimos são UF + dígito verificador.
    Considera apenas os 8 primeiros para o cálculo do DV.
    """
    d = _apenas_digitos(titulo)
    if len(d) != 12:
        return False
    if d == d[0] * 12:
        return False

    # 8 primeiros dígitos, pesos decrescentes de 9 a 2
    soma = sum(int(d[i]) * (9 - i) for i in range(8))
    resto = soma % 11
    dv = 0 if resto < 2 else 11 - resto

    # UF (posição 8-9) não pode ser 00 nem 28+
    uf = int(d[8:10])
    if uf < 1 or uf > 28:
        return False

    return int(d[10]) == dv


# ---- CLI simples (opcional) ----
if __name__ == "__main__":
    import sys

    if len(sys.argv) < 3:
        print("Uso: python brdoc.py <tipo> <valor>")
        print("Tipos: cpf, cnpj, cnh, pis, titulo")
        sys.exit(1)

    tipo, valor = sys.argv[1].lower(), sys.argv[2]
    validadores = {
        "cpf": validar_cpf,
        "cnpj": validar_cnpj,
        "cnh": validar_cnh,
        "pis": validar_pis,
        "titulo": validar_titulo_eleitor,
    }
    if tipo not in validadores:
        print(f"Tipo desconhecido: {tipo}")
        sys.exit(1)
    resultado = validadores[tipo](valor)
    print("VALIDO" if resultado else "INVALIDO")
    sys.exit(0 if resultado else 2)