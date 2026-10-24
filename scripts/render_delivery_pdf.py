#!/usr/bin/env python3
"""Render a Mindforge data-sample delivery brief from a JSON content file."""

import argparse
import json
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.cidfonts import UnicodeCIDFont
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    BaseDocTemplate,
    Frame,
    HRFlowable,
    PageBreak,
    PageTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
)
from xml.sax.saxutils import escape


INK = colors.HexColor("#303943")
MUTED = colors.HexColor("#63717A")
BLUE = colors.HexColor("#256DA7")
LINE = colors.HexColor("#DCE4E5")
SOFT = colors.HexColor("#EDF7F5")
PAPER = colors.HexColor("#FCFBF8")
PAGE_W, PAGE_H = A4
LEFT = RIGHT = 48
CONTENT_W = PAGE_W - LEFT - RIGHT
ASSETS = Path(__file__).resolve().parents[1] / "assets"


def fonts():
    """Use bundled system CJK fonts when present; fall back to PDF CID fonts."""
    serif = Path("/System/Library/Fonts/Supplemental/Songti.ttc")
    sans = Path("/System/Library/Fonts/Supplemental/Arial Unicode.ttf")
    if serif.exists() and sans.exists():
        pdfmetrics.registerFont(TTFont("MindforgeSerif", str(serif), subfontIndex=0))
        pdfmetrics.registerFont(TTFont("MindforgeSans", str(sans)))
        return "MindforgeSerif", "MindforgeSans"
    pdfmetrics.registerFont(UnicodeCIDFont("STSong-Light"))
    return "STSong-Light", "STSong-Light"


def p(text, style):
    return Paragraph(escape(str(text)).replace("\n", "<br/>"), style)


def styles(serif, sans):
    common = dict(textColor=INK, wordWrap="CJK", allowWidows=0, allowOrphans=0)
    return {
        "kicker": ParagraphStyle("kicker", fontName=sans, fontSize=8.2, leading=12, textColor=BLUE, spaceAfter=10, **{k:v for k,v in common.items() if k!="textColor"}),
        "title": ParagraphStyle("title", fontName=serif, fontSize=29, leading=38, spaceAfter=8, **common),
        "subtitle": ParagraphStyle("subtitle", fontName=sans, fontSize=11.5, leading=18, textColor=MUTED, spaceAfter=15, **{k:v for k,v in common.items() if k!="textColor"}),
        "body": ParagraphStyle("body", fontName=sans, fontSize=9.5, leading=16, spaceAfter=4, **common),
        "small": ParagraphStyle("small", fontName=sans, fontSize=8.2, leading=13, textColor=MUTED, **{k:v for k,v in common.items() if k!="textColor"}),
        "table": ParagraphStyle("table", fontName=sans, fontSize=8.8, leading=14, **common),
        "reward": ParagraphStyle("reward", fontName=sans, fontSize=8.2, leading=12.5, **common),
        "rewardcenter": ParagraphStyle("rewardcenter", fontName=sans, fontSize=8.2, leading=12.5, alignment=1, **common),
        "rewardright": ParagraphStyle("rewardright", fontName=sans, fontSize=8.2, leading=12.5, alignment=2, **common),
        "tablehead": ParagraphStyle("tablehead", fontName=sans, fontSize=8.2, leading=12, textColor=MUTED, **{k:v for k,v in common.items() if k!="textColor"}),
        "tableheadcenter": ParagraphStyle("tableheadcenter", fontName=sans, fontSize=8.2, leading=12, alignment=1, textColor=MUTED, **{k:v for k,v in common.items() if k!="textColor"}),
        "tableheadright": ParagraphStyle("tableheadright", fontName=sans, fontSize=8.2, leading=12, alignment=2, textColor=MUTED, **{k:v for k,v in common.items() if k!="textColor"}),
        "tasktitle": ParagraphStyle("tasktitle", fontName=serif, fontSize=17, leading=25, **common),
        "taskmeta": ParagraphStyle("taskmeta", fontName=sans, fontSize=8.2, leading=13, textColor=MUTED, **{k:v for k,v in common.items() if k!="textColor"}),
        "label": ParagraphStyle("label", fontName=sans, fontSize=8, leading=12, textColor=BLUE, spaceAfter=5, **{k:v for k,v in common.items() if k!="textColor"}),
        "cell": ParagraphStyle("cell", fontName=sans, fontSize=8.7, leading=14, **common),
    }


def labels(language):
    if language == "en":
        return dict(overview="TASK OVERVIEW", number="NO.", task="TASK", topic="TOPIC", difficulty="DIFFICULTY", reward_list="REWARD LIST", model="MODEL", run="RUN / ID", thinking="THINKING", turns="TURNS", reward="REWARD", description="TASK DESCRIPTION", work="WORK COVERED", requirements="REQUIREMENTS COVERED", verification="SAMPLE RESULT", scope="SCOPE", footer="Data sample brief")
    return dict(overview="任务概览", number="序号", task="题目", topic="题目内容", difficulty="难点", reward_list="Reward list", model="模型", run="运行 / ID", thinking="Thinking 强度", turns="Turn 轮数", reward="Reward", description="题目描述", work="工作内容", requirements="要求覆盖", verification="样例结果", scope="范围说明", footer="数据 Sample 说明")


def page_furniture(canvas, doc, label, logo_path, sans, brand_context):
    canvas.saveState()
    canvas.setFillColor(PAPER)
    canvas.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)
    canvas.drawImage(str(logo_path), LEFT, PAGE_H - 66, width=148, height=38, preserveAspectRatio=True, anchor="sw", mask="auto")
    canvas.setStrokeColor(LINE)
    canvas.setLineWidth(.7)
    canvas.line(LEFT, PAGE_H - 74, PAGE_W - RIGHT, PAGE_H - 74)
    canvas.line(LEFT, 48, PAGE_W - RIGHT, 48)
    canvas.setFillColor(MUTED)
    canvas.setFont(sans, 8)
    canvas.drawString(LEFT, 33, f"MINDFORGE  /  {brand_context}")
    canvas.drawRightString(PAGE_W - RIGHT, 33, f"{label}   {doc.page:02d}")
    canvas.restoreState()


def task_block(task, index, S, L):
    heading = Table([
        [p(f"{index:02d}", S["kicker"]), p(task["name"], S["tasktitle"]), p(f"{task['domain']}\n{task['id']}", S["taskmeta"])],
    ], colWidths=[31, CONTENT_W - 171, 140])
    heading.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 0),
        ("RIGHTPADDING", (0, 0), (-1, -1), 0),
        ("TOPPADDING", (0, 0), (-1, -1), 0),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
    ]))
    inner = [heading, Spacer(1, 5), HRFlowable(width="100%", thickness=.7, color=LINE), Spacer(1, 11)]
    inner.extend([p(L["description"], S["label"]), p(task["description"], S["body"]), Spacer(1, 8)])
    work = [p(L["work"], S["label"])] + [p("•  " + x, S["cell"]) for x in task["work"]]
    reqs = [p(L["requirements"], S["label"])] + [p("•  " + x, S["cell"]) for x in task["requirements"]]
    panel = Table([[work, reqs]], colWidths=[CONTENT_W / 2, CONTENT_W / 2])
    panel.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), SOFT),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 13),
        ("RIGHTPADDING", (0, 0), (-1, -1), 13),
        ("TOPPADDING", (0, 0), (-1, -1), 11),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 11),
        ("LINEBEFORE", (1, 0), (1, 0), .5, LINE),
    ]))
    inner.extend([panel, Spacer(1, 10)])
    if task.get("verification"):
        inner.extend([p(L["verification"], S["label"]), p(task["verification"], S["body"])])
    if task.get("scope_note"):
        inner.extend([p(L["scope"], S["label"]), p(task["scope_note"], S["small"])])
    return inner


def render(data, output, logo):
    serif, sans = fonts()
    S = styles(serif, sans)
    L = labels(data.get("language", "zh"))
    tasks = data["tasks"]
    if not tasks or any(not all(k in task for k in ("name", "id", "domain", "topic", "difficulty", "description", "work", "requirements")) for task in tasks):
        raise ValueError("Each task needs name, id, domain, topic, difficulty, description, work, and requirements")
    reward_list = data.get("reward_list", [])
    if reward_list:
        if not data.get("reward_scope"):
            raise ValueError("reward_scope is required when reward_list is provided")
        required = ("task_id", "model", "thinking", "turns", "reward")
        if any(not all(k in row for k in required) for row in reward_list):
            raise ValueError("Each reward_list row needs task_id, model, thinking, turns, and reward")
    doc = BaseDocTemplate(str(output), pagesize=A4, leftMargin=LEFT, rightMargin=RIGHT, topMargin=92, bottomMargin=62, title=data["title"], author="Mindforge")
    frame = Frame(LEFT, 62, CONTENT_W, PAGE_H - 92 - 62, leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)
    doc.addPageTemplates(PageTemplate(id="Branded", frames=[frame], onPage=lambda c, d: page_furniture(c, d, data.get("footer_label", L["footer"]), logo, sans, data.get("brand_context", "DATA SAMPLE"))))
    story = [Spacer(1, 23), p(data.get("kicker", "MINDFORGE / DATA SAMPLE"), S["kicker"]), p(data["title"], S["title"]), p(data.get("subtitle", ""), S["subtitle"]), p(data.get("version", ""), S["small"]), Spacer(1, 24), HRFlowable(width="100%", thickness=1.1, color=BLUE), Spacer(1, 19)]
    if data.get("intro"):
        story.extend([p(data["intro"], S["body"]), Spacer(1, 20)])
    story.extend([p(L["overview"], S["kicker"]), Spacer(1, 4)])
    rows = [[p(L["number"], S["tablehead"]), p(L["task"], S["tablehead"]), p(L["topic"], S["tablehead"]), p(L["difficulty"], S["tablehead"])]]
    for index, task in enumerate(tasks, 1):
        rows.append([p(f"{index:02d}", S["table"]), p(task["name"], S["table"]), p(task["topic"], S["table"]), p(task["difficulty"], S["table"])])
    table = Table(rows, colWidths=[40, 100, 226, CONTENT_W - 366], repeatRows=1)
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), SOFT),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LINEBELOW", (0, 0), (-1, -1), .5, LINE),
        ("LEFTPADDING", (0, 0), (-1, -1), 10),
        ("RIGHTPADDING", (0, 0), (-1, -1), 10),
        ("TOPPADDING", (0, 0), (-1, -1), 10),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
    ]))
    story.append(table)
    if reward_list:
        story.extend([PageBreak(), p(L["reward_list"], S["title"]), p(data["reward_scope"], S["small"]), Spacer(1, 17)])
        task_ids = {task["id"] for task in tasks}
        if any(row["task_id"] not in task_ids for row in reward_list):
            raise ValueError("reward_list contains an unknown task_id")
        reward_rows = [[
            p(L["task"], S["tablehead"]), p(L["model"], S["tablehead"]),
            p(L["thinking"], S["tablehead"]), p(L["run"], S["tableheadcenter"]),
            p(L["turns"], S["tableheadright"]), p(L["reward"], S["tableheadright"]),
        ]]
        group_styles = []
        for task in tasks:
            entries = [row for row in reward_list if row["task_id"] == task["id"]]
            if not entries:
                continue
            task_start = len(reward_rows)
            model_start = task_start
            previous_key = None
            for index, row in enumerate(entries):
                model_key = (str(row["model"]), str(row["thinking"]))
                new_model = model_key != previous_key
                current_row = len(reward_rows)
                if new_model and previous_key is not None and current_row - model_start > 1:
                    group_styles.extend([
                        ("SPAN", (1, model_start), (1, current_row - 1)),
                        ("SPAN", (2, model_start), (2, current_row - 1)),
                    ])
                if new_model:
                    model_start = current_row
                run_label = row.get("run_label", row.get("run_id", "—"))
                reward_rows.append([
                    p(task["name"] if index == 0 else "", S["reward"]),
                    p(row["model"] if new_model else "", S["reward"]),
                    p(row["thinking"] if new_model else "", S["reward"]),
                    p(run_label, S["rewardcenter"]),
                    p(row["turns"], S["rewardright"]),
                    p(row["reward"], S["rewardright"]),
                ])
                previous_key = model_key
            task_end = len(reward_rows) - 1
            if task_end - model_start > 0:
                group_styles.extend([
                    ("SPAN", (1, model_start), (1, task_end)),
                    ("SPAN", (2, model_start), (2, task_end)),
                ])
            if task_end > task_start:
                group_styles.append(("SPAN", (0, task_start), (0, task_end)))
            group_styles.extend([
                ("BACKGROUND", (0, task_start), (0, task_end), SOFT),
                ("LINEBELOW", (0, task_end), (-1, task_end), .8, LINE),
            ])
        reward_table = Table(reward_rows, colWidths=[101, 96, 75, 64, 72, CONTENT_W - 408], repeatRows=1)
        reward_table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), SOFT),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("LINEBELOW", (3, 1), (-1, -1), .35, LINE),
            ("LEFTPADDING", (0, 0), (-1, -1), 8),
            ("RIGHTPADDING", (0, 0), (-1, -1), 8),
            ("TOPPADDING", (0, 0), (-1, -1), 2.5),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 2.5),
        ] + group_styles))
        story.append(reward_table)
    for index, task in enumerate(tasks, 1):
        if index % 2 == 1:
            story.append(PageBreak())
        else:
            story.append(Spacer(1, 23))
        story.extend(task_block(task, index, S, L))
    doc.build(story)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--logo", type=Path, default=ASSETS / "mindforge-logo-horizontal.png")
    args = parser.parse_args()
    content = json.loads(args.input.read_text(encoding="utf-8"))
    args.output.parent.mkdir(parents=True, exist_ok=True)
    render(content, args.output, args.logo)
