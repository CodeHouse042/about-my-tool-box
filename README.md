# About My Tool Box

Base pública, em português, para iniciar e conduzir projetos de software com IA
sem confundir referência, recomendação e evidência. O agente entrevista, escreve a
spec, escolhe a menor stack justificável, constrói em ciclos pequenos e prova o
resultado antes de declarar conclusão.

Este repositório não é uma lista de links para instalar inteira. Ele é um sistema de
decisão para desenvolvimento guiado por IA.

## Início rápido

Abra o repositório no agente de sua preferência e use:

```text
Use este repositório como política de desenvolvimento guiado por IA.
Leia README.md, AGENTS.md e guides/ai-guided-development.md.
Entreviste-me somente sobre informações materiais que ainda faltarem.
Antes de escrever código, produza uma spec verificável, escolha o perfil mínimo e
explique cada ferramenta proposta com status, evidência, custo e riscos.
Para todo serviço pago ou híbrido, pesquise uma alternativa open source pública e
ativa no Git, informe a licença e deixe clara qualquer diferença funcional.
Nunca registre dados pessoais, credenciais, caminhos pessoais ou conteúdo privado.
Só declare funcionamento quando houver evidência executada no ambiente informado.
```

O primeiro resultado do agente deve conter objetivo, fora de escopo, critérios de
aceite, decisões de stack, plano de verificação e dúvidas bloqueantes. Use o
[roteiro completo](guides/ai-guided-development.md) ou copie o
[modelo de entrevista](projects/interview-template.md).

## Como a base decide

1. **Entrevista** — descobre problema, usuários, restrições, dados, orçamento e
   definição de concluído.
2. **Spec** — transforma respostas em requisitos observáveis e registra o que não
   será feito.
3. **Perfil** — escolhe o menor ponto de partida em [profiles/](profiles/).
4. **Ferramentas** — consulta [o catálogo](catalog/tools.md), sem instalar uma
   candidata só porque foi citada.
5. **Custo e liberdade** — compara qualquer serviço pago ou híbrido com uma
   [alternativa open source](catalog/paid-services.md).
6. **Entrega** — executa `SPEC → RECON → RED → BUILD → TEST → REVIEW → CORRECT →
   VERIFY → CI → LEARN`, uma tarefa focal por ciclo.
7. **Evidência** — separa o que foi provado, inferido, não verificado ou bloqueado.

## Mapa do repositório

| Necessidade | Arquivo canônico |
|---|---|
| Conduzir o agente do briefing à entrega | [Desenvolvimento guiado por IA](guides/ai-guided-development.md) |
| Iniciar um projeto | [Primeiro projeto](guides/first-project.md) |
| Escrever requisitos | [Template de spec](projects/spec-template.md) |
| Escolher uma stack | [Perfis](profiles/README.md) e [stacks](catalog/stacks.md) |
| Entender uma ferramenta | [Catálogo](catalog/tools.md) |
| Comparar serviços pagos | [Serviços e alternativas OSS](catalog/paid-services.md) |
| Integrar MCP com limites | [MCP servers](catalog/mcp-servers.md) |
| Interpretar evidência | [Verificação](guides/verification.md) |
| Manter fontes atuais | [Manutenção](guides/maintenance.md) |
| Aplicar procedimentos reutilizáveis | [Playbooks](playbooks/README.md) e [skills](skills/README.md) |
| Orquestrar Codex em iterações Ralph | [Codex + Ralph Loop](playbooks/codex-ralph.md) |

## Status e evidência

| Status | Evidência mínima | Pode entrar por padrão? |
|---|---|---:|
| **Verificada** | E3: instalação, uso e resultado executados em ambiente registrado | Sim, se necessária |
| **Em avaliação** | E1 ou E2: fonte identificada e, no máximo, procedimento documentado | Não; validar no projeto |
| **Referência** | Material de comparação, protocolo ou prática | Não |
| **Retirada** | Fonte ambígua, arquivada ou inadequada | Não |

Uma fonte oficial, uma licença aberta ou muitas estrelas não provam adequação. O
[registro de evidência da base](catalog/evidence/base-toolchain.md) diz exatamente
o que foi executado e o que permanece bloqueado.

## Política pública

- exemplos usam somente dados fictícios inequívocos e domínios reservados;
- credenciais, PII, caminhos pessoais e conteúdo de clientes são proibidos;
- todo serviço pago ou híbrido exige alternativa open source pública no Git,
  licença, data da consulta e diferenças declaradas;
- open source não significa custo zero: hospedagem, operação, atualizações e
  resposta a incidentes continuam existindo;
- somente E3 recebe o status **Verificada**;
- uma alteração só termina depois de revisão, verificação e CI compatíveis com a
  afirmação feita.

Execute antes de contribuir:

```bash
python scripts/verify_repository.py
```

Consulte [CONTRIBUTING.md](CONTRIBUTING.md) e [SECURITY.md](SECURITY.md). O conteúdo
é distribuído sob a licença [MIT](LICENSE).
