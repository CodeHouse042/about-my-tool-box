# Catálogo de ferramentas

Catálogo curado para seleção por agentes de IA. A presença de uma ferramenta nesta
página não autoriza sua instalação. As fontes foram consolidadas em 2026-09-04; a
checagem pública de licença/arquivamento desta revisão cobre as alternativas e as
licenças resolvidas em [evidence/public-oss-sources-2026-09-04.md](evidence/public-oss-sources-2026-09-04.md).
Valide novamente antes de uma decisão de longo prazo.

## Toolchain de base

| Ferramenta | Para que serve | Status | Evidência | Modelo/licença | Fonte oficial | Alternativa OSS |
|---|---|---|---|---|---|---|
| Git | Versionamento e colaboração | Verificada | [E3](evidence/base-toolchain.md) | OSS, GPL-2.0 | [git/git](https://github.com/git/git) | — |
| Python | Automação, backend, dados e IA | Verificada | [E3](evidence/base-toolchain.md) | OSS, PSF License | [python/cpython](https://github.com/python/cpython) | — |
| Node.js | Runtime JavaScript e TypeScript | Verificada | [E3](evidence/base-toolchain.md) | OSS, MIT | [nodejs/node](https://github.com/nodejs/node) | — |
| npm CLI | Dependências e scripts Node | Verificada | [E3](evidence/base-toolchain.md) | OSS, Artistic-2.0 | [npm/cli](https://github.com/npm/cli) | — |
| Docker Engine | Containers reproduzíveis | Em avaliação | [E2](evidence/base-toolchain.md) | OSS, Apache-2.0 | [moby/moby](https://github.com/moby/moby) | [Podman](https://github.com/podman-container-tools/podman) |
| Docker Compose | Serviços locais compostos | Em avaliação | [E2](evidence/base-toolchain.md) | OSS, Apache-2.0 | [docker/compose](https://github.com/docker/compose) | [Podman Compose](https://github.com/containers/podman-compose) |
| GitHub Actions | CI/CD hospedado | Verificada | [E3](evidence/base-toolchain.md) | Híbrido; uso gratuito e cotas pagas | [documentação](https://docs.github.com/actions) | [Woodpecker CI](https://github.com/woodpecker-ci/woodpecker) — exige hospedagem própria |

E3 cobre somente os ambientes e comandos registrados. Docker e Compose ficaram E2
porque há versão/daemon registrados, mas não há saída preservada de container e
stack mínimos. Docker Desktop é um produto separado e está na
[comparação de serviços](paid-services.md).

## Desenvolvimento de aplicações

Estas entradas têm fonte oficial identificada, mas não foram executadas nesta
revisão; permanecem em E1.

| Ferramenta | Para que serve | Status | Evidência | Licença/modelo | Fonte oficial |
|---|---|---|---|---|---|
| Vite | Build e servidor local para frontend | Em avaliação | E1 | MIT | [vitejs/vite](https://github.com/vitejs/vite) |
| React | Interfaces componentizadas | Em avaliação | E1 | MIT | [react/react](https://github.com/react/react) |
| Next.js | Aplicações React com renderização e backend | Em avaliação | E1 | MIT | [vercel/next.js](https://github.com/vercel/next.js) |
| TypeScript | Tipagem estática para JavaScript | Em avaliação | E1 | Apache-2.0 | [microsoft/TypeScript](https://github.com/microsoft/TypeScript) |
| Laravel | Aplicações PHP | Em avaliação | E1 | MIT | [laravel/framework](https://github.com/laravel/framework) |
| Filament | Painéis administrativos em Laravel | Em avaliação | E1 | MIT | [filamentphp/filament](https://github.com/filamentphp/filament) |
| Livewire | Interfaces reativas em Laravel | Em avaliação | E1 | MIT | [livewire/livewire](https://github.com/livewire/livewire) |
| Better Auth | Autenticação para TypeScript | Em avaliação | E1 | MIT | [better-auth/better-auth](https://github.com/better-auth/better-auth) |
| PostgreSQL | Banco relacional | Em avaliação | E1 | PostgreSQL License | [postgres/postgres](https://github.com/postgres/postgres) |
| Valkey | Cache, sessão e filas compatíveis com Redis | Em avaliação | E1 | BSD-3-Clause | [valkey-io/valkey](https://github.com/valkey-io/valkey) |
| Kubernetes | Orquestração de containers em escala | Referência | E1 | Apache-2.0 | [kubernetes/kubernetes](https://github.com/kubernetes/kubernetes) |
| Coolify | PaaS hospedada pelo próprio usuário | Em avaliação | E1 | Apache-2.0 | [coollabsio/coolify](https://github.com/coollabsio/coolify) |
| Apache CloudStack | Infraestrutura IaaS própria | Referência | E1 | Apache-2.0 | [apache/cloudstack](https://github.com/apache/cloudstack) |
| Supabase self-hosted | Banco, auth, storage e APIs | Em avaliação | E1 | Apache-2.0 | [supabase/supabase](https://github.com/supabase/supabase) |
| Gitea | Hospedagem própria de Git, issues e pull requests | Em avaliação | E1 | MIT | [go-gitea/gitea](https://github.com/go-gitea/gitea) |

## Desenvolvimento e orquestração com IA

Comece pelo SDK direto do modelo. Adicione agente, memória, grafo ou swarm somente
quando a spec provar essa necessidade.

| Ferramenta | Para que serve | Status | Evidência | Licença/modelo | Fonte oficial |
|---|---|---|---|---|---|
| OpenHands | Agente de desenvolvimento self-hosted | Em avaliação | E1 | MIT | [OpenHands/OpenHands](https://github.com/OpenHands/OpenHands) |
| OpenClaw | Gateway e operador de agentes | Em avaliação | E1 | MIT | [openclaw/openclaw](https://github.com/openclaw/openclaw) |
| RTK | Reduzir e estruturar saída de ferramentas CLI | Em avaliação | E1 | Apache-2.0 | [rtk-ai/rtk](https://github.com/rtk-ai/rtk) |
| PRobe extension | Revisão de código assistida por IA | Em avaliação | E1 | AGPL-3.0 | [getprobe-dev/probe-extension](https://github.com/getprobe-dev/probe-extension) |
| Graphify CLI (`graphifyy`) | Grafo estrutural de código | Em avaliação | E1 | Apache-2.0 | [Graphify-Labs/graphify](https://github.com/Graphify-Labs/graphify) |
| Superpowers | Skills para planejamento, TDD e revisão | Em avaliação | E1 | MIT | [obra/superpowers](https://github.com/obra/superpowers) |
| Ruflo | Orquestração de agentes e memória | Em avaliação | E1 | MIT | [ruvnet/ruflo](https://github.com/ruvnet/ruflo) |
| CrewAI | Orquestração por agentes e tarefas | Em avaliação | E1 | MIT | [crewAIInc/crewAI](https://github.com/crewAIInc/crewAI) |
| LangGraph | Workflows de agentes como grafos | Em avaliação | E1 | MIT | [langchain-ai/langgraph](https://github.com/langchain-ai/langgraph) |
| Aider | Pair programming por IA no terminal | Em avaliação | E1 | Apache-2.0 | [Aider-AI/aider](https://github.com/Aider-AI/aider) |
| Cline | Agente de código em IDE, CLI e SDK | Em avaliação | E1 | Apache-2.0 | [cline/cline](https://github.com/cline/cline) |
| FastMCP | Criar servidores MCP em Python | Em avaliação | E1 | Apache-2.0 | [PrefectHQ/fastmcp](https://github.com/PrefectHQ/fastmcp) |
| Codebase Memory MCP | Indexar e consultar código via MCP | Em avaliação | E1 | MIT | [DeusData/codebase-memory-mcp](https://github.com/DeusData/codebase-memory-mcp) |
| Grok Mem, pacote `claude-mem` | Memória entre sessões de agentes | Em avaliação | E1 | Apache-2.0 | [thedotmack/claude-mem](https://github.com/thedotmack/claude-mem) |
| Humanizer | Referência de skill para revisão de texto | Em avaliação | E1 | MIT | [blader/humanizer](https://github.com/blader/humanizer) |
| MarketingSkills | Skills de marketing e conteúdo | Em avaliação | E1 | MIT | [coreyhaines31/marketingskills](https://github.com/coreyhaines31/marketingskills) |
| OpenAI Evals | Avaliar saídas e comportamentos de modelos | Em avaliação | E1 | MIT | [openai/evals](https://github.com/openai/evals) |
| Ollama | Executar modelos localmente | Em avaliação | E1 | MIT | [ollama/ollama](https://github.com/ollama/ollama) |
| llama.cpp | Inferência local otimizada | Em avaliação | E1 | MIT | [ggml-org/llama.cpp](https://github.com/ggml-org/llama.cpp) |

## Browser, scraping e extração

Use somente em alvos autorizados. HTTP direto vem antes de browser; browser vem
antes de uma camada de agente; serviço gerenciado entra apenas com justificativa.

| Ferramenta | Para que serve | Status | Evidência | Licença/modelo | Fonte oficial |
|---|---|---|---|---|---|
| Playwright | Testar e controlar navegadores | Em avaliação | E1 | Apache-2.0 | [microsoft/playwright](https://github.com/microsoft/playwright) |
| Browser Use | Automação de browser por agentes | Em avaliação | E1 | MIT | [browser-use/browser-use](https://github.com/browser-use/browser-use) |
| Chrome DevTools MCP | Inspeção e controle de Chrome via MCP | Em avaliação | E1 | Apache-2.0 | [ChromeDevTools/chrome-devtools-mcp](https://github.com/ChromeDevTools/chrome-devtools-mcp) |
| Crawl4AI | Crawling e extração orientada a LLM | Em avaliação | E1 | Apache-2.0 | [unclecode/crawl4ai](https://github.com/unclecode/crawl4ai) |
| Firecrawl self-hosted | Crawling e extração por API própria | Em avaliação | E1 | AGPL-3.0 | [firecrawl/firecrawl](https://github.com/firecrawl/firecrawl) |
| Crawlee | Crawling e automação programável | Em avaliação | E1 | Apache-2.0 | [apify/crawlee](https://github.com/apify/crawlee) |
| Maxun self-hosted | Extração visual/no-code | Em avaliação | E1 | AGPL-3.0 | [getmaxun/maxun](https://github.com/getmaxun/maxun) |
| Google Maps Scraper | Coleta autorizada de resultados de mapas | Em avaliação | E1 | MIT | [gosom/google-maps-scraper](https://github.com/gosom/google-maps-scraper) |
| Nominatim | Busca e geocodificação sobre dados OpenStreetMap | Em avaliação | E1 | Python: GPL-3.0-or-later; outros arquivos: GPL-2.0 ou Apache-2.0; dados OSM: ODbL | [osm-search/Nominatim](https://github.com/osm-search/Nominatim) |
| SearXNG | Metabusca hospedada pelo usuário | Em avaliação | E1 | AGPL-3.0 | [searxng/searxng](https://github.com/searxng/searxng) |

## Interface, documentos, qualidade e segurança

| Ferramenta | Para que serve | Status | Evidência | Licença/modelo | Fonte oficial | Alternativa OSS |
|---|---|---|---|---|---|---|
| Three.js | Gráficos 3D na web | Em avaliação | E1 | MIT | [mrdoob/three.js](https://github.com/mrdoob/three.js) | — |
| Anime.js | Animações web | Em avaliação | E1 | MIT | [juliangarnier/anime](https://github.com/juliangarnier/anime) | — |
| Motion | Animações e gestos em interfaces | Em avaliação | E1 | MIT | [motiondivision/motion](https://github.com/motiondivision/motion) | — |
| shadcn/ui | Componentes copiáveis para React | Em avaliação | E1 | MIT | [shadcn-ui/ui](https://github.com/shadcn-ui/ui) | — |
| Magic UI | Componentes visuais para React | Em avaliação | E1 | MIT | [magicuidesign/magicui](https://github.com/magicuidesign/magicui) | — |
| React Bits (repositório público) | Componentes animados para React | Em avaliação | E1 | [MIT + Commons Clause](https://github.com/DavidHDev/react-bits/blob/main/LICENSE.md); source-available, não OSS | [DavidHDev/react-bits](https://github.com/DavidHDev/react-bits) | [shadcn/ui](https://github.com/shadcn-ui/ui) — não oferece os mesmos efeitos |
| pytest | Testes em Python | Em avaliação | E1 | MIT | [pytest-dev/pytest](https://github.com/pytest-dev/pytest) | — |
| Ruff | Lint e formatação de Python | Em avaliação | E1 | MIT | [astral-sh/ruff](https://github.com/astral-sh/ruff) | — |
| python-docx | Gerar e editar DOCX | Em avaliação | E1 | MIT | [python-openxml/python-docx](https://github.com/python-openxml/python-docx) | — |
| python-pptx | Gerar e editar PPTX | Em avaliação | E1 | MIT | [scanny/python-pptx](https://github.com/scanny/python-pptx) | — |
| pypdf | Ler e transformar PDF | Em avaliação | E1 | BSD-3-Clause | [py-pdf/pypdf](https://github.com/py-pdf/pypdf) | — |
| XlsxWriter | Gerar arquivos XLSX | Em avaliação | E1 | BSD-2-Clause | [jmcnamara/XlsxWriter](https://github.com/jmcnamara/XlsxWriter) | — |
| OpenSSF Scorecard | Sinais automatizados de segurança de repositório | Em avaliação | E1 | Apache-2.0 | [ossf/scorecard](https://github.com/ossf/scorecard) | — |
| OWASP ASVS | Requisitos verificáveis de segurança de aplicações | Referência | E1 | CC BY-SA 4.0 | [OWASP/ASVS](https://github.com/OWASP/ASVS) | — |
| OWASP Cheat Sheet Series | Guias práticos de segurança | Referência | E1 | CC BY-SA 4.0 | [OWASP/CheatSheetSeries](https://github.com/OWASP/CheatSheetSeries) | — |
| EspoCRM | CRM hospedado pelo usuário | Em avaliação | E1 | AGPL-3.0 | [espocrm/espocrm](https://github.com/espocrm/espocrm) | — |

## Regra de promoção

Para mudar uma entrada para **Verificada**, crie um registro pelo
[modelo de ferramenta](tool-entry-template.md), execute instalação e caso mínimo em
ambiente declarado e ligue a linha à evidência E3. Consulta de repositório, licença
ou documentação sustenta E1; não sustenta funcionamento.
