# Contribuindo

Contribuições devem tornar a base mais clara, reproduzível e segura para uso por
agentes de IA.

## Antes do pull request

1. Explique o problema concreto que a mudança resolve.
2. Faça uma mudança focal; não misture ferramentas sem relação.
3. Use somente dados fictícios inequívocos.
4. Para ferramenta nova, preencha
   [tool-entry-template.md](catalog/tool-entry-template.md) e aponte a fonte exata.
5. Para serviço pago, freemium ou híbrido, atualize
   [paid-services.md](catalog/paid-services.md) com alternativa OSS pública,
   licença, data e diferença funcional.
6. Use **Verificada** apenas com E3 reproduzível e ligado na linha do catálogo.
7. Execute `python scripts/verify_repository.py`.

## Critérios de revisão

- necessidade e perfil de uso definidos;
- fonte canônica, versão/commit, licença e data registrados;
- projeto público e estado de arquivamento conferidos;
- instalação e exemplo separados da evidência observada;
- custo, permissões, dados, retenção e limites documentados;
- alternativa OSS não apresentada como equivalente sem prova;
- nenhuma credencial, PII, caminho pessoal ou informação privada no estado atual,
  histórico novo, fixtures ou artefatos.

Uma consulta à documentação sustenta E1. Para E3, inclua ambiente, comandos, saída
essencial e falhas exercitadas. Se a execução depender de conta ou orçamento
indisponível, marque como bloqueada.

## Testes do verificador

Ao alterar os scripts de validação, execute também:

```bash
python -m unittest discover -s scripts -p 'test_*.py' -v
```

Os testes executam a CLI em cópias temporárias do repositório. Eles cobrem arquivos
obrigatórios ausentes, diagnósticos simultâneos e continuidade das verificações de
catálogo e privacidade. O checkout original é preservado. A matriz de CI executa
a mesma suíte em Ubuntu, Windows e macOS.

## Pull request

Responda: o que mudou, por que é necessário, como foi verificado, qual afirmação a
evidência cobre e o que continua pendente. Alterações de status, licença, segurança
e compatibilidade exigem revisão explícita.
