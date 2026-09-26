<div align="center">

# 🇧🇷 brdoc

### Validação, formatação e mascaramento de documentos brasileiros em Python puro.

**Zero dependências. Um arquivo. 44 testes.**

[![Python](https://img.shields.io/badge/python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org)
[![Tests](https://img.shields.io/badge/tests-44%20passed-2ea44f?style=for-the-badge&logo=pytest&logoColor=white)](https://github.com/gabrielconceicao01/brdoc)
[![License](https://img.shields.io/badge/license-MIT-yellow?style=for-the-badge)](https://github.com/gabrielconceicao01/brdoc/blob/main/LICENSE)
[![Made in Brazil](https://img.shields.io/badge/made%20in-Brasil-009c3b?style=for-the-badge&logo=flags&logoColor=white)](#)

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
| Validação por dígito verificador | ✅ | ✅ |
| Rejeita sequências repetidas | ✅ | ⚠️ |
| Mascaramento LGPD | ✅ | ❌ |
| CLI pronta | ✅ | ❌ |
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

**Requisitos:** Python 3.10+

```bash
git clone https://github.com/gabrielconceicao01/brdoc.git
cd brdoc
pip install pytest
