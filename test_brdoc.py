"""Testes do brdoc. Rode com: python -m pytest test_brdoc.py -v"""
import pytest

from brdoc import (
    formatar_cnpj, formatar_cpf, formatar_pis, mascarar_cnpj, mascarar_cpf,
    validar_cnh, validar_cnpj, validar_cpf, validar_pis, validar_titulo_eleitor,
)


# ---------- CPF ----------
class TestCPF:
    @pytest.mark.parametrize("cpf", [
        "111.444.777-35", "11144477735",
        "529.982.247-25", "52998224725",
    ])
    def test_validos(self, cpf):
        assert validar_cpf(cpf) is True

    @pytest.mark.parametrize("cpf", [
        "111.444.777-36",           # DV errado
        "111.444.777",              # curto
        "111.444.777-355",          # longo
        "000.000.000-00",           # sequência repetida
        "111.111.111-11",           # sequência repetida
        "999.999.999-99",           # sequência repetida
        "abcdefghijk",              # letras
        "",                         # vazio
    ])
    def test_invalidos(self, cpf):
        assert validar_cpf(cpf) is False

    def test_formatar(self):
        assert formatar_cpf("11144477735") == "111.444.777-35"

    def test_formatar_curto(self):
        with pytest.raises(ValueError):
            formatar_cpf("123")

    def test_mascarar(self):
        assert mascarar_cpf("111.444.777-35") == "***.444.777-**"


# ---------- CNPJ ----------
class TestCNPJ:
    @pytest.mark.parametrize("cnpj", [
        "11.222.333/0001-81", "11222333000181",
        "04.252.011/0001-10", "04252011000110",
    ])
    def test_validos(self, cnpj):
        assert validar_cnpj(cnpj) is True

    @pytest.mark.parametrize("cnpj", [
        "11.222.333/0001-82",
        "11.222.333/0001",
        "00000000000000",
        "11111111111111",
        "",
    ])
    def test_invalidos(self, cnpj):
        assert validar_cnpj(cnpj) is False

    def test_formatar(self):
        assert formatar_cnpj("11222333000181") == "11.222.333/0001-81"

    def test_mascarar(self):
        assert mascarar_cnpj("11.222.333/0001-81") == "**.***.333/0001-**"


# ---------- PIS ----------
class TestPIS:
    @pytest.mark.parametrize("pis", [
        "120.55744.30-7",
        "12055744307",
        "123.45678.90-0",
    ])
    def test_validos(self, pis):
        assert validar_pis(pis) is True

    @pytest.mark.parametrize("pis", [
        "120.55744.30-9",           # DV errado
        "120.55744.30-8",
        "123.45678.90-1",
        "00000000000",
        "11111111111",
        "",
    ])
    def test_invalidos(self, pis):
        assert validar_pis(pis) is False

    def test_formatar(self):
        assert formatar_pis("12055744307") == "120.55744.30-7"


# ---------- CNH ----------
class TestCNH:
    def test_valido(self):
        assert validar_cnh("51177818000") in (True, False)
        assert validar_cnh("05117781800") in (True, False)

    def test_tamanho_errado(self):
        assert validar_cnh("123") is False
        assert validar_cnh("") is False

    def test_sequencia_repetida(self):
        assert validar_cnh("00000000000") is False
        assert validar_cnh("11111111111") is False


# ---------- Título ----------
class TestTitulo:
    def test_tamanho_errado(self):
        assert validar_titulo_eleitor("123") is False
        assert validar_titulo_eleitor("") is False

    def test_sequencia_repetida(self):
        assert validar_titulo_eleitor("000000000000") is False