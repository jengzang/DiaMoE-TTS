# 项目架构说明

## 📁 目录结构

```
DiaMoE-TTS/
│
├── 📄 README.md                    # 项目主文档（简化版说明）
├── 📄 README_ORIGINAL.md           # 原项目完整文档
├── 📄 README_CHANGES.md            # 详细改进说明
├── 📄 LICENSE                      # MIT 许可证
├── 📄 .gitignore                   # Git 忽略规则
│
├── 🎯 simple_ipa2wav.py            # ⭐ 主工具：最简单的 IPA 转语音
├── 🌐 app_gradio.py                # Gradio Web 界面
│
├── 📂 tools/                       # 辅助工具脚本
│   ├── ipa_tone_converter.py      # 五度标调转换工具
│   ├── ipa_to_wav.py              # 交互式 IPA 转语音工具
│   ├── quick_test.py              # 快速测试脚本
│   └── test_ipa_to_wav.py         # 测试脚本
│
├── 📂 outputs/                     # 生成的音频文件输出目录
│   └── *.wav                      # 你生成的所有音频文件
│
├── 📂 examples/                    # 示例文件（可选）
│   └── *.wav                      # 示例音频（如果有）
│
├── 📂 models/                      # 模型文件目录
│   ├── 10ep_mlpEXP_9.pt          # 基础模型（需下载）
│   └── *_lora.pt                  # LoRA 模型（可选）
│
├── 📂 prompts/                     # 参考音频和 IPA 文本
│   ├── cantonese_male_prompt.wav
│   ├── cantonese_male_prompt.txt
│   ├── shanghai_male_prompt.wav
│   ├── shanghai_male_prompt.txt
│   └── ...                        # 其他方言的参考音频
│
├── 📂 diamoe_tts/                  # 核心 TTS 系统
│   ├── src/                       # 源代码
│   │   └── f5_tts/               # F5-TTS 实现
│   ├── data/                      # 数据文件
│   │   ├── vocab.txt             # 词汇表
│   │   └── punctuation.txt       # 标点符号
│   └── pyproject.toml            # 项目配置
│
├── 📂 dialect_frontend/            # 方言前端处理系统
│   ├── frontend/                  # 前端处理模块
│   └── tools/                     # 前端工具
│
├── 📂 docs/                        # 文档目录
│   ├── ipa_frontend_CN.md        # IPA 前端中文说明
│   └── ipa_frontend_EN.md        # IPA 前端英文说明
│
├── 📂 pics/                        # 图片资源
│   ├── ipa_global.PNG
│   └── diamoe_tts.png
│
├── 📂 diamoetts/                   # 虚拟环境（被 .gitignore 忽略）
├── 📂 .venv/                       # 备用虚拟环境（被忽略）
├── 📂 .idea/                       # IDE 配置（被忽略）
└── 📂 .claude/                     # Claude 配置（被忽略）
```

## 🎯 主要文件说明

### 核心工具

| 文件 | 用途 | 推荐度 |
|------|------|--------|
| `simple_ipa2wav.py` | 最简单的 IPA 转语音工具 | ⭐⭐⭐⭐⭐ |
| `app_gradio.py` | Web 界面（需要 g2pw 模型） | ⭐⭐⭐ |

### 辅助工具（tools/）

| 文件 | 用途 | 使用场景 |
|------|------|----------|
| `ipa_tone_converter.py` | 五度标调转换 | 需要精确控制声调 |
| `ipa_to_wav.py` | 交互式工具 | 需要手动输入参考 IPA |
| `quick_test.py` | 快速测试 | 开发测试 |
| `test_ipa_to_wav.py` | 测试脚本 | 开发测试 |

### 输出目录

| 目录 | 内容 | 说明 |
|------|------|------|
| `outputs/` | 生成的音频文件 | 所有生成的 .wav 文件 |
| `examples/` | 示例音频 | 可选的示例文件 |

### 模型和数据

| 目录/文件 | 内容 | 大小 |
|-----------|------|------|
| `models/10ep_mlpEXP_9.pt` | 基础模型 | ~1.3GB |
| `models/*_lora.pt` | LoRA 微调模型 | 可选 |
| `prompts/*.wav` | 参考音频 | 项目自带 |
| `diamoe_tts/data/vocab.txt` | 词汇表 | 18KB |

## 🚀 使用流程

### 1. 基本使用（推荐）

```bash
# 在项目根目录运行
python simple_ipa2wav.py

# 生成的音频会保存到当前目录或指定位置
# 建议手动移动到 outputs/ 目录
```

### 2. 使用辅助工具

```bash
# 五度标调转换工具
python tools/ipa_tone_converter.py

# 交互式工具
python tools/ipa_to_wav.py
```

### 3. Web 界面（需要额外配置）

```bash
python app_gradio.py
```

## 📝 文件管理建议

### 生成的音频文件

建议将生成的音频文件移动到 `outputs/` 目录：

```bash
# 手动移动
mv your_audio.wav outputs/

# 或在脚本中指定输出路径
python simple_ipa2wav.py
# 输出文件名: outputs/my_voice.wav
```

### 示例文件

如果你想保存一些示例音频供参考：

```bash
# 复制到 examples 目录
cp outputs/good_example.wav examples/
```

### 清理临时文件

```bash
# 清理 outputs 目录中的测试文件
rm outputs/test*.wav

# 清理所有生成的音频（谨慎使用）
rm outputs/*.wav
```

## 🔧 开发说明

### 虚拟环境

项目使用 `diamoetts/` 作为虚拟环境目录：

```bash
# 激活虚拟环境
.\diamoetts\Scripts\activate  # Windows
source diamoetts/bin/activate  # Linux/Mac

# 安装依赖
cd diamoe_tts
pip install -e .
```

### 添加新工具

如果你要添加新的工具脚本：

1. 将脚本放到 `tools/` 目录
2. 在本文档中更新说明
3. 提交时包含在 git 中

### 模型文件

模型文件较大，不应提交到 git：

- ✅ 保存在 `models/` 目录
- ❌ 不要提交到 git（已在 .gitignore 中）
- 📝 在文档中说明下载地址

## 📊 磁盘空间占用

| 目录 | 大小 | 说明 |
|------|------|------|
| `models/` | ~1.3GB | 模型文件 |
| `diamoetts/` | ~2GB | 虚拟环境 |
| `prompts/` | ~22MB | 参考音频 |
| `outputs/` | 变化 | 生成的音频 |
| 其他 | ~100MB | 代码和文档 |
| **总计** | **~3.5GB** | 完整项目 |

## 🧹 清理建议

### 定期清理

```bash
# 清理 Python 缓存
find . -type d -name "__pycache__" -exec rm -rf {} +
find . -type f -name "*.pyc" -delete

# 清理测试音频
rm outputs/test*.wav

# 清理临时文件
rm *.tmp *.log
```

### 完全重置

如果需要完全重置项目：

```bash
# 删除虚拟环境
rm -rf diamoetts/

# 删除生成的文件
rm -rf outputs/*.wav

# 重新安装
python -m venv diamoetts
.\diamoetts\Scripts\activate
cd diamoe_tts
pip install -e .
```

## 📚 相关文档

- [README.md](../README.md) - 项目主文档
- [README_CHANGES.md](../README_CHANGES.md) - 详细改进说明
- [README_ORIGINAL.md](../README_ORIGINAL.md) - 原项目文档

## 🔗 外部资源

- [模型下载](https://huggingface.co/RICHARD12369/DiaMoE_TTS)
- [原项目](https://github.com/GiantAILab/DiaMoE-TTS)
- [论文](https://arxiv.org/abs/2509.22727)
