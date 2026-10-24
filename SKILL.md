---
name: data-sample-qc-style
description: Standardize Mindforge data sample deliveries, create client-facing PDF descriptions to accompany data ZIP packages, and produce Chinese or English QC feedback HTML reports. Use for sample packages, data handoffs, and quality inspection reports; preserve client-specified schema or updated brand requirements.
---

# Data Sample 与质检交付风格

将同一批交付物做成清晰、可核验、视觉一致的成果。先识别用户已有的字段、格式、验收标准和品牌规范；这些要求优先于本 Skill 的默认建议。不要为了套模板改动数据含义或凭空补齐检测结果。

## 选择交付形式

- **数据 Sample**：读取 [references/sample-format.md](references/sample-format.md)。输出机器可读的样本文件、字段说明和交付清单。字段名及机器可读键保持约定格式，面向人的字段描述和说明使用用户要求的语言。单文件预览可以简化目录。
- **完整数据 ZIP 交付**：同时生成一份面向接收方的 PDF 说明，读取 [references/pdf-delivery.md](references/pdf-delivery.md)，使用 [scripts/render_delivery_pdf.py](scripts/render_delivery_pdf.py) 保持版式统一。首页概览列出各题内容和难点，紧随其后用实际运行记录生成 Reward list，逐行呈现模型、thinking 强度、turn 轮数和 reward。PDF 与 ZIP 应使用同一批次、任务名和实际数据范围。
- **质检反馈**：中文使用 [assets/qc-report-template.html](assets/qc-report-template.html)，英文使用 [assets/qc-report-template-en.html](assets/qc-report-template-en.html)。两者共享视觉系统，生成最终可独立打开的 HTML。根据实际检查项目删减模块；不要保留空占位符或虚构的指标。
- **两者同时交付**：在 HTML 中写清样本文件名、版本和检查范围，保证与交付清单一致。

## 共通规则

1. 标题、批次/版本、生成日期、数据范围和口径说明要醒目；不确定的信息标为“待确认”，不要推断为事实。
2. 所有数字与要求覆盖都应能回到实际文件或已确认的验证结果。质检反馈区分事实、观察与建议；对外交付 PDF 只陈述题目内容、工作内容、满足的要求和必要的范围说明。
3. 默认使用 Mindforge 品牌：暖白 `#FCFBF8`、深灰 `#303943`，蓝 `#4597F5`、青 `#59C8D7`、薄荷绿 `#6BDEB4` 用作少量强调。HTML 使用 [assets/mindforge-logo-horizontal.svg](assets/mindforge-logo-horizontal.svg)，PDF 使用同款 [PNG](assets/mindforge-logo-horizontal.png)；保持原始比例、四周留白和渐变方向。HTML 模板已内嵌 SVG，可独立离线打开。不要引入其他品牌的标志、插图或文案。颜色不能是唯一的状态表达；同时写文字标签。
4. 表格与字段说明优先保证可读性：长值换行，数值右对齐，单位和分母明确。不要为了紧凑省略关键说明。
5. 对外发送前核对样本行数、字段数、版本号、文件名、指标分母、结论与证据。涉及敏感数据时，先按交付约定脱敏。

## 质检 HTML 的内容原则

推荐顺序：概览 → 关键指标 → 问题清单 → 证据/样例 → 处理建议 → 检查口径。问题清单应包含严重程度、对象或范围、发现、影响、建议和可定位证据；不适用的列可以删去。汇总指标要显示检查范围与统计口径；缺少依据时用文字说明，而非显示 `0%`。结论状态仅在有明确阈值或验收标准时标注“通过/不通过”；否则使用“待确认”。

从对应语言的模板复制内容后，用真实数据替换所有示例文本，并将 CSS 保留在最终 HTML 内，使单文件离线可用。除非用户要求双语，不要混排中文和英文的正文标签；文件名或字段名等原始标识符可以保留。确认桌面和窄屏布局、表格溢出、打印分页及字体回退正常。保留宽松而有节奏的排版，不要把每项内容都做成卡片，也不要使用大面积渐变作为报告主视觉。
