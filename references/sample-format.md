# Sample 交付格式

目标是让接收方快速判断“这是什么、字段是什么意思、样本代表什么、如何复现”。保留源数据的语义、类型和原有主键；优先沿用用户指定的 CSV、JSONL、Parquet、XLSX 等格式。

正式对外交付时，将数据与字段说明打包为 ZIP，并在 ZIP 旁提供一份同批次的 PDF 描述文档。PDF 的内容与制作方法见 [pdf-delivery.md](pdf-delivery.md)。

## 建议的最小交付包

```text
delivery/
├── sample.csv             # 或用户指定的其他机器可读格式
├── fields.csv             # 字段名、类型、含义、单位、空值/枚举口径
└── manifest.json          # 批次、来源/范围、抽样方法、行数、版本等
```

单文件交付也可以；把清单信息放在相邻说明中即可。不要为了模板重复导出多个等价文件。

## manifest.json 建议字段

```json
{
  "delivery_id": "batch-2026-10-20-v1",
  "dataset": "数据集名称",
  "version": "v1",
  "created_at": "2026-10-20T12:00:00+08:00",
  "sample_file": "sample.csv",
  "format": "csv",
  "encoding": "utf-8",
  "row_count": 100,
  "field_count": 12,
  "scope": "覆盖的时间、来源或对象范围",
  "sampling_method": "抽样方法；未知时写待确认",
  "filters": "纳入/排除条件；不适用时可省略",
  "null_values": [""],
  "notes": "脱敏、时区、单位或已知限制"
}
```

这些是建议字段，不是强制业务 schema。日期、数量和文件名必须与实际交付一致。

## 字段说明表

列建议为 `field_name, data_type, description, unit_or_format, nullable, allowed_values, example, notes`。仅保留有意义的列；示例值需脱敏。复杂嵌套结构可用 JSON Schema、Markdown 或源系统字段字典替代。

## 文件细节

- CSV：UTF-8；首行字段名；统一分隔符、换行和引号规则；保留前导零的标识符为文本；明确日期时区。
- JSONL：每行一条有效 JSON；字段类型一致；缺失与显式 `null` 的含义要说明。
- 样本选择：说明是随机、分层、连续截取还是人工挑选，以及样本是否可代表全集。不能确认时直说。
- 建议对最终样本做一次解析检查，并核对行数、字段数、重复主键与空值口径；这些检查结果只有实际执行后才能写入报告。
