# ADR-0014: Parser próprio para arquivos OFX

- **Status:** Aceito
- **Data:** 2026-09-23
- **Relacionados:** RFC-0005, ADR-0007, ADR-0013

## Contexto

A importação de extratos OFX (RFC-0005) foi priorizada antes do Open Finance. Os
arquivos vêm de bancos brasileiros (PF: Itaú, Nubank, BTG; PJ: Itaú, InfinitePay, C6)
e têm particularidades conhecidas: codificação Windows-1252/Latin-1 declarada de forma
errada, datas com fuso `[-3:BRT]`, SGML sem fechamento de tags, vírgula decimal e
`FITID` instável em alguns bancos.

## Decisão

Vamos escrever um **parser OFX próprio**, com licença MIT como o repositório:

- Suporta OFX 1.x (SGML) e 2.x (XML). O XML é lido com `defusedxml`, sem entidades
  externas.
- Fica atrás de uma porta (`StatementFileParser`), então o domínio não depende dele e
  ele pode ser trocado no futuro.
- Devolve valores como `Decimal`/`Money` (ADR-0007) e **preserva a data do lançamento
  no fuso informado pelo banco**.
- Detecta a codificação pelo conteúdo quando o cabeçalho está errado.
- É desenvolvido em TDD, começando pelos 8 casos sintéticos documentados na RFC-0005 e
  depois com um arquivo real anonimizado de cada banco.

## Alternativas consideradas

| Opção | Por que não |
|---|---|
| `ofxtools` 1.1.1 | Licença GPL-3.0-only, incompatível com a licença MIT do repositório e com a publicação das imagens Docker. |
| `ofxparse` 0.21 | Testado em 2026-09-23 (RFC-0005): falha em OFX 2.x com acentos UTF-8 e em codificação declarada errada, e converte datas para UTC sem fuso, o que move uma compra de 31/01 às 22:00 BRT para fevereiro. Sem release desde 2021. |

## Consequências

- Mantemos um código a mais, pequeno e restrito ao subconjunto de OFX que usamos:
  conta, cartão, transações e saldo.
- Um formato novo de algum banco vira um caso de teste com o arquivo anonimizado,
  seguido do ajuste no parser.
- Sem dependência externa para OFX, além de `defusedxml`.
