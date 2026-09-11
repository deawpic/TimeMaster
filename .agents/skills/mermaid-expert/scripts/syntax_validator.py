#!/usr/bin/env python3
"""
Mermaid & Markdown Syntax Validator Engine for TimeMaster
Audits Markdown documents and embedded Mermaid diagrams for syntax integrity,
structural validity, unquoted special characters, unclosed blocks, and table alignment.
"""

import re
import sys
import json
import argparse
from pathlib import Path
from typing import List, Dict, Any, Tuple


# Supported diagram types according to TimeMaster specifications & Mermaid standards
SUPPORTED_DIAGRAM_TYPES = [
    "graph",
    "flowchart",
    "sequenceDiagram",
    "stateDiagram",
    "stateDiagram-v2",
    "classDiagram",
    "classDiagram-v2",
    "erDiagram",
    "journey",
    "gantt",
    "pie",
    "gitGraph",
    "mindmap",
    "timeline",
    "quadrantChart",
    "requirementDiagram",
    "c4Context",
    "c4Container",
    "c4Component",
    "c4Dynamic",
    "c4Deployment",
    "xychart-beta",
    "architecture-beta",
    "kanban",
    "packet-beta",
    "sankey-beta",
]

# Shape delimiters for flowcharts / graphs
SHAPE_DELIMITERS = {
    "[(": ")]",
    "([": "])",
    "[[": "]]",
    "[/": "/]",
    "[\\": "\\]",
    "{{": "}}",
    "((": "))",
    "[": "]",
    "(": ")",
    "{": "}",
    ">": "]",
}

NODE_PATTERN = re.compile(
    r"(?<![A-Za-z0-9_])([A-Za-z0-9_]+)\s*(\[\(|\(\[|\[\[|\[\/|\[\\|\{\{|\(\(|\[|\(|\{|\>)"
)


def validate_code_fences(
    lines: List[str], filename: str
) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
    """
    Scans lines for code fence integrity (matched triple/quadruple backticks)
    and extracts fence metadata (ranges, languages, code content).
    """
    issues: List[Dict[str, Any]] = []
    code_blocks: List[Dict[str, Any]] = []

    in_fence = False
    fence_char = ""
    fence_len = 0
    fence_start = 0
    fence_lang = ""
    block_lines: List[str] = []

    for line_idx, line in enumerate(lines, start=1):
        stripped = line.strip()
        # Check for fence opening or closing
        fence_match = re.match(r"^(`{3,}|~{3,})(.*)$", stripped)
        if fence_match:
            marker = fence_match.group(1)
            info = fence_match.group(2).strip()
            char = marker[0]
            length = len(marker)

            if not in_fence:
                # Open fence
                in_fence = True
                fence_char = char
                fence_len = length
                fence_start = line_idx
                fence_lang = info.split()[0] if info else ""
                block_lines = []
            else:
                # Potential close fence
                if char == fence_char and length >= fence_len:
                    # Successfully closed fence
                    code_blocks.append(
                        {
                            "start_line": fence_start,
                            "end_line": line_idx,
                            "lang": fence_lang,
                            "code": "\n".join(block_lines),
                        }
                    )
                    in_fence = False
                    fence_char = ""
                    fence_len = 0
                    fence_start = 0
                    fence_lang = ""
                    block_lines = []
                else:
                    block_lines.append(line)
        else:
            if in_fence:
                block_lines.append(line)

    if in_fence:
        issues.append(
            {
                "file": filename,
                "line": fence_start,
                "category": "unclosed_code_fence",
                "severity": "error",
                "matched": f"```{fence_lang} (opened at line {fence_start})",
                "suggestion": f"Close code block opened at line {fence_start} with matching closing backticks ```",
            }
        )

    return issues, code_blocks


def validate_markdown_tables(
    lines: List[str],
    filename: str,
    code_ranges: List[Tuple[int, int]],
) -> List[Dict[str, Any]]:
    """
    Audits Markdown tables for:
    - Consistent column count across header, delimiter/separator, and all data rows.
    - Valid separator row formatting (| :--- | :---: | ---: |).
    Ignores lines located within code fence blocks.
    """
    issues: List[Dict[str, Any]] = []

    def is_in_code_block(line_num: int) -> bool:
        return any(start <= line_num <= end for start, end in code_ranges)

    table_lines: List[Tuple[int, str]] = []

    def process_table_buffer(buf: List[Tuple[int, str]]):
        if len(buf) < 2:
            return

        header_idx, header_line = buf[0]
        sep_idx, sep_line = buf[1]

        # Split on unescaped pipes
        h_cells = [
            c.strip() for c in re.split(r"(?<!\\)\|", header_line.strip().strip("|"))
        ]
        s_cells = [
            c.strip() for c in re.split(r"(?<!\\)\|", sep_line.strip().strip("|"))
        ]

        # Check if row 2 is genuinely a separator row
        is_sep = len(s_cells) > 0 and all(re.match(r"^:?-+:?$", c) for c in s_cells)
        if not is_sep:
            return

        col_count = len(h_cells)
        if col_count == 0:
            return

        # Check separator column count
        if len(s_cells) != col_count:
            issues.append(
                {
                    "file": filename,
                    "line": sep_idx,
                    "category": "table_separator_column_mismatch",
                    "severity": "error",
                    "matched": sep_line[:80],
                    "suggestion": f"Separator row has {len(s_cells)} columns, but header has {col_count} columns.",
                }
            )

        # Check data rows
        for row_idx, row_line in buf[2:]:
            r_cells = [
                c.strip() for c in re.split(r"(?<!\\)\|", row_line.strip().strip("|"))
            ]
            if len(r_cells) != col_count:
                issues.append(
                    {
                        "file": filename,
                        "line": row_idx,
                        "category": "table_row_column_mismatch",
                        "severity": "error",
                        "matched": row_line[:80],
                        "suggestion": f"Row has {len(r_cells)} columns; expected {col_count} matching the table header.",
                    }
                )

    for line_idx, line in enumerate(lines, start=1):
        if is_in_code_block(line_idx):
            if table_lines:
                process_table_buffer(table_lines)
                table_lines = []
            continue

        stripped = line.strip()
        if "|" in stripped and (stripped.startswith("|") or stripped.endswith("|")):
            table_lines.append((line_idx, stripped))
        else:
            if table_lines:
                process_table_buffer(table_lines)
                table_lines = []

    if table_lines:
        process_table_buffer(table_lines)

    return issues


def validate_flowchart_line(
    line: str, line_num: int, filename: str
) -> List[Dict[str, Any]]:
    """
    Validates a single line in a flowchart/graph diagram for:
    - Unclosed edge label pipes (-->|label|)
    - Malformed arrows (-->-, ---x-)
    - Unquoted special characters inside node labels (e.g. () or [] without quotes)
    - Unclosed quotes in labels
    """
    issues: List[Dict[str, Any]] = []
    s = line.strip()
    if (
        not s
        or s.startswith("%%")
        or s.startswith("classDef")
        or s.startswith("class ")
        or s.startswith("style ")
        or s.startswith("subgraph")
        or s.startswith("end")
        or s.startswith("click ")
    ):
        return issues

    # 1. Mask edge labels to avoid false positives on pipes and arrows
    def mask_edge(m):
        return m.group(1) + " " * (len(m.group(0)) - len(m.group(1)))

    masked = re.sub(r"(-->|-\.->|==>|---|~~~)\s*\|([^|\n]*)\|", mask_edge, s)

    # Check for unclosed edge label pipe
    if re.search(r"(-->|-\.->|==>|---|~~~)\s*\|[^|\n]*$", s):
        issues.append(
            {
                "file": filename,
                "line": line_num,
                "category": "mermaid_unclosed_edge_pipe",
                "severity": "error",
                "matched": s[:80],
                "suggestion": "Edge label pipe opened with '|' is missing closing '|'",
            }
        )
        return issues

    # Check for malformed arrows
    if re.search(r"(-->-|---\s*-|===>=)", s):
        issues.append(
            {
                "file": filename,
                "line": line_num,
                "category": "mermaid_malformed_arrow",
                "severity": "error",
                "matched": s[:80],
                "suggestion": "Check arrow syntax for invalid trailing dash or malformed arrowhead.",
            }
        )

    # 2. Find node definitions and inspect label escaping
    pos = 0
    while True:
        m = NODE_PATTERN.search(masked, pos)
        if not m:
            break
        node_id = m.group(1)
        open_shape = m.group(2)
        expected_close = SHAPE_DELIMITERS[open_shape]

        content_start = m.end()
        orig_rem = s[content_start:]

        if orig_rem.startswith('"'):
            # Quoted label
            q_end = -1
            i = 1
            while i < len(orig_rem):
                if orig_rem[i] == '"' and orig_rem[i - 1] != "\\":
                    q_end = i
                    break
                i += 1

            if q_end == -1:
                issues.append(
                    {
                        "file": filename,
                        "line": line_num,
                        "category": "mermaid_unclosed_label_quote",
                        "severity": "error",
                        "matched": s[:80],
                        "suggestion": f"Node '{node_id}' label has unclosed double quote (\").",
                    }
                )
                pos = m.end()
            else:
                close_pos = orig_rem.find(expected_close, q_end + 1)
                if close_pos == -1:
                    issues.append(
                        {
                            "file": filename,
                            "line": line_num,
                            "category": "mermaid_missing_shape_delimiter",
                            "severity": "error",
                            "matched": s[:80],
                            "suggestion": f"Node '{node_id}' is missing closing shape delimiter '{expected_close}'.",
                        }
                    )
                    pos = m.end()
                else:
                    pos = content_start + close_pos + len(expected_close)
        else:
            # Unquoted label
            close_pos = orig_rem.find(expected_close)
            if close_pos == -1:
                issues.append(
                    {
                        "file": filename,
                        "line": line_num,
                        "category": "mermaid_unclosed_shape",
                        "severity": "error",
                        "matched": s[:80],
                        "suggestion": f"Node '{node_id}' shape opened with '{open_shape}' is missing closing '{expected_close}'.",
                    }
                )
                pos = m.end()
            else:
                label = orig_rem[:close_pos]
                # Check for risky unquoted special characters in label
                risky = [ch for ch in "()[]{}\"" if ch in label]
                if risky:
                    issues.append(
                        {
                            "file": filename,
                            "line": line_num,
                            "category": "mermaid_unquoted_special_chars",
                            "severity": "error",
                            "matched": s[:80],
                            "suggestion": f"Node '{node_id}' has unquoted special char(s) {set(risky)} in label: '{label}'. Wrap in double quotes: {node_id}[\"{label}\"].",
                        }
                    )
                pos = content_start + close_pos + len(expected_close)

    return issues


def validate_mermaid_diagram(
    code: str, start_line: int, filename: str
) -> List[Dict[str, Any]]:
    """
    Validates an extracted Mermaid code block:
    - Validates diagram declaration
    - Checks subgraph / loop / block nesting balance
    - Validates flowchart node quotes and arrows
    - Validates sequence diagram block balances (loop, alt, opt, par, critical)
    """
    issues: List[Dict[str, Any]] = []
    lines = code.splitlines()

    # 1. Determine diagram type
    first_code_line = ""
    first_code_line_offset = 0
    for idx, line in enumerate(lines):
        stripped = line.strip()
        if stripped and not stripped.startswith("%%"):
            first_code_line = stripped
            first_code_line_offset = idx
            break

    if not first_code_line:
        issues.append(
            {
                "file": filename,
                "line": start_line,
                "category": "mermaid_empty_diagram",
                "severity": "error",
                "matched": "```mermaid",
                "suggestion": "Mermaid block is empty. Provide a valid diagram definition.",
            }
        )
        return issues

    diagram_type = first_code_line.split()[0]
    if diagram_type not in SUPPORTED_DIAGRAM_TYPES:
        issues.append(
            {
                "file": filename,
                "line": start_line + first_code_line_offset + 1,
                "category": "mermaid_unsupported_diagram_type",
                "severity": "error",
                "matched": first_code_line[:80],
                "suggestion": f"Unknown or unsupported diagram type '{diagram_type}'. Supported: {', '.join(SUPPORTED_DIAGRAM_TYPES[:7])}...",
            }
        )

    # 2. Block nesting check
    subgraph_stack: List[Tuple[int, str]] = []
    sequence_block_stack: List[Tuple[int, str]] = []
    brace_stack: List[Tuple[int, str]] = []

    for idx, line in enumerate(lines, start=1):
        actual_line_num = start_line + idx
        s = line.strip()

        # Ignore comments
        if s.startswith("%%"):
            continue

        # Flowchart / Graph checks
        if diagram_type in ["graph", "flowchart"]:
            if re.match(r"^subgraph\b", s):
                subgraph_stack.append((actual_line_num, s))
            elif s == "end":
                if subgraph_stack:
                    subgraph_stack.pop()
                else:
                    issues.append(
                        {
                            "file": filename,
                            "line": actual_line_num,
                            "category": "mermaid_unexpected_end",
                            "severity": "error",
                            "matched": s,
                            "suggestion": "'end' encountered without matching opening 'subgraph'.",
                        }
                    )

            # Node & label validation
            line_issues = validate_flowchart_line(line, actual_line_num, filename)
            issues.extend(line_issues)

        # Sequence diagram block checks
        elif diagram_type == "sequenceDiagram":
            if re.match(r"^(loop|alt|opt|par|critical|rect|break)\b", s):
                block_kw = s.split()[0]
                sequence_block_stack.append((actual_line_num, block_kw))
            elif s == "end":
                if sequence_block_stack:
                    sequence_block_stack.pop()
                else:
                    issues.append(
                        {
                            "file": filename,
                            "line": actual_line_num,
                            "category": "mermaid_unexpected_end",
                            "severity": "error",
                            "matched": s,
                            "suggestion": "'end' encountered without matching sequence block (loop, alt, opt, par, critical).",
                        }
                    )

        # State / Class diagram composite braces check
        elif diagram_type in [
            "stateDiagram",
            "stateDiagram-v2",
            "classDiagram",
            "classDiagram-v2",
        ]:
            for ch in s:
                if ch == "{":
                    brace_stack.append((actual_line_num, ch))
                elif ch == "}":
                    if brace_stack:
                        brace_stack.pop()
                    else:
                        issues.append(
                            {
                                "file": filename,
                                "line": actual_line_num,
                                "category": "mermaid_unexpected_closing_brace",
                                "severity": "error",
                                "matched": s[:80],
                                "suggestion": "'}' encountered without matching opening '{'.",
                            }
                        )

    # Check unclosed blocks at diagram end
    for unclosed_line, unclosed_text in subgraph_stack:
        issues.append(
            {
                "file": filename,
                "line": unclosed_line,
                "category": "mermaid_unclosed_subgraph",
                "severity": "error",
                "matched": unclosed_text[:80],
                "suggestion": "Subgraph is missing closing 'end' statement.",
            }
        )

    for unclosed_line, unclosed_kw in sequence_block_stack:
        issues.append(
            {
                "file": filename,
                "line": unclosed_line,
                "category": "mermaid_unclosed_sequence_block",
                "severity": "error",
                "matched": unclosed_kw,
                "suggestion": f"Sequence block '{unclosed_kw}' is missing closing 'end' statement.",
            }
        )

    for unclosed_line, _ in brace_stack:
        issues.append(
            {
                "file": filename,
                "line": unclosed_line,
                "category": "mermaid_unclosed_brace",
                "severity": "error",
                "matched": "{",
                "suggestion": "Composite block is missing closing '}' brace.",
            }
        )

    return issues


def audit_markdown_content(content: str, filename: str = "<string>") -> Dict[str, Any]:
    """
    Audits an entire Markdown string for code fence, table, and Mermaid syntax integrity.
    """
    lines = content.splitlines()
    all_issues: List[Dict[str, Any]] = []

    # 1. Validate code fences and extract code blocks
    fence_issues, code_blocks = validate_code_fences(lines, filename)
    all_issues.extend(fence_issues)

    code_ranges = [(b["start_line"], b["end_line"]) for b in code_blocks]

    # 2. Validate Markdown tables outside of code fences
    table_issues = validate_markdown_tables(lines, filename, code_ranges)
    all_issues.extend(table_issues)

    # 3. Validate embedded Mermaid diagrams
    mermaid_blocks = [b for b in code_blocks if b["lang"].lower() == "mermaid"]
    for mb in mermaid_blocks:
        m_issues = validate_mermaid_diagram(mb["code"], mb["start_line"], filename)
        all_issues.extend(m_issues)

    error_count = sum(1 for i in all_issues if i.get("severity") == "error")
    warning_count = sum(1 for i in all_issues if i.get("severity") == "warning")

    return {
        "file": filename,
        "total_lines": len(lines),
        "code_blocks_count": len(code_blocks),
        "mermaid_blocks_count": len(mermaid_blocks),
        "issues_count": len(all_issues),
        "errors_count": error_count,
        "warnings_count": warning_count,
        "issues": all_issues,
        "passed": error_count == 0,
    }


def audit_path(path_str: str) -> Dict[str, Any]:
    """
    Audits a file or recursively scans all Markdown files in a directory.
    """
    target = Path(path_str)
    if not target.exists():
        raise FileNotFoundError(f"Target path does not exist: {path_str}")

    results = []
    if target.is_file():
        content = target.read_text(encoding="utf-8", errors="replace")
        results.append(audit_markdown_content(content, str(target)))
    elif target.is_dir():
        for file_path in sorted(target.glob("**/*")):
            if file_path.is_file() and file_path.suffix.lower() == ".md":
                # Skip .git directory
                if ".git" in file_path.parts:
                    continue
                content = file_path.read_text(encoding="utf-8", errors="replace")
                results.append(audit_markdown_content(content, str(file_path)))

    total_issues = sum(r["issues_count"] for r in results)
    total_errors = sum(r["errors_count"] for r in results)
    total_warnings = sum(r["warnings_count"] for r in results)
    total_mermaid = sum(r["mermaid_blocks_count"] for r in results)

    return {
        "target": path_str,
        "files_scanned": len(results),
        "mermaid_blocks_scanned": total_mermaid,
        "total_issues": total_issues,
        "total_errors": total_errors,
        "total_warnings": total_warnings,
        "passed": total_errors == 0,
        "details": results,
    }


def main():
    parser = argparse.ArgumentParser(
        description="Mermaid & Markdown Syntax Validator for TimeMaster"
    )
    parser.add_argument(
        "--path", help="File or directory path to audit (defaults to workspace root)"
    )
    parser.add_argument("--text", help="Raw Markdown text string to audit")
    parser.add_argument(
        "--strict", action="store_true", help="Exit code 1 if errors are detected"
    )
    parser.add_argument("--json", action="store_true", help="Output results in JSON")

    args = parser.parse_args()

    if args.text:
        report = audit_markdown_content(args.text)
    elif args.path:
        report = audit_path(args.path)
    else:
        # Default: scan current workspace
        default_dir = Path(__file__).resolve().parent.parent.parent.parent
        report = audit_path(str(default_dir))

    if args.json:
        print(json.dumps(report, indent=2, ensure_ascii=False))
    else:
        passed = report["passed"]
        files = report.get("files_scanned", 1)
        diagrams = report.get("mermaid_blocks_scanned", report.get("mermaid_blocks_count", 0))
        errors = report.get("total_errors", report.get("errors_count", 0))
        warnings = report.get("total_warnings", report.get("warnings_count", 0))

        print("=" * 70)
        print(" TimeMaster Mermaid & Markdown Syntax Validator")
        print("=" * 70)
        print(f"Target:               {report.get('target', report.get('file', '<string>'))}")
        print(f"Files Scanned:        {files}")
        print(f"Mermaid Blocks:       {diagrams}")
        print(f"Total Errors:         {errors}")
        print(f"Total Warnings:       {warnings}")
        print(f"Status:               {'[PASSED] Clean & Compliant' if passed else '[FAILED] Syntax Issues Detected'}")
        print("-" * 70)

        issues = report.get("issues") or []
        if not issues and "details" in report:
            for d in report["details"]:
                issues.extend(d.get("issues", []))

        if issues:
            print("Detected Issues:")
            for issue in issues:
                sev = issue.get("severity", "error").upper()
                print(f"  - [{issue['file']}:{issue['line']}] [{sev}] ({issue['category']})")
                print(f"    Matched:    {issue['matched']}")
                print(f"    Suggestion: {issue['suggestion']}")
        else:
            print("No syntax errors or table misalignments found.")

    if args.strict and not report["passed"]:
        sys.exit(1)


if __name__ == "__main__":
    main()
