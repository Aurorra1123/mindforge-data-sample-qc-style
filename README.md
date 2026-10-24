# Mindforge Data Sample & QC Style

A Codex skill for consistent data sample deliveries, PDF descriptions that accompany data ZIP packages, and client-facing QC reports in Chinese or English.

## Contents

- `SKILL.md` — entry point and shared delivery rules
- `references/sample-format.md` — machine-readable sample format and delivery manifest
- `references/pdf-delivery.md` — PDF content structure and JSON input format
- `scripts/render_delivery_pdf.py` — branded PDF renderer
- `assets/qc-report-template.html` and `assets/qc-report-template-en.html` — standalone Chinese and English HTML templates
- `assets/mindforge-logo-horizontal.*` — Mindforge brand assets used by the templates

## Use

Copy this folder to your Codex skills directory as `data-sample-qc-style`, then invoke the skill for a sample package, delivery PDF, or QC report. The templates contain illustrative content; replace it with verified delivery data before sending a report.

To render a PDF, prepare a UTF-8 JSON file following [the PDF reference](references/pdf-delivery.md), install `reportlab`, and run:

```bash
python3 scripts/render_delivery_pdf.py --input content.json --output delivery-description.pdf
```

The renderer supports `language: "zh"` and `language: "en"`. Include `reward_list` only when actual run records and a matching `reward_scope` are available. The list groups repeated tasks and models and displays thinking strength before run ID.

The HTML templates are self-contained and can be opened offline. The PDF renderer uses system CJK fonts when available and falls back to PDF CID fonts.

## Brand

This skill uses the Mindforge visual identity and logo. Apply any updated brand requirements supplied for a delivery.
