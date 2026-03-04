# DiaMoE-TTS 简化版 - 简单易用的 IPA 转语音工具

> 基于 [GiantAILab/DiaMoE-TTS](https://github.com/GiantAILab/DiaMoE-TTS) 的简化版本，专注于提供简单易用的 IPA 转语音功能

[![Original Project](https://img.shields.io/badge/Original-GiantAILab/DiaMoE--TTS-blue)](https://github.com/GiantAILab/DiaMoE-TTS)
[![arXiv](https://img.shields.io/badge/arXiv-2509.22727-b31b1b.svg)](https://arxiv.org/abs/2509.22727)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

---

## 🎯 为什么选择这个版本？

原项目功能强大但配置复杂，本版本进行了大幅简化：

| 特性 | 原项目 | 本简化版 |
|------|--------|----------|
| **使用难度** | 需要配置多个参数和文件 | 一键运行，交互式操作 |
| **IPA 输入** | 必须使用严格的方括号格式 | 支持多种格式自动转换 |
| **参考音频** | 需要手动准备和输入 IPA | 自动读取项目自带音频 |
| **Windows 支持** | 存在编码问题 | 已完全修复 |
| **依赖问题** | torchcodec 冲突 | 已解决 |
| **上手时间** | 需要研究文档 | 5 分钟即可开始使用 |

---

## ⚡ 快速开始（3 步）

### 1. 安装依赖

```bash
# 创建虚拟环境
python -m venv venv
.\venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac

# 安装
cd diamoe_tts
pip install -e .
```

### 2. 下载模型

从 [Hugging Face](https://huggingface.co/RICHARD12369/DiaMoE_TTS/blob/main/10ep_mlpEXP_9.pt) 下载模型（约 1.3GB），放到 `models/` 目录：

```
models/10ep_mlpEXP_9.pt
```

### 3. 运行

```bash
python simple_ipa2wav.py
```

就这么简单！

---

## 🎤 使用示例

### 示例 1：使用五度标调（推荐）

```
可用的参考音频:
  1. Cantonese Female
  2. Shanghai Male
  ...

选择参考音频编号: 2
✓ 自动读取参考 IPA

请输入你想生成的 IPA:
> ni21 xɔ35 ma55

输出文件名: my_voice

✓✓✓ 成功! ✓✓✓
输出文件: my_voice.wav
```

### 示例 2：使用空格分隔

```
请输入你想生成的 IPA:
> n i h ɑ

✓ 自动转换为: [n] [i] [h] [ɑ]
```

### 示例 3：直接使用方括号格式

```
请输入你想生成的 IPA:
> [n] [ˈi] [h] [ˈɑ]

✓ 格式正确，直接使用
```

---

## ✨ 主要改进

### 🔧 新增工具

#### `simple_ipa2wav.py` ⭐ 推荐

最简单的 IPA 转语音工具：
- ✅ 自动读取项目自带的参考音频和 IPA
- ✅ 支持多种 IPA 输入格式（五度标调、空格分隔、方括号）
- ✅ 自动格式转换和验证
- ✅ 自动添加 .wav 文件扩展名
- ✅ 完美支持 Windows

#### `ipa_tone_converter.py`

五度标调转换工具：
- 支持数字声调（1-5）到上标字母（ᴴᴹᴸ）的自动转换
- 适合需要精确控制声调的场景

#### `ipa_to_wav.py`

交互式工具：
- 支持手动输入参考 IPA
- 更灵活的配置选项

### 🛠️ 技术修复

- ✅ **Windows 编码问题**：修复 GBK 编码错误
- ✅ **依赖冲突**：解决 torchaudio/torchcodec 兼容性问题
- ✅ **模型加载**：正确导入 DiT 模型类
- ✅ **音频加载**：使用 soundfile 替代 torchcodec
- ✅ **文件处理**：自动处理文件扩展名

---

## 📝 支持的 IPA 格式

### 1. 五度标调（推荐）

使用数字 1-5 表示音高：

```
输入: ni21 xɔ35 ma55
转换: [n] [ˈiᴸᴴ] [x] [ˈɔᴹᴴ] [m] [ˈaᴴᴴ]
```

**声调映射表**：

| 数字 | 音高 | 上标 | 示例 |
|------|------|------|------|
| 5    | 最高 | ᴴ    | 55 → ᴴᴴ (高平) |
| 4    | 高   | ᴴ    | 45 → ᴴᴴ |
| 3    | 中   | ᴹ    | 35 → ᴹᴴ (中升) |
| 2    | 低   | ᴸ    | 21 → ᴸᴴ (低升) |
| 1    | 最低 | ᴸ    | 51 → ᴴᴸ (高降) |

### 2. 空格分隔

```
输入: n i h ɑ
转换: [n] [i] [h] [ɑ]
```

### 3. 方括号格式

```
输入: [n] [i] [h] [ɑ]
保持: [n] [i] [h] [ɑ]
```

---

## 🎵 参考音频

项目在 `prompts/` 目录提供了多个方言的参考音频：

- 🇭🇰 **粤语**（Cantonese）：男声、女声
- 🏙️ **上海话**（Shanghai）：男声、女声
- 🌶️ **成都话**（Chengdu）：男声、女声
- 🌊 **闽南语**（Hokkien）：男声、女声
- 🏛️ **南京话**（Nanjing）：男声、女声
- 🏔️ **西安话**（Xi'an）：男声、女声
- 🎭 **京剧**（Peking Opera）：京白、云白

每个音频都配有对应的 IPA 文本文件，**自动读取，无需手动输入**！

---

## ⚙️ 系统要求

### 最低配置
- Python 3.10+
- 4GB RAM
- 2GB 磁盘空间

### 推荐配置
- Python 3.10+
- 8GB+ RAM
- NVIDIA GPU（可选，用于加速）

### 性能参考

| 硬件 | 生成 1 秒音频 | 生成 5 秒音频 |
|------|---------------|---------------|
| CPU  | ~30-60 秒     | ~2-5 分钟     |
| GPU  | ~3-5 秒       | ~10-20 秒     |

---

## 📚 文档

- **[项目架构说明](PROJECT_STRUCTURE.md)** - 完整的目录结构和文件说明
- **[详细改进说明](README_CHANGES.md)** - 所有改进的详细文档
- **[原项目 README](README_ORIGINAL.md)** - 原始项目的完整文档
- **[原项目仓库](https://github.com/GiantAILab/DiaMoE-TTS)** - GiantAILab 的原始项目
- **[论文](https://arxiv.org/abs/2509.22727)** - DiaMoE-TTS 技术论文

---

## 🔧 高级用法

### 使用 GPU 加速

如果你有 NVIDIA GPU：

```bash
# 安装 CUDA 版本的 PyTorch
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
```

然后修改脚本中的 `device="cpu"` 为 `device="cuda"`。

### 使用 LoRA 模型

下载特定方言的 LoRA 模型：
- [京剧云白](https://huggingface.co/RICHARD12369/DiaMoE_TTS/blob/main/10ep_mlpEXP_9_jjyb_lora.pt)
- [京剧京白](https://huggingface.co/RICHARD12369/DiaMoE_TTS/blob/main/10ep_mlpEXP_9_jjjb_lora.pt)
- [南京方言](https://huggingface.co/RICHARD12369/DiaMoE_TTS/blob/main/10ep_mlpEXP_9_nanjing_lora.pt)

---

## ❓ 常见问题

### Q: 为什么生成速度这么慢？
A: 你在使用 CPU。安装 CUDA 版本的 PyTorch 可以大幅提速。

### Q: 支持哪些语言/方言？
A: 支持所有使用 IPA 标注的语言，项目自带 11 种中国方言的参考音频。

### Q: 可以使用自己的参考音频吗？
A: 可以！使用 `ipa_to_wav.py` 工具，提供你的音频文件和对应的 IPA 即可。

### Q: 生成的音频质量如何？
A: 使用高质量的参考音频可以获得很好的效果。建议参考音频清晰、无噪音。

### Q: EMA 参数是什么？
A: Exponential Moving Average，训练时的权重平滑技术。当前使用 `False`（原始权重），不影响质量。

---

## 🆚 与原项目的关系

本项目是 [GiantAILab/DiaMoE-TTS](https://github.com/GiantAILab/DiaMoE-TTS) 的**简化版本**，专注于：

- ✅ 降低使用门槛
- ✅ 提供开箱即用的工具
- ✅ 修复 Windows 平台问题
- ✅ 简化 IPA 输入流程

**原项目的优势**：
- 完整的训练代码
- 详细的技术文档
- 研究级别的功能

**本项目的优势**：
- 极简的使用流程
- 开箱即用
- 适合快速测试和应用

---

## 📄 许可证

本项目继承原项目的 MIT License。

---

## 🙏 致谢

感谢 [GiantAILab](https://github.com/GiantAILab) 团队开发的 DiaMoE-TTS 项目！

本项目在其基础上进行了简化和改进，让更多人能够轻松使用这个强大的 TTS 系统。

---

## 📮 反馈与贡献

- 🐛 **问题反馈**：[提交 Issue](https://github.com/jengzang/DiaMoE-TTS/issues)
- 💡 **功能建议**：欢迎提出改进建议
- 🤝 **贡献代码**：欢迎提交 Pull Request

---

## 🌟 Star History

如果这个项目对你有帮助，请给个 Star ⭐

---

<div align="center">

**[开始使用](#-快速开始3-步)** | **[查看文档](README_CHANGES.md)** | **[原项目](https://github.com/GiantAILab/DiaMoE-TTS)**

Made with ❤️ by simplifying DiaMoE-TTS

</div>
