# 📚 二月无雪书源发布页（Legado 阅读）

免服务器的书源发布页：**七猫 × 番茄小说详情页美化风格**，支持分组展示、一键导入、二维码、搜索。

## ✨ 功能

- 6 大分组：**小说源 / 起飞源 / 听书源 / 漫画源 / 视频源 / 综合源**
- 一键导入（legado://import/bookSource?src=... 深链，自动唤起阅读 App）
- 网络导入地址 + 二维码（手机扫码直接导入）
- 全站搜索（按名称 / 网址 / 分组）
- 移动端优先，适配桌面端
- 纯静态，无需服务器 / 数据库

## 📁 目录结构

```
发布页/
├── index.html            # 发布页主体（单文件，样式脚本内联）
├── assets/
│   └── qrcode.min.js     # 二维码生成库（本地引用，无外链）
├── sources/
│   ├── 小说源.json
│   ├── 起飞源.json
│   ├── 听书源.json
│   ├── 漫画源.json
│   ├── 视频源.json
│   ├── 综合源.json
│   └── 全部书源.json     # 全部合集（用于“一键导入全部”）
└── README.md
```

## 🚀 部署（免费，任选一种）

### 1. GitHub Pages（推荐）

1. 新建仓库（如 `shuyuan`），把 `发布页/` 内所有文件推到仓库根目录；
2. 仓库 Settings → Pages → Source 选 `Deploy from a branch` → `main` 分支根目录；
3. 等 1~2 分钟，访问 `https://<用户名>.github.io/shuyuan/` 即可。

### 2. Gitee Pages（国内快）

推送到 Gitee 仓库后，在「服务 → Gitee Pages」开启（需实名认证，改版后需人工审核）。

### 3. Cloudflare Pages / Netlify / Vercel

直接拖拽 `发布页/` 文件夹上传，或关联 Git 仓库自动部署，均可免费绑定自定义域名。

### 4. 只分享链接（不想做页面）

把 `sources/` 里的 JSON 推到 GitHub 仓库，然后用 jsDelivr 加速：

```
https://cdn.jsdelivr.net/gh/<用户名>/<仓库名>@main/<分组>.json
```

在阅读 App → 我的 → 书源管理 → 右上角 ⋮ → 网络导入，粘贴该地址即可。

## 🔧 更新书源

1. 把新的书源 JSON 文件放到工作区 `D:\桌面\书源制作合集\`（或 `书源\` 子目录）；
2. 按分组调整 `sources/` 内对应 JSON（保持为书源数组格式）；
3. 重新 `git push`，GitHub Pages 自动生效（jsDelivr 需刷新缓存：`https://purge.jsdelivr.net/gh/用户名/仓库@main/分组.json`）。

## ⚠️ 说明

- 部分书源含成人（🔞）内容，请自行甄别；
- 一键导入深链仅在已安装阅读 App 的手机上有效；
- `index.html` 通过相对路径自动计算当前部署地址，改域名 / 路径无需改代码。
