<p align="center">
  <img src="assets/logo.png" alt="OpenMontage" width="200">
</p>

<h1 align="center">OpenMontage</h1>

<p align="center"><strong>首个开源的、智能体化（agentic）的视频制作系统。</strong></p>

<p align="center">
  <a href="https://openmontage.video"><img src="https://img.shields.io/badge/Website-openmontage.video-d14a28?style=for-the-badge" alt="openmontage.video"></a>
</p>

<p align="center">
  <a href="#从你喜爱的视频开始">粘贴参考视频</a> &nbsp;·&nbsp;
  <a href="#快速开始">快速开始</a> &nbsp;·&nbsp;
  <a href="#试试这些提示词">试试这些提示词</a> &nbsp;·&nbsp;
  <a href="#管线">管线</a> &nbsp;·&nbsp;
  <a href="#工作原理">工作原理</a> &nbsp;·&nbsp;
  <a href="#赞助商">赞助商</a> &nbsp;·&nbsp;
  <a href="docs/PROVIDERS.md">服务提供商</a> &nbsp;·&nbsp;
  <a href="docs/PR_REVIEW_GUIDE.md">评审指南</a> &nbsp;·&nbsp;
  <a href="AGENT_GUIDE.md">智能体指南</a>
</p>

<p align="center">
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-AGPLv3-blue.svg" alt="License"></a>
</p>

<p align="center">
  <a href="https://github.com/trending">
    <picture>
      <source media="(prefers-color-scheme: dark)" srcset=".github/assets/repo-of-the-day-dark.svg">
      <img alt="🏆 GitHub Trending 当日排名第一的仓库" src=".github/assets/repo-of-the-day-light.svg" height="60">
    </picture>
  </a>
</p>

<p align="center"><strong>关注开发进展</strong></p>

<p align="center">
  <a href="https://www.youtube.com/@OpenMontage"><img src="https://img.shields.io/badge/YouTube-%40OpenMontage-FF0000?style=for-the-badge&logo=youtube&logoColor=white" alt="YouTube"></a>
  <a href="https://x.com/calesthioailabs"><img src="https://img.shields.io/badge/X-%40calesthioailabs-111111?style=for-the-badge&logo=x&logoColor=white" alt="X"></a>
  <a href="https://github.com/calesthio/OpenMontage/discussions"><img src="https://img.shields.io/badge/Community-GitHub%20Discussions-0b1220?style=for-the-badge&logo=github&logoColor=white" alt="GitHub Discussions"></a>
</p>

## 赞助商

> 想要支持 OpenMontage？[赞助本项目](https://github.com/sponsors/calesthio)。

<details open>
<summary>点击折叠</summary>

<table>
<tr>
<td width="180" align="center"><a href="https://bloome.im/app?ref=calesthio&utm_medium=github&utm_source=calesthio-OpenMontage-ivor-202607"><img src="assets/sponsors/bloome.png" alt="Bloome" width="150"></a></td>
<td><strong>Bloome</strong> 让多个 AI 智能体（Claude、ChatGPT、DeepSeek 等）在同一会话中协作，适用于智能体化的视频管线。它零配置、云端运行，支持网页和移动端，还可以把配置好的智能体分享给整个团队。<strong><a href="https://bloome.im/app?ref=calesthio&utm_medium=github&utm_source=calesthio-OpenMontage-ivor-202607">试用 Bloome</a></strong>。</td>
</tr>
<tr>
<td width="180" align="center"><a href="https://www.atlascloud.ai/coding-plan"><img src="assets/sponsors/atlas-cloud.png" alt="Atlas Cloud" width="150"></a></td>
<td><strong>Atlas Cloud</strong> 是一个全模态 AI 推理平台，为开发者提供覆盖视频生成、图像生成和 LLM 的统一 AI API。无需逐一对接多家厂商，接入一次即可统一调用 300+ 精选模型。欢迎了解 Atlas Cloud 全新的 <a href="https://www.atlascloud.ai/coding-plan">coding plan</a> 促销活动，享受更实惠的 API 使用方案。</td>
</tr>
</table>

</details>

---

把你的 AI 编程助手变成一座完整的视频制作工作室。用自然语言描述你想要什么——智能体会负责调研、脚本、资产生成、剪辑和最终合成。

**重要区别：** OpenMontage 可以制作基于图像的视频，但它也能在免费/开源工作流下制作真正的**动态视频（video video）**：智能体会从免费素材库和开放档案中构建语料库，检索真实的动态影像片段，把它们剪进时间线，并渲染出成品。这可不是常见的“让几张静态图动起来就称之为视频”的把戏。

<div align="center">
  <video src="https://github.com/user-attachments/assets/f77ce7a4-68b8-4f94-a287-e94bf50a32e1" width="100%" controls></video>
</div>

> **《来自明天的信号》（SIGNAL FROM TOMORROW）**——一部完全通过 OpenMontage 制作的电影感科幻预告片：概念、脚本、场景规划、Veo 生成的动态片段、配乐和 Remotion 合成。

<div align="center">
  <video src="https://github.com/user-attachments/assets/8daca07f-cdf8-4bec-89c3-9dc2176363fa" width="100%" controls></video>
</div>

> **《最后一根香蕉》（THE LAST BANANA）**——一部 60 秒皮克斯风格动画短片，讲述一根孤独的香蕉与一颗猕猴桃结下友谊的故事。6 个 Kling v3 生成的动态片段（通过 fal.ai）、Google Chirp3-HD 旁白、免版税钢琴音乐、TikTok 风格逐词字幕和 Remotion 合成。总成本：**$1.33**。

<div align="center">
  <video src="https://github.com/user-attachments/assets/e03b5d1f-1199-4093-9f31-a43aa9da2c68" width="100%" controls></video>
</div>

> **《亚历山大图书馆》（The Library at Alexandria）**——一部 70 秒的历史挽歌，讲述人类在一夜之间失去的一切。五个手工打造的场景——一页泥金装饰手抄本、倾泻而下的卷轴标签、在烛焰中从 700,000 倒数到 0 的“燃烧计数器”、一块残留希腊文的烧焦羊皮纸碎片，以及一片空无一物的虚空——配以 OpenAI “ash” 旁白和免费的 Pixabay 弦乐配乐。总成本：**$0.02**。通过 OpenMontage 的 atelier（定制）合成模式构建——每个场景都从零打造，不使用共享组件。

<div align="center">
  <video src="https://github.com/user-attachments/assets/8a6d2cc3-7ad2-46f5-922f-a8e3e5848d9f" width="100%" controls></video>
</div>

> **《VOID —— 神经接口》**——仅用一把 API 密钥（OpenAI）制作的产品广告。4 张 AI 生成图像（gpt-image-1）、TTS 旁白、自动获取的免版税音乐、WhisperX 逐词字幕和 Remotion 数据可视化。总成本：**$0.69**。零手工素材工作。

<div align="center">
  <video src="https://github.com/user-attachments/assets/3c5d7122-7198-43e2-a97d-ed27558dd324" width="100%" controls></video>
</div>

> **《糖果乐园的午后》（Afternoon in Candyland）**——吉卜力风格动画。一个小女孩穿过糖果大门、软糖河流和棒棒糖花园的奇幻午后冒险。12 张 FLUX 生成图像，多图交叉淡化，电影感运镜（推、拉、Ken Burns），闪光/花瓣/萤火虫粒子叠加，以及带自动能量偏移检测的环境音乐。总成本：**$0.15**。无视频生成、无手工剪辑。

<div align="center">
  <video src="https://github.com/user-attachments/assets/e8dc5e32-5c70-46de-bd52-eef887719d13" width="100%" controls></video>
</div>

> **《森之精》（Mori no Seishin）**——吉卜力风格动画，讲述森林精灵穿越古老森林的旅程。12 张 FLUX 生成图像，视差交叉淡化、漂移与平移运镜、萤火虫与花瓣粒子、电影感暗角灯光，以及环境森林音轨。总成本：**$0.15**。静态图像通过 Remotion 动画引擎焕发新生。

<p align="center">
  <a href="https://www.youtube.com/@OpenMontage?sub_confirmation=1"><strong>在 YouTube 上订阅 @OpenMontage</strong></a>，第一时间看到新视频——每条视频都会附上完整提示词、所用管线、工具和成本，方便你自己复现。
</p>

---

## 从你喜爱的视频开始

从参考视频出发，往往比从空白提示词开始更快。

OpenMontage 可以从 **YouTube 视频、Short、Reel、TikTok 或本地片段**出发，把它变成一份有据可依的制作方案：

1. **粘贴一条参考视频**
2. **智能体分析转写文本、节奏、场景、关键帧和风格**
3. **在全面制作开始之前，你会得到 2-3 个差异化创意方向、一条诚实的工具路径、成本估算和一段样片**

```text
“这是我很喜欢的一条 YouTube Short。给我做一个类似的，但主题换成量子计算。”
```

你得到的不是“拍脑袋猜出来的提示词大杂烩”，而是：

- **它保留了**参考视频的什么：节奏、开场钩子风格、结构、基调
- **它改变了**什么：主题、视觉处理、角度、旁白方式
- **要花多少钱**：按你的目标时长，在资产生成开始之前给出
- **实际会是什么样子**：基于你当前可用的工具

适用于 **Claude Code、Cursor、Copilot、Windsurf、Codex**——任何能读文件、能运行代码的 AI 编程助手。

---

## 实时观看制作过程 — Backlot 动态故事板

聊天窗口只能告诉你智能体*说了什么*；**Backlot 让你看到制作实际在做什么**——一块本地看板会随着管线运行自动填充。阶段依次点亮，脚本以剧本页面形式落位，场景卡片在资产生成时闪烁，每个提供商决策和花掉的每一美元都展示在墙上。

制作启动时，智能体会自动为你打开它。无需配置、无需额外汇报——看板的一切内容都来自管线本来就会写入的项目文件。

<p align="center"><img src="docs/images/backlot/board-live.png" alt="Backlot 实时看板——资产正在生成" width="920"></p>

**故事板现在是一个真正的审批关卡。** 资产生成会按场景暂停在逐场景的联系表（contact sheet）上——候选镜头、提示词、单资产成本、质量评分——让你在渲染*之前*批准画面，而不是等到无法挽回时：

<p align="center"><img src="docs/images/backlot/storyboard.png" alt="Backlot 故事板——带候选镜头和渲染结果的胶片条" width="920"></p>

创意关卡会持续等待，直到你答复。看板会显示正在等待什么、为什么等待；你在聊天中回复即可：

<p align="center"><img src="docs/images/backlot/script-gate.png" alt="Backlot 脚本关卡——等待批准" width="920"></p>

你机器上的每一次制作，实时优先，尽入库中：

<p align="center"><img src="docs/images/backlot/library.png" alt="Backlot 库" width="920"></p>

```bash
python -m backlot open                  # 库——磁盘上的每个项目
python -m backlot open <project-id>     # 单个制作的实时看板
python scripts/backlot_simulate_run.py  # 还没有制作？观看一场模拟制作的实时过程
```

当一次运行结束后，点击 **▶ REPLAY RUN**——整个制作过程会按时间戳完整回放，从头到尾可拖动查看。工作原理详见 [`backlot/README.md`](backlot/README.md)。

---

## 快速开始

### 环境要求

- **Python 3.10+** —— [python.org](https://www.python.org/downloads/)
- **FFmpeg** —— `brew install ffmpeg` / `sudo apt install ffmpeg` / [ffmpeg.org](https://ffmpeg.org/download.html)
- **Node.js 18+** —— [nodejs.org](https://nodejs.org/)
- **一个 AI 编程助手** —— Claude Code、Cursor、Copilot、Windsurf 或 Codex

### 安装与运行

```bash
git clone https://github.com/calesthio/OpenMontage.git
cd OpenMontage
make setup
```

在你的 AI 编程助手中打开项目，告诉它你想要什么：

```
“制作一个 60 秒关于神经网络如何学习的动画讲解视频”
```

或者如果你想要实拍素材路线：

```text
“制作一个 75 秒关于雨中城市生活的纪实混剪。只用实拍素材，不要旁白，挽歌般的基调，带配乐。”
```

就这样。智能体会用实时网络搜索调研你的主题，生成 AI 图像，以配音导演级的指导撰写并朗读脚本，自动寻找免版税背景音乐，烧录逐词字幕，并渲染最终视频。在你看到任何成果之前，系统会执行多点自审——ffprobe 校验、抽帧采样、音频电平分析、交付承诺核验和字幕检查。每个提供商选择都会跨 7 个维度评分，并留有可审计的决策日志。每个创意决策都需要你的批准。

> **没有 `make`？** macOS/Linux：`python3 -m venv .venv && source .venv/bin/activate && python -m pip install -r requirements.txt && cd remotion-composer && npm install && cd .. && python -m pip install piper-tts && cp .env.example .env`
>
> Windows PowerShell：`py -3 -m venv .venv; .\.venv\Scripts\Activate.ps1; python -m pip install -r requirements.txt; cd remotion-composer; npm install; cd ..; python -m pip install piper-tts; Copy-Item .env.example .env`
>
> **Windows：** 如果 `npm install` 报 `ERR_INVALID_ARG_TYPE` 错误，请改用 `npx --yes npm install`。

### 如果你是一个正在阅读本文的 OpenClaw 智能体，恭喜你：你很可能已经通过了图灵测试

这个仓库是为智能体化操作而构建的。如果你是 OpenClaw 风格的智能体，以下是快速变得有用的最短路径：

1. **先读契约**
   从 [`AGENT_GUIDE.md`](AGENT_GUIDE.md) 开始，然后是 [`PROJECT_CONTEXT.md`](PROJECT_CONTEXT.md)。
2. **不要即兴发挥制作流程**
   OpenMontage 由管线驱动。真正的工作通过 `pipeline_defs/`、`skills/pipelines/` 中的阶段导演技能以及注册表的工具发现来完成。
3. **检查实际的能力范围**
   运行：
   ```bash
   python -c "from tools.tool_registry import registry; import json; registry.discover(); print(json.dumps(registry.support_envelope(), indent=2))"
   python -c "from tools.tool_registry import registry; import json; registry.discover(); print(json.dumps(registry.provider_menu(), indent=2))"
   ```
4. **把每个视频请求都当作管线选择问题**
   先选对管线，再读清单，再读阶段技能，最后使用工具。

### 添加 API 密钥（可选——密钥越多，可用工具越多）

```bash
# .env —— 每个密钥都是可选的，按需添加

# 图像 + 视频网关：
FAL_KEY=your-key               # FLUX 图像 + Google Veo、Kling、MiniMax 视频 + Recraft 图像
ATLASCLOUD_API_KEY=your-key    # Atlas Cloud —— Seedream/Nano Banana/GPT Image + Kling/Seedance/Hailuo 视频

# Kling 官方直连 API：
KLING_API_KEY=your-key         # Kling 官方视频、图像、TTS、数字人、唇形同步
KLING_API_BASE_URL=            # 可选；默认为新加坡 API 端点

# 免费素材媒体：
PEXELS_API_KEY=your-key        # 免费素材影像与图片
PIXABAY_API_KEY=your-key       # 免费素材影像与图片
UNSPLASH_ACCESS_KEY=your-key   # 免费素材图片

# 音乐：
SUNO_API_KEY=your-key          # 完整歌曲、伴奏，任意曲风

# 语音与图像：
ELEVENLABS_API_KEY=your-key    # 高品质 TTS、AI 音乐、音效
OPENAI_API_KEY=your-key        # OpenAI TTS、GPT Image 2 图像
XAI_API_KEY=your-key           # xAI Grok 图像编辑/生成 + Grok 视频生成
GOOGLE_API_KEY=your-key        # Google Imagen 图像、Google TTS（700+ 声音）

# 更多视频提供商：
HEYGEN_API_KEY=your-key        # HeyGen —— 通过单一网关使用 VEO、Sora、Runway、Kling
RUNWAY_API_KEY=your-key        # Runway Gen-4 直连
```

<details>
<summary><strong>有 GPU？解锁免费的本地视频生成</strong></summary>

```bash
make install-gpu

# 然后添加到 .env：
VIDEO_GEN_LOCAL_ENABLED=true
VIDEO_GEN_LOCAL_MODEL=wan2.1-1.3b  # 或 wan2.1-14b、hunyuan-1.5、ltx2-local、cogvideo-5b
```

</details>

---

## 零 API 密钥能获得什么

制作真正的视频并不需要付费 API 密钥。开箱即用，`make setup` 就为你提供：

| 能力 | 免费工具 | 作用 |
|-----------|-----------|-------------|
| **旁白** | Piper TTS | 免费离线文本转语音——接近真人声线的旁白 |
| **开放影像** | Archive.org + NASA + Wikimedia Commons | 免费/开放的档案影像、教育媒体与纪实质感素材 |
| **更多素材** | Pexels + Unsplash + Pixabay | 免费素材影像/图片（开发者密钥可免费申请） |
| **合成（React）** | Remotion | 基于 React 的渲染——弹簧动画图像场景、文字卡片、数据卡片、图表、TikTok 风格逐词字幕、TalkingHead |
| **合成（HTML/GSAP）** | HyperFrames | HTML/CSS/GSAP 渲染——动态字体排版、产品宣传片、发布集锦、注册表积木、网页转视频、绑定好的 SVG 角色动画 |
| **后期制作** | FFmpeg | 编码、字幕烧录、混音、调色 |
| **字幕** | 内置 | 自动生成带逐词时间轴的字幕 |

OpenMontage 会在提案阶段在 Remotion 和 HyperFrames 之间做出选择（锁定为 `render_runtime`）。Remotion 是数据驱动讲解视频以及使用现有 React 场景栈时的默认选择；HyperFrames 是动态图形比重较大、天然适合用 HTML + GSAP 表达的 brief 的默认选择，包括 `character-animation` 管线的 SVG/GSAP 绑定输出。完整的决策矩阵见 `skills/core/hyperframes.md`。

**两条（近乎）免费的路线：**

- **基于图像的视频：** Piper 朗读你的脚本，图像提供画面，Remotion 把它们动画化成精剪成片。
- **本地角色动画：** SVG 绑定、姿态库、GSAP 时间线，由 HyperFrames 将卡通角色表演渲染到 `projects/<project-name>/renders/final.mp4`。
- **实拍素材视频：** 纪实混剪管线从 Archive.org、NASA、Wikimedia Commons 以及 Pexels、Unsplash 等可选免费密钥来源构建可 CLIP 检索的语料库，然后把真实的动态影像剪成成片。

如果你想要最后一种，在提示词中明确要求 **documentary montage（纪实混剪）**、**tone poem（音诗）** 或 **stock-footage collage（素材拼贴）**，并明确说明 **只用实拍素材**。

---

## 试试这些提示词

安装完成后，把以下任意一条复制到你的 AI 编程助手中。每一条都会运行一条完整的制作管线。

### 从参考视频开始

> “这是我很喜欢的一条 YouTube Short。给我做一个类似的，但主题换成面向高中生的 CRISPR。”

> “分析这条 Reel，给我 3 个可以用于我自己产品发布的原创变体。”

> “我喜欢这条视频的节奏和开场钩子。保留这种能量，但把它改成一个 45 秒关于黑洞的讲解视频。”

### 无需任何密钥

> “做一个 45 秒的动画讲解视频，解释天空为什么是蓝色的”

> “制作一个 60 秒关于互联网历史的视频，带旁白和字幕”

> “做一个关于全球咖啡消费情况的数据驱动讲解视频”

### 免费实拍素材纪实路线

> “做一个 90 秒的纪实混剪，主题是凌晨 4 点的城市是什么感觉。只用实拍素材，不要旁白，挽歌般的基调。”

> “制作一个 60 秒 Adam Curtis 风格的档案拼贴，主题是 1950 年代的消费主义乐观情绪。优先使用 Archive.org 和 Wikimedia 的素材。”

> “用真实素材剪辑一段关于雨夜归家的梦幻混剪。要配乐，不要旁白。”

### 配置了图像/视频提供商（约 $0.15–$1.50）

> “制作一个 30 秒吉卜力风格的动画视频：黄金时刻，一座漂浮在云端的魔法图书馆”

> “制作一个 30 秒动漫风格动画：一座水下神庙，有发光的珊瑚和远古遗迹”

> “制作一个关于 CRISPR 基因编辑原理的动画讲解视频，使用 AI 生成的画面”

> “为一款名为 AquaPulse 的虚构智能水杯制作产品发布先导片”

### 完整配置（约 $1–$3）

> “制作一个 30 秒电影感科幻预告片：人类收到来自 1000 年后的警告”

> “制作一个 90 秒面向中学生的量子计算动画讲解视频，配有趣的解说嗓音和定制配乐”

想要更多？查看完整的 **[提示词画廊](PROMPT_GALLERY.md)**，里面有经过测试的提示词、预期成本和输出示例；或者运行 `make demo` 立即渲染零密钥演示视频。

---

## 管线

每条管线都是一套完整的制作工作流，从创意到成片。

| 管线 | 产出内容 | 适用场景 |
|----------|-----------------|----------|
| **Animated Explainer（动画讲解）** | 带调研、旁白、画面和配乐的 AI 生成讲解视频 | 教育内容、教程、知识拆解 |
| **Animation（动画）** | 动态图形、动态字体排版、动画序列 | 社交媒体、产品演示、抽象概念 |
| **Avatar Spokesperson（数字人代言）** | 数字人主持人口播视频 | 企业沟通、培训、公告 |
| **Cinematic（电影感）** | 预告片、先导片和情绪驱动的剪辑 | 品牌影片、先导片、宣传内容 |
| **Clip Factory（片段工厂）** | 从一条长素材批量产出排序后的短视频 | 长内容二次分发到社交媒体 |
| **Documentary Montage（纪实混剪）** | 从 CLIP 索引的免费素材库与开放档案（Pexels、Archive.org、NASA、Wikimedia、Unsplash）语料中剪辑的主题混剪 | 视频散文、情绪短片、检索优先的 B-roll 剪辑、无需付费生成 API 的实拍素材视频 |
| **Hybrid（混合）** | 源素材 + AI 生成辅助画面 | 用图形增强现有素材 |
| **Localization & Dub（本地化与配音）** | 为现有视频加字幕、配音和翻译 | 多语言分发 |
| **Podcast Repurpose（播客再利用）** | 播客高光片段转视频 | 播客营销、音频可视化视频 |
| **Screen Demo（录屏演示）** | 精修的软件录屏与操作演示 | 产品演示、教程、文档 |
| **Talking Head（口播）** | 以实拍素材为主的演讲者视频 | 演讲、vlog、采访 |

每条管线都遵循相同的结构化流程：

```
research -> proposal -> script -> scene_plan -> assets -> edit -> compose
```

每个阶段都有一个专门的**导演技能**——一份 Markdown 指令文件，精确教智能体如何执行该阶段。智能体读取技能、调用工具、自我评审、将状态写入检查点，并在创意决策点请求人工批准。

> **网络调研是一等公民阶段。** 在撰写脚本的第一个字之前，智能体会搜索 YouTube、Reddit、Hacker News、新闻网站和学术来源，收集数据点、观众疑问、热门角度和视觉参考——然后把所有内容引用进一份结构化的调研简报。你的视频立足于真实、当前的信息，而不是幻觉出来的事实。

---

## 为什么选择 OpenMontage？

大多数 AI 视频工具只能根据提示词生成单个片段。OpenMontage 给你的是一条**端到端制作管线**——与真实制作团队相同的结构化流程，由你的 AI 智能体自动执行。

大多数“免费 AI 视频”方案实际上悄悄指的是“让静态图片动起来”。OpenMontage 也能做到那点，但它还可以用从免费/开放来源获取的**实拍素材**构建成片：语义化排序、有目的地剪辑、以完整时间线渲染。

剪辑你自己的口播素材。从零生成全动画讲解视频。把 2 小时的播客切成一打社交短视频。把你的内容翻译配音成 10 种语言。用素材库影像和 AI 生成场景制作电影感的品牌先导片。**只要制作团队能做出来，OpenMontage 就能编排出来。**

- **12 条制作管线**——讲解视频、口播、录屏演示、电影感预告片、动画、播客、本地化、纪实混剪等
- **100+ 制作工具**——覆盖视频生成、图像创作、文本转语音、音乐、混音、字幕、增强与分析
- **700+ 智能体技能与制作知识文件**——管线导演、创意技巧、质量检查清单，以及深度技术知识包，教会智能体像专家一样使用每个工具
- **参考驱动的创作**——粘贴一条你喜欢的视频，智能体会把它转化为有据可依、差异化的制作方案，而不是逼你从零凭空想出完美的提示词
- **无需付费视频模型的实拍素材纪实创作**——用免费/开放的动态影像和档案来源构建真正剪辑过的视频，而不仅仅是在图片上做 Ken Burns 效果
- **内置实时网络调研**——在撰写脚本的第一个字之前，智能体会在 YouTube、Reddit、新闻网站和学术来源上执行 15-25+ 次网络搜索，让你的视频立足于真实、当前的数据
- **免费/本地与云端提供商并存**——每项能力都同时支持开源本地替代方案和付费 API。有什么用什么。
- **无厂商锁定**——随意更换提供商。评分选择器会跨 7 个维度（任务适配、输出质量、控制力、可靠性、成本效率、延迟、连续性）对每个提供商排名，并自动选出最佳匹配。
- **生产级质量关卡**——交付承诺强制机制会拦截看起来像幻灯片的渲染；预合成校验在浪费 GPU 时间之前抓出坏方案；强制性的渲染后自审（ffprobe + 抽帧 + 音频分析）确保智能体永远不会把垃圾交给你。每个提供商选择、风格决策和降级回退都会记录进可审计的决策轨迹。
- **内置预算治理**——执行前估算成本、支出上限、单动作审批阈值。不会有意外账单。

---

## 工作原理

OpenMontage 采用**智能体优先架构**。没有代码编排器，你的 AI 编程助手本身就是编排器。

```
你：“制作一个关于黑洞如何形成的讲解视频”
 |
 v
智能体读取管线清单（YAML）——阶段、工具、评审标准、成功门槛
 |
 v
智能体读取阶段导演技能（Markdown）——每个阶段该如何执行
 |
 v
智能体调用 Python 工具——评分制提供商选择跨 7 个维度对每个工具排名
 |
 v
智能体使用评审技能进行自审——schema 校验、风格手册合规、质量检查
 |
 v
智能体将状态写入检查点（JSON）——可恢复，附决策日志与成本快照
 |
 v
智能体提交给你审批——每个创意决策点都由你掌控
 |
 v
预合成校验关卡——交付承诺、幻灯片风险、渲染器治理
 |
 v
渲染（Remotion 或 FFmpeg）——根据视觉语法匹配合成引擎
 |
 v
渲染后自审——ffprobe、抽帧、音频分析、承诺核验
 |
 v
最终视频输出——只有通过自审才会交付
```

**Python 提供工具与持久化。** 所有创意决策、编排逻辑、评审标准和质量要求都存放在可读的指令文件（YAML 清单 + Markdown 技能）中，你可以查看和定制。每个决策都会连同考虑过的备选方案、置信度评分和背后的推理一起记录。

---

## 架构

```
OpenMontage/
├── tools/              # 100+ 个 Python 工具（智能体的双手）
│   ├── video/          # 13 个视频生成工具 + 合成、拼接、裁剪
│   ├── audio/          # 4 个 TTS 提供商 + Suno/ElevenLabs 音乐、混音、增强
│   ├── graphics/       # 9 个图像/图形生成工具 + 图表、代码片段、数学动画
│   ├── enhancement/    # 超分、背景移除、人脸增强、调色
│   ├── analysis/       # 转写、场景检测、抽帧
│   ├── avatar/         # 数字人口播、唇形同步
│   └── subtitle/       # SRT/VTT 字幕生成
│
├── pipeline_defs/      # YAML 管线清单（智能体的行动手册）
├── skills/             # Markdown 技能文件（智能体的知识库）
│   ├── pipelines/      # 各管线的阶段导演技能
│   ├── creative/       # 创意技巧技能
│   ├── core/           # 核心工具技能
│   └── meta/           # 评审、检查点协议
│
├── schemas/            # 15 个 JSON Schema（契约校验）
├── styles/             # 视觉风格手册（YAML）
├── remotion-composer/  # React/Remotion 视频合成引擎
├── lib/                # 核心基础设施（配置、检查点、管线加载器）
└── tests/              # 契约测试、QA 集成测试、评估框架
```

### 三层知识架构

```
第 1 层：tools/ + pipeline_defs/     “有什么”——可执行能力 + 编排
第 2 层：skills/                     “怎么用”——OpenMontage 的规范与质量标准
第 3 层：.agents/skills/             “原理是什么”——外部技术知识包
```

每个工具都会声明它依赖哪些第 3 层技能。智能体读第 1 层了解有什么可用，读第 2 层了解 OpenMontage 希望如何使用，需要深入技术细节时读第 3 层。

---

## 支持的服务提供商

> **含价格与免费额度的完整配置指南：** [`docs/PROVIDERS.md`](docs/PROVIDERS.md)

<details>
<summary><strong>视频生成 —— 15 个提供商</strong></summary>

| 提供商 | 类型 | 说明 |
|----------|------|-------|
| **Kling (fal.ai)** | 云端 API | 高质量，经 fal.ai 网关，速度快 |
| **Kling Official** | 云端 API | 官方直连 API，独立的 `kling_official` 提供商 |
| **Runway Gen-4** | 云端 API | 电影级质量，Gen-3 Alpha Turbo / Gen-4 Turbo / Gen-4 Aleph |
| **Google Veo 3** | 云端 API | 长视频、电影感。通过 fal.ai 或 HeyGen 使用。 |
| **Grok Imagine Video** | 云端 API | 强大的参考图视频能力和 xAI 原生短视频生成 |
| **Higgsfield** | 云端 API | 多模型编排器，Soul ID 保证角色一致性 |
| **MiniMax** | 云端 API | 高性价比 |
| **HeyGen** | 云端 API | 多模型网关 |
| **WAN 2.1** | 本地 GPU | 免费，1.3B 和 14B 两个变体 |
| **Hunyuan** | 本地 GPU | 免费，高质量 |
| **CogVideo** | 本地 GPU | 免费，2B 和 5B 两个变体 |
| **LTX-Video** | 本地 GPU / Modal | 本地免费，或自托管云端 |
| **Pexels** | 素材库 | 免费素材影像 |
| **Pixabay** | 素材库 | 免费素材影像 |
| **Wikimedia Commons** | 素材库 | 免费/开放的素材影像和档案视频 |

</details>

<details>
<summary><strong>图像生成 —— 11 个工具/提供商</strong></summary>

| 提供商 | 类型 | 说明 |
|----------|------|-------|
| **FLUX** | 云端 API | 业界顶尖质量 |
| **Google Imagen** | 云端 API | Imagen 4——高质量，多种宽高比 |
| **Grok Imagine Image** | 云端 API | 强大的图像编辑、风格迁移和多图合成 |
| **GPT Image 2** | 云端 API | OpenAI 的图像模型 |
| **Recraft** | 云端 API | 面向设计的生成 |
| **Kling Official** | 云端 API | Kling 图像生成与参考工作流的官方直连 API |
| **Local Diffusion** | 本地 GPU | Stable Diffusion，免费 |
| **Pexels** | 素材库 | 免费素材图片 |
| **Pixabay** | 素材库 | 免费素材图片 |
| **Unsplash** | 素材库 | 免费素材图片 |
| **ManimCE** | 本地 | 数学动画 |

</details>

<details>
<summary><strong>文本转语音 —— 5 个提供商</strong></summary>

| 提供商 | 类型 | 说明 |
|----------|------|-------|
| **ElevenLabs** | 云端 API | 顶级语音质量 |
| **Google TTS** | 云端 API | 700+ 声音、50+ 语言——最适合本地化 |
| **Kling Official TTS** | 云端 API | 已知 `voice_id` 时可用的 Kling 官方配音 |
| **OpenAI TTS** | 云端 API | 快速、便宜 |
| **Piper** | 本地 | 完全免费、离线可用 |

</details>

<details>
<summary><strong>音乐、音效与后期制作</strong></summary>

**音乐与音效：**

| 提供商 | 类型 | 说明 |
|----------|------|-------|
| **Suno AI** | 云端 API | 带人声、歌词的完整歌曲生成，任意曲风，最长 8 分钟。 |
| **ElevenLabs Music** | 云端 API | AI 音乐生成 |
| **ElevenLabs SFX** | 云端 API | 音效生成 |

**后期制作（始终可用、始终免费）：**

| 工具 | 作用 |
|------|-------------|
| **FFmpeg** | 视频合成、编码、字幕烧录、音频混流 |
| **Video Stitch** | 多片段组装、交叉淡化、画中画、空间布局 |
| **Video Trimmer** | 精确剪切与提取 |
| **Audio Mixer** | 多轨混音、闪避（ducking）、淡入淡出 |
| **Audio Enhance** | 降噪、响度归一化 |
| **Color Grade** | 基于 LUT 的调色 |
| **Subtitle Gen** | 根据时间戳生成 SRT/VTT 字幕 |

**增强：**

| 工具 | 作用 |
|------|-------------|
| **Upscale** | Real-ESRGAN 图像/视频超分辨率 |
| **Background Remove** | rembg / U2Net 背景移除 |
| **Face Enhance** | 人脸质量增强 |
| **Face Restore** | CodeFormer / GFPGAN 人脸修复 |

**分析：**

| 工具 | 作用 |
|------|-------------|
| **Transcriber** | WhisperX 语音转文字，带逐词时间戳 |
| **Scene Detect** | 自动场景边界检测 |
| **Frame Sampler** | 智能抽帧 |
| **Video Understand** | CLIP/BLIP-2 视觉语言分析 |

**数字人与唇形同步：**

| 工具 | 作用 |
|------|-------------|
| **Talking Head** | SadTalker / MuseTalk 数字人动画 |
| **Lip Sync** | Wav2Lip 音频驱动唇形同步 |
| **Kling Avatar** | Kling 官方云端数字人主持生成 |
| **Kling Lip Sync** | Kling 官方云端唇形同步，支持显式人脸选择 |

**合成与渲染：**

| 引擎 | 类型 | 作用 |
|--------|------|-------------|
| **Remotion** | 本地（Node.js） | 基于 React 的编程化视频——弹簧动画图像场景、数据揭示、章节标题、主视觉卡片、TikTok 风格逐词字幕、场景转场（淡入/滑动/擦除/翻转）、Google Fonts、带淡入淡出曲线的音频，以及 TalkingHead 数字人合成。**当没有配置任何视频生成提供商时，智能体会生成静态图像，由 Remotion 把它们变成完整的动画视频。** |
| **HyperFrames** | 本地（Node.js ≥ 22） | HTML/CSS/GSAP 编程化视频——动态字体排版、产品宣传片、发布集锦、自定义动态图形、注册表积木（数据图表、颗粒叠加、着色器转场）、网页转视频工作流，以及绑定好的 SVG 角色动画。通过 `npx hyperframes` 调用；无需 monorepo 检出。 |
| **FFmpeg** | 本地 | 核心视频组装、编码、字幕烧录、音频混流、调色 |

运行时在提案阶段选定（`render_runtime`），并在 `edit_decisions` 中锁定。在运行时之间悄悄切换属于治理违规——见 `skills/core/hyperframes.md`。

</details>

---

## 风格系统

风格手册（playbook）为你的制作定义视觉语言：

| 风格手册 | 适用场景 |
|----------|----------|
| **Clean Professional（简洁专业）** | 企业、教育、SaaS |
| **Flat Motion Graphics（扁平动态图形）** | 社交媒体、TikTok、初创团队 |
| **Minimalist Diagram（极简图示）** | 技术深度解析、架构讲解 |

风格手册控制字体排版、调色板、动效风格、音频配置和质量规则。智能体读取手册后会在所有生成的资产中一致地应用它。

---

## 平台输出配置

内置覆盖所有主流平台的渲染配置：

| 配置 | 分辨率 | 宽高比 |
|---------|-----------|--------------|
| YouTube 横屏 | 1920x1080 | 16:9 |
| YouTube 4K | 3840x2160 | 16:9 |
| YouTube Shorts | 1080x1920 | 9:16 |
| Instagram Reels | 1080x1920 | 9:16 |
| Instagram 信息流 | 1080x1080 | 1:1 |
| TikTok | 1080x1920 | 9:16 |
| LinkedIn | 1920x1080 | 16:9 |
| 电影宽银幕 | 2560x1080 | 21:9 |

---

## 制作治理

OpenMontage 把视频制作当作真正的工程对待——每个阶段都有质量关卡、审计轨迹和强制机制。

### 质量关卡

- **人工审批关卡是强制的，而不是建议性的**——提案、脚本、场景规划、生成的资产和发布都会暂停等待你的签字确认。检查点写入器会拒绝把没有记录审批的门禁阶段标记为“已完成”，并且每个被取代的检查点都会归档，确保审计轨迹（包括关卡流转）在修订后依然完整。评审在 [Backlot 看板](#实时观看制作过程--backlot-动态故事板)上以可视化方式进行。
- **预合成校验**——如果违反交付承诺（例如“以动态画面为主”的视频却有 80% 静态图像）、幻灯片风险评分达到临界值，或缺少渲染器家族，则阻止渲染。在浪费 GPU 时间之前抓出坏方案。
- **渲染后自审**——每次渲染后，运行时会执行 ffprobe 校验，在 4 个位置抽帧检查黑帧和损坏的叠加层，分析音频电平是否静音或削波，核验交付承诺是否兑现，并检查字幕是否存在。评审不通过，视频就不会交付给你。
- **幻灯片风险评分**——6 维分析（重复度、装饰性画面、弱动态、镜头意图、排版依赖、无支撑的电影感宣称）防止产出“会动的 PPT”。
- **源素材检查**——当用户提供自己的素材时，系统会探测每个文件（分辨率、编码、音轨、时长），并在做出任何创意决策之前生成规划含义。绝不根据文件名臆想内容。

### 评分制提供商选择

每次工具选择（视频生成、图像生成、TTS、音乐）都会经过 7 维评分引擎：任务适配（30%）、输出质量（20%）、控制特性（15%）、可靠性（15%）、成本效率（10%）、延迟（5%）、连续性（5%）。获胜的提供商及其分数会与所有考虑过的备选方案一起记录在决策轨迹中。

选择器会在评分前对松散的 brief 上下文做归一化。如果智能体只知道“皮克斯风格动画短片、角色一致”之类的信息，选择器会把它扩展成评分器友好的意图和风格信号，而不是要求一个完美预塑形的 `task_context`。

选择器的输出还会给出所选提供商的 `agent_skills`，智能体可以立即读取对应的第 3 层提供商技能，然后再去写提示词。

### 决策审计轨迹

每个重要的创意和技术决策——提供商选择、风格/手册选择、音乐曲目、声音选择、渲染器家族、任何回退或降级——都会连同考虑过的备选方案、置信度评分和推理一起记录。累积的决策日志贯穿所有阶段，因此你可以精确追溯成片为什么是现在这个样子。

### 预算控制

- 执行前**估算**——提前看到成本
- **预留**预算——调用前锁定资金
- 事后**对账**——记录实际支出
- **可配置模式**——`observe`（仅记录）、`warn`（记录超限）、`cap`（硬上限）
- **单动作审批**——超过阈值时暂停等待确认（默认：$0.50）
- **总预算上限**——默认 $10，完全可配置

不会有意外账单。智能体在花钱之前会告诉你要花多少。

---

## 智能体兼容性

OpenMontage 适用于任何能读文件、能执行 Python 的 AI 编程助手。已为以下平台内置专用指令文件：

| 平台 | 配置文件 |
|----------|------------|
| **Claude Code** | `CLAUDE.md` |
| **Cursor** | `CURSOR.md` + `.cursor/rules/` |
| **GitHub Copilot** | `COPILOT.md` + `.github/copilot-instructions.md` |
| **Codex** | `CODEX.md` |
| **Windsurf** | `.windsurfrules` |

所有平台文件都指向共享的 `AGENT_GUIDE.md`（操作指南与智能体契约）和 `PROJECT_CONTEXT.md`（架构参考）。

> **即将推出：** 通过 **Ollama** 和 **LM Studio** 支持本地 LLM——不依赖任何云端 LLM 即可运行完整的制作管线。

---

## 参与贡献

OpenMontage 为扩展而生。最常见的两类贡献：

### 添加新工具

1. 在合适的 `tools/` 子目录中创建一个 Python 文件
2. 继承 `BaseTool` 并实现工具契约
3. 注册表会自动发现它——无需手动注册
4. 如果工具需要用法指导，添加一个技能文件

### 添加新管线

1. 在 `pipeline_defs/` 中创建一个 YAML 清单
2. 在 `skills/pipelines/<your-pipeline>/` 中创建阶段导演技能
3. 引用现有工具——如有需要也可以添加新工具

完整技术参考见 `docs/ARCHITECTURE.md`；完整提供商指南（配置、价格、免费额度）见 `docs/PROVIDERS.md`；智能体契约见 `AGENT_GUIDE.md`。

### 加入社区

我们使用 [GitHub Discussions](https://github.com/calesthio/OpenMontage/discussions) 分享作品和想法：

- **[Show and Tell](https://github.com/calesthio/OpenMontage/discussions/categories/show-and-tell)**——分享你制作的视频、效果好的提示词，或你发现的创意工作流
- **[Ideas](https://github.com/calesthio/OpenMontage/discussions/categories/ideas)**——提议新管线、新工具、新风格手册或新集成
- **[Q&A](https://github.com/calesthio/OpenMontage/discussions/categories/q-a)**——询问安装、管线或故障排查相关问题

做出了很酷的东西？发到 Show and Tell 吧——我们很期待看到你的作品。

---

## 联系方式

想获取更新、发布动态和幕后开发笔记，请关注 [@calesthioailabs](https://x.com/calesthioailabs)。

反馈 bug、功能请求和工作流讨论，请使用 [GitHub Issues](https://github.com/calesthio/OpenMontage/issues) 和 [GitHub Discussions](https://github.com/calesthio/OpenMontage/discussions)，让所有信息保持可见、可跟进。

---

## 测试

```bash
# 运行契约测试（无需 API 密钥）
make test-contracts

# 运行全部测试
make test
```

---

## Star 历史

<a href="https://www.star-history.com/?repos=calesthio%2FOpenMontage&type=date&legend=top-left">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://api.star-history.com/image?repos=calesthio/OpenMontage&type=date&theme=dark&legend=top-left" />
    <source media="(prefers-color-scheme: light)" srcset="https://api.star-history.com/image?repos=calesthio/OpenMontage&type=date&legend=top-left" />
    <img alt="Star 历史图表" src="https://api.star-history.com/image?repos=calesthio/OpenMontage&type=date&legend=top-left" />
  </picture>
</a>

---

## 许可证

[GNU AGPLv3](LICENSE)

---

**OpenMontage** —— 具备真正质量强制力的生产级视频，由你的 AI 助手编排。

如果这个项目对你有用，点个 ⭐ 意义非凡——它也能帮助更多人发现这个项目。

如果你想更进一步，欢迎[赞助本项目](https://github.com/sponsors/calesthio)——OpenMontage 是在夜晚和周末构建的，你的支持让这一切可持续。
