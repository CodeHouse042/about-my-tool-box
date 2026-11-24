"""Exercise the repository verifier CLI against isolated repository copies."""

from __future__ import annotations

import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
READ_REQUIRED_FILES = (
    "catalog/tools.md",
    "catalog/paid-services.md",
    "guides/verification.md",
)


class RepositoryVerifierTests(unittest.TestCase):
    def setUp(self) -> None:
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.repository = Path(temporary.name) / "repository"
        shutil.copytree(
            ROOT,
            self.repository,
            ignore=shutil.ignore_patterns(".git", "reports", "__pycache__"),
        )

    def run_verifier(self) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, "-X", "utf8", "scripts/verify_repository.py"],
            cwd=self.repository,
            capture_output=True,
            text=True,
            encoding="utf-8",
            check=False,
            timeout=30,
        )

    def assert_reported_failure(self, result: subprocess.CompletedProcess[str]) -> None:
        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        self.assertEqual(result.stderr, "")
        self.assertIn("Falhas:", result.stdout)
        self.assertNotIn("Verificação concluída sem falhas.", result.stdout)

    def assert_catalog_counts(self, output: str, missing: str) -> None:
        for label, path in (
            ("Ferramentas validadas no contrato", "catalog/tools.md"),
            ("Serviços pagos/híbridos validados", "catalog/paid-services.md"),
        ):
            expected = "0" if path == missing else "[1-9][0-9]*"
            self.assertRegex(output, rf"(?m)^{label}: {expected}$")

    def test_complete_repository_passes(self) -> None:
        result = self.run_verifier()
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual(result.stderr, "")
        self.assertIn("Verificação concluída sem falhas.", result.stdout)

    def test_missing_required_file_is_reported(self) -> None:
        cases = READ_REQUIRED_FILES + (
            "README.md",
            "catalog/evidence/public-oss-sources-2026-09-04.md",
        )
        for relative in cases:
            with self.subTest(missing=relative):
                path = self.repository / relative
                original = path.read_bytes()
                path.unlink()
                try:
                    result = self.run_verifier()
                    self.assert_reported_failure(result)
                    self.assertIn(f"arquivo obrigatório ausente: {relative}", result.stdout)
                    self.assert_catalog_counts(result.stdout, relative)
                finally:
                    path.write_bytes(original)

    def test_simultaneous_missing_files_are_reported_together(self) -> None:
        for relative in READ_REQUIRED_FILES:
            (self.repository / relative).unlink()
        result = self.run_verifier()
        self.assert_reported_failure(result)
        for relative in READ_REQUIRED_FILES:
            self.assertIn(f"arquivo obrigatório ausente: {relative}", result.stdout)
        self.assertIn("Ferramentas validadas no contrato: 0", result.stdout)
        self.assertIn("Serviços pagos/híbridos validados: 0", result.stdout)

    def test_missing_files_do_not_skip_privacy_checks(self) -> None:
        for relative in READ_REQUIRED_FILES:
            (self.repository / relative).unlink()
        (self.repository / ".env").write_text("EXAMPLE_VALUE\n", encoding="utf-8")
        result = self.run_verifier()
        self.assert_reported_failure(result)
        self.assertIn("arquivo sensível proibido: .env", result.stdout)

    def test_missing_catalog_does_not_skip_remaining_catalog(self) -> None:
        cases = (
            ("catalog/tools.md", "catalog/paid-services.md", "nenhum serviço reconhecido"),
            ("catalog/paid-services.md", "catalog/tools.md", "nenhuma ferramenta reconhecida"),
        )
        for missing, remaining, diagnostic in cases:
            with self.subTest(missing=missing):
                missing_path = self.repository / missing
                remaining_path = self.repository / remaining
                original_missing = missing_path.read_bytes()
                original_remaining = remaining_path.read_bytes()
                missing_path.unlink()
                remaining_path.write_text("# Catálogo vazio\n", encoding="utf-8")
                try:
                    result = self.run_verifier()
                    self.assert_reported_failure(result)
                    self.assertIn(diagnostic, result.stdout)
                finally:
                    missing_path.write_bytes(original_missing)
                    remaining_path.write_bytes(original_remaining)

    def test_present_guide_still_requires_e3_rule(self) -> None:
        (self.repository / "guides/verification.md").write_text(
            "# Guia incompleto\n", encoding="utf-8"
        )
        result = self.run_verifier()
        self.assert_reported_failure(result)
        self.assertIn("critério 'Somente E3' não está declarado", result.stdout)


if __name__ == "__main__":
    unittest.main()
