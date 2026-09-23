# RFC-0006: Múltiplas moedas, câmbio e taxas (spread, IOF)

- **Status:** Em discussão
- **Autor(es):** Hitomi Growth + Claude Code
- **Criada em:** 2026-09-23
- **ADRs resultantes:** [ADR-0016](../adr/0016-multi-currency-from-day-one.md) (múltiplas moedas desde o início). A fonte de cotações ficará num ADR futuro.

## Resumo

Suportar contas, cartões e lançamentos em **qualquer moeda ISO 4217** desde a
primeira versão. Converter valores para uma **moeda de referência** nos relatórios e
registrar o **custo real do câmbio**: a taxa efetiva aplicada, o **spread** em relação
a uma cotação de referência, o **IOF** e as tarifas explícitas.

**Conclusão da análise: é viável.** O `Money` já impede misturar moedas por acidente
(ADR-0007). O trabalho novo tem três partes: dados das moedas (casas decimais), fonte
de cotações e o modelo de "operação de câmbio" com as taxas.

## Motivação

- Contas em outras moedas são comuns: conta global em dólar ou euro, corretora no
  exterior, recebimentos PJ de clientes de fora.
- Compras no exterior no cartão chegam em reais, com câmbio e IOF embutidos. Sem
  separar esses custos, o usuário não enxerga quanto pagou pela conversão.
- Um consolidado que soma reais com dólares sem converter é simplesmente errado.

## Proposta detalhada

### 1. Moedas

- Qualquer moeda ISO 4217, cada uma com **suas casas decimais** (BRL 2, JPY 0, BHD 3).
  Hoje o `Money` só habilita BRL/USD/EUR e assume 2 casas para todas. Isso muda numa
  proposta OpenSpec que altera a spec `money`.
- Fonte dos dados: **Babel** (BSD-3-Clause, v2.18.0), que traz 307 moedas, casas
  decimais e formatação por idioma. Exemplo testado: `US$ 1.234,50` em pt-BR e
  `R$1,234.50` em en-US. Para manter o domínio sem dependências (ADR-0004), a tabela
  pode ser gerada como dado estático no `shared_kernel`, e a Babel fica na formatação.
- Cada conta e cada cartão têm uma moeda. Cada usuário escolhe uma **moeda de
  referência** para relatórios, com BRL como padrão.

### 2. Cotações

| Fonte | Cobertura | Custo | Observação |
|---|---|---|---|
| **PTAX, Banco Central do Brasil** | Moedas contra o real, cotação oficial diária (compra e venda) | Gratuita, API pública | Referência natural no Brasil. Só dias úteis: em fim de semana e feriado vale a do último dia útil. |
| BCE (Banco Central Europeu) | Moedas contra o euro | Gratuita | Útil como complemento ou para cruzamento entre moedas sem par com o real. |
| APIs comerciais | Várias, intradiárias | Paga | Desnecessárias por enquanto, dado o objetivo de não ter custo recorrente. |

**Recomendação: PTAX como fonte principal.** O acesso direto não pôde ser testado a
partir do ambiente de desenvolvimento, porque a rede bloqueia os domínios do BCB e do
BCE. A validação fica como primeira tarefa da issue de cotações.

Regras:
- Cotações armazenadas localmente (data, par de moedas, compra, venda, fonte), como
  `Decimal` com precisão suficiente (a PTAX usa 4 casas). Nunca `float`.
- Busca diária agendada, mais backfill sob demanda para datas antigas, por exemplo ao
  importar um OFX antigo.
- Conversão entre duas moedas estrangeiras passa pelo real (ex.: EUR → BRL → USD), com
  a regra registrada.

### 3. Operação de câmbio e taxas

Três situações reais, com o mesmo modelo:

| Situação | Exemplo | O que o app registra |
|---|---|---|
| **Compra no exterior no cartão em reais** | US$ 100 num site americano, fatura cobra R$ 5.xx | Valor original (USD), valor cobrado (BRL), **IOF** (linha da fatura), taxa efetiva e **spread** implícito |
| **Conversão entre contas próprias** | R$ 5.000 da conta Itaú para a conta global em USD | Débito em BRL, crédito em USD, tarifas, taxa efetiva, spread e IOF |
| **Lançamento numa conta em moeda estrangeira** | Assinatura de US$ 20 debitada da conta em USD | Só o valor em USD. A conversão acontece apenas nos relatórios. |

Conceito de domínio proposto, `FxDetails`, anexado ao lançamento ou à transferência:

```
original:        Money   # ex.: 100.00 USD
charged:         Money   # ex.: 540.00 BRL (antes do IOF)
effective_rate:  Decimal # charged / original          → 5.40
reference_rate:  Decimal # PTAX venda da data          → 5.10
reference_source: "PTAX" + data
spread_cost:     Money   # charged − original × reference → 30.00 BRL
spread_pct:      Decimal # effective / reference − 1    → 5,88%
fees:            [ {kind: iof | service | wire | other, amount: Money} ]
total_cost_of_fx: Money  # spread_cost + soma das fees
```

- O **valor efetivamente cobrado** vem do extrato ou da fatura (digitado ou importado).
  O app **calcula** o spread comparando com a cotação de referência. O spread nunca é
  "inventado".
- **IOF:** as alíquotas sobre cartão internacional e câmbio mudaram várias vezes nos
  últimos anos. O app guarda o IOF **efetivamente cobrado** como uma taxa do lançamento.
  A alíquota vigente fica como **parâmetro com data de vigência**, usado só para estimar
  (previsão, sugestão ao digitar), e deve ser conferida na legislação antes de cada
  cadastro.
- No cartão, o IOF costuma vir como uma **linha separada** na fatura. A importação
  (OFX/CSV) permite vincular essa linha à compra original como taxa.

### 4. Relatórios e previsão

- **Consolidado na moeda de referência.** Receitas e despesas são convertidas pela
  cotação **da data do lançamento**, ou pelo valor cobrado em reais quando existir.
  Saldos são convertidos pela cotação **da data do relatório**.
- **Variação cambial:** a diferença de valor de um saldo em moeda estrangeira entre
  duas datas aparece como linha própria, não como receita ou despesa.
- Todo valor convertido é **sinalizado** na interface ("convertido a PTAX de dd/mm"),
  sempre com o valor original disponível.
- **Custo do câmbio** vira um relatório: quanto se pagou de spread, IOF e tarifas por
  período e por instituição. Isso responde se vale a pena usar o cartão ou uma conta
  global.
- **Previsão:** valores futuros em moeda estrangeira são convertidos pela última
  cotação disponível e marcados como estimativa.
- **Orçamentos:** definidos na moeda de referência. Despesas em outras moedas contam
  pelo valor convertido.

### 5. Onde fica no código

| Parte | Local |
|---|---|
| `Money`, `Currency` (ISO 4217 completo), `ExchangeRate` (value object) | `shared_kernel` |
| Busca e armazenamento de cotações, conversão | **novo contexto `exchange`**, com uma porta `RateProvider` e o adaptador PTAX |
| `FxDetails` e taxas no lançamento | `ledger` |
| Moeda de referência do usuário | `identity` (preferências) |
| Consolidado convertido, variação cambial, custo do câmbio | `reporting`, que consulta `exchange` pela camada `application` |

Um contexto separado segue a mesma lógica dos outros dados externos: a fonte pode ser
trocada sem afetar `ledger` e `reporting`.

## Alternativas

| Opção | Por que não |
|---|---|
| Só BRL no início, multimoeda depois | Descartada pelo dono do produto. Migrar dados de moeda única para multimoeda depois é caro e arriscado. |
| Converter tudo para BRL no momento do lançamento | Perde o valor original e distorce saldos em moeda estrangeira. |
| Registrar só o valor em BRL da fatura | Esconde o custo do câmbio, que é justamente o que o usuário quer ver. |
| `py-moneyed` para o `Money` | Sem release desde 2022, e nosso `Money` já cobre as regras de domínio. Basta completar a tabela de moedas. |

## Perguntas em aberto

- [ ] Fonte de cotações: PTAX como principal (recomendado) e BCE como complemento?
- [ ] Cotação de referência para o spread: **PTAX venda** do dia da compra (recomendado), ou do dia do fechamento/pagamento da fatura? *Padrão provisório: dia da compra, aguardando confirmação do dono do produto.*
- [x] Moedas em uso: **BRL, USD e EUR** (2026-09-23). São os casos de teste prioritários. As demais moedas ISO 4217 continuam suportadas.
- [x] Relatório de custo do câmbio: **depois da primeira versão** (2026-09-23). Issue #32 com label `adiado`. Os dados (`FxDetails`) continuam sendo registrados desde o início, então o relatório pode ser feito depois sem migração.

## Fora de escopo

Criptomoedas (não são ISO 4217), cotação intradiária em tempo real, operações de
câmbio pelo app (compra ou venda de moeda), contabilidade de hedge.
