from pathlib import Path
import ast
import unittest


ROOT = Path(__file__).resolve().parents[1]


class RepositoryHygieneTests(unittest.TestCase):
    def test_active_sources_do_not_embed_credentials(self) -> None:
        sources = [
            ROOT / "streamlit_app.py",
            ROOT / "scripts" / "legacy" / "run_happy_case.py",
        ]

        for source in sources:
            tree = ast.parse(source.read_text(encoding="utf-8"), filename=str(source))
            embedded_names = {
                target.id
                for node in tree.body
                if isinstance(node, ast.Assign)
                for target in node.targets
                if isinstance(target, ast.Name) and target.id in {"API_KEY", "HF_TOKEN"}
            }
            with self.subTest(source=source):
                self.assertEqual(set(), embedded_names)

    def test_active_sources_load_dotenv(self) -> None:
        sources = [
            ROOT / "streamlit_app.py",
            ROOT / "scripts" / "legacy" / "run_happy_case.py",
        ]

        for source in sources:
            content = source.read_text(encoding="utf-8")
            with self.subTest(source=source):
                self.assertTrue(
                    "from dotenv import load_dotenv" in content and "load_dotenv(" in content,
                    f"{source} must load credentials from the root .env file",
                )

    def test_canonical_project_documentation_exists(self) -> None:
        expected = {
            ROOT / "docs" / "spec.md",
            ROOT / "docs" / "plan.md",
            ROOT / "docs" / "process.md",
        }

        self.assertEqual(set(), {path for path in expected if not path.is_file()})

    def test_generated_and_local_environment_directories_are_ignored(self) -> None:
        ignore_file = ROOT / ".gitignore"
        self.assertTrue(ignore_file.is_file())

        ignore_rules = set(ignore_file.read_text(encoding="utf-8").splitlines())
        self.assertLessEqual(
            {
                ".venv/",
                "__pycache__/",
                ".env",
                ".env.*",
                "!.env.example",
                "AI Thesis & Accessibility Solution Analyst_BK/",
                ".streamlit/",
                "_bmad-output/",
                "*.pem",
                "*.key",
            },
            ignore_rules,
        )

    def test_dotenv_dependency_is_declared(self) -> None:
        requirements = (ROOT / "requirements.txt").read_text(encoding="utf-8")
        self.assertTrue(
            "python-dotenv" in requirements,
            "requirements.txt must declare python-dotenv",
        )

    def test_root_cli_resolves_relative_paths_from_project_root(self) -> None:
        wrapper = (ROOT / "run_happy_case.py").read_text(encoding="utf-8")
        legacy = (ROOT / "scripts" / "legacy" / "run_happy_case.py").read_text(
            encoding="utf-8"
        )

        self.assertIn("cwd=root_dir", wrapper)
        self.assertIn('default="assets/samples/bar.png"', legacy)

    def test_personal_bmad_config_is_ignored_and_scan_state_is_absent(self) -> None:
        ignore_rules = set((ROOT / ".gitignore").read_text(encoding="utf-8").splitlines())

        self.assertIn("_bmad/config.user.toml", ignore_rules)
        self.assertFalse((ROOT / "docs" / "project-scan-report.json").exists())

    def test_legacy_cli_does_not_accept_api_keys_on_the_command_line(self) -> None:
        legacy = (ROOT / "scripts" / "legacy" / "run_happy_case.py").read_text(
            encoding="utf-8"
        )

        self.assertNotIn('"--api-key"', legacy)

    def test_tts_helper_does_not_import_source_files_to_find_secrets(self) -> None:
        helper = ROOT / "scripts" / "legacy" / "hf_inference_tts.py"
        source = helper.read_text(encoding="utf-8")

        self.assertNotIn("importlib.util", source)
        self.assertNotIn("getattr(rc, \"HF_TOKEN\"", source)


if __name__ == "__main__":
    unittest.main()
