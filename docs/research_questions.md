# 練習主題：少子化與高中一年級學生數

臺灣出生人數長期下降，高中的新生規模也跟著改變。全班使用同一份資料，每組從下面 **3 個研究問題中選 1 個**。

這三題都只需要 `data/hs_school_year.csv` 裡現成的欄位，分析在一般筆電上幾秒內就能完成。

| 題目 | 研究問題 | 主要欄位 | 方向提示 |
|---|---|---|---|
| **A** | 103→114 學年度，私立高中一年級學生數的下降幅度，是否大於公立高中？ | `students_grade1`、`sector`、`academic_year`、`school_id` | 比較兩組的變化 |
| **B** | 哪些縣市的高中一年級學生數下降最多？下降幅度和縣市內學校的平均規模有關嗎？ | `students_grade1`、`county_name`、`student_total`、`academic_year` | 區域差異 |
| **C** | 103→114 學年度，專業群科學生占全體學生的比例是上升還是下降？公立和私立的變化是否不同？ | `students_vocational`、`student_total`、`sector`、`academic_year` | 學程結構與教育政策 |

## 討論方法時可以想想

這些都沒有標準答案，請組內討論後寫進 `analysis_plan.yml`，並說明理由：

- **分析單位**：用「全部學校加總」比較，還是先算「每所學校」的變化再比較？兩者回答的問題不一樣。
- **樣本**：要不要排除進修學校（`continuing_school`）、特殊教育學校（`special_education_school`）、矯正學校（`sector = correctional`）？學生數為 0 的學校怎麼處理？
- **學年度**：只比較 103 和 114 學年度兩個端點，還是看 12 年的趨勢？
- **中途新設或退場的學校**：只比較 103–114 學年度每年都存在的學校，還是全部納入？
- **公私立**：`sector` 有 public_national、public_local、private、correctional 四類，要怎麼合併成「公立／私立」？

## 欄位說明

完整定義見 [codebook.md](codebook.md)。幾個常用欄位：

| 欄位 | 說明 |
|---|---|
| `academic_year` | 學年度（民國），103–114 |
| `school_id` | 跨年追蹤同一所學校用的代碼 |
| `county_name` | 縣市（現行 22 縣市） |
| `sector` | 設立別：public_national 國立、public_local 地方公立、private 私立、correctional 矯正學校 |
| `student_total` | 學生總數 |
| `students_grade1` | 一年級學生數（新生規模的近似值，不等於招生人數） |
| `students_vocational` | 專業群科學生數 |
| `continuing_school`、`special_education_school` | 進修學校、特殊教育學校的標記（True／False） |
