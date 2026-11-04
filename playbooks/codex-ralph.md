# Codex + Ralph Loop — entrega granular auditável

**Estado:** procedimento documentado (E2). Não é instalação testada/E3.  
**Última verificação documental:** 2026-11-04.

## Quando usar

Quando uma spec tem múltiplas tarefas de engenharia independentes, critérios de aceite executáveis e um repositório com testes confiáveis. Não usar um loop autônomo para decidir metodologia científica, liberar produção, publicar dados sensíveis ou aprovar uma alteração sem gate humano.

O [Ralph original](https://github.com/snarktank/ralph) (licença MIT) mantém memória em `prd.json`, `progress.txt` e Git; seu script oficial atualmente suporta **Amp e Claude Code**, não Codex. Para Codex, implemente um adaptador local pequeno ou selecione uma implementação auditada compatível. Não copiar `--dangerously-skip-permissions` ou `--dangerously-allow-all` do runner original.

O [Codex CLI](https://github.com/openai/codex) possui código Apache-2.0 e executa tarefas via `codex exec`. O serviço/modelo de inferência e seu custo são distintos da licença do executável. Alternativa com componentes abertos: [Aider](https://github.com/Aider-AI/aider) (Apache-2.0) com [Ollama](https://github.com/ollama/ollama) (MIT); o fluxo, qualidade de modelo, integrações e manutenção não são equivalentes.

## Encadeamento

1. **SPEC (humano + agente):** definir objetivo, fora de escopo, risco, evidências, critérios de aceite e gates irreversíveis.
2. **PRD:** converter a spec em `prd.json` com stories microgranulares, prioridade e `passes: false`; cada story deve caber em uma execução.
3. **RECON:** inspecionar árvore Git limpa, branch isolada, documentação e testes existentes; carregar skills pertinentes sob demanda.
4. **Loop:** para cada story, iniciar **novo processo** Codex com apenas o item e resumo persistente de `progress.txt`. Não criar sub-loop oculto nem repetir tentativas sem causa nova.
5. **RED → BUILD → TEST → REVIEW → CORRECT → VERIFY:** produzir testes, implementar o mínimo, revisar diff, executar checks e documentar evidências.
6. **Checkpoint:** se os checks passaram, o runner atualiza `passes`, anexa progresso e cria **commit local atômico**. Se falhar, não marcar sucesso.
7. **CI + gate humano:** abrir PR e exigir checks remotos; ações destrutivas, alterações de método, release e publicação necessitam autorização específica.
8. **LEARN:** escrever padrões reutilizáveis sem copiar dados privados ou inflar o `AGENTS.md`.

## Contrato mínimo de uma story

```json
{
  "id": "ENG-001",
  "title": "Instrumentar uma métrica",
  "description": "Gerar diagnóstico determinístico sem modificar dados congelados",
  "acceptanceCriteria": [
    "Teste independente confere a métrica",
    "Configuração e unidade registradas",
    "Sem alterações em artefatos protegidos"
  ],
  "priority": 1,
  "passes": false
}
```

## Exemplo do backend Codex (PowerShell)

```powershell
# Executar somente em branch isolada e repositório confiável.
Get-Content -Raw .\planning\ralph\prompt.md |
  codex exec --sandbox workspace-write -c "approval_policy='never'" -
```

`-` lê o prompt da entrada padrão. O runner **deve** conferir exit code, mudança efetiva, caminhos permitidos, verificações e diff antes de commitar. `approval_policy='never'` não abre a rede por si só e não substitui sandbox. Não usar `danger-full-access`.

## Gates de parada

- **Bloquear** mudanças em segredos, política de segurança, histórico congelado ou artefatos fora da tarefa.
- **Bloquear** conclusão se testes não foram executados ou se faltam dados necessários.
- **Não** converter `passes: true` em prova de correção científica, CI verde, E3 completo ou aceite humano.
- **Não** fazer push/merge automático, exceto se o projeto possui autorização explícita, controles equivalentes e trilha de auditoria.
- Limitar o número de iterações; nunca executar retries sem limite.

## Integração à toolbox

Este playbook aplica [desenvolvimento guiado por IA](../guides/ai-guided-development.md) e [verificação honesta](../guides/verification.md). O runner é específico do projeto; a toolbox oferece critérios de escolha, não instalações automáticas.

**Evidência pendente para E3:** ambiente e versões reais, autenticação, teste de uma iteração, falha induzida, proteção de paths, commits, CI e revisão de privacidade.
