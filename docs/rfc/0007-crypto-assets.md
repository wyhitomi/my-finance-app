# RFC-0007: Criptoativos e stablecoins no patrimônio

- **Status:** Em discussão
- **Autor(es):** Hitomi Growth + Claude Code
- **Criada em:** 2026-09-23
- **ADRs resultantes:** a criar, após responder as perguntas em aberto

## Resumo

Incluir criptoativos e stablecoins (ex.: USDG, USDT, USDC) no **patrimônio** do
usuário: quanto ele tem de cada ativo e quanto isso vale hoje na moeda de referência.
O objetivo decidido é **só patrimônio** (2026-09-23). Cálculo de imposto, preço médio
e ganho de capital ficam fora desta RFC.

Cripto entra como **ativo de investimento** (quantidade × preço), e **não** como mais
uma moeda do `Money`.

## Motivação

- O patrimônio real inclui o que está em cripto. Sem isso, o consolidado fica
  incompleto.
- Stablecoins como a USDG são usadas como "dólar digital". O usuário quer ver esse
  valor junto do resto, em reais.

## Por que ativo, e não moeda

| | Moeda (`Money`) | Criptoativo |
|---|---|---|
| Identificador | ISO 4217 (BRL, USD, EUR) | Símbolo sem padrão oficial. O mesmo símbolo pode existir em várias redes. |
| Precisão | 0 a 3 casas | Até 8 (BTC) ou 18 (ETH e muitos tokens) |
| O que se guarda | Saldo | **Quantidade**, com o valor calculado pelo preço do momento |
| Volatilidade | Baixa a média | Alta (exceto stablecoins) |

Misturar isso no `Money` quebraria as regras do ADR-0007 e do ADR-0016 (casas
decimais ISO, soma só na mesma moeda). Então o modelo é separado:

```
Asset           id, symbol (ex.: BTC, USDG), name, network (opcional), decimals,
                kind: crypto | stablecoin, peg: USD (só stablecoin)
AssetQuantity   asset + Decimal (precisão do ativo)
Holding         conta/carteira + ativo + quantidade atual
AssetPrice      ativo, moeda de cotação (USD ou BRL), preço Decimal, data/hora, fonte
Valuation       quantidade × preço → Money (na moeda da cotação), convertido para a
                moeda de referência pelo contexto exchange (PTAX, RFC-0006)
```

- Persistência da quantidade em `NUMERIC(38,18)`. O `NUMERIC(19,4)` do ADR-0005 é
  para dinheiro e não comporta 18 casas.

## Proposta detalhada

### Escopo da primeira versão (só patrimônio)

1. **Carteiras e contas de cripto** do titular (PF ou PJ): corretora ou carteira própria.
   Cada uma com os ativos e as quantidades.
2. **Registro manual das movimentações:** compra, venda, recebimento, envio,
   conversão. A quantidade atual é a soma das movimentações. Também é possível
   informar só o saldo atual, para quem quer começar rápido.
3. **Valor atual** de cada posição e do total, na moeda de referência, com a cotação,
   a fonte e o horário visíveis.
4. **Patrimônio consolidado:** contas + cripto, com cripto como linha própria. A
   variação de preço aparece como valorização/desvalorização, nunca como receita ou
   despesa (mesma lógica da variação cambial da RFC-0006).

### Stablecoins (USDG e similares)

- Cadastradas com `kind = stablecoin` e `peg = USD`.
- **Valor padrão: 1 unidade = 1 USD**, convertido para reais pela **PTAX** (RFC-0006).
  É a fonte oficial, gratuita e já prevista no app.
- **Alerta de desvio de paridade:** se o preço de mercado disponível se afastar do
  dólar além de um limite (ex.: 2%), o app avisa e mostra os dois valores. Stablecoins
  podem perder a paridade, e esconder isso seria enganoso.

### Cotações de cripto

| Opção | Custo | Observação |
|---|---|---|
| **CoinGecko** (plano gratuito) | Gratuito, com limite de requisições | Ampla cobertura de ativos e stablecoins |
| API pública de corretora (ex.: Binance, Mercado Bitcoin) | Gratuita | Cobre só os pares negociados ali |

**Recomendação:** um adaptador atrás de uma porta `AssetPriceProvider` no contexto
`exchange`, com cotações diárias guardadas localmente (a mesma lógica da PTAX).
Cobertura, limites e disponibilidade de ativos como a USDG ainda não foram validados:
a rede do ambiente de desenvolvimento bloqueia APIs externas. Isso fica como primeira
tarefa da issue de cotações de cripto.

### Onde fica no código

| Parte | Local |
|---|---|
| `Asset`, `AssetQuantity`, `Holding`, movimentações | **novo contexto `investments`** (cripto é o primeiro tipo de ativo; ações e FIIs podem vir depois) |
| `AssetPrice` e o adaptador de cotações de cripto | `exchange` (junto da PTAX) |
| Patrimônio consolidado com cripto | `reporting` |

### Segurança

- **Nunca** pedir ou guardar chave privada, frase-semente (seed) ou senha de corretora.
- Integração futura com corretora: só chaves de API **somente leitura**, guardadas
  criptografadas. Carteira própria: só o **endereço público**.

## Evoluções futuras (fora desta RFC)

- Importação de CSV das corretoras (reaproveitando o assistente da issue #28).
- Leitura de saldo de carteira própria pelo endereço público (blockchain explorer).
- Preço médio, ganho realizado e relatório de apoio ao IR, se o objetivo mudar.
- Outros ativos de investimento (ações, FIIs, renda fixa) no mesmo contexto.

## Alternativas

| Opção | Por que não |
|---|---|
| Cripto como moeda do `Money` | Casas decimais e natureza diferentes. Quebraria as regras de moeda dos ADRs 0007 e 0016. |
| Stablecoin valorizada só pelo preço de mercado | Depende de uma fonte a mais para um valor que, na prática, é 1 USD. A paridade com alerta de desvio é mais simples e mais honesta. |
| Stablecoin como conta em USD | Esconde o risco de perda de paridade e a rede ou emissor do token. |

## Perguntas em aberto

- [x] Objetivo: **só patrimônio** (2026-09-23).
- [x] Stablecoins: **sim**, ex.: USDG (2026-09-23).
- [ ] Onde estão os ativos hoje: quais corretoras e/ou carteiras próprias (e em quais redes)?
- [ ] Prioridade: depois do núcleo (contas, lançamentos, OFX, orçamentos, relatórios), como recomendado, ou antes?
- [ ] Limite do alerta de desvio de paridade das stablecoins: 2% está bom?

## Fora de escopo

Cálculo de imposto, preço médio e ganho de capital; DeFi, staking e rendimentos;
NFTs; negociação ou envio de cripto pelo app.
