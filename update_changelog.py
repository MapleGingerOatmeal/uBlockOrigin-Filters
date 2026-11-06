import re
import sys
from datetime import date
from pathlib import Path

# Exit codes:
#   0 = no changelog notes found, nothing to do
#   1 = error
#   2 = changelog updated successfully (files modified)

FILTER_LIST_FILENAME = "uBlockOrigin-StaticFilters.txt"
CHANGELOG_FILENAME = "CHANGELOG.md"

BANNER_RULE = r"![ \t]*={3,}[ \t]*!?[ \t]*"
CHANGELOG_SECTION_RE = re.compile(
    r"^" + BANNER_RULE + r"\n"
    r"![ \t]*CHANGELOG[ \t]*!?[ \t]*\n"
    + BANNER_RULE + r"\n"
    r"(?P<body>.*?)"
    r"(?=^" + BANNER_RULE + r"$|\Z)",
    re.DOTALL | re.MULTILINE,
)
SUBSECTION_RE = re.compile(r"^![ \t]*-{3,}[ \t]*(?P<title>.*?)[ \t]*-{3,}[ \t]*!?$")
ITEM_RE = re.compile(r"^!(?P<rest>.*)$")
NESTED_RE = re.compile(r"^(?P<dashes>-+)[ \t]+(?P<text>.*)$")

HEADING_MAP = {
    "NEW & UPDATED FILTERS": "New Filters",
    "NEW FILTERS": "New Filters",
    "GENERAL CLEANUP & OPTIMIZATION": "General cleanup & optimization",
}


def read_text(path):
    raw = path.read_bytes().decode("utf-8")
    newline = "\r\n" if "\r\n" in raw else "\n"
    return raw.replace("\r\n", "\n"), newline


def write_text(path, text, newline):
    path.write_bytes(text.replace("\n", newline).encode("utf-8"))


def heading_for(title):
    title = re.sub(r"\s+", " ", title).strip()
    return HEADING_MAP.get(title.upper(), title.capitalize())


def parse_changelog_body(body):
    sections = []
    current = None
    for line in body.split("\n"):
        line = line.strip()
        if not line:
            continue

        sub = SUBSECTION_RE.match(line)
        if sub:
            current = (heading_for(sub.group("title")), [])
            sections.append(current)
            continue

        item = ITEM_RE.match(line)
        if not item:
            raise ValueError(f"Unexpected line in CHANGELOG section: {line!r}")
        text = item.group("rest").strip()
        if not text:
            continue

        if current is None:
            current = ("Changes", [])
            sections.append(current)

        nested = NESTED_RE.match(text)
        if nested:
            depth = len(nested.group("dashes"))
            current[1].append(f"{'  ' * depth}- {nested.group('text').strip()}")
        else:
            current[1].append(f"- {text}")

    return [(heading, lines) for heading, lines in sections if lines]


def build_entry(sections, today):
    parts = [f"## {today}", ""]
    for heading, lines in sections:
        parts += [f"### {heading}", "", *lines, ""]
    return "\n".join(parts)


def main():
    filter_list_path = Path(FILTER_LIST_FILENAME)
    changelog_path = Path(CHANGELOG_FILENAME)

    if not filter_list_path.exists():
        sys.stderr.write(f"Error: Filter list file not found at '{filter_list_path}'.\n")
        sys.exit(1)
    if not changelog_path.exists():
        sys.stderr.write(f"Error: Changelog file not found at '{changelog_path}'.\n")
        sys.exit(1)

    filter_content, filter_newline = read_text(filter_list_path)
    match = CHANGELOG_SECTION_RE.search(filter_content)
    if not match:
        sys.exit(0)

    try:
        sections = parse_changelog_body(match.group("body"))
    except ValueError as e:
        sys.stderr.write(f"Error: {e}\n")
        sys.exit(1)
    if not sections:
        sys.exit(0)

    today = date.today().strftime("%Y-%m-%d")
    entry = build_entry(sections, today)

    changelog_content, _ = read_text(changelog_path)
    header = re.match(r"\s*#[ \t]*CHANGELOG[ \t]*\n\s*", changelog_content)
    if not header:
        sys.stderr.write("Error: '# CHANGELOG' heading not found at top of CHANGELOG.md.\n")
        sys.exit(1)
    rest = changelog_content[header.end():]
    updated_changelog = f"# CHANGELOG\n\n{entry}\n{rest}"
    if not updated_changelog.endswith("\n"):
        updated_changelog += "\n"

    cleared_filter = (
        filter_content[:match.start()] + filter_content[match.end():]
    ).lstrip("\n")

    write_text(changelog_path, updated_changelog, "\r\n")
    write_text(filter_list_path, cleared_filter, filter_newline)

    print(f"Changelog updated with entry for {today}.")
    sys.exit(2)


if __name__ == "__main__":
    main()
