# 项目目录结构

```
DiaMoE-TTS/
│
├── 📄 README.md                    # 项目主文档
├── 📄 LICENSE                      # MIT 许可证
├── 📄 .gitignore                   # Git 忽略规则
│
├── 🎯 simple_ipa2wav.py            # ⭐ 主工具：最简单的 IPA 转语音
├── 🌐 app_gradio.py                # Gradio Web 界面
│
├── 📂 tools/                       # 辅助工具脚本
│   ├── README.md
│   ├── ipa_tone_converter.py
│   ├── ipa_to_wav.py
│   ├── quick_test.py
│   └── test_ipa_to_wav.py
│
├── 📂 outputs/                     # 生成的音频文件
│   ├── README.md
│   └── *.wav
│
├── 📂 docs/                        # 📚 所有文档
│   ├── README.md                  # 文档目录索引
│   ├── PROJECT_STRUCTURE.md       # 项目架构说明
│   ├── README_CHANGES.md          # 详细改进说明
│   ├── README_ORIGINAL.md         # 原项目文档
│   ├── ipa_frontend_CN.md         # IPA 前端中文说明
│   └── ipa_frontend_EN.md         # IPA 前端英文说明
│
├── 📂 models/                      # 模型文件
│   └── 10ep_mlpEXP_9.pt
│
├── 📂 prompts/                     # 参考音频和 IPA
│   ├── cantonese_male_prompt.wav
│   ├── cantonese_male_prompt.txt
│   └── ...
│
├── 📂 diamoe_tts/                  # 核心 TTS 系统
│   ├── src/
│   ├── data/
│   └── pyproject.toml
│
├── 📂 dialect_frontend/            # 方言前端处理
│   ├── frontend/
│   └── tools/
│
├── 📂 pics/                        # 图片资源
│
└── 📂 venv/                        # Python 虚拟环境（被忽略）
```

## 🎯 根目录文件说明

| 文件 | 说明 | 用途 |
|------|------|------|
| `README.md` | 项目主文档 | 快速了解项目 |
| `simple_ipa2wav.py` | 主工具 | 日常使用 ⭐ |
| `app_gradio.py` | Web 界面 | 可选的 Web 界面 |

## 📚 文档组织

所有文档都在 `docs/` 目录下：

- **项目架构** → `docs/PROJECT_STRUCTURE.md`
- **改进说明** → `docs/README_CHANGES.md`
- **原项目文档** → `docs/README_ORIGINAL.md`
- **IPA 前端** → `docs/ipa_frontend_CN.md`

## 🗂️ 目录用途

| 目录 | 用途 | 说明 |
|------|------|------|
| `tools/` | 辅助工具 | 特殊需求时使用 |
| `outputs/` | 生成文件 | 你的音频输出 |
| `docs/` | 文档 | 所有说明文档 |
| `models/` | 模型 | 预训练模型 |
| `prompts/` | 参考音频 | 项目自带 |
| `diamoe_tts/` | 核心代码 | TTS 系统 |
| `dialect_frontend/` | 前端 | 文本处理 |
| `venv/` | 虚拟环境 | Python 依赖 |

## 🚀 快速开始

1. **查看主文档**：`README.md`
2. **运行主工具**：`python simple_ipa2wav.py`
3. **查看详细文档**：`docs/` 目录

## 📝 文件管理

### 根目录保持简洁

根目录只保留：
- ✅ 主 README
- ✅ 主要工具脚本
- ✅ 许可证和配置文件

### 其他文件分类存放

- 📚 文档 → `docs/`
- 🛠️ 工具 → `tools/`
- 🎵 输出 → `outputs/`

## 🔗 相关链接

- [主 README](../README.md)
- [文档目录](docs/README.md)
- [工具目录](tools/README.md)
- [输出目录](outputs/README.md)
