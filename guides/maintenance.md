# Manutenção do catálogo

## Cadência

| Frequência | Verificação | Resultado |
|---|---|---|
| Em cada mudança | Estrutura, links internos, privacidade e contrato de serviços pagos | CI verde ou correção |
| Semanal | Estado HTTP, redirecionamentos, fonte canônica, repositório público, arquivamento e atividade | Relatório e CI vermelho quando houver sinal para revisão |
| Mensal | Licença, modelo de custo, fonte canônica e alternativa OSS | Data e diferenças atualizadas |
| Trimestral | Repetição da instalação e caso mínimo de cada E3 | Evidência renovada ou rebaixamento |

Automação detecta sinais; não promove ferramenta. Estrelas e frequência de commits
não são critério suficiente de qualidade ou segurança.

O relatório de atualidade consulta fontes GitHub dos Markdown no nível superior
de `catalog/`. Ao retirar uma fonte arquivada, registre sua URL histórica e a
justificativa em `catalog/evidence/` e referencie a evidência em
`catalog/retired.md`; mantenha as alternativas ativas sob a verificação periódica.

## Revalidar uma ferramenta

1. Confirme a fonte oficial e se o projeto mudou de organização.
2. Verifique licença, arquivamento, releases e avisos de segurança.
3. Repita a instalação em ambiente limpo.
4. Execute caso feliz, entrada inválida e limite relevante.
5. Registre data, versão, ambiente, saída e limitações.
6. Para serviço pago/híbrido, atualize preço/modelo e pesquise novamente alternativas
   em repositórios Git públicos; declare diferenças.
7. Atualize `catalog/tools.md` e a evidência no mesmo commit.

Rebaixe imediatamente para E1/E2 se a evidência não puder ser repetida. Mova para
[retired.md](../catalog/retired.md) se a fonte ficar ambígua, arquivada ou
incompatível com o propósito.

## Pesquisa de alternativa open source

Use a fonte primária do projeto e registre:

- URL exata do repositório, não perfil ou busca;
- licença explícita; “source available” não deve ser chamado automaticamente de OSS;
- estado público e não arquivado na data;
- capacidade necessária, não apenas categoria parecida;
- trabalho de self-hosting, migração, backup, monitoramento e segurança;
- lacunas em SLA, integrações, UX e suporte.

Se nenhuma opção satisfizer o requisito, preserve o serviço pago como decisão
consciente ou altere o requisito; não invente equivalência.
