# Perfil: IA e agentes

## Início mínimo

- Git e Python ou TypeScript;
- SDK direto do provedor ou runtime local;
- prompt, esquema de saída e casos de avaliação versionados;
- timeout, retry limitado, teto de custo e política de dados;
- caso feliz, entrada inválida, recusa e falha do provedor.

Para dados que não podem sair do ambiente, avalie Ollama ou llama.cpp com modelo
compatível. Isso muda hardware, qualidade, latência e operação; execute avaliação
comparável antes da decisão.

## Quando adicionar camadas

| Necessidade comprovada | Candidata |
|---|---|
| Estado e branching duráveis | LangGraph |
| Papéis e tarefas colaborativas | CrewAI |
| Ferramentas interoperáveis | MCP/FastMCP |
| Desenvolvimento por agente self-hosted | OpenHands |
| Memória entre sessões | solução de memória após política de retenção |

Valide uma camada por vez. Não combine swarm, memória, RAG e vários frameworks antes
de medir uma limitação do fluxo simples.

## Serviço pago

Para API ou agente hospedado, compare
[alternativas OSS](../catalog/paid-services.md). Registre modelo e região, dados
enviados, retenção, treinamento, custo por cenário e procedimento de exclusão.

## Verificação mínima

Execute conjunto pequeno e versionado, valide estrutura e semântica, meça custo e
latência, exercite timeout/retry e revise traces sem segredos. Resultado de modelo é
variável; declare amostra, configuração e tolerância.
