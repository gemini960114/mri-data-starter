# 課後作業二　轉成 APA 第 7 版格式（約 1 小時）

**目標**：把定稿的論文排成 APA 第 7 版的 PDF。**只轉換格式，不改內容。**

教育與社會科學領域的期刊多半使用 APA 格式。不建議轉成 IEEE：IEEE 要把（作者，年份）改成 [1] 這種編號引用，參考文獻格式也要全部改寫，等於動到內容。

## 開始之前

1. 確認已經完成作業一，並打了 `paper-final` 標籤：

   ```bash
   git tag --list paper-final
   ```

   沒有輸出的話，先執行 `git add -A && git commit -m "定稿" && git tag paper-final`。

2. 選擇版面（在提示詞中填入）：

   | 模式 | 外觀 | 用途 |
   |---|---|---|
   | `jou`（建議） | 雙欄、單倍行距、標題與摘要在第一頁、圖放在正文中 | 看起來像已發表的期刊論文，適合繳交作業 |
   | `man` | 單欄、雙倍行距、獨立標題頁、圖放在最後 | 投稿用的稿件格式，給審稿人看的，不是期刊版面 |

   試跑時先產生了 `man` 版，試跑者覺得「看起來不像論文」，其實那是稿件格式本來的樣子。

## 貼給 AI 的提示詞

把 `[jou／man]` 換成你們選的模式：

````
# 把定稿論文轉成 APA 第 7 版格式（apa7，[jou／man] 模式）

請把 paper/ 的定稿內容轉成 APA 第 7 版格式（apa7 類別，[jou／man] 模式），輸出 LaTeX 原始檔與 PDF 到 latex_apa7/。

## 規則（AGENTS.md 優先）

- 只轉換格式，不改內容：不可以改寫句子、改變或新增任何數字、新增或刪除文獻。
- 不可以修改 analysis_plan.yml、paper/、results/、refs/ 的任何檔案。
- 文中引用已經是 APA 格式，原樣保留。
- 如果還有「TODO：需補文獻」，原樣保留並在 PDF 中用紅字顯示。
- 新產生的檔案放在 latex_apa7/；下載的工具放在 tools/，並把 tools/ 加進 .gitignore。

## 步驟 1：安裝工具

| 工具 | 用途 | 安裝方式 |
|---|---|---|
| pypandoc-binary | Markdown 轉 LaTeX（內含 pandoc） | uv add pypandoc-binary |
| Tectonic | 編譯 LaTeX 成 PDF（支援中文，需要的 LaTeX 套件第一次編譯時自動下載） | 從 https://github.com/tectonic-typesetting/tectonic/releases 下載符合作業系統的最新穩定版，解壓縮到 tools/；下載前告訴我版本號與檔名，發布頁有 SHA-256 就核對 |

無法下載 Tectonic 時，請停下來告訴我，改用備案：只產生 latex_apa7/ 的原始檔，由我上傳到 Overleaf，編譯器選 XeLaTeX。
不要使用 biblatex／biber；參考文獻用手動排版。

## 步驟 2：寫轉換程式 src/to_apa7.py

1. 依閱讀順序讀取 paper/ 的章節：00_title、05_abstract、03_intro、01_methods、02_results、04_discussion、06_references；去掉每章開頭以 > 開頭的說明行和 HTML 註解（做法同 src/assemble.py）。
2. 用 pypandoc 轉成 LaTeX，套進 \documentclass[jou 或 man]{apa7}：
   - 中文用 xeCJK，字型依序嘗試 Microsoft JhengHei → Noto Serif CJK TC → Noto Sans CJK TC，說明實際用了哪個
   - 依 apa7 類別設定 \title、\shorttitle、\authorsnames、\authorsaffiliations；組別與組員作為作者
   - \abstract{} 放摘要；\keywords{} 從論文內容選 3–5 個既有詞彙
   - 前言不加「前言」標題；方法、結果、討論用第 1 級標題（\section），小標題用第 2 級（\subsection）
   - man 模式維持預設（圖放在全文最後，這是 APA 稿件格式本來的樣子）；jou 模式的圖放在正文中，可以跨兩欄
3. APA 的符號與數字格式：
   - 英文字母的統計符號用斜體：n、p、t、r
   - 希臘字母（ρ、α）用正體，不要設成斜體
   - 不會超過 1 的數值去掉小數點前的 0（ρ = 0.365 → ρ = .365、p = 0.094 → p = .094），這只是格式變更，數值不變
   - 不要改變任何數字的位數（不重新四捨五入）
   - 統計符號、運算符號與數值之間用不斷行空格，避免「p <」和數值被斷在兩行
4. 來源標註：paper/02_results.md 每個數字後面的（results/…csv）是本課程的查核用標註，不屬於 APA 格式。PDF 中移除這些標註；Markdown 草稿保留不動。
5. 圖：把 results/ 中被論文提到的 PNG 複製到 latex_apa7/figures/；圖號用粗體（**圖 1**），下一行是斜體圖標題；圖說不可以新增數字。
6. 表格：表號用粗體、標題用斜體，只用水平線（booktabs）。
7. 參考文獻：照 06_references.md 手動排版，懸掛縮排、保留原有順序，DOI 與網址可點擊、長網址可斷行（xurl）。
8. 輸出 latex_apa7/paper_apa7.tex。

## 步驟 3：編譯與檢查

1. 執行 tools/tectonic latex_apa7/paper_apa7.tex，產生 latex_apa7/paper_apa7.pdf。
2. 數字一致性：比對 paper.md（去掉來源標註後）與 tex 中的所有數字，兩邊必須相同（去掉小數點前的 0 視為相同），列出比對結果。
3. 引用一致性：文中引用的數量、作者與年份和 paper.md 相同；參考文獻筆數相同。
4. 內容未被修改：執行 git diff paper-final -- paper/ results/ refs/ analysis_plan.yml，應該沒有輸出。
5. 把 PDF 每一頁轉成圖片看一遍：中文沒有方框或缺字、紅字 TODO 正常、圖和參考文獻排版正常。

## 完成後回報

- 工具與版本、中文字型
- 三項一致性檢查的結果，以及做了「去掉小數點前的 0」的數字
- PDF 頁數與排版問題
- 新增或修改的檔案清單
````

## 完成後

```bash
git add -A
git commit -m "轉成 APA 第 7 版格式"
```

## 可以再做：APA 稽核（選做）

如果想進一步檢查 APA 格式，可以請 AI 逐項列出不符合 APA 第 7 版的地方，**只列出、不修改**，你們看過再決定要改哪些。要注意：

- 稽核標準要和你們選的模式一致。APA 的「學生論文」格式是單欄、雙倍行距，用它來稽核 `jou` 期刊版面，會冒出一大堆版面差異，那不是錯誤。
- 牽涉內容的建議（例如改寫句子、刪掉文獻）不能在排版階段處理；要改的話回到作業一，改完 commit 後用 `git tag -f paper-final` 把標籤移到新版本，再重新排版。
