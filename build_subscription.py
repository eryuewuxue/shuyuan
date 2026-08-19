#!/usr/bin/env python3
import json
import re
from pathlib import Path
from urllib.parse import quote

ROOT = Path(__file__).resolve().parent
BASE_URL = "https://eryuewuxue.github.io/shuyuan/"
GROUPS = [
    ("小说源", "novel"),
    ("漫画源", "comic"),
    ("听书源", "audio"),
    ("视频源", "video"),
    ("福利源", "adult"),
]


def read_build_date():
    html = (ROOT / "index.html").read_text(encoding="utf-8")
    match = re.search(r'var BUILD_DATE = "([^"]+)"', html)
    if not match:
        raise RuntimeError("index.html 中未找到 BUILD_DATE")
    return match.group(1)


def generate():
    build_date = read_build_date()
    entries = [
        {
            "title": "二月无雪书源发布页",
            "link": BASE_URL,
            "description": "打开发布页，查看全部书源与导入入口。",
        }
    ]
    for name, key in GROUPS:
        data = json.loads((ROOT / "sources" / f"{key}.json").read_text(encoding="utf-8"))
        entries.append(
            {
                "title": f"{name}（{len(data)} 个）",
                "link": BASE_URL + quote(f"sources/{key}.json"),
                "description": f"网络导入二月无雪{name}，共 {len(data)} 个。",
            }
        )
    all_count = len(json.loads((ROOT / "sources" / "all.json").read_text(encoding="utf-8")))
    entries.append(
        {
            "title": f"全部书源（{all_count} 个）",
            "link": BASE_URL + "sources/all.json",
            "description": f"网络导入二月无雪全部书源，共 {all_count} 个。",
        }
    )

    subscription = {
        "sourceName": "书源发布",
        "sourceUrl": BASE_URL + "subscription.json",
        "sourceGroup": "书源发布",
        "sourceIcon": BASE_URL + "assets/icon.png",
        "enabled": True,
        "enabledCookieJar": False,
        "customOrder": 0,
        "lastUpdateTime": 0,
        "loadWithBaseUrl": True,
        "articleStyle": 0,
        "singleUrl": True,
        "sortUrl": f"更新列表::{BASE_URL}subscription.html",
        "headerMap": {},
        "loginUrl": "",
        "bookSourceComment": f"更新时间：{build_date}；共 {all_count} 个书源。",
        "ruleArticles": "class.article",
        "ruleTitle": "tag.h2@text",
        "ruleLink": "tag.a@href",
        "rulePubDate": "class.pub-date@text",
        "ruleDescription": "class.description@text",
        "ruleContent": "id.content@html",
    }
    output = ROOT / "subscription.json"
    output.write_text(
        json.dumps([subscription], ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
        newline="\n",
    )

    articles = []
    for entry in entries:
        articles.append(
            "      <article>"
            f'<h2><a href="{entry["link"]}">{entry["title"]}</a></h2>'
            f'<p class="pub-date">{build_date}</p>'
            f'<p class="description">{entry["description"]}</p>'
            "</article>"
        )
    html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head><meta charset="UTF-8"><title>二月无雪书源更新</title></head>
<body><main id="content">
<h1>二月无雪书源更新</h1>
<p>最近更新时间：{build_date}，共 {all_count} 个书源。</p>
{chr(10).join(articles)}
</main></body></html>
"""
    page = ROOT / "subscription.html"
    page.write_text(html, encoding="utf-8", newline="\n")
    print(f"已生成 subscription.json / subscription.html：更新时间 {build_date}，共 {all_count} 个书源")


if __name__ == "__main__":
    generate()
