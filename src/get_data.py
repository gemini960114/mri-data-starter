"""下載練習用資料，並核對 SHA-256。

用法：uv run python src/get_data.py
輸出：data/hs_school_year.csv
"""
import hashlib
import sys
import urllib.request
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]


def sha256_of(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    cfg = yaml.safe_load((ROOT / "data_source.yml").read_text(encoding="utf-8"))
    (ROOT / "data").mkdir(exist_ok=True)
    ok = True
    for f in cfg["files"]:
        dest = ROOT / "data" / f["name"]
        if dest.exists() and sha256_of(dest) == f["sha256"]:
            print(f"[已存在] {f['name']}")
        else:
            print(f"[下載中] {f['name']} ← {cfg['dataset']} {cfg['version']}")
            try:
                with urllib.request.urlopen(f["url"], timeout=120) as resp:
                    dest.write_bytes(resp.read())
            except OSError as e:
                print(f"[失敗] 無法下載：{e}\n        請改用老師提供的 zip 檔，把 {f['name']} 放到 data/ 資料夾後再執行一次。")
                return 1
        if sha256_of(dest) == f["sha256"]:
            print(f"[OK] {f['name']} 的 SHA-256 正確，和全班使用的資料完全相同。")
        else:
            print(f"[錯誤] {f['name']} 的 SHA-256 不符，檔案可能損毀，請刪除後重新執行。")
            ok = False
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
