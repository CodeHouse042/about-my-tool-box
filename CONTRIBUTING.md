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
7. Execute `python scripts/verify_repository.py --history`.

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

## Identidade Git e histórico público

Este repositório exige um identificador público sem espaços no nome do autor e um
endereço `noreply` do GitHub nos commits. Configure **somente neste repositório**
seu login público e o endereço exibido em suas configurações de e-mail. Substitua
os placeholders abaixo pelos seus dados públicos de autoria:

```bash
git config --local user.name LOGIN_PUBLICO
git config --local user.email ID+LOGIN_PUBLICO@users.noreply.github.com
```

Use mensagens de commit com apenas o assunto, conforme o contrato do verificador.
Depois de criar o commit, confira autor e committer e execute a validação:

```bash
git log -1 --format="Autor: %an <%ae>%nCommitter: %cn <%ce>"
python scripts/verify_repository.py --history
```

A [configuração de e-mail do GitHub](https://docs.github.com/en/account-and-profile/how-tos/email-preferences/setting-your-commit-email-address)
distingue commits feitos no site dos feitos no computador. A configuração local
afeta os próximos commits criados pelo Git e não altera os anteriores. Para
commits feitos no site, habilite a privacidade de e-mail. Integrações podem definir
[autor e committer pela API](https://docs.github.com/en/rest/git/commits#create-a-commit);
confirme os dados do commit efetivo, inclusive os produzidos pelo GitHub no CI.
O e-mail retornado por uma consulta ao perfil não basta para essa confirmação.

Para recuperar alterações de uma contribuição com histórico reprovado, use um
checkout isolado com base validada, crie uma branch nova e reaplique somente o
diff revisado. `--history` inspeciona `HEAD`, branches locais e tags: criar uma
branch nova não remove ancestrais ainda alcançáveis pelas outras referências.
Valide o histórico novo e o CI antes de substituir o PR anterior. Não faça
force-push nem reescreva uma branch compartilhada sem autorização específica.

## Pull request

Responda: o que mudou, por que é necessário, como foi verificado, qual afirmação a
evidência cobre e o que continua pendente. Alterações de status, licença, segurança
e compatibilidade exigem revisão explícita.
