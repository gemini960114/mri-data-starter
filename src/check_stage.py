"""檢查 MRI-DATA 各階段是否完成。

用法：
    uv run python src/check_stage.py        # 顯示所有階段的狀態
    uv run python src/check_stage.py M      # 只檢查某一階段：M R I D A T X（X = Assembly）

符號：✅ 通過　⚠️ 請人工確認　❌ 未完成或違反規則
數字核對會列出「在來源檔中找不到」的數字，請逐一確認；它只是輔助工具，最後仍要人工查核。
不核對的數字：標題行、來源標註、0–10 的整數、學年度與年份、90%／95%／99%、0.05／0.01／0.001。
"""
import re
import subprocess
import sys
from pathlib import Path

import pandas as pd
import yaml

ROOT = Path(__file__).resolve().parents[1]
PAPER = ROOT / "paper"
RESULTS = ROOT / "results"
PLAN_KEYS = ["research_question", "primary_hypothesis", "outcome", "comparison", "sample", "method", "seed"]

results: list[tuple[str, str, str]] = []


def say(stage: str, status: str, msg: str) -> None:
    results.append((stage, status, msg))


def git(*args) -> subprocess.CompletedProcess:
    return subprocess.run(["git", *args], cwd=ROOT, capture_output=True, text=True, encoding="utf-8")


def frozen() -> bool:
    return git("tag", "--list", "methods-frozen").stdout.strip() == "methods-frozen"


def read(name: str) -> str:
    p = PAPER / name
    return p.read_text(encoding="utf-8") if p.exists() else ""


REF_TODO = "TODO：需補文獻"


def filled(name: str, min_chars: int = 200) -> tuple[bool, str]:
    """章節是否已填寫。「TODO：需補文獻」只提醒、不擋關（課堂時間內不一定能補齊文獻）。"""
    text = read(name)
    body = "\n".join(line for line in text.splitlines() if not line.lstrip().startswith(("#", ">", "<!--")))
    if "TODO" in text.replace(REF_TODO, ""):
        return False, f"{name} 還有 TODO 沒填"
    if len(body.strip()) < min_chars:
        return False, f"{name} 內容太少（{len(body.strip())} 字）"
    if REF_TODO in text:
        say(name_stage.get(name, "?"), "⚠️", f"{name} 有 {text.count(REF_TODO)} 處「{REF_TODO}」，課後請補上可查證的文獻")
    return True, f"{name} 已填寫"


name_stage = {"01_methods.md": "M", "02_results.md": "R", "03_intro.md": "I", "04_discussion.md": "D",
              "05_abstract.md": "A", "00_title.md": "T"}


# ---------- 數字核對 ----------
NUM = re.compile(r"(?<![\w.])-?\d[\d,]*(?:\.\d+)?%?")
# 統計慣用的常數（信賴水準、顯著水準），不需要來源檔
CONSTANTS = {"90%", "95%", "99%", "0.05", "0.01", "0.001"}


def numbers_in_text(text: str) -> list[tuple[str, str]]:
    """回傳 (數字字串, 所在行)。忽略標題行、來源標註，以及學年度、年份與 0–10 的整數（多半是編號）。"""
    out = []
    for line in text.splitlines():
        if line.lstrip().startswith(("#", "<!--", ">")):
            continue
        clean = re.sub(r"[（(][^（()）]*results/[^（()）]*[)）]", "", line)  # 去掉（results/xxx.csv）
        clean = re.sub(r"`[^`]*`", "", clean)  # 去掉程式碼與欄位名稱
        for tok in NUM.findall(clean):
            if tok in CONSTANTS:
                continue
            raw = tok.replace(",", "").rstrip("%")
            try:
                val = float(raw)
            except ValueError:
                continue
            if "." not in raw and not tok.endswith("%") and (0 <= val <= 10 or 100 <= val <= 120 or 1900 <= val <= 2100):
                continue
            out.append((tok, line.strip()))
    return out


def matches(tok: str, pool: list[float]) -> bool:
    raw = tok.replace(",", "").rstrip("%")
    target = abs(float(raw))
    decimals = len(raw.split(".")[1]) if "." in raw else 0
    for v in pool:
        for cand in (abs(v), abs(v) * 100):  # 允許比例寫成百分比
            if round(cand, decimals) == round(target, decimals):
                return True
    return False


def csv_numbers() -> list[float]:
    pool = []
    for f in RESULTS.glob("**/*.csv"):
        df = pd.read_csv(f)
        for c in df.columns:
            pool += pd.to_numeric(df[c], errors="coerce").dropna().tolist()
    return pool


def text_numbers(name: str) -> list[float]:
    vals = []
    for tok, _ in numbers_in_text(read(name)):
        vals.append(float(tok.replace(",", "").rstrip("%")))
    return vals


def report_unmatched(stage: str, name: str, pool: list[float], source_desc: str) -> None:
    nums = numbers_in_text(read(name))
    missing = [(t, line) for t, line in nums if not matches(t, pool)]
    if not nums:
        say(stage, "⚠️", f"{name} 沒有偵測到需要核對的數字")
    elif missing:
        say(stage, "⚠️", f"{name} 有 {len(missing)}/{len(nums)} 個數字在{source_desc}找不到，請人工確認：")
        for t, line in missing[:15]:
            say(stage, "  ", f"   「{t}」← {line[:70]}")
    else:
        say(stage, "✅", f"{name} 的 {len(nums)} 個數字都能在{source_desc}找到")


# ---------- 各階段 ----------
def check_M() -> None:
    plan_path = ROOT / "analysis_plan.yml"
    plan = yaml.safe_load(plan_path.read_text(encoding="utf-8")) or {}
    missing = [k for k in PLAN_KEYS if not plan.get(k) or "TODO" in str(plan.get(k))]
    say("M", "❌" if missing else "✅", f"analysis_plan.yml 未填欄位：{missing}" if missing else "analysis_plan.yml 必填欄位都已填寫")
    data = ROOT / "data" / "hs_school_year.csv"
    if data.exists() and plan.get("variables"):
        cols = set(pd.read_csv(data, nrows=0).columns)
        bad = [v for v in plan["variables"] if v not in cols]
        say("M", "❌" if bad else "✅", f"計畫用到資料中不存在的欄位：{bad}" if bad else f"計畫用到的 {len(plan['variables'])} 個欄位都存在")
    ok, msg = filled("01_methods.md", 300)
    say("M", "✅" if ok else "❌", msg)
    if frozen():
        say("M", "✅", "已凍結（git tag methods-frozen 存在）")
        changed = git("diff", "--name-only", "methods-frozen", "--", "analysis_plan.yml", "paper/01_methods.md").stdout.split()
        if changed:
            say("M", "❌", f"凍結後被修改：{changed}。請還原，並把變更寫進 deviations.md")
    else:
        say("M", "❌", "尚未凍結。確認方法無誤後執行：git add -A && git commit -m \"凍結研究方法\" && git tag methods-frozen")
        if any(RESULTS.glob("**/*.csv")) or any(RESULTS.glob("**/*.png")):
            say("M", "⚠️", "方法還沒凍結，results/ 卻已經有結果檔，請確認沒有先偷看結果")


def check_R() -> None:
    if not frozen():
        say("R", "❌", "方法尚未凍結，不能開始 R 階段")
        return
    files = list(RESULTS.glob("**/*.csv"))
    say("R", "✅" if files else "❌", f"results/ 有 {len(files)} 個 CSV 結果檔" if files else "results/ 還沒有 CSV 結果檔")
    ok, msg = filled("02_results.md")
    say("R", "✅" if ok else "❌", msg)
    if files and ok:
        report_unmatched("R", "02_results.md", csv_numbers(), " results/ 的 CSV 中")
        if "results/" not in read("02_results.md"):
            say("R", "⚠️", "02_results.md 沒有標註任何來源檔（例如：（results/table1.csv））")


def check_I() -> None:
    ok, msg = filled("03_intro.md")
    say("I", "✅" if ok else "❌", msg)


def check_D() -> None:
    ok, msg = filled("04_discussion.md")
    say("D", "✅" if ok else "❌", msg)
    if ok and "限制" not in read("04_discussion.md"):
        say("D", "⚠️", "04_discussion.md 沒有提到「限制」")
    if ok:
        report_unmatched("D", "04_discussion.md", text_numbers("02_results.md"), " 02_results.md 中")


def check_A() -> None:
    ok, msg = filled("05_abstract.md", 100)
    say("A", "✅" if ok else "❌", msg)
    if ok:
        report_unmatched("A", "05_abstract.md", text_numbers("02_results.md"), " 02_results.md 中")


def check_T() -> None:
    ok, msg = filled("00_title.md", 5)
    say("T", "✅" if ok else "❌", msg)


def check_X() -> None:
    p = ROOT / "paper.md"
    if not p.exists():
        say("X", "❌", "尚未組裝。執行：uv run python src/assemble.py")
        return
    text = p.read_text(encoding="utf-8")
    other_todo = text.replace(REF_TODO, "").count("TODO")
    if other_todo:
        say("X", "❌", f"paper.md 還有 {other_todo} 個 TODO 沒填")
    elif REF_TODO in text:
        say("X", "⚠️", f"paper.md 已組裝；還有 {text.count(REF_TODO)} 處需補文獻")
    else:
        say("X", "✅", "paper.md 已組裝，沒有 TODO")
    dev = re.sub(r"<!--.*?-->", "", (ROOT / "deviations.md").read_text(encoding="utf-8"), flags=re.S)
    n = len([l for l in dev.splitlines() if re.match(r"^\|\s*D\d+", l)])
    say("X", "✅", f"deviations.md 共 {n} 筆計畫變更（0 筆也可以，分享時說明即可）")


STAGES = {"M": ("Methods", check_M), "R": ("Results", check_R), "I": ("Introduction", check_I),
          "D": ("Discussion", check_D), "A": ("Abstract", check_A), "T": ("Title", check_T),
          "X": ("Assembly", check_X)}


def main() -> int:
    want = [s.upper() for s in sys.argv[1:]] or list(STAGES)
    for s in want:
        if s not in STAGES:
            print(f"未知階段 {s}；可用：{' '.join(STAGES)}")
            return 2
        STAGES[s][1]()
    for s in want:
        print(f"\n【{s}】{STAGES[s][0]}")
        for stage, status, msg in results:
            if stage == s:
                print(f"  {status} {msg}")
    return 1 if any(st == "❌" for _, st, _ in results) else 0


if __name__ == "__main__":
    sys.exit(main())
