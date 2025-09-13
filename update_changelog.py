import re
import sys
from datetime import date
from pathlib import Path

# --- CONFIGURATION ---
FILTER_LIST_FILENAME = "uBlockOrigin-StaticFilters.txt"
CHANGELOG_FILENAME = "CHANGELOG.md"
# --- END CONFIGURATION ---

def main():
    filter_list_path = Path(FILTER_LIST_FILENAME)
    changelog_path = Path(CHANGELOG_FILENAME)

    if not filter_list_path.exists():
        sys.stderr.write(f"Error: Filter list file not found at '{filter_list_path}'.\n")
        sys.exit(1)
    if not changelog_path.exists():
        sys.stderr.write(f"Error: Changelog file not found at '{changelog_path}'.\n")
        sys.exit(1)

    filter_content = filter_list_path.read_text(encoding='utf-8')
    match = re.search(
        r"(! ====================\s*!     CHANGELOG:     \s*! ====================)(.*?)(! ====================)",
        filter_content, re.DOTALL
    )

    if not match or not match.group(2).strip():
        sys.exit(0)

    notes_block = match.group(2)

    markdown_lines = []
    lines = notes_block.strip().split('\n')
    for line in lines:
        content = re.sub(r'^!\s?', '', line).strip()
        if not content: continue
        if "NEW & UPDATED FILTERS" in content:
            markdown_lines.append("### New Filters")
        elif "GENERAL CLEANUP & OPTIMIZATION" in content:
            markdown_lines.append("### General cleanup & optimization")
        elif content.startswith('- '):
            markdown_lines.append(f"  - {content[2:]}")
        elif content.startswith("----") or content.startswith("===="):
            continue
        else:
            markdown_lines.append(f"- {content}")
    markdown_output = "\n".join(markdown_lines)

    if not markdown_output.strip():
        sys.exit(0)

    today = date.today().strftime("%Y-%m-%d")
    new_changelog_entry = f"## {today}\n\n{markdown_output}\n"

    original_changelog_content = changelog_path.read_text(encoding='utf-8')
    updated_changelog_content = re.sub(
        r"(#\s*CHANGELOG\s*\n)", f"\\1\n{new_changelog_entry}",
        original_changelog_content, count=1
    )
    changelog_path.write_text(updated_changelog_content, encoding='utf-8')

    cleared_filter_content = filter_content.replace(notes_block, '\n')
    filter_list_path.write_text(cleared_filter_content, encoding='utf-8')

    sys.exit(0)

if __name__ == "__main__":
    main()