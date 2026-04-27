# 个人主页

基于 [Hugo](https://gohugo.io) 构建的个人简历主页，内容与样式分离——所有个人信息均存放在 `data/` 目录的 YAML 文件中，无需修改代码即可更新内容。

**在线地址：** https://mahanxin.github.io/my-homepage/

---

## 目录结构

```
my-homepage/
├── data/                   # 所有个人信息（只需改这里）
│   ├── profile.yaml        # 基本信息、头像、联系方式
│   ├── experience.yaml     # 工作经历
│   ├── projects.yaml       # 项目经历
│   └── education.yaml      # 教育背景
├── static/
│   ├── images/             # 头像等图片
│   └── videos/             # 项目演示视频
├── scripts/
│   └── gen_resume_pdf.py   # PDF 简历生成脚本
├── layouts/                # 页面模板（一般无需修改）
└── hugo.yaml               # Hugo 配置
```

---

## 修改个人信息

### 基本信息 `data/profile.yaml`

```yaml
name: 马汉新
title: 高级算法工程师
bio: 一句话介绍自己

avatar: /images/avatar.jpg   # 头像路径，图片放在 static/images/

age: 32
gender: 男
location: 北京市

contacts:
  - icon: "✉"
    label: "your@email.com"
    href: "mailto:your@email.com"
  - icon: "📱"
    label: "138xxxxxxxx"
    href: "tel:138xxxxxxxx"
```

### 工作经历 `data/experience.yaml`

```yaml
items:
  - company: 公司名称
    position: 职位名称
    period: 2022.04 — 至今
    tags: [技术标签1, 技术标签2]
    highlights:
      # 普通条目
      - text: 工作描述一句话

      # 带子项的条目
      - text: 主要职责描述
        sub:
          - 子项说明 A
          - 子项说明 B
```

### 项目经历 `data/projects.yaml`

```yaml
items:
  - name: 项目名称
    period: 2024.01 — 2024.06
    desc: 项目一句话描述
    achievements:
      - 成果描述 A
      - 成果描述 B
    tags: [技术1, 技术2]
    video: /videos/demo.mp4   # 可选，视频放在 static/videos/
```

### 教育背景 `data/education.yaml`

```yaml
items:
  - school: 学校名称
    degree: 专业 · 学历
    period: 2017.09 — 2020.06
    desc: 补充说明（可留空 ""）
```

---

## 更换头像

1. 将照片放入 `static/images/`，建议分辨率 320px 以上
2. 修改 `data/profile.yaml` 中的 `avatar` 字段：
   ```yaml
   avatar: /images/你的照片.jpg
   ```

> **提示：** 若原图较大（>1MB），可用以下命令压缩：
> ```bash
> ffmpeg -i static/images/原图.jpg -vf "scale=320:-1" -q:v 2 static/images/avatar.jpg
> ```

---

## 添加/处理视频

将视频放入 `static/videos/`，在 `projects.yaml` 中通过 `video:` 字段引用。

**建议先压缩视频再上传（720p，控制在 5MB 以内）：**

```bash
# 压缩视频（原始 → 720p web 版）
ffmpeg -i static/videos/原视频.mp4 \
  -vf "scale=1280:720" -c:v libx264 -crf 26 -preset medium \
  -c:a aac -b:a 96k -movflags +faststart \
  static/videos/输出视频.mp4

# 加速并添加倍速标注（如 2x）
ffmpeg -i static/videos/原视频.mp4 \
  -filter_complex "[0:v]setpts=PTS/2,drawtext=text='2X':fontsize=48:fontcolor=white:borderw=3:bordercolor=black:x=w-tw-20:y=20[v];[0:a]atempo=2.0[a]" \
  -map "[v]" -map "[a]" -c:v libx264 -crf 26 -preset medium \
  static/videos/输出视频_2x.mp4

# 拼接两段视频
ffmpeg -i static/videos/视频1.mp4 -i static/videos/视频2.mp4 \
  -filter_complex "[0:v][1:v]concat=n=2:v=1:a=0[v];[0:a][1:a]concat=n=2:v=0:a=1[a]" \
  -map "[v]" -map "[a]" -c:v libx264 -crf 26 -preset medium \
  static/videos/合并视频.mp4
```

---

## 生成 PDF 简历

脚本自动读取 `data/` 目录下所有 YAML 数据，生成 A4 格式 PDF。

**依赖安装（首次使用）：**

```bash
pip3 install weasyprint pyyaml
```

**生成简历：**

```bash
python3 scripts/gen_resume_pdf.py
```

输出文件：`马汉新_简历.pdf`（项目根目录）

> 每次修改 `data/` 中的内容后，重新执行上述命令即可同步更新 PDF。

---

## 本地预览

```bash
# 安装 Hugo（如未安装）
# macOS:   brew install hugo
# Linux:   snap install hugo

# 启动本地开发服务器
hugo server

# 浏览器访问
open http://localhost:1313
```

---

## 发布到 GitHub Pages

项目已配置 GitHub Actions 自动部署，每次推送 `master` 分支后自动构建发布。

```bash
# 修改内容后提交推送即可
git add .
git commit -m "update: 更新简历内容"
git push origin master
```

约 1-2 分钟后，访问 https://mahanxin.github.io/my-homepage/ 查看更新效果。

> **首次部署：** 需在 GitHub 仓库 Settings → Pages → Source 中选择 **GitHub Actions**。
