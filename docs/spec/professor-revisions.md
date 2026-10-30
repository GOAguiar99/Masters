# Professor revision specification

Source: [`professor-revisions-main.pdf`](../../professor-revisions-main.pdf), copied from `~/Downloads/main (1).pdf` on 2026-10-30. The PDF has 100 pages and contains 28 comment entries. This document transcribes those comments and turns them into a revision checklist; the PDF remains the reference for the exact highlighted passages and their visual context.

The comments are in review order. Locations below use **PDF viewer page numbers** (1–100) and line numbers from a `pdftotext -layout` extraction of that page; blank lines are counted. The printed dissertation folio is included where useful. The quoted anchor is the text selected by the PDF annotation (or the nearest corresponding text lines). This lets you jump directly to the passage even when the comment asks for a broader structural change.

## Triage by effort

**Hard** means the note needs one-by-one review, new information, or a careful evidence/artifact audit. **Medium** means it needs synthesis, a table/figure, or structural work beyond a straightforward text edit. **Easy** means it can be handled as a focused text-only change.

### Hard

- [ ] **#1 V2X example and IEEE transition** — PDF p. 19, line 9. Choose and substantiate a useful V2X crash-alert scenario.
- [ ] **#2 Crash-alert example figure** — PDF p. 19, line 23. Develop an example that demonstrates the crash-alert problem and illustrate it.
- [ ] **#3 Compare wireless options** — PDF p. 20, lines 4–9. Add a supported comparison of 802.11p and relevant alternatives.
- [ ] **#16 Related-work comparison table** — PDF p. 51, lines 10–22. Review all related work individually, synthesize the comparison, and add this dissertation as a row.
- [ ] **#17 AI-use disclosure** — PDF p. 53, line 4. Establish the actual AI use and locations before writing the disclosure; do not infer or invent usage.
- [ ] **#23 Simulator changes/originals table** — PDF p. 69, lines 23–25. Audit the active implementation and distinguish study modifications from reused framework components.
- [ ] **#26 AI-dependent writing review** — PDF p. 78, lines 10–17. Review the dissertation prose and section structure individually, checking authorial understanding and claims.
- [ ] **#28 Publications mapping** — PDF p. 94, lines 32–35. Verify the publications and map their actual content to dissertation sections.

### Medium

- [ ] **#9 Research-question/scope restructuring** — PDF p. 20, lines 23–38. Remove the research-question section and place the scope after the objectives.
- [ ] **#12 External-table reference** — PDF p. 24, lines 25–35. Bring the relevant content into the dissertation by reproducing the table or describing it.
- [ ] **#15 Evaluated-policy comparison table** — PDF p. 40, lines 24–33. Synthesize the policy characteristics and distinctions, including `plain`.
- [ ] **#20 Architecture figure** — PDF p. 59, lines 13–20. Diagram component roles and communication paths.
- [ ] **#21 Move repository layout to appendix** — PDF p. 60, lines 9–16. Relocate the marked material and check resulting references/structure.
- [ ] **#22 Convert short subsections to items** — PDF p. 61, lines 6–21. Reshape the marked implementation subsections into a readable item list.
- [ ] **#25 Experiment-decisions table** — PDF p. 77, lines 8–9. Synthesize the experiment choices into a concise table.

### Easy

- [ ] **#4 Rewrite the gap statement** — PDF p. 20, lines 10–12.
- [ ] **#5 Explain DSCP categories or generalize the reference** — PDF p. 20, lines 12–15.
- [ ] **#6 Remove simulator framework from the research question** — PDF p. 20, lines 25–29.
- [ ] **#7 Remove the marked research-question sentence** — PDF p. 20, lines 27–29.
- [ ] **#8 Re-state objective and applicability** — PDF p. 20, lines 31–38.
- [ ] **#10 Change “general objective” to “main objective”** — PDF p. 20, line 43.
- [ ] **#11 Revise the specific-objectives lead-in** — PDF p. 21, line 6.
- [ ] **#13 Remove “as developed by”** — PDF p. 26, lines 48–52.
- [ ] **#14 Define the acronym at first use** — PDF p. 40, lines 4–8.
- [ ] **#18 Remove implementation-parameter reference from the system model** — PDF p. 53, line 16.
- [ ] **#19 Remove the marked Table 12 reference** — PDF p. 55, line 50.
- [ ] **#24 Clarify or remove evaluation citations** — PDF p. 76, lines 11–15.
- [ ] **#27 Add a short section transition** — PDF p. 87, lines 31–33.

## Introduction and objectives

- [ ] **#1 V2X context and transition** — **PDF p. 19, line 9** (printed folio 18; selected anchor: “…pedestrians, and Institute…”). Professor: “essa transição não está legal. Talvez citar um exemplo de cenário de aplicação de V2X e depois no outro parágrafo linkar com a IEEE.” Add a concrete V2X use case, then make a separate transition from that use case to the relevant IEEE standard.
- [ ] **#2 Crash-alert example** — **PDF p. 19, line 23** (folio 18; selected anchor: “A crash alert that arrives late competes for the channel…”). Professor: “se for usar um exemplo, poderia usar um que seja útil para também mostrar o problema do crash alert, incluindo uma figura aqui.” If adding an example, use one that illustrates the crash-alert problem and add a figure.
- [ ] **#3 Motivate wireless and 802.11p** — **PDF p. 20, lines 4–9** (folio 19; anchor: “This leaves a practical gap for a local…”). Professor: “porque usar wireless? Embora tenha a justificativa na última frase, acho que precisa ter um pouco mais de profundidade comparando as escolhas. ADicionaria mais algumas frases justificando a escolha e comparando 802.11p com outras alternativas.” Expand the rationale for wireless communication and compare 802.11p with relevant alternatives.
- [ ] **#4 Rewrite the gap statement** — **PDF p. 20, lines 10–12** (folio 19; anchor: “This dissertation addresses that gap with a deliberately narrow study…”). Professor: “não é comum o uso de ':' em inglês. Sugiro reescrever algo como: This work addresses that gap by proposing a crash-aware prioritization...” Remove the colon construction and use a natural English sentence along the suggested lines.
- [ ] **#5 Explain DSCP categories before using them** — **PDF p. 20, lines 12–15** (folio 19; anchor: “mapped to the Voice (VO) access category”). Professor: “não explicou isso e apareceu do nada aqui. Ou coloque a explicação das categorias do DSCP em algum parágrafo acima, ou escreva de maneira genérica sem entrar nos detalhes.” Introduce the DSCP categories earlier or keep the later reference general.
- [ ] **#6 Keep the research question independent of the simulator** — **PDF p. 20, lines 25–29** (folio 19; anchor: “Veins/INET Framework (INET) simulations”). Professor: “novamente apareceu Veins/INET do nada no texto. A pergunta de pesquisa não pode estar relacionada a um framework de simulação.” Remove Veins/INET from the research question and frame it around the research problem.
- [ ] **#7 Remove the marked sentence** — **PDF p. 20, lines 27–29** (folio 19; anchor: research-question sentence ending “…what cost does that protection impose on ordinary traffic?”). Professor: “remove essa frase.” Delete the highlighted sentence; confirm the exact sentence against the PDF annotation.
- [ ] **#8 Re-state purpose and applicability** — **PDF p. 20, lines 31–38** (folio 19; anchor: “multi-class traffic orchestration” through the scope limits). Professor: “Falou do que o estudo não vai fazer, mas relembre o objetivo e aplicabilidade.” After describing limits, remind readers of the study’s objective and where its findings apply.
- [ ] **#9 Research-question/scope passage** — **PDF p. 20, lines 23–38** (folio 19; anchor: heading “1.1 RESEARCH QUESTION AND SCOPE”). Professor: “acho que essa seção poderia ser removida por completo. Após apresentar os objetivos, aí sim pode adicionar o parágrafo do escopo. Mas tiraria a pegunta de pesquisa.” Remove the marked section/research question; present objectives first, then a scope paragraph.
- [ ] **#10 Use “main” for the objective label** — **PDF p. 20, line 43** (folio 19; selected word: “general”). Professor’s entire comment is “main”; interpret this as changing “general objective” to “main objective.”
- [ ] **#11 Specific objectives lead-in** — **PDF p. 21, line 6** (printed folio 20; anchor: “The specific objectives are:”). Professor’s annotation selects the lead-in “To achieve the main objetive, we define the following specific objectives:”. Use the lead-in at this location, correcting “objetive” to “objective,” or retain the current concise wording.

## Background and related work

- [ ] **#12 Avoid referring to a table in another document** — **PDF p. 24, lines 25–35** (printed folio 23; anchor: “Table 5.2-1 of that specification lists…”). Professor: “Não deve citar uma tabela de um documento. Ou replica a tabela aqui ou descreve o conteúdo dela.” Put the needed table in the dissertation or describe its content directly.
- [ ] **#13 Remove redundant author wording** — **PDF p. 26, lines 48–52** (folio 25; anchor: “as developed by Bianchi (2000)”). Professor: “pode remover as developed by e deixar só a citação, pois o nome do autor já é citado no início.” Delete “as developed by” where marked and keep the citation.
- [ ] **#14 Define V2X at first use** — **PDF p. 40, lines 4–8** (folio 39; selected anchor: “3rd Generation Partnership Project (3GPP)”). Professor: “define o acronimo no primeiro uso, durante a seção acima.” Spell out the term and define V2X at its first occurrence in the earlier section.
- [ ] **#15 Compare the evaluated policies** — **PDF p. 40, lines 24–33** (folio 39; selected anchor: end of the policy summary, “design space”). Professor: “A seção 2.2.3 define a política plain que depois vai ser usada na avaliação. Poderia adicionar aqui uma tabela comparativa definindo as características das políticas e deixando claro suas diferenças.” Add a comparison table that defines the policy characteristics and distinctions, including `plain` and the policies later evaluated.
- [ ] **#16 Summarize related work in a comparison table** — **PDF p. 51, lines 10–22** (printed folio 50; anchor: “TSN and OFDMA solve determinism…”). Professor: “Tens que resumir todos os trabalhos em uma tabela comparativa e depois incluir uma linha pro teu trabalho.” Include all reviewed works and add a row for this dissertation.

## System model and terminology

- [ ] **#18 Move implementation parameters out of the system model** — **PDF p. 53, line 16** (printed folio 52; selected anchor: “…implementation parameters in Table 12”). Professor: “Não faz sentido citar parâmetros de implementação no modelo de sistema. Remova a referência pra tabela.” Remove the marked table reference from the system model; keep implementation parameters in the implementation chapter.
- [ ] **#19 Remove the marked reference** — **PDF p. 55, line 50** (printed folio 54; selected anchor: “…listed in Table 12”). Professor: “remove a referência aqui.” Inspect the highlighted location and remove the reference there.
- [ ] **#20 Add an explanatory architecture figure** — **PDF p. 59, lines 13–20** (printed folio 58; anchor: “The realization is an OMNeT++ 6.1 / INET 4.5.4 / Veins 5.3.1 project”). Professor: “se conseguir colocar uma figura aqui, mostrando o que cada elemento faz e como se comunica com o outro ficaria mais fácil entender o papel de cada um deles.” Add a figure showing each element’s role and the communication paths between elements.

## Implementation and dissertation structure

- [ ] **#21 Move the marked section to an appendix** — **PDF p. 60, lines 9–16** (printed folio 59; anchor: heading “5.1.2 Repository layout” and its introductory text). Professor: “joga como anexo”. Move the highlighted material to an appendix.
- [ ] **#22 Flatten short subsections into items** — **PDF p. 61, lines 6–21** (printed folio 60; anchor: heading “5.2.1 Vehicle host”; the section continues into the adjacent short subsections). Professor: “subseções aqui estão pequenas. Talvez colocar em formato de itens ao invés de subseções.” Replace the marked short subsections with a list of items where that improves readability.
- [ ] **#23 Summarize simulator changes and reused components** — **PDF p. 69, lines 23–25** (printed folio 68; anchor: “the five policies of Section 4.3”). Professor: “no final dessa seção você poderia resumir o que foi modificado nos simuladores e o que foi usado de original. Uma tabela nesse formato vai deixar claro o trabalho que teve dentro dos frameworks de simulação.” End the section with a table distinguishing modifications from original simulator/framework components.
- [ ] **#28 Add a publications section** — **PDF p. 94, lines 32–35** (printed folio 93; anchor: heading “7.4 FUTURE WORK” and its opening paragraph). Professor: “adiciona uma seção de publications, cita as publicações e onde os conteúdos delas estão representados nas seções das dissertações.” Add a publications section listing the publications and mapping their content to dissertation sections.

## Evaluation and closing material

- [ ] **#24 Clarify the evaluation citations** — **PDF p. 76, lines 11–15** (printed folio 75; anchor: “The evaluation is a protection-versus-cost study…”). Professor: “não faz sentido essas citações aqui. A frase é sua, a não ser que quis dizer que a avaliação é baseada nos trabalhos citados. Se for isso, reescreva para deixar claro.” Remove citations if the statement is the author’s own; otherwise rewrite it to say explicitly that the evaluation is based on the cited work.
- [ ] **#25 Summarize experiment decisions** — **PDF p. 77, lines 8–9** (printed folio 76; anchor: “Best Effort cost, not a Voice-tail race under saturation”). Professor: “tente pensar numa tabela resumindo as principais decisões dos experimentos. São bastante detalhes, acredito que vai ajudar a deixar mais claro.” Add a table of the principal experimental decisions to make the evaluation setup easier to follow.
- [ ] **#27 Insert a transition between sections** — **PDF p. 87, lines 31–33** (printed folio 86; selected anchor: headings “6.7 DISCUSSION” and “6.7.1 Event-triggered escalation…”). Professor: “adiciona um texto entre as seções.” Add a short linking paragraph at the marked boundary; verify the exact insertion point in the PDF.

## Cross-cutting

- [ ] **#17 Document AI use** — **PDF p. 53, line 4** (printed folio 52; anchor: “Figure 7 – System architecture…”). Professor: “gerada por IA? adicionar um disclaimer no final da tese citando como a IA foi usada e onde (seções, figuras, tabelas, etc)” Add a disclosure at the end of the dissertation describing how AI was used and identifying affected sections, figures, tables, or other material.
- [ ] **#26 Review for AI-dependent writing** — **PDF p. 78, lines 10–17** (printed folio 77; anchor: section heading “6.3 VOICE PROTECTION UNDER LOAD: THE HEADLINE ANSWER”). Professor: “teu texto e as seções estão muito IA-dependent. Fica claro o uso bastante grande de IA, tem que ter cuidado.” Review the prose and section structure carefully; ensure the final text reflects the author’s own understanding, voice, and verified claims.

## Markup-only entries

- **PDF p. 53, line 17** (printed folio 52): a highlight on “Table 12.” It overlaps the system-model table-reference comment at line 16.
- **PDF p. 53, lines 14–20** (folio 52): a second, larger highlight over the radio-model paragraph, including the line 16 table reference. It has no separate written instruction; treat it as part of the system-model comment above.
- **PDF p. 58, lines 22–23** (printed folio 57): a highlight on the implementation-table reference in the assumptions/scope discussion: “radio parameters fix concrete instances of the model; their reference values are recorded with the implementation in Table 12.” No comment text is attached.
- **PDF p. 91, line 4** (printed folio 90): a strikeout over “CHAPTER” in the heading “6.8 CHAPTER SUMMARY.” No comment text is attached.

