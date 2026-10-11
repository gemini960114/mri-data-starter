# 第 2 步　R：分析與結果（約 45 分鐘）

**目標**：完全照凍結的計畫執行分析，並把結果寫下來。每個數字都要查得到來源。

## 2-1 請 AI 寫分析程式並執行（25 分鐘）

```
方法已經凍結。請依照 analysis_plan.yml 寫 src/analysis.py 並執行
（用 uv run python src/analysis.py）。
表格存成 CSV、圖存成 PNG，都放在 results/，檔名照 analysis_plan.yml 的 outputs。

不要修改 analysis_plan.yml 和 paper/01_methods.md。
如果發現計畫行不通，請先停下來告訴我們原因和建議做法；
我們同意後，先寫進 deviations.md 再執行。
```

AI 寫完程式後，**方法把關**組員請 AI 解釋程式的每一段在做什麼，確認和計畫一致。

## 2-2 請 AI 寫結果段落（15 分鐘）

```
請根據 results/ 裡的檔案寫 paper/02_results.md。
只描述結果，不要解讀原因。
每個數字後面都要標註來源檔，例如：（results/table1.csv）。
```

## 2-3 數字查核（5 分鐘）

```bash
uv run python src/check_stage.py R
```

工具會列出「找不到來源的數字」。**數字查核員**逐一打開結果檔確認：

- 真的找不到 → 請 AI 刪除或改正
- 其實有（例如換算方式不同）→ 確認無誤即可
- 是衍生數字（例如「減少了多少人」）→ 請 AI 在程式中計算並存成結果檔；這個表不在計畫裡，所以先寫進 `deviations.md`

> **為什麼要標註來源？** 這是防止 AI 編造數據最簡單有效的方法：查不到來源的數字一律刪除。
