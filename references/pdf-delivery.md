# 数据 ZIP 随附 PDF 说明

PDF 是给接收方看的最终陈述文档。先核对实际 ZIP、任务规格和已完成的验证记录，再撰写内容。旧审查报告可作为事实来源，但其判断、修复讨论和审查过程不能直接搬进交付说明。

## 内容顺序

1. 标题、批次/资料版本、数据范围；文件名和数量以实际 ZIP 为准。
2. 多题交付先列题目概览：每题的名称、一句话题目内容和难点。紧接概览列出实际 **Reward list**：按题目、模型、thinking 强度、运行编号、turn 轮数、reward 的顺序呈现。表格按题目和模型分组，题目名与模型名在一组中只显示一次，逐次的 turn 与 reward 仍各占一行。注明评测版本、预算及 reward 口径；同题多次运行分别列行并保留 run ID。Thinking 强度应标明是配置档位还是实测 token；定义 turn 的计数口径。达到时限的运行在 turn 数后加 `†`，并在表旁说明该轮数是截断值。只有取得原始运行记录后才填写这一表，不根据审查摘要推算，也不把不同预算的结果混为同一口径。没有原始记录时，省略该表并在交付前补齐。
3. 每题依次写：**题目描述**（问题是什么）、**工作内容**（样本/任务做了什么）、**要求覆盖**（已证实满足的项目）、**样例结果**（必要时给具体指标与条件）。覆盖范围较窄时，简短写明范围。

保持客观、简洁。不要写“为什么可以交付”、接收/退回建议、内部审查过程、AI 生成或审查痕迹、无关失败归因。Reward list 的模型运行数据属于交付事实，应如实呈现。也不要删去会改变结论的范围限制：未验证的要求不能写成已满足。没有真实 ZIP 或最终运行记录时，只写现有材料能支持的范围，待与最终交付文件核对后再发出。

## 统一版式

使用 [PDF 生成脚本](../scripts/render_delivery_pdf.py) 和 [Mindforge 横版 Logo](../assets/mindforge-logo-horizontal.png)。A4 页面、品牌暖白底、深灰字、蓝色层级标记和淡青色内容区。Logo 每页出现，避免占据正文。每页保留页码，表格和段落不截断；通常每页安排两题，内容较长时允许自然分页。

脚本读取 UTF-8 JSON：

```json
{
  "language": "zh",
  "title": "项目数据 Sample 说明",
  "subtitle": "题目内容与要求覆盖",
  "version": "批次与版本信息",
  "brand_context": "项目短名，显示在页脚",
  "footer_label": "页脚文档类型",
  "intro": "交付范围的一句话说明。",
  "tasks": [
    {
      "name": "题目名称",
      "id": "task-id",
      "domain": "领域",
      "topic": "一行题目内容",
      "difficulty": "难点的简短客观描述",
      "description": "题目描述",
      "work": ["工作内容一", "工作内容二"],
      "requirements": ["已满足的要求一", "已满足的要求二"],
      "verification": "有依据的样例结果，可省略",
      "scope_note": "必要的覆盖范围说明，可省略"
    }
  ],
  "reward_scope": "评测版本、运行预算、reward 口径；有 reward_list 时必填",
  "reward_list": [
    {
      "task_id": "task-id",
      "run_id": "原始运行 ID，可省略",
      "run_label": "表内短编号，可省略；不替代原始 run_id",
      "model": "实际模型名称",
      "thinking": "实际 thinking 强度",
      "turns": 12,
      "reward": 0.75
    }
  ]
}
```

上面的 Reward 行仅说明字段形状，不是可直接交付的数据。若真实记录尚未取得，应从 JSON 中去掉 `reward_scope` 和 `reward_list`；最终交付版需要核对并补上真实记录。

执行：`python3 scripts/render_delivery_pdf.py --input content.json --output delivery-description.pdf`。运行环境需有 `reportlab`；在 Codex 桌面环境优先使用内置 Python。生成后逐页渲染检查 Logo、中文字体、换行、页眉页脚与打印分页，并用文本提取核对任务数量、文件名、数字及无占位符。
