from pathlib import Path
import ast
import subprocess
import unittest


ROOT = Path(__file__).resolve().parents[1]

DOTENV_ENTRYPOINTS = (
    ROOT / "archive" / "happy-case-mvp" / "streamlit_app.py",
    ROOT / "archive" / "happy-case-mvp" / "run_happy_case.py",
)

PRODUCTION_SOURCES = (
    ROOT / "app.py",
    *sorted((ROOT / "src").rglob("*.py")),
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
                "/.streamlit.*.log",
                "/.superpowers/",
                "_bmad-output/",
                "*.pem",
                "*.key",
            },
            ignore_rules,
        )

    def test_runtime_artifact_ignore_rules_are_root_scoped(self) -> None:
        for runtime_path in (
            ".streamlit.stderr.log",
            ".superpowers/brainstorm/state/server.pid",
        ):
            result = subprocess.run(
                ["git", "check-ignore", "--quiet", "--no-index", "--", runtime_path],
                cwd=ROOT,
                capture_output=True,
                text=True,
                check=False,
            )
            with self.subTest(runtime_path=runtime_path):
                self.assertEqual(0, result.returncode, result.stderr)

        for nested_path in (
            "src/.streamlit.stderr.log",
            "docs/.superpowers/brainstorm/state/server.pid",
            "docs/superpowers/specs/2026-08-03-midnight-aurora-ui-design.md",
        ):
            result = subprocess.run(
                ["git", "check-ignore", "--quiet", "--no-index", "--", nested_path],
                cwd=ROOT,
                capture_output=True,
                text=True,
                check=False,
            )
            with self.subTest(nested_path=nested_path):
                self.assertEqual(1, result.returncode, result.stderr)

    def test_runtime_artifacts_are_untracked_or_pending_deletion(self) -> None:
        tracked_result = subprocess.run(
            ["git", "ls-files", "-z"],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=True,
        )
        deleted_result = subprocess.run(
            ["git", "ls-files", "--deleted", "-z"],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=True,
        )
        tracked = {path for path in tracked_result.stdout.split("\0") if path}
        pending_deletion = {path for path in deleted_result.stdout.split("\0") if path}
        tracked_runtime = {
            path
            for path in tracked
            if (
                path.startswith(".superpowers/")
                or (path.startswith(".streamlit.") and path.endswith(".log"))
            )
        }

        self.assertEqual(set(), tracked_runtime - pending_deletion)

    def test_production_sources_do_not_import_archive(self) -> None:
        for source in PRODUCTION_SOURCES:
            tree = ast.parse(source.read_text(encoding="utf-8"), filename=str(source))
            imported_modules = {
                alias.name
                for node in ast.walk(tree)
                if isinstance(node, ast.Import)
                for alias in node.names
            }
            imported_modules.update(
                node.module
                for node in ast.walk(tree)
                if isinstance(node, ast.ImportFrom) and node.module
            )
            importlib_aliases = {"importlib"}
            import_module_aliases = {"__import__", "import_module"}
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    importlib_aliases.update(
                        alias.asname or alias.name
                        for alias in node.names
                        if alias.name == "importlib"
                    )
                elif isinstance(node, ast.ImportFrom) and node.module == "importlib":
                    import_module_aliases.update(
                        alias.asname or alias.name
                        for alias in node.names
                        if alias.name == "import_module"
                    )

            for node in ast.walk(tree):
                if not isinstance(node, ast.Call):
                    continue
                calls_import_module = (
                    (
                        isinstance(node.func, ast.Name)
                        and node.func.id in import_module_aliases
                    )
                    or (
                        isinstance(node.func, ast.Attribute)
                        and isinstance(node.func.value, ast.Name)
                        and node.func.value.id in importlib_aliases
                        and node.func.attr == "import_module"
                    )
                )
                if not calls_import_module:
                    continue
                module_argument = node.args[0] if node.args else next(
                    (
                        keyword.value
                        for keyword in node.keywords
                        if keyword.arg == "name"
                    ),
                    None,
                )
                if (
                    isinstance(module_argument, ast.Constant)
                    and isinstance(module_argument.value, str)
                ):
                    imported_modules.add(module_argument.value)
            archive_imports = {
                module
                for module in imported_modules
                if module == "archive" or module.startswith("archive.")
            }
            with self.subTest(source=source):
                self.assertEqual(set(), archive_imports)

    def test_main_app_uses_stretch_width_without_deprecated_keyword(self) -> None:
        source = ROOT / "app.py"
        tree = ast.parse(source.read_text(encoding="utf-8"), filename=str(source))
        calls = [node for node in ast.walk(tree) if isinstance(node, ast.Call)]
        deprecated_lines = [
            call.lineno
            for call in calls
            if any(keyword.arg == "use_container_width" for keyword in call.keywords)
        ]
        self.assertEqual([], deprecated_lines)

        def is_streamlit_call(call: ast.Call, name: str) -> bool:
            return (
                isinstance(call.func, ast.Attribute)
                and isinstance(call.func.value, ast.Name)
                and call.func.value.id == "st"
                and call.func.attr == name
            )

        def has_stretch_width(call: ast.Call) -> bool:
            return any(
                keyword.arg == "width"
                and isinstance(keyword.value, ast.Constant)
                and keyword.value.value == "stretch"
                for keyword in call.keywords
            )

        analyze_button = [
            call
            for call in calls
            if is_streamlit_call(call, "button")
            and call.args
            and isinstance(call.args[0], ast.Constant)
            and call.args[0].value == "Phân tích tài liệu"
        ]
        preview_popover = [
            call
            for call in calls
            if is_streamlit_call(call, "popover")
            and call.args
            and isinstance(call.args[0], ast.Constant)
            and call.args[0].value == "Mở ảnh lớn"
        ]
        preview_expression = ast.dump(
            ast.parse("document.pages[0].data", mode="eval").body,
            include_attributes=False,
        )
        preview_images = [
            call
            for call in calls
            if is_streamlit_call(call, "image")
            and call.args
            and ast.dump(call.args[0], include_attributes=False) == preview_expression
        ]

        self.assertEqual(1, len(analyze_button))
        self.assertTrue(has_stretch_width(analyze_button[0]))
        self.assertEqual(1, len(preview_popover))
        self.assertTrue(has_stretch_width(preview_popover[0]))
        self.assertEqual(2, len(preview_images))
        self.assertTrue(all(has_stretch_width(call) for call in preview_images))

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
