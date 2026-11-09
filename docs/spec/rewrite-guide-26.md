# Guia de reescrita — comentário #26 ("texto muito IA-dependent")

> **Status (09/11/2026):** concluído. §6.3, §7.1–7.2, Resumo e Abstract foram reescritos na voz do autor, e os parágrafos narrativos foram aceitos. Este guia fica como referência de estilo para textos futuros.

## O que o professor quis dizer

"Teu texto e as seções estão muito IA-dependent. Fica claro o uso bastante grande de IA, tem que ter cuidado."

Ele não está pedindo para esconder o uso de IA, que já está declarado no Apêndice B. O alerta é que o texto **soa** como saída de um modelo de linguagem, e a banca pode concluir que o entendimento não é seu. Os sinais que ele percebe:

- frases longas e densas, cheias de números e termos técnicos, todas com o mesmo ritmo;
- as mesmas ressalvas e os mesmos resultados repetidos em vários lugares;
- parágrafos que anunciam o que o capítulo vai fazer ("The chapter is organized as follows…");
- termos inventados e nomes de configuração no meio da prosa (`hotspot_high`, "floor", "escalation step");
- conectivos automáticos ("therefore", "rather than", "not X but Y");
- nenhum relato seu de **como** o estudo foi feito e do que você aprendeu.

## O que já foi feito (não precisa refazer)

- **1ª passada (PR #5):** títulos-slogan, travessões, metáforas e subseções minúsculas.
- **2ª passada (branch `revision/26-second-pass`):**
  - parágrafos de roteiro removidos (4 → 0);
  - ressalvas repetidas cortadas;
  - nomes de configuração trocados por palavras comuns;
  - frases com mais de 35 palavras: 147 → 50;
  - "therefore": 55 → 17.

Nenhum número ou conclusão mudou.

## O que só você pode fazer

Reescreva os trechos abaixo **com suas palavras**. A melhor forma: feche o texto atual, olhe só as tabelas e figuras e escreva como você explicaria na defesa. Depois compare com o texto antigo para conferir que nenhum fato ficou de fora.

### 1. §6.3 "Overview of the Results" (`chapters/5-chapter.tex`, seção `sec:eval:headline`)

Foi este o trecho que o professor marcou.

- **Por que soa como IA:** abre com uma frase longa que condensa todo o resultado. Usa nomes de configuração (`netload_high`, `hotspot_high`) e termos como "floor" e "escalation step" sem explicar.
- **Fatos a manter** (fonte: `tab:eval:glance`, `tab:eval:hotspot`, `tab:eval:heavy_qos`):
  - **Carga uniforme alta, 100 veículos:** P95 de Voz ≈ 2,2 ms em todas as políticas. Esse valor vem do jitter de 2 ms que o gerador aplica a cada cópia, não do acesso ao canal. Nos perfis baixo e médio, com jitter de 5 ms, fica em ≈ 4,6–4,9 ms.
  - **Carga concentrada (hotspot) alta:** P95 de Voz de 18,5 ms (plain) e ≈ 20 ms (EDCA).
    - Só o emergency reduz: 14,6 ms de P95 e média de 4,54 → 2,78 ms, ou seja −39 % na média e −21 % no P95 em relação ao plain.
    - As perdas de Voz por colisão caem 30 % em relação ao EDCA.
  - **Hotspot médio e baixo:** nenhum ganho de Voz (a média até piora: +10 % e +16 %).
  - **Custo:** o emergency descarta ≈ 16,1 mil quadros BE no hotspot contra ≈ 2,5 mil na carga uniforme.
- **Sugestão:** comece pela pergunta do capítulo e responda em duas ou três frases simples. Deixe os detalhes para §6.4–6.6.

### 2. §7.1 "Main Findings" e §7.2 "Practical Implications" (`chapters/6-chapter.tex`)

- **Por que soa como IA:** repete os números da Avaliação no mesmo formato compacto e fecha com frases de efeito ("the risk is the Best Effort cost and not alert latency").
- **Fatos a manter:**
  - os números do item 1;
  - `stable` eleva o P95 de BE da frota de 0,51 para 30 ms, e `guarded` para 3,9 ms;
  - o emergency mantém 0,37 ms porque descarta quadros;
  - 2,21 ms × 2,24 ms não é diferença material;
  - mapeamento DSCP→Voz explícito como padrão razoável;
  - bloqueio adaptativo só como escalonamento disparado pelo acidente, sob carga concentrada;
  - autenticação e limitação de taxa como pré-requisito;
  - orçamento de 25 ms do 3GPP TS 22.186: os baselines no hotspot chegam a 18,5–20 ms e o emergency mantém 14,6 ms.
- **Sugestão:**
  - **§7.1:** os achados em três ou quatro frases, cada uma com um resultado.
  - **§7.2:** o que um projetista de sistema V2X deve fazer com isso.

### 3. Os três parágrafos narrativos (aceitos pelo autor em 09/11/2026)

1. **Introdução da Avaliação:** como a primeira campanha foi corrigida.
2. **Abertura de §6.4:** a hipótese e as duas previsões.
3. **Abertura da Conclusão:** o que o resultado negativo ensinou.

Os rascunhos foram escritos com IA a partir das notas `EVAL_MEASUREMENT_REVIEW.md` e `EVAL_HOTSPOT_VO_PROTECTION.md` e aceitos pelo autor como estão; os marcadores `\todo` foram removidos. Se quiser ajustá-los às suas palavras, os fatos abaixo continuam valendo.

- **Fatos:**
  - O BE sorteava o intervalo uma única vez por veículo, então algumas sementes tinham veículos quase gulosos.
  - O atraso de Voz era medido a partir de cada repetição física, não do início do alerta.
  - Os dois problemas foram corrigidos e a campanha foi refeita.
  - Na carga uniforme, nenhuma política mudou o serviço de Voz.
  - Hipótese: com ~100 emissores uniformes, suprimir BE num nó remove uma fração ínfima da carga.
  - Previsões: (P2) invariância sob carga uniforme; (P1) ganho de Voz com poucos emissores pesados perto do acidente.
  - Ambas foram confirmadas.

## Regras para a reescrita

- **Faça:**
  - uma ideia por frase;
  - use "we" quando o estudo tomou uma decisão;
  - use os nomes das políticas (`plain`, `emergency`…) e palavras comuns para os cenários.
- **Não faça:**
  - números novos;
  - repetir ressalvas que já estão em §6.7.4 e §7.3;
  - "therefore", "rather than" e "not X but Y" em toda frase;
  - travessões;
  - títulos de efeito.

## Verificação

1. `./compile.sh` sem erros.
2. Peça uma conferência dos números reescritos contra `context/eval-kpis/` antes de enviar.
