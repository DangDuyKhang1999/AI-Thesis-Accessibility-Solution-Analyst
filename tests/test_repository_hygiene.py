from pathlib import Path, PurePosixPath
import ast
from collections import Counter
from html import unescape as html_unescape
import re
import subprocess
import unittest
from urllib.parse import unquote, urlsplit


ROOT = Path(__file__).resolve().parents[1]

DOTENV_ENTRYPOINTS = (
    ROOT / "archive" / "happy-case-mvp" / "streamlit_app.py",
    ROOT / "archive" / "happy-case-mvp" / "run_happy_case.py",
)

PRODUCTION_SOURCES = (
    ROOT / "app.py",
    *sorted((ROOT / "src").rglob("*.py")),
)

WINDOWS_ABSOLUTE_RE = re.compile(r"^[A-Za-z]:[\\/]")


def _visible_markdown(text: str) -> str:
    text = re.sub(r"<!--.*?-->", "", text, flags=re.DOTALL)
    visible = []
    fence_character = None
    fence_length = 0
    for line in text.splitlines():
        fence = re.match(r"^ {0,3}(`{3,}|~{3,})", line)
        if fence:
            marker = fence.group(1)
            if fence_character is None:
                fence_character = marker[0]
                fence_length = len(marker)
            elif marker[0] == fence_character and len(marker) >= fence_length:
                fence_character = None
                fence_length = 0
            visible.append("")
            continue
        if fence_character or line.startswith(("    ", "\t")):
            visible.append("")
            continue
        visible.append(
            re.sub(r"(`+)(.*?)\1", lambda match: " " * len(match.group(0)), line)
        )
    return "\n".join(visible)


def _inline_link_destinations(text: str):
    cursor = 0
    while True:
        marker = text.find("](", cursor)
        if marker < 0:
            return
        if text.rfind("[", 0, marker) < 0:
            cursor = marker + 2
            continue
        position = marker + 2
        while position < len(text) and text[position].isspace():
            position += 1
        if position >= len(text):
            return
        if text[position] == "<":
            end = text.find(">", position + 1)
            if end >= 0:
                yield text[position + 1:end]
                cursor = end + 1
                continue
        start = position
        depth = 0
        escaped = False
        while position < len(text):
            character = text[position]
            if escaped:
                escaped = False
            elif character == "\\":
                escaped = True
            elif character == "(":
                depth += 1
            elif character == ")":
                if depth == 0:
                    yield re.sub(r"\\(.)", r"\1", text[start:position].strip())
                    cursor = position + 1
                    break
                depth -= 1
            elif character.isspace() and depth == 0:
                yield re.sub(r"\\(.)", r"\1", text[start:position].strip())
                closing = text.find(")", position)
                cursor = closing + 1 if closing >= 0 else len(text)
                break
            position += 1
        else:
            return


def _reference_link_destinations(text: str):
    definitions = {}
    definition_spans = []
    for match in re.finditer(
        r"(?m)^\s{0,3}\[([^\]]+)\]:\s*(?:<([^>]+)>|(\S+))",
        text,
    ):
        label = " ".join(match.group(1).casefold().split())
        definitions.setdefault(label, match.group(2) or match.group(3))
        definition_spans.append(match.span())

    occupied = []
    for match in re.finditer(r"\[([^\]]+)\]\[([^\]]*)\]", text):
        occupied.append(match.span())
        label = match.group(2) or match.group(1)
        target = definitions.get(" ".join(label.casefold().split()))
        if target:
            yield target
    for match in re.finditer(r"\[([^\]]+)\](?![\[(])", text):
        if any(
            start <= match.start() < end
            for start, end in [*occupied, *definition_spans]
        ):
            continue
        target = definitions.get(" ".join(match.group(1).casefold().split()))
        if target:
            yield target


def _missing_reference_labels(text: str) -> set[str]:
    definitions = {
        " ".join(match.group(1).casefold().split())
        for match in re.finditer(
            r"(?m)^\s{0,3}\[([^\]]+)\]:\s*(?:<[^>]+>|\S+)",
            text,
        )
    }
    definition_spans = [
        match.span()
        for match in re.finditer(
            r"(?m)^\s{0,3}\[([^\]]+)\]:\s*(?:<[^>]+>|\S+)",
            text,
        )
    ]
    occupied = []
    used = set()
    for match in re.finditer(r"\[([^\]]+)\]\[([^\]]*)\]", text):
        occupied.append(match.span())
        label = match.group(2) or match.group(1)
        used.add(" ".join(label.casefold().split()))
    for match in re.finditer(r"\[([^\]]+)\](?![\[(])", text):
        if any(
            start <= match.start() < end
            for start, end in [*occupied, *definition_spans]
        ):
            continue
        label = " ".join(match.group(1).casefold().split())
        if label in definitions:
            used.add(label)
    return used - definitions


def _markdown_destinations(text: str):
    visible = _visible_markdown(text)
    yield from _inline_link_destinations(visible)
    yield from _reference_link_destinations(visible)
    for match in re.finditer(
        r"\b(?:href|src)\s*=\s*(?:(['\"])(.*?)\1|([^\s\"'=<>`]+))",
        visible,
        re.IGNORECASE,
    ):
        yield match.group(2) or match.group(3)


def _local_markdown_links(source: Path):
    for target in _markdown_destinations(source.read_text(encoding="utf-8")):
        target = target.strip()
        parsed = urlsplit(target)
        if parsed.netloc:
            continue
        if (
            parsed.scheme
            and parsed.scheme.casefold() != "file"
            and not WINDOWS_ABSOLUTE_RE.match(target)
        ):
            continue
        path_part = unquote(parsed.path)
        resolved = source if not path_part else (source.parent / path_part).resolve()
        yield target, resolved, unquote(parsed.fragment)


def _path_has_exact_case(source: Path, path_part: str) -> bool:
    current = source.parent
    for part in PurePosixPath(unquote(path_part)).parts:
        if part == ".":
            continue
        if part == "..":
            current = current.parent
            continue
        if not current.is_dir() or part not in {child.name for child in current.iterdir()}:
            return False
        current /= part
    return True


def _markdown_heading_anchors(source: Path) -> set[str]:
    anchors = set()
    occurrences = Counter()
    visible = _visible_markdown(source.read_text(encoding="utf-8"))
    lines = visible.splitlines()
    headings = []
    for index, line in enumerate(lines):
        match = re.match(r"^ {0,3}#{1,6}\s+(.+?)\s*#*\s*$", line)
        if match:
            headings.append(match.group(1))
        elif (
            line.strip()
            and index + 1 < len(lines)
            and re.match(r"^ {0,3}(?:=+|-+)\s*$", lines[index + 1])
        ):
            headings.append(line.strip())

    for heading in headings:
        heading = re.sub(r"`([^`]*)`", r"\1", heading)
        heading = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", heading)
        heading = re.sub(r"<[^>]+>", "", html_unescape(heading))
        base = re.sub(r"[^\w\s-]", "", heading.lower(), flags=re.UNICODE)
        base = re.sub(r"\s+", "-", base.strip())
        index = occurrences[base]
        occurrences[base] += 1
        anchors.add(base if index == 0 else f"{base}-{index}")
    anchors.update(re.findall(r"\bid\s*=\s*['\"]([^'\"]+)['\"]", visible, re.IGNORECASE))
    return anchors


def _frontmatter_paths(source: Path):
    lines = source.read_text(encoding="utf-8").splitlines()
    if not lines or lines[0].strip() != "---":
        return
    closing = next(
        (index for index, line in enumerate(lines[1:], start=1) if line.strip() == "---"),
        None,
    )
    if closing is None:
        raise ValueError("frontmatter is missing its closing delimiter")
    current_key = None
    for line in lines[1:closing]:
        key = re.match(r"^(sources|companions):\s*(.*?)\s*$", line)
        if key:
            inline_value = key.group(2)
            if inline_value:
                if not (inline_value.startswith("[") and inline_value.endswith("]")):
                    raise ValueError(f"unsupported frontmatter value: {line}")
                for item in inline_value[1:-1].split(","):
                    if item.strip():
                        yield item.strip().strip("'\"")
                current_key = None
            else:
                current_key = key.group(1)
            continue
        item = re.match(r"^\s+-\s+(.+?)\s*$", line)
        if current_key and item:
            yield item.group(1).strip("'\"")
        elif line and not line.startswith((" ", "\t")):
            current_key = None


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

    def test_documentation_index_covers_every_file_once(self) -> None:
        docs_root = ROOT / "docs"
        index = docs_root / "index.md"
        inventory_result = subprocess.run(
            [
                "git",
                "ls-files",
                "--cached",
                "--others",
                "--exclude-standard",
                "-z",
                "--",
                "docs",
            ],
            cwd=ROOT,
            check=True,
            stdout=subprocess.PIPE,
        )
        inventory = {
            ROOT / raw_path.decode("utf-8")
            for raw_path in inventory_result.stdout.split(b"\0")
            if raw_path
        }
        symlinks = sorted(path for path in inventory if path.is_symlink())
        indexed_targets = [
            target.resolve()
            for _, target, _ in _local_markdown_links(index)
            if target.resolve() != index.resolve()
        ]
        target_counts = Counter(indexed_targets)
        actual_files = {
            path.resolve()
            for path in inventory
            if path.is_file() and path != index
        }

        self.assertEqual([], symlinks)
        self.assertEqual(actual_files, set(target_counts))
        self.assertEqual(
            {},
            {str(path): count for path, count in target_counts.items() if count != 1},
        )

    def test_local_markdown_links_and_anchors_resolve(self) -> None:
        syntax_sample = """
[inline](guide(v2).md "Guide")
![image](image.png)
[reference][guide]
[guide]: guide.md "Reference"
<a href=details.html>Details</a>
`[hidden](inline.md)`
    [hidden](indented.md)
[duplicate][dupe]
[dupe]: guide.md
[dupe]: ignored-later-definition.md
[missing][undefined]
<!-- [hidden](comment.md) -->
```markdown
[hidden](fence.md)
```
"""
        self.assertCountEqual(
            ["guide(v2).md", "image.png", "guide.md", "guide.md", "details.html"],
            list(_markdown_destinations(syntax_sample)),
        )
        self.assertEqual({"undefined"}, _missing_reference_labels(_visible_markdown(syntax_sample)))
        markdown_files = [ROOT / "README.md", *sorted((ROOT / "docs").rglob("*.md"))]
        failures = []
        for source in markdown_files:
            visible = _visible_markdown(source.read_text(encoding="utf-8"))
            for label in sorted(_missing_reference_labels(visible)):
                failures.append(f"{source}: missing reference definition [{label}]")
            for raw_target, target, fragment in _local_markdown_links(source):
                parsed = urlsplit(raw_target)
                path_part = unquote(parsed.path)
                if (
                    raw_target.casefold().startswith("file:")
                    or "\\" in path_part
                    or path_part.startswith("/")
                    or WINDOWS_ABSOLUTE_RE.match(raw_target)
                ):
                    failures.append(f"{source}: non-portable path {raw_target}")
                    continue
                try:
                    target.relative_to(ROOT.resolve())
                except ValueError:
                    failures.append(f"{source}: target leaves repository {raw_target}")
                    continue
                if not target.is_file():
                    failures.append(f"{source}: missing target {raw_target}")
                    continue
                if path_part and not _path_has_exact_case(source, path_part):
                    failures.append(f"{source}: path case mismatch {raw_target}")
                    continue
                if not fragment:
                    continue
                line_anchor = re.fullmatch(r"L(\d+)(?:-L(\d+))?", fragment)
                if line_anchor:
                    if target.suffix.lower() not in {".md", ".txt", ".py"}:
                        failures.append(f"{source}: line anchor on non-text target {raw_target}")
                        continue
                    line_count = len(target.read_text(encoding="utf-8").splitlines())
                    start = int(line_anchor.group(1))
                    end = int(line_anchor.group(2) or start)
                    if not (1 <= start <= end <= line_count):
                        failures.append(f"{source}: invalid line anchor {raw_target}")
                elif target.suffix.lower() != ".md" or fragment not in _markdown_heading_anchors(target):
                    failures.append(f"{source}: missing heading anchor {raw_target}")

        spec = ROOT / "docs" / "spec.md"
        try:
            frontmatter_paths = list(_frontmatter_paths(spec))
        except ValueError as exc:
            failures.append(f"{spec}: {exc}")
            frontmatter_paths = []
        for raw_target in frontmatter_paths:
            if "\\" in raw_target or raw_target.startswith("/"):
                failures.append(f"{spec}: non-portable frontmatter path {raw_target}")
                continue
            target = (spec.parent / unquote(raw_target)).resolve()
            if not target.is_file():
                failures.append(f"{spec}: missing frontmatter target {raw_target}")
            elif not _path_has_exact_case(spec, raw_target):
                failures.append(f"{spec}: frontmatter path case mismatch {raw_target}")

        self.assertEqual([], failures)

    def test_historical_and_reference_documents_have_status_banners(self) -> None:
        historical = {
            *sorted((ROOT / "docs" / "superpowers").rglob("*.md")),
            ROOT / "docs" / "references" / "original-mvp-proposal.md",
            ROOT / "docs" / "references" / "mvp-happy-case-status-2026-06-07.md",
        }
        references = set((ROOT / "docs" / "references").rglob("*.md"))

        for source in historical | references:
            opening = "\n".join(
                _visible_markdown(source.read_text(encoding="utf-8")).splitlines()[:12]
            )
            opening_lines = opening.splitlines()
            banner_lines = [
                index
                for index, line in enumerate(opening_lines)
                if line.startswith("> **Trạng thái tài liệu:**")
            ]
            with self.subTest(source=source):
                self.assertEqual(1, len(banner_lines))
                self.assertLessEqual(banner_lines[0], 4)
                banner = []
                for line in opening_lines[banner_lines[0]:]:
                    if not line.startswith(">"):
                        break
                    banner.append(line)
                banner_text = "\n".join(banner)
                self.assertTrue(list(_markdown_destinations(banner_text)))
                if source in historical:
                    self.assertIn("Artifact lịch sử", banner_text)

    def test_current_documentation_has_one_status_source_and_no_stale_claims(self) -> None:
        historical = {
            *sorted((ROOT / "docs" / "superpowers").rglob("*.md")),
            ROOT / "docs" / "references" / "project-request.md",
            ROOT / "docs" / "references" / "original-mvp-proposal.md",
            ROOT / "docs" / "references" / "mvp-happy-case-status-2026-06-07.md",
        }
        canonical = [
            ROOT / "README.md",
            *[
                source
                for source in sorted((ROOT / "docs").rglob("*.md"))
                if source not in historical
            ],
        ]
        stale_patterns = {
            "completed browser test": re.compile(
                r"(?:Playwright[^\n]{0,80}(?:đã\s+(?:được\s+)?dùng|hoàn tất|đạt|pass)|"
                r"(?:đã\s+(?:dùng|chạy)|hoàn tất|đạt|pass)[^\n]{0,80}Playwright)",
                re.IGNORECASE,
            ),
            "old two-column UI": re.compile(
                r"(?:desktop[^\n]{0,60}(?:hai|2)\s+cột|(?:hai|2)\s+cột[^\n]{0,60}desktop)",
                re.IGNORECASE,
            ),
            "dotenv-only key": re.compile(
                r"(?:key|GEMINI_API_KEY)[^\n]{0,80}(?<!không )\bchỉ\b[^\n]{0,80}\.env",
                re.IGNORECASE,
            ),
        }
        test_count_pattern = re.compile(
            r"\b\d+\s+(?:(?:bài|unit|repository|unit/repository)\s+)?tests?\b",
            re.IGNORECASE,
        )
        failures = []
        process = ROOT / "docs" / "process.md"
        for source in canonical:
            content = _visible_markdown(source.read_text(encoding="utf-8"))
            for label, pattern in stale_patterns.items():
                if pattern.search(content):
                    failures.append(f"{source}: {label}")
            if source != process and test_count_pattern.search(content):
                failures.append(f"{source}: duplicated numeric test count")

        status_sources = [
            source
            for source in canonical
            if "**Vai trò file:** nguồn trạng thái duy nhất"
            in _visible_markdown(source.read_text(encoding="utf-8"))
        ]
        self.assertEqual([process], status_sources)
        declared_count = re.search(
            r"suite discovery có\s+(\d+)\s+unit/repository contract tests",
            _visible_markdown(process.read_text(encoding="utf-8")),
            re.IGNORECASE,
        )
        self.assertIsNotNone(declared_count)
        discovered_count = unittest.defaultTestLoader.discover(
            str(ROOT / "tests"),
            pattern="test*.py",
        ).countTestCases()
        self.assertEqual(discovered_count, int(declared_count.group(1)))
        self.assertEqual([], failures)

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
