#!/usr/bin/env python3
import json
import re
from pathlib import Path

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
    all_count = len(json.loads((ROOT / "sources" / "all.json").read_text(encoding="utf-8")))
    subscription = {
        "sourceName": "书源发布",
        "sourceUrl": BASE_URL,
        "sourceGroup": "书源发布",
        "sourceIcon": BASE_URL + "assets/icon.png",
        "enabled": True,
        "enabledCookieJar": False,
        "customOrder": 0,
        "lastUpdateTime": 0,
        "loadWithBaseUrl": True,
        "articleStyle": 0,
        "singleUrl": True,
        "bookSourceComment": f"更新时间：{build_date}；共 {all_count} 个书源。",
    }
    output = ROOT / "subscription.json"
    output.write_text(
        json.dumps([subscription], ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    print(f"已生成单 URL 订阅源：更新时间 {build_date}，共 {all_count} 个书源")


if __name__ == "__main__":
    generate()
