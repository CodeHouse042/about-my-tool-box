#!/usr/bin/env python3
"""Validate structure, catalog contracts, privacy and optional external URLs."""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
import time
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import urlparse
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
PUBLIC_SOURCE_EVIDENCE = (
    ROOT / "catalog/evidence/public-oss-sources-2026-09-04.md"
)
REQUIRED = (
    "README.md",
    "AGENTS.md",
    "LICENSE",
    "CONTRIBUTING.md",
    "SECURITY.md",
    "catalog/tools.md",
    "catalog/paid-services.md",
    "catalog/mcp-servers.md",
    "catalog/retired.md",
    "catalog/evidence/base-toolchain.md",
    "catalog/evidence/public-oss-sources-2026-09-04.md",
    "guides/ai-guided-development.md",
    "guides/verification.md",
    "projects/interview-template.md",
    "projects/spec-template.md",
)
LINK_RE = re.compile(r"(?<!!)\[[^\]]+\]\(([^)]+)\)")
PLACEHOLDER_URL_RE = re.compile(r"https?://[^\s`)\]]*<[^\s`)\]]*>")
PRIVATE_PATH_RE = re.compile(
    r"(?:[A-Za-z]:\\Users\\[^\\\s]+|/(?:home|Users)/[^/\s`]+)"
)
EMAIL_RE = re.compile(
    r"(?<![\w.+-])[A-Za-z0-9.!#$%&'*+/=?^_`{|}~-]+@"
    r"[A-Za-z0-9-]+(?:\.[A-Za-z0-9-]+)+"
)
PHONE_RE = re.compile(
    r"(?<!\d)(?:\+?55[ .-]?)?\(?\d{2}\)?[ .-]?9?\d{4}[ .-]\d{4}(?!\d)"
)
GITHUB_RE = re.compile(
    r"https://github\.com/[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+"
)
SECRET_ASSIGNMENT_RE = re.compile(
    r"(?i)\b(api[_-]?key|access[_-]?token|auth[_-]?token|password|passwd|secret)"
    r"\s*[:=]\s*[\"']?([^\s\"'#]{8,})"
)
SECRET_PATTERNS = (
    ("chave privada", re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH |DSA )?PRIVATE KEY-----")),
    ("token GitHub", re.compile(r"\b(?:gh[pousr]_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{20,})\b")),
    ("chave OpenAI", re.compile(r"\bsk-[A-Za-z0-9_-]{20,}\b")),
    ("chave AWS", re.compile(r"\bAKIA[0-9A-Z]{16}\b")),
    ("token Slack", re.compile(r"\bxox[baprs]-[A-Za-z0-9-]{10,}\b")),
    ("Bearer literal", re.compile(r"(?i)\bBearer\s+[A-Za-z0-9._~+/-]{16,}={0,2}\b")),
    ("JWT literal", re.compile(r"\beyJ[A-Za-z0-9_-]{8,}\.[A-Za-z0-9_-]{8,}\.[A-Za-z0-9_-]{8,}\b")),
)
ALLOWED_EMAIL_DOMAINS = {
    "example.com",
    "example.org",
    "example.net",
    "users.noreply.github.com",
}
PLACEHOLDER_MARKERS = (
    "EXAMPLE",
    "CHANGEME",
    "REPLACE",
    "YOUR_",
    "DUMMY",
    "REDACTED",
    "<",
    "${",
)
TEXT_SUFFIXES = {
    ".md",
    ".py",
    ".yml",
    ".yaml",
    ".json",
    ".toml",
    ".txt",
    ".ini",
    ".cfg",
    ".sh",
    ".ps1",
}
FORBIDDEN_FILE_SUFFIXES = {".pem", ".key", ".token", ".p12", ".pfx", ".jks"}
FORBIDDEN_FILE_NAMES = {"credentials.json", "id_rsa", "id_ed25519"}


def markdown_files() -> list[Path]:
    return sorted(
        path
        for path in ROOT.rglob("*.md")
        if ".git" not in path.parts and "reports" not in path.parts
    )


def text_files() -> list[Path]:
    selected: list[Path] = []
    for path in ROOT.rglob("*"):
        if not path.is_file() or ".git" in path.parts or "reports" in path.parts:
            continue
        lowered = path.name.lower()
        if (
            path.suffix.lower() in TEXT_SUFFIXES | FORBIDDEN_FILE_SUFFIXES
            or path.name in {"LICENSE", ".gitignore", ".gitattributes"}
            or lowered in FORBIDDEN_FILE_NAMES
            or lowered.startswith("service-account")
            or lowered.startswith(".env")
        ):
            selected.append(path)
    return sorted(selected)


def external_links() -> list[tuple[Path, str]]:
    links: list[tuple[Path, str]] = []
    for path in markdown_files():
        for match in LINK_RE.finditer(path.read_text(encoding="utf-8")):
            target = match.group(1).strip().strip("<>")
            if target.startswith(("http://", "https://")):
                links.append((path, target))
    return sorted(set(links))


def split_table_row(line: str) -> list[str]:
    return [cell.strip() for cell in line.strip().strip("|").split("|")]


def markdown_tables(text: str) -> list[tuple[list[str], list[list[str]]]]:
    lines = text.splitlines()
    tables: list[tuple[list[str], list[list[str]]]] = []
    index = 0
    while index + 1 < len(lines):
        if not lines[index].lstrip().startswith("|"):
            index += 1
            continue
        header = split_table_row(lines[index])
        separator = split_table_row(lines[index + 1])
        if len(header) != len(separator) or not all(
            re.fullmatch(r":?-{3,}:?", cell) for cell in separator
        ):
            index += 1
            continue
        rows: list[list[str]] = []
        index += 2
        while index < len(lines) and lines[index].lstrip().startswith("|"):
            row = split_table_row(lines[index])
            if len(row) == len(header):
                rows.append(row)
            index += 1
        tables.append((header, rows))
    return tables


def check_local_links(errors: list[str]) -> int:
    count = 0
    for path in markdown_files():
        text = path.read_text(encoding="utf-8")
        for match in LINK_RE.finditer(text):
            target = match.group(1).strip().strip("<>")
            if not target or target.startswith(("http://", "https://", "#")):
                continue
            target = target.split("#", 1)[0].split("?", 1)[0]
            if not target:
                continue
            count += 1
            destination = (path.parent / target).resolve()
            if not destination.is_relative_to(ROOT) or not destination.exists():
                errors.append(
                    f"link interno inexistente: {path.relative_to(ROOT)} -> {target}"
                )
    return count


def sensitive_findings(text: str) -> list[str]:
    findings: list[str] = []
    if PRIVATE_PATH_RE.search(text):
        findings.append("caminho pessoal")
    if PHONE_RE.search(text):
        findings.append("telefone provável")
    for email in EMAIL_RE.findall(text):
        domain = email.rsplit("@", 1)[1].lower()
        if domain not in ALLOWED_EMAIL_DOMAINS:
            findings.append("e-mail não reservado")
            break
    for label, pattern in SECRET_PATTERNS:
        if pattern.search(text):
            findings.append(label)
    for match in SECRET_ASSIGNMENT_RE.finditer(text):
        value = match.group(2).upper()
        if not any(marker in value for marker in PLACEHOLDER_MARKERS):
            findings.append(f"valor literal para {match.group(1)}")
            break
    return findings


def is_forbidden_path(path: Path) -> bool:
    lowered = path.name.lower()
    return (
        path.suffix.lower() in FORBIDDEN_FILE_SUFFIXES
        or lowered in FORBIDDEN_FILE_NAMES
        or lowered.startswith("service-account")
        or (lowered.startswith(".env") and lowered != ".env.example")
    )


def check_sensitive_tree(errors: list[str]) -> int:
    checked = 0
    for path in text_files():
        relative = path.relative_to(ROOT)
        if is_forbidden_path(path):
            errors.append(f"arquivo sensível proibido: {relative}")
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        checked += 1
        for finding in sensitive_findings(text):
            errors.append(f"dado sensível ({finding}): {relative}")
    return checked


def check_tool_catalog(errors: list[str]) -> int:
    path = ROOT / "catalog/tools.md"
    text = path.read_text(encoding="utf-8")
    evidence_text = (
        PUBLIC_SOURCE_EVIDENCE.read_text(encoding="utf-8")
        if PUBLIC_SOURCE_EVIDENCE.exists()
        else ""
    )
    checked = 0
    allowed_statuses = {"Verificada", "Em avaliação", "Referência"}
    for header, rows in markdown_tables(text):
        if not header or header[0] != "Ferramenta":
            continue
        indexes = {name: position for position, name in enumerate(header)}
        required_columns = {
            "Ferramenta",
            "Status",
            "Evidência",
            "Fonte oficial",
        }
        missing = required_columns.difference(indexes)
        if missing:
            errors.append(f"colunas ausentes em catalog/tools.md: {sorted(missing)}")
            continue
        for row in rows:
            checked += 1
            name = row[indexes["Ferramenta"]]
            status = row[indexes["Status"]]
            evidence = row[indexes["Evidência"]]
            source = row[indexes["Fonte oficial"]]
            if status not in allowed_statuses:
                errors.append(f"status inválido para {name}: {status}")
            if "http://" not in source and "https://" not in source:
                errors.append(f"fonte oficial ausente para {name}")
            if status == "Verificada" and "E3" not in evidence:
                errors.append(f"ferramenta Verificada sem E3: {name}")
            if status != "Verificada" and "E3" in evidence:
                errors.append(f"E3 com status incompatível: {name} -> {status}")
            model_column = indexes.get("Modelo/licença", indexes.get("Licença/modelo"))
            alternative_column = indexes.get("Alternativa OSS")
            if model_column is None:
                errors.append(f"licença/modelo ausente para {name}")
                continue
            model = row[model_column]
            if not model or re.search(
                r"Confirmar|Desconhecid[oa]|(?:^|\s)[?—](?:\s|$)",
                model,
                re.IGNORECASE,
            ):
                errors.append(f"licença/modelo não resolvido para {name}: {model}")
            if re.search(
                r"Pago|Híbrido|Freemium|source-available", model, re.IGNORECASE
            ):
                alternative = (
                    row[alternative_column] if alternative_column is not None else ""
                )
                repositories = GITHUB_RE.findall(alternative)
                if not repositories:
                    errors.append(
                        f"entrada paga/híbrida/source-available sem alternativa Git OSS: {name}"
                    )
                for repository in repositories:
                    if repository not in evidence_text:
                        errors.append(
                            f"alternativa sem evidência pública datada: {name} -> {repository}"
                        )
    if checked == 0:
        errors.append("nenhuma ferramenta reconhecida em catalog/tools.md")
    return checked


def check_paid_services(errors: list[str]) -> int:
    path = ROOT / "catalog/paid-services.md"
    text = path.read_text(encoding="utf-8")
    evidence_text = (
        PUBLIC_SOURCE_EVIDENCE.read_text(encoding="utf-8")
        if PUBLIC_SOURCE_EVIDENCE.exists()
        else ""
    )
    if not re.search(r"Consulta.+20\d{2}-\d{2}-\d{2}", text):
        errors.append("data de consulta ausente em catalog/paid-services.md")
    checked = 0
    for header, rows in markdown_tables(text):
        if not header or header[0] != "Serviço e modelo":
            continue
        indexes = {name: position for position, name in enumerate(header)}
        for required in (
            "Serviço e modelo",
            "Alternativa OSS pública no Git",
            "Licença da alternativa",
            "Diferença essencial",
        ):
            if required not in indexes:
                errors.append(f"coluna ausente em catalog/paid-services.md: {required}")
                return checked
        for row in rows:
            checked += 1
            service = row[indexes["Serviço e modelo"]]
            alternative = row[indexes["Alternativa OSS pública no Git"]]
            license_name = row[indexes["Licença da alternativa"]]
            difference = row[indexes["Diferença essencial"]]
            if not re.search(r"Pago|Híbrido|Freemium|source-available", service, re.IGNORECASE):
                errors.append(f"modelo de custo ausente: {service}")
            if "https://github.com/" not in alternative:
                errors.append(f"alternativa sem repositório GitHub público: {service}")
            if not license_name or license_name in {"—", "?"}:
                errors.append(f"licença da alternativa ausente: {service}")
            if re.search(
                r"source-available|Commons Clause|BUSL|BSL|SSPL",
                license_name,
                re.IGNORECASE,
            ):
                errors.append(f"alternativa declarada como OSS tem licença restritiva: {service}")
            for repository in GITHUB_RE.findall(alternative):
                if repository not in evidence_text:
                    errors.append(
                        f"alternativa sem evidência pública datada: {service} -> {repository}"
                    )
            if len(re.sub(r"\[[^]]+\]\([^)]+\)", "", difference).strip()) < 20:
                errors.append(f"diferença funcional insuficiente: {service}")
    if checked == 0:
        errors.append("nenhum serviço reconhecido em catalog/paid-services.md")
    return checked


def check_content(errors: list[str]) -> tuple[int, int, int]:
    for relative in REQUIRED:
        if not (ROOT / relative).exists():
            errors.append(f"arquivo obrigatório ausente: {relative}")

    for path in markdown_files():
        text = path.read_text(encoding="utf-8")
        if PLACEHOLDER_URL_RE.search(text):
            errors.append(f"URL placeholder encontrada: {path.relative_to(ROOT)}")

    verification_path = ROOT / "guides/verification.md"
    if verification_path.exists():
        verification = verification_path.read_text(encoding="utf-8")
        if "Somente E3" not in verification:
            errors.append("critério 'Somente E3' não está declarado")

    sensitive_count = check_sensitive_tree(errors)
    tool_count = (
        check_tool_catalog(errors) if (ROOT / "catalog/tools.md").exists() else 0
    )
    paid_count = (
        check_paid_services(errors) if (ROOT / "catalog/paid-services.md").exists() else 0
    )
    return sensitive_count, tool_count, paid_count


def run_git(*args: str, text: bool = True) -> subprocess.CompletedProcess:
    return subprocess.run(
        ["git", *args],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=text,
    )


def check_history(errors: list[str]) -> int:
    if not (ROOT / ".git").exists():
        errors.append("histórico solicitado, mas checkout Git não está disponível")
        return 0

    authors = run_git(
        "log", "HEAD", "--branches", "--tags", "--format=%H%x00%an%x00%ae"
    )
    if authors.returncode != 0:
        errors.append("não foi possível ler autores do histórico Git")
        return 0
    commit_ids: list[str] = []
    for line in authors.stdout.splitlines():
        parts = line.split("\x00")
        if len(parts) != 3:
            continue
        commit, name, email = parts
        commit_ids.append(commit)
        if not email.lower().endswith("@users.noreply.github.com"):
            errors.append(f"autor com e-mail não anonimizado no commit {commit[:12]}")
        if any(character.isspace() for character in name.strip()):
            errors.append(f"autor deve usar identificador público no commit {commit[:12]}")

    for commit in commit_ids:
        message = run_git("show", "-s", "--format=%B", commit)
        if message.returncode != 0:
            errors.append(f"não foi possível ler mensagem do commit {commit[:12]}")
            continue
        nonempty_lines = [line for line in message.stdout.splitlines() if line.strip()]
        if len(nonempty_lines) != 1:
            errors.append(f"mensagem histórica deve ter somente assunto: {commit[:12]}")
        for finding in sensitive_findings(message.stdout):
            errors.append(
                f"mensagem de commit contém dado sensível ({finding}): {commit[:12]}"
            )

    objects = run_git("rev-list", "--objects", "HEAD", "--branches", "--tags")
    if objects.returncode != 0:
        errors.append("não foi possível enumerar objetos do histórico Git")
        return 0

    checked = 0
    seen: set[str] = set()
    for line in objects.stdout.splitlines():
        parts = line.split(" ", 1)
        object_id = parts[0]
        display_path = parts[1] if len(parts) == 2 else "objeto-sem-caminho"
        if is_forbidden_path(Path(display_path)):
            errors.append(f"histórico contém arquivo sensível: {display_path}")
        # O próprio detector contém assinaturas e regex de caminhos; tratá-las como
        # achado histórico produziria um falso positivo inevitável.
        if display_path == "scripts/verify_repository.py":
            continue
        if object_id in seen:
            continue
        seen.add(object_id)
        kind = run_git("cat-file", "-t", object_id)
        if kind.returncode != 0 or kind.stdout.strip() != "blob":
            continue
        size = run_git("cat-file", "-s", object_id)
        if size.returncode != 0 or int(size.stdout.strip()) > 1_000_000:
            continue
        blob = run_git("cat-file", "blob", object_id, text=False)
        if blob.returncode != 0 or b"\x00" in blob.stdout:
            continue
        checked += 1
        text = blob.stdout.decode("utf-8", errors="ignore")
        for finding in sensitive_findings(text):
            errors.append(
                f"histórico contém dado sensível ({finding}): {display_path} [{object_id[:12]}]"
            )
    return checked


def request_status(url: str) -> tuple[int | None, str | None]:
    headers = {"User-Agent": "about-my-tool-box-link-check/2.0"}
    for method in ("HEAD", "GET"):
        try:
            request = Request(url, method=method, headers=headers)
            with urlopen(request, timeout=20) as response:
                return response.status, None
        except HTTPError as exc:
            if method == "HEAD" and exc.code in (403, 405):
                continue
            return exc.code, None
        except (URLError, TimeoutError, OSError) as exc:
            if method == "HEAD":
                continue
            return None, str(exc)
    return None, "sem resposta"


def check_network(errors: list[str], warnings: list[str]) -> int:
    checked = 0
    for path, url in external_links():
        parsed = urlparse(url)
        if parsed.hostname in {"localhost", "127.0.0.1", "::1"}:
            continue
        checked += 1
        status, problem = request_status(url)
        if status in {401, 403, 405, 429}:
            warnings.append(
                f"acesso automatizado restrito: {path.relative_to(ROOT)} -> {url} [{status}]"
            )
        elif status is None or status >= 400:
            suffix = f" ({problem})" if problem else ""
            errors.append(
                f"link externo indisponível: {path.relative_to(ROOT)} -> {url} [{status}]{suffix}"
            )
        time.sleep(0.05)
    return checked


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--network", action="store_true", help="also check external URLs")
    parser.add_argument("--history", action="store_true", help="also scan all reachable Git blobs and author e-mails")
    args = parser.parse_args()

    errors: list[str] = []
    warnings: list[str] = []
    local_count = check_local_links(errors)
    sensitive_count, tool_count, paid_count = check_content(errors)
    history_count = check_history(errors) if args.history else 0
    external_count = check_network(errors, warnings) if args.network else 0

    print(f"Arquivos Markdown: {len(markdown_files())}")
    print(f"Links internos verificados: {local_count}")
    print(f"Arquivos de texto inspecionados: {sensitive_count}")
    print(f"Ferramentas validadas no contrato: {tool_count}")
    print(f"Serviços pagos/híbridos validados: {paid_count}")
    if args.history:
        print(f"Blobs históricos inspecionados: {history_count}")
    if args.network:
        print(f"Links externos verificados: {external_count}")
        if warnings:
            print(f"Avisos de acesso restrito: {len(warnings)}")
            for warning in warnings:
                print(f"- {warning}")
    if errors:
        print(f"Falhas: {len(errors)}")
        for error in errors:
            print(f"- {error}")
        return 1
    print("Verificação concluída sem falhas.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
