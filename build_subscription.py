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
    subscription = {
        "sourceName": "二月无雪书源更新",
        "sourceUrl": BASE_URL + "subscription.json",
        "sourceGroup": "书源发布",
        "sourceComment": f"更新时间：{build_date}；订阅本源后可快速进入发布页并导入各分组书源。",
        "enabled": True,
        "enabledCookieJar": False,
        "customOrder": 0,
        "lastUpdateTime": 0,
        "concurrentRate": "",
        "headerMap": {},
        "loginUrl": "",
        "bookSourceComment": "",
        "ruleArticles": {
            "sourceRegex": ".*",
            "searchUrl": "/search?wd={{key}}",
            "articles": {
                "articleList": "class.book-list@tag.article",
                "articleTitle": "class.title@text",
                "articleUrl": "class.title@href",
                "articleDate": "",
            },
            "detail": {
                "content": "id.content@html",
                "nextPageUrl": "",
            },
        },
        "ruleExplore": {},
        "exploreUrl": BASE_URL,
        "searchUrl": BASE_URL,
        "ruleSearch": {},
    }
    items = [
        {
            "title": "二月无雪书源发布页",
            "url": BASE_URL,
            "group": "发布页",
            "description": "打开书源发布页，查看全部书源与导入入口。",
        }
    ]
    for name, key in GROUPS:
        data = json.loads((ROOT / "sources" / f"{key}.json").read_text(encoding="utf-8"))
        items.append(
            {
                "title": f"{name}（{len(data)} 个）",
                "url": BASE_URL + quote(f"sources/{key}.json"),
                "group": "书源导入",
                "description": f"网络导入二月无雪{name}，共 {len(data)} 个。",
            }
        )
    all_count = sum(len(items) - 1 for _ in [0])
    all_count = len(json.loads((ROOT / "sources" / "all.json").read_text(encoding="utf-8")))
    items.append(
        {
            "title": f"全部书源（{all_count} 个）",
            "url": BASE_URL + "sources/all.json",
            "group": "书源导入",
            "description": f"网络导入二月无雪全部书源，共 {all_count} 个。",
        }
    )
    subscription["items"] = items
    subscription["articles"] = items
    output = ROOT / "subscription.json"
    output.write_text(
        json.dumps([subscription], ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    print(f"已生成 subscription.json：更新时间 {build_date}，共 {all_count} 个书源")

if __name__ == "__main__":
    generate()
