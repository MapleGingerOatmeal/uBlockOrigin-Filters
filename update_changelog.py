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
        r"(\s*)("
        r"!\s*====================\s*!\s+CHANGELOG:\s*! ====================.*?"
        r")(?=\s*! ====================)",
        filter_content, re.DOTALL
    )

    if not match or not match.group(2).strip():
        sys.exit(0)

    # Full changelog block to remove is group 0, block to parse for changes is group 2
    notes_block = match.group(2)

    section_parts = []
    is_first_section = True
    for line in notes_block.strip().split('\n'):
        content = re.sub(r'^!\s?', '', line).strip()
        if not content: continue
        
        is_header = False
        if "NEW & UPDATED FILTERS" in content:
            is_header = True
            header_text = "### New Filters"
        elif "GENERAL CLEANUP & OPTIMIZATION" in content:
            is_header = True
            header_text = "### General cleanup & optimization"
        
        if is_header:
            if not is_first_section:
                section_parts.append("")
            section_parts.append(header_text)
            section_parts.append("")
            is_first_section = False
        elif content.startswith('- '):
            section_parts.append(f"  - {content[2:]}")
        elif "CHANGELOG:" in content or content.startswith("===="):
            continue
        else:
            section_parts.append(f"- {content}")
    
    section_content = "\n".join(section_parts)

    today = date.today().strftime("%Y-%m-%d")
    new_changelog_entry = f"## {today}\n\n{section_content}\n"
    
    original_changelog_content = changelog_path.read_text(encoding='utf-8')

    updated_changelog_content = re.sub(
        r"(#\s*CHANGELOG\s*\n)", f"\\1\n{new_changelog_entry}",
        original_changelog_content, count=1
    )
    changelog_path.write_text(updated_changelog_content, encoding='utf-8')
    
    cleared_filter_content = filter_content.replace(match.group(0), '')
    filter_list_path.write_text(cleared_filter_content, encoding='utf-8')
    
    sys.exit(0)

if __name__ == "__main__":
    main()