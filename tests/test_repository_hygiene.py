from pathlib import Path
import ast
import unittest


ROOT = Path(__file__).resolve().parents[1]

DOTENV_ENTRYPOINTS = (
    ROOT / "archive" / "happy-case-mvp" / "streamlit_app.py",
    ROOT / "archive" / "happy-case-mvp" / "run_happy_case.py",
)


class RepositoryHygieneTests(unittest.TestCase):
    def test_happy_case_mvp_is_archived_and_root_entrypoint_is_released(self):
        archive = ROOT / "archive" / "happy-case-mvp"
        self.assertTrue((archive / "streamlit_app.py").is_file())
        self.assertTrue((archive / "run_happy_case.py").is_file())
        self.assertTrue((archive / "README.md").is_file())
        self.assertFalse((ROOT / "streamlit_app.py").exists())
        self.assertFalse((ROOT / "run_happy_case.py").exists())

    def test_active_sources_do_not_embed_credentials(self) -> None:
        for source in DOTENV_ENTRYPOINTS:
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
        for source in DOTENV_ENTRYPOINTS:
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

    def test_archived_cli_resolves_streamlit_app_from_project_root(self) -> None:
        wrapper = (
            ROOT / "archive" / "happy-case-mvp" / "run_happy_case.py"
        ).read_text(encoding="utf-8")

        self.assertIn('PROJECT_ROOT = Path(__file__).resolve().parents[2]', wrapper)
        self.assertIn(
            'app_path = PROJECT_ROOT / "archive" / "happy-case-mvp" / "streamlit_app.py"',
            wrapper,
        )

    def test_personal_bmad_config_is_ignored_and_scan_state_is_absent(self) -> None:
        ignore_rules = set((ROOT / ".gitignore").read_text(encoding="utf-8").splitlines())

        self.assertIn("_bmad/config.user.toml", ignore_rules)
        self.assertFalse((ROOT / "docs" / "project-scan-report.json").exists())

if __name__ == "__main__":
    unittest.main()
