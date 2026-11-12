# florr.io DPS Build Analyzer (Web版)

这是一个基于 [Pyodide](https://pyodide.org/) 的 florr.io 网页版 DPS 构筑计算器。所有的 Python 计算逻辑都在用户的浏览器本地运行，无需后端服务器。

## 🌐 在线体验 (Live Demo)

👉 **[点击这里访问在线计算器](https://huoguotu.github.io/florr-dps/)**

## ✨ 功能特点

- **实时 TP 计算**：在选择天赋时，右侧会自动显示消耗的 TP 和对应等级。
- **多模式支持**：支持 `lentil`、`yy` 和 `wheel` 模式。
- **精准计算**：针对 `wheel` 模式加入了“攻击范围角”和“转速指令值”的自定义计算。
- **一键微调**：生物体伤、护甲和角度均支持快捷档位切换。

## 🛠️ 技术栈

- **前端**：原生 HTML / CSS / JavaScript
- **核心计算**：Python (通过 WebAssembly 在浏览器运行)
- **字体**：Ubuntu (Google Fonts)

## 📝 使用说明

1. 在“花瓣”框输入构筑，各花瓣名用空格隔开（如：`2ugl 4dust bur 2ulentil`）。
2. 通过下拉框配置 10 项天赋。
3. 输入生物体伤和生物护甲。
4. 选择模式，点击“计算 DPS”即可在下方表格看到结果。

## 👨‍💻 原作者

- 核心 Python 算法与设计：**Hu0_gu0_4u31** (florr: Huo_guo_tu31)