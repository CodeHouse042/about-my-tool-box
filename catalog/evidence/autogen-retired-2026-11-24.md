# Evidência E1: retirada do AutoGen

Consulta de manutenção: 2026-11-24.

## Fontes e observações

- Fonte canônica: [microsoft/autogen](https://github.com/microsoft/autogen).
- O [workflow de atualidade de 2026-11-23](https://github.com/CodeHouse042/about-my-tool-box/actions/runs/45156192382)
  verificou 77 repositórios e sinalizou um para revisão. O relatório identificou
  AutoGen como público e arquivado.
- Nova consulta aos metadados públicos do GitHub em 2026-11-24 confirmou
  `archived: true` e `visibility: public`. O
  [README no commit consultado](https://github.com/microsoft/autogen/blob/8390985108cb1e3881f5f7297765758d8ad2540c/README.md)
  também declara o arquivamento e o encerramento da manutenção pela Microsoft.
- O metadado `license.spdx_id` retornou `CC-BY-4.0`. O mesmo README distingue
  documentação e conteúdo sob CC-BY-4.0 de código sob MIT; o
  [LICENSE-CODE](https://github.com/microsoft/autogen/blob/8390985108cb1e3881f5f7297765758d8ad2540c/LICENSE-CODE)
  confirma a licença MIT do código. O motivo da retirada é o arquivamento.
- CrewAI e LangGraph já estavam no catálogo. Na mesma consulta, os repositórios
  [CrewAI](https://github.com/crewAIInc/crewAI) e
  [LangGraph](https://github.com/langchain-ai/langgraph) retornaram visibilidade
  pública, `archived: false` e metadado SPDX MIT. Essa consulta não audita todas as
  dependências, versões ou condições de uso.

## Decisão e limites

Retirar AutoGen das candidatas ativas e conservar a referência histórica neste
registro. Avaliar CrewAI para papéis e tarefas colaborativas e LangGraph para
fluxos com estado e branching quando a spec justificar. Não presumir equivalência,
migração direta ou instalação validada. Ambos permanecem E1.
