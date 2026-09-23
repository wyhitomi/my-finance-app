# ADR-0018: Criptoativos como ativos de investimento, só no patrimônio

- **Status:** Aceito
- **Data:** 2026-09-23
- **Relacionados:** RFC-0007, ADR-0007, ADR-0016, ADR-0004

## Contexto

O usuário tem criptoativos e stablecoins (ex.: USDG) em plataformas custodiais (OKX,
Mercado Bitcoin, Coinbase, BitGo) e em carteira de autocustódia (MetaMask, em redes
compatíveis com Ethereum). O objetivo decidido é mostrar esse valor no **patrimônio**,
sem cálculo de imposto. A entrega fica **depois do núcleo** do produto.

## Decisão

1. Criptoativos e stablecoins são **ativos de investimento** (quantidade × preço) num
   novo contexto `investments`. Eles **não** são moedas do `Money`, cujas regras
   (ADR-0007, ADR-0016) valem só para moedas ISO 4217.
2. Modelo: `Asset` (símbolo, rede, casas decimais, `crypto | stablecoin`, `peg`),
   `Wallet` (titular, instituição ou endereço, custódia `custodial | self_custody`),
   `Holding` (carteira + ativo + rede + quantidade) e movimentações. Quantidades em
   `Decimal`, persistidas em `NUMERIC(38,18)`.
3. Valorização: quantidade × preço de mercado (`AssetPrice`, contexto `exchange`),
   convertida para a moeda de referência pela PTAX. Valorização e desvalorização nunca
   contam como receita ou despesa.
4. Stablecoins valem **1 unidade da moeda de paridade** (ex.: 1 USD), convertidas pela
   PTAX. O app alerta quando o preço de mercado se afasta **mais de 2%** da paridade.
5. **Nunca** pedir nem guardar chave privada, frase-semente ou senha. Integrações
   futuras usam só endereço público (autocustódia) ou chaves de API somente leitura,
   guardadas criptografadas (custodial).
6. Fora de escopo: imposto, preço médio, ganho de capital, DeFi, staking, NFTs e
   qualquer operação de envio ou negociação.

## Alternativas consideradas

| Opção | Por que não |
|---|---|
| Cripto como moeda do `Money` | Até 18 casas decimais, símbolos sem padrão oficial e o mesmo token em várias redes. Quebraria as regras de moeda dos ADRs 0007 e 0016. |
| Stablecoin como conta em USD | Esconde o risco de perda de paridade, a rede e o emissor. |

## Consequências

- O contexto `investments` pode receber outros ativos depois (ações, FIIs).
- Surge a dependência de uma fonte de preços de cripto (ADR próprio após a issue #37).
- Relatórios de patrimônio passam a combinar contas (`Money`) e posições (ativos).
