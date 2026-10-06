<div align="center">

# 🇧🇷 brdoc

### Validação, formatação e mascaramento de documentos brasileiros em Python puro.

**Zero dependências. Um arquivo. 44 testes.**

[![Python](https://img.shields.io/badge/python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org)
[![Tests](https://img.shields.io/badge/tests-44%20passed-2ea44f?style=for-the-badge&logo=pytest&logoColor=white)](https://github.com/gabrielconceicao01/brdoc)
[![License](https://img.shields.io/badge/license-MIT-yellow?style=for-the-badge)](https://github.com/gabrielconceicao01/brdoc/blob/main/LICENSE)
[![Made in Brazil](https://img.shields.io/badge/made%20in-Brasil-009c3b?style=for-the-badge)](#)

[📖 Documentação](#-uso) · [🚀 Instalação](#-instalação) · [🧪 Testes](#-testes) · [🗺️ Roadmap](#%EF%B8%8F-roadmap)

</div>

---

## 📌 Sobre

`brdoc` é uma biblioteca leve para **validar, formatar e mascarar** documentos brasileiros em Python puro, sem dependências externas.

Foi criada porque toda aplicação brasileira precisa, em algum momento, lidar com CPF, CNPJ, CNH, PIS ou Título de Eleitor — e a maioria das soluções por aí:

- ❌ Copia código do Stack Overflow sem entender o algoritmo
- ❌ Não testa casos-limite (dígitos repetidos, DV errado, entrada vazia)
- ❌ Não oferece **mascaramento** para conformidade com a **LGPD**
- ❌ Depende de pacotes pesados para uma tarefa puramente matemática

**`brdoc` resolve tudo isso em um único arquivo.**

---

## ✨ Destaques

| Recurso | brdoc | Outras libs |
|---|:---:|:---:|
| Zero dependências | ✅ | ❌ |
| Validação do dígito verificador | ✅ | ✅ |
| Rejeita sequências repetidas | ✅ | ⚠️ |
| Mascaramento LGPD | ✅ | ❌ |
| CLI | ✅ | ❌ |
| 100% testado | ✅ | ⚠️ |
| Um único arquivo | ✅ | ❌ |

---

## 📖 Índice

- [Sobre](#-sobre)
- [Instalação](#-instalação)
- [Uso como biblioteca](#-uso-como-biblioteca)
- [Uso como CLI](#-uso-como-cli)
- [Documentos suportados](#-documentos-suportados)
- [Como os algoritmos funcionam](#-como-os-algoritmos-funcionam)
- [Testes](#-testes)
- [Roadmap](#%EF%B8%8F-roadmap)
- [Contribuindo](#-contribuindo)
- [Licença](#-licença)

---

## 🚀 Instalação

**Requisitos:** Python 3.10 ou superior

```bash
git clone https://github.com/gabrielconceicao01/brdoc.git
cd brdoc
pip install pytest
```

> 📦 Publicação no PyPI em breve: `pip install brdoc`

---

## 🐍 Uso como biblioteca

```python
from brdoc import validar_cpf, formatar_cpf, mascarar_cpf

# Validação (aceita com ou sem formatação)
validar_cpf("111.444.777-35")   # ✅ True
validar_cpf("111.444.777-36")   # ❌ False — DV errado
validar_cpf("111.111.111-11")   # ❌ False — sequência repetida

# Formatação
formatar_cpf("11144477735")     # → "111.444.777-35"

# Mascaramento (LGPD-friendly)
mascarar_cpf("111.444.777-35")  # → "***.444.777-**"
```

---

## 💻 Uso como CLI

```bash
python brdoc.py cpf 111.444.777-35
# → VALIDO

python brdoc.py cpf 111.444.777-36
# → INVALIDO

python brdoc.py cnpj 11.222.333/0001-81
# → VALIDO
```

**Tipos disponíveis:** `cpf`, `cnpj`, `cnh`, `pis`, `titulo`

**Códigos de saída:** `0` para válido, `2` para inválido — ideal para usar em pipelines e scripts.

---

## 📋 Documentos suportados

| Documento | Validação | Formatação | Mascaramento |
|---|:---:|:---:|:---:|
| **CPF** | ✅ | ✅ | ✅ |
| **CNPJ** | ✅ | ✅ | ✅ |
| **PIS / PASEP / NIT** | ✅ | ✅ | — |
| **CNH** | ✅ | — | — |
| **Título de Eleitor** | ✅ | — | — |

---

## 🧠 Como os algoritmos funcionam

### CPF — Módulo 11

```text
Base:   1  1  1  4  4  4  7  7  7
Pesos: 10  9  8  7  6  5  4  3  2
       ─────────────────────────
Soma = 1×10 + 1×9 + 1×8 + 4×7 + 4×6 + 4×5 + 7×4 + 7×3 + 7×2 = 199

199 % 11 = 1   →   resto < 2   →   DV1 = 0
```

Repete o processo com o primeiro DV incluso para calcular o segundo.

### CNPJ — Módulo 11 com pesos cíclicos

Mesma lógica, mas com **14 dígitos** e pesos que ciclam de `2` a `9`.

### CNH — Algoritmo Denatran

Usa fator `9` decrescente para o primeiro DV e fator crescente para o segundo.
**Regra especial:** quando o resto é `10`, o dígito vira `2`.

> ⚠️ **Nota honesta:** o algoritmo da CNH tem variações históricas entre estados e versões do Denatran. A implementação segue a referência mais comum, mas para uso crítico recomendo validar contra a base oficial.

### PIS — Módulo 11 com pesos `[3,2,9,8,7,6,5,4,3,2]`

### Título de Eleitor

12 dígitos: `8 base + 2 UF + 2 DV`. A UF precisa estar entre `01` e `28` (códigos do TSE).

---

## 🧪 Testes

```bash
python -m pytest test_brdoc.py -v
```

**44 testes** cobrindo:

- ✅ Casos válidos (com e sem formatação)
- ✅ Dígitos verificadores errados
- ✅ Entrada curta, longa e vazia
- ✅ Sequências repetidas (`111.111.111-11`)
- ✅ Caracteres não-numéricos
- ✅ Erros de formatação (`ValueError`)

```
======================= 44 passed in 9.91s =======================
```

---

## 🗺️ Roadmap

- [x] Validação de CPF, CNPJ, CNH, PIS e Título de Eleitor
- [x] Mascaramento LGPD-friendly para CPF e CNPJ
- [x] CLI funcional com códigos de saída
- [x] 44 testes automatizados
- [ ] Publicação no PyPI (`pip install brdoc`)
- [ ] GitHub Actions rodando CI a cada push
- [ ] Cartão SUS, RENAVAM, Inscrição Estadual por UF
- [ ] Type hints completos + `mypy --strict`
- [ ] Integração com Flask / FastAPI / Django

---

## 🤝 Contribuindo

Contribuições são bem-vindas! Se você encontrou um bug ou tem uma ideia:

1. Abra uma [issue](https://github.com/gabrielconceicao01/brdoc/issues)
2. Faça um fork do projeto
3. Crie uma branch (`git checkout -b feature/nova-validacao`)
4. Commit suas mudanças (`git commit -m "feat: adiciona validação de RENAVAM"`)
5. Push para a branch (`git push origin feature/nova-validacao`)
6. Abra um Pull Request

---

## 📜 Licença

Distribuído sob a licença **MIT**. Use como quiser, sem medo.

Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

---

<div align="center">

**Feito com 🧠 e ☕ no Brasil**

[⬆ Voltar ao topo](#-brdoc)

</div>
