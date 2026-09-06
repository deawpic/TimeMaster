#!/usr/bin/env python3
"""
Writing & Citation Linter Engine for TimeMaster
Audits academic, technical, and reporting documents against 21 AI writing clichés,
vague attributions, and checks for authentic metrological citations.
"""

import re
import sys
import json
from pathlib import Path
from typing import List, Dict, Any


# 21 Banned AI Clichés & Buzzwords
ENGLISH_AI_CLICHES = [
    (r"\bdelv(e|es|ed|ing)\b", "delve -> use examine, analyze, trace, investigate"),
    (r"\btapestr(y|ies)\b", "tapestry -> use architecture, structure, topology"),
    (r"\bpivotal\b", "pivotal -> use essential, necessary, determinant"),
    (r"\bgame-?changer\b", "game-changer -> describe the quantitative improvement"),
    (r"\btestament to\b", "testament to -> use evidence of, demonstrates, confirms"),
    (r"\bembark(s|ed|ing)?\b", "embark -> use design, deploy, begin, initiate"),
    (r"\bstreamlin(e|es|ed|ing)\b", "streamline -> use optimize, simplify, accelerate"),
    (r"\bground-?breaking\b", "groundbreaking -> use novel, high-precision, state-of-the-art"),
    (r"\bunleash(es|ed|ing)?\b", "unleash -> state operational performance boundary directly"),
    (r"\bseamless(ly)?\b", "seamless -> use continuous, uninterrupted, low-jitter"),
    (r"\brich tapestry\b", "rich tapestry -> use multi-layered architecture"),
    (r"\bvibrant ecosystem\b", "vibrant ecosystem -> use network topology, component matrix"),
    (r"\bbeacon of\b", "beacon of -> state technical milestone directly"),
    (r"\btransformative journey\b", "transformative journey -> state engineering project"),
    (r"\bnavigating the (complex )?landscape\b", "navigating the landscape -> analyzing the domain"),
    (r"\bfeatures a robust architecture\b", "copula avoidance -> has a fault-tolerant architecture"),
    (r"\bboasts exceptional\b", "copula avoidance -> delivers, achieves, provides"),
    (r"\bdeeply fascinating\b", "hollow intensifier -> explain physical significance"),
    (r"\bremarkably crucial\b", "hollow intensifier -> necessary / required by standard"),
    (r"\bin a nutshell\b", "chatbot artifact -> in summary / concluding analysis"),
    (r"\blet'?s dive in\b", "chatbot artifact -> delete and start directly with the thesis")
]

THAI_AI_CLICHES = [
    (r"เป็นพยานถึง", "เป็นพยานถึง -> ใช้ 'เป็นหลักฐานยืนยัน' หรือ 'แสดงให้เห็นว่า'"),
    (r"นำทางภูมิทัศน์", "นำทางภูมิทัศน์ -> ใช้ 'วิเคราะห์ขอบเขต' หรือ 'บริหารจัดการระบบ'"),
    (r"ก้าวเข้าสู่การเดินทาง", "ก้าวเข้าสู่การเดินทาง -> ใช้ 'เริ่มดำเนินการ' หรือ 'เข้าสู่กระบวนการ'"),
    (r"มีความสำคัญอย่างยิ่งยวด", "มีความสำคัญอย่างยิ่งยวด -> อธิบายผลกระทบเชิงวิศวกรรมโดยตรง"),
    (r"เจาะลึก", "เจาะลึก -> ใช้ 'วิเคราะห์', 'ตรวจสอบ', หรือ 'สืบค้น'"),
    (r"ระบบนิเวศอันมีชีวิตชีวา", "ระบบนิเวศอันมีชีวิตชีวา -> ใช้ 'โครงข่ายการทำงาน' หรือ 'สถาปัตยกรรมระบบ'"),
    (r"ปลดปล่อยพลัง", "ปลดปล่อยพลัง -> ระบุขีดความสามารถเชิงตัวเลขโดยตรง"),
    (r"การเปลี่ยนแปลงกระบวนทัศน์อันน่าทึ่ง", "คำโฆษณาเกินจริง -> ระบุการเปลี่ยนแปลงตามข้อกำหนดสากล")
]

VAGUE_ATTRIBUTIONS = [
    (r"\bexperts agree\b", "vague attribution -> cite specific committee or paper"),
    (r"\bscientists widely acknowledge\b", "vague attribution -> cite BIPM, CGPM, or author"),
    (r"\bindustry leaders note\b", "vague attribution -> cite standard specification"),
    (r"\bmany believe\b", "vague attribution -> cite verifiable source"),
    (r"\bit is widely known that\b", "filler / ungrounded claim -> state facts directly"),
    (r"หลายฝ่ายยอมรับ", "การอ้างคลุมเครือ -> ระบุองค์กรหรือมาตรฐานที่รองรับ"),
    (r"เป็นที่ทราบกันดี", "คำเติมเต็มไร้หลักฐาน -> ระบุข้อเท็จจริงทางเทคนิคโดยตรง"),
    (r"ผู้เชี่ยวชาญเห็นตรงกัน", "การอ้างลอยๆ -> ระบุคณะกรรมการมาตรฐานหรือรายงานวิชาการ")
]

CITATION_PATTERNS = [
    r"\bRFC\s*\d+\b",
    r"\bIEEE\s*(?:1588|802\.\d+)\b",
    r"\bBIPM\b",
    r"\bCGPM\b",
    r"\bISO\s*\d+\b",
    r"\bITU-T\s*[A-Z]\.\d+(?:\.\d+)?\b",
    r"\bMiFID\s*II\b",
    r"\bRTS\s*25\b",
    r"\bFINRA\s*Rule\s*\d+\b",
    r"\b10\.\d{4,9}/[-._;()/:A-Za-z0-9]+\b",
    r"\bCircular\s*T\b"
]


def lint_text(text: str, filename: str = "<string>") -> Dict[str, Any]:
    """
    Lint a given text string for AI writing clichés, vague attributions, and citations.
    """
    lines = text.splitlines()
    issues: List[Dict[str, Any]] = []

    # 1. Scan for AI Clichés (English + Thai)
    all_cliches = ENGLISH_AI_CLICHES + THAI_AI_CLICHES
    for line_idx, line in enumerate(lines, start=1):
        for pattern, suggestion in all_cliches:
            for match in re.finditer(pattern, line, re.IGNORECASE):
                issues.append({
                    "file": filename,
                    "line": line_idx,
                    "category": "ai_cliche",
                    "matched": match.group(0),
                    "context": line.strip()[:100],
                    "suggestion": suggestion
                })

        for pattern, suggestion in VAGUE_ATTRIBUTIONS:
            for match in re.finditer(pattern, line, re.IGNORECASE):
                issues.append({
                    "file": filename,
                    "line": line_idx,
                    "category": "vague_attribution",
                    "matched": match.group(0),
                    "context": line.strip()[:100],
                    "suggestion": suggestion
                })

    # 2. Check for authentic citations
    detected_citations = []
    for pattern in CITATION_PATTERNS:
        matches = re.findall(pattern, text, re.IGNORECASE)
        detected_citations.extend(matches)

    return {
        "file": filename,
        "total_lines": len(lines),
        "issues_count": len(issues),
        "issues": issues,
        "citations_found": list(set(detected_citations)),
        "passed": len(issues) == 0
    }


def audit_path(path_str: str) -> Dict[str, Any]:
    """
    Audit a specific file or all markdown/text files in a directory.
    """
    target = Path(path_str)
    if not target.exists():
        raise FileNotFoundError(f"Target path does not exist: {path_str}")

    results = []
    if target.is_file():
        content = target.read_text(encoding="utf-8", errors="replace")
        results.append(lint_text(content, str(target)))
    elif target.is_dir():
        for file_path in target.glob("**/*"):
            if file_path.is_file() and file_path.suffix.lower() in [".md", ".txt"]:
                content = file_path.read_text(encoding="utf-8", errors="replace")
                results.append(lint_text(content, str(file_path)))

    total_issues = sum(r["issues_count"] for r in results)
    all_passed = total_issues == 0

    return {
        "target": path_str,
        "files_scanned": len(results),
        "total_issues": total_issues,
        "passed": all_passed,
        "details": results
    }


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Writing & Citation Linter")
    parser.add_argument("--path", help="File or directory path to audit")
    parser.add_argument("--text", help="Raw text string to audit")
    parser.add_argument("--strict", action="store_true", help="Exit code 1 if issues found")
    parser.add_argument("--json", action="store_true", help="Output as JSON")

    args = parser.parse_args()

    if args.text:
        report = lint_text(args.text)
    elif args.path:
        report = audit_path(args.path)
    else:
        # Default: audit reports/ directory
        default_dir = Path(__file__).resolve().parent.parent.parent.parent / "reports"
        report = audit_path(str(default_dir))

    if args.json:
        print(json.dumps(report, indent=2, ensure_ascii=False))
    else:
        passed = report["passed"]
        print(f"Audit Target: {report.get('target', '<string>')}")
        print(f"Status: {'[PASSED] Clean Scholarly Text' if passed else '[FAILED] Clichés or Issues Detected'}")
        print(f"Total Issues: {report.get('total_issues', report.get('issues_count', 0))}")
        
        issues = report.get("issues") or []
        if not issues and "details" in report:
            for d in report["details"]:
                issues.extend(d.get("issues", []))
                
        for issue in issues:
            print(f"  - [{issue['file']}:{issue['line']}] ({issue['category']}) '{issue['matched']}'")
            print(f"    Suggestion: {issue['suggestion']}")

    if args.strict and not report["passed"]:
        sys.exit(1)
