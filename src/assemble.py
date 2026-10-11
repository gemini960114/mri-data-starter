"""把各章依「閱讀順序」組裝成 paper.md（MRI-DATA 的最後一步：Assembly）。

寫作順序是 M → R → I → D → A → T，但讀者看到的順序是：
標題 → 摘要 → 前言 → 方法 → 結果 → 討論 → 參考文獻。

用法：uv run python src/assemble.py
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ORDER = ["00_title.md", "05_abstract.md", "03_intro.md", "01_methods.md", "02_results.md",
         "04_discussion.md", "06_references.md"]


def strip_guidance(text: str) -> str:
    """去掉章節檔開頭給學生看的說明（以 > 開頭的引言行與 HTML 註解）。"""
    lines, in_comment = [], False
    for line in text.splitlines():
        if line.strip().startswith("<!--"):
            in_comment = True
        if not in_comment and not line.startswith(">"):
            lines.append(line)
        if in_comment and line.strip().endswith("-->"):
            in_comment = False
    return "\n".join(lines).strip()


def main() -> int:
    parts = []
    for name in ORDER:
        p = ROOT / "paper" / name
        if not p.exists():
            print(f"[缺少] paper/{name}")
            return 1
        parts.append(strip_guidance(p.read_text(encoding="utf-8")))
    (ROOT / "paper.md").write_text("\n\n".join(parts) + "\n", encoding="utf-8")
    todo = sum(part.count("TODO") for part in parts)
    print(f"[OK] 已組裝 paper.md（{len(ORDER)} 個部分）" + (f"；還有 {todo} 個 TODO" if todo else ""))
    return 0


if __name__ == "__main__":
    sys.exit(main())
