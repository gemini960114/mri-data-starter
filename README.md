# MRI-DATA 研究練習：用 AI 協作完成一篇研究短報告

> **第一次使用？請看詳細的 [學生操作手冊](docs/student_guide.md)**：每一步要輸入什麼、會看到什麼、AI 會問哪些問題與建議選項。

這是一份練習模板。你們會用**真實的臺灣高中資料**，和 AI 一起完成一篇研究短報告，練習一套「用 AI 做研究、但結果可以信任」的流程。

## 這個練習要學什麼

| 原則 | 為什麼重要 |
|---|---|
| **先定方法，再看結果** | 避免看到數字後才改方法、挑好看的結果來報 |
| **每個數字都要查得到來源** | 避免 AI 編造數據 |
| **改了計畫就要記錄** | 讓研究過程透明、可檢驗 |

這三個原則排成寫作順序，就是 **MRI-DATA**：

| 順序 | 階段 | 寫什麼 | 檔案 |
|---|---|---|---|
| 1 | **M**ethods | 研究方法，寫完就**凍結** | `analysis_plan.yml`、`paper/01_methods.md` |
| 2 | **R**esults | 執行分析、描述結果 | `src/analysis.py`、`results/`、`paper/02_results.md` |
| 3 | **I**ntroduction | 為什麼研究這個問題 | `paper/03_intro.md` |
| 4 | **D**iscussion | 結果代表什麼、有哪些限制 | `paper/04_discussion.md` |
| 5 | **A**bstract | 摘要 | `paper/05_abstract.md` |
| 6 | **T**itle | 標題 | `paper/00_title.md` |
| 7 | **A**ssembly | 依閱讀順序組裝成完整論文 | `paper.md` |

## 開始之前：分組與角色

每組 3–4 人，統計所與教育所混合：

| 角色 | 做什麼 |
|---|---|
| **AI 操作員**（輪流擔任） | 輸入提示詞、執行指令 |
| **方法把關**（統計所） | 檢查 AI 寫的方法和程式是否合理 |
| **教育解讀**（教育所） | 定義研究問題、解讀教育意義、寫限制 |
| **數字查核員** | 逐一核對論文裡的數字是否查得到來源 |

## 第 0 步：準備環境（約 10 分鐘）

需要 [git](https://git-scm.com/)、[uv](https://docs.astral.sh/uv/)，以及一個 AI 程式助理（例如 Claude Code）。

```bash
git clone https://github.com/gemini960114/mri-data-starter
cd mri-data-starter
uv sync
uv run python src/get_data.py
```

看到 `[OK] hs_school_year.csv 的 SHA-256 正確` 就完成了。全班使用的資料完全相同，所以結果不同一定是方法不同。

> 無法 `git clone` 時：向老師拿 zip 檔，解壓縮後在資料夾內執行 `git init`，再從 `uv sync` 開始。

**用 AI 之前**：在這個資料夾裡啟動 AI 助理。AI 會先讀 [`AGENTS.md`](AGENTS.md)，裡面寫好了 MRI-DATA 的規則，例如「方法凍結前不能計算結果」。你也可以打開來看看，AI 被要求遵守哪些事。

## 第 1–7 步：照著提示詞做

每一步的目標、可以直接複製給 AI 的提示詞、檢查方式，都寫在 [`prompts/`](prompts/)：

| 步驟 | 檔案 | 時間 |
|---|---|---|
| 1　M：研究方法並凍結 | [`prompts/1_M_methods.md`](prompts/1_M_methods.md) | 40 分鐘 |
| 2　R：分析與結果 | [`prompts/2_R_results.md`](prompts/2_R_results.md) | 45 分鐘 |
| 3　I：前言 | [`prompts/3_I_intro.md`](prompts/3_I_intro.md) | 10 分鐘 |
| 4　D：討論 | [`prompts/4_D_discussion.md`](prompts/4_D_discussion.md) | 15 分鐘 |
| 5–6　A + T：摘要與標題 | [`prompts/5_AT_abstract_title.md`](prompts/5_AT_abstract_title.md) | 10 分鐘 |
| 7　Assembly：組裝與分享準備 | [`prompts/7_X_assembly.md`](prompts/7_X_assembly.md) | 5 分鐘 |

課後作業：

| 作業 | 檔案 | 時間 |
|---|---|---|
| 一　補充文獻（自己搜尋、閱讀、決定） | [`prompts/8_references.md`](prompts/8_references.md) | 約 1 小時 |
| 二　轉成 APA 第 7 版格式 | [`prompts/9_format_apa.md`](prompts/9_format_apa.md) | 約 1 小時 |

研究題目在 [`docs/research_questions.md`](docs/research_questions.md)：主題是「**少子化與高中一年級學生數**」，每組從 A、B、C 三題選一題。

## 隨時檢查進度

```bash
uv run python src/check_stage.py        # 所有階段
uv run python src/check_stage.py R      # 只看某一階段
```

✅ 通過　⚠️ 請人工確認　❌ 未完成或違反規則。它也會列出「找不到來源的數字」，但最後仍要由數字查核員人工確認。

## 資料來源

本練習使用 **tw-highschool-panel** 資料集 v2026.10.1，原始資料來自教育部統計處公開的高級中等學校校別與科別資料：

> Chuang, C.-C. (2026). *tw-highschool-panel：臺灣高級中等學校校級面板資料（103–114 學年度）* (Version 2026.10.1) [Data set]. Zenodo. https://doi.org/10.5281/zenodo.23293536

欄位定義見 [`docs/codebook.md`](docs/codebook.md)。資料是**學校層級**的彙總統計，沒有學生個人資料。

## 授權

模板的程式與文件採 [MIT](LICENSE) 授權；資料依資料集的授權（CC BY 4.0，原始資料為政府資料開放授權條款—第 1 版）。
