# DiaMoE-TTS 简化版本

本项目基于 [GiantAILab/DiaMoE-TTS](https://github.com/GiantAILab/DiaMoE-TTS) 进行了简化和改进，专注于提供简单易用的 IPA 转语音功能。

## 🎯 主要改进

### 1. 新增简化工具脚本

#### `simple_ipa2wav.py` - 最简单的 IPA 转语音工具 ⭐ 推荐使用

**功能特点**：
- ✅ 自动读取项目自带的参考音频和对应的 IPA
- ✅ 支持多种 IPA 输入格式（五度标调、空格分隔、方括号格式）
- ✅ 自动格式转换和验证
- ✅ 修复了 Windows 平台的编码问题
- ✅ 修复了 torchaudio/torchcodec 依赖冲突
- ✅ 自动添加 .wav 文件扩展名

**使用方法**：
```bash
# 激活虚拟环境
.\diamoetts\Scripts\activate

# 运行脚本
python simple_ipa2wav.py
```

**支持的 IPA 格式**：
- 五度标调：`ni21 xɔ35 ma55`
- 空格分隔：`n i h ɑ`
- 方括号格式：`[n] [i] [h] [ɑ]`

#### `ipa_tone_converter.py` - 五度标调转换工具

**功能**：
- 将标准 IPA（五度标调法）转换为模型所需格式
- 支持数字声调（1-5）到上标字母（ᴴᴹᴸ）的自动转换

#### `ipa_to_wav.py` - 交互式 IPA 转语音工具

**功能**：
- 支持多种 IPA 输入格式
- 交互式选择参考音频
- 手动输入参考 IPA

### 2. 配置文件修改

#### `app_gradio.py`
- 修改了模型路径配置：`./models/10ep_mlpEXP_9.pt`
- 便于用户直接使用下载的模型文件

### 3. 依赖问题修复

**解决的问题**：
- ✅ Windows 平台 GBK 编码错误
- ✅ torchaudio 与 torchcodec 的兼容性问题
- ✅ 模型类导入错误（DiT 类需要正确导入）
- ✅ 文件扩展名自动处理

**技术方案**：
- 使用 soundfile 替代 torchcodec 进行音频加载
- 添加 Windows 控制台编码修复
- 正确导入 DiT 模型类

## 📁 项目结构

```
DiaMoE-TTS/
├── simple_ipa2wav.py          # ⭐ 最简单的 IPA 转语音工具（推荐）
├── ipa_tone_converter.py      # 五度标调转换工具
├── ipa_to_wav.py              # 交互式工具
├── quick_test.py              # 快速测试脚本
├── test_ipa_to_wav.py         # 测试脚本
├── app_gradio.py              # Gradio Web 界面（已修改模型路径）
├── models/                    # 模型文件目录
│   └── 10ep_mlpEXP_9.pt      # 基础模型（需下载）
├── prompts/                   # 参考音频和 IPA 文本
├── diamoe_tts/               # 核心 TTS 系统
└── dialect_frontend/         # 方言前端处理系统
```

## 🚀 快速开始

### 1. 安装依赖

```bash
# 创建虚拟环境
python -m venv diamoetts
.\diamoetts\Scripts\activate

# 安装依赖
cd diamoe_tts
pip install -e .
```

### 2. 下载模型

从 [Hugging Face](https://huggingface.co/RICHARD12369/DiaMoE_TTS/blob/main/10ep_mlpEXP_9.pt) 下载基础模型，放到 `models/` 目录：

```
models/10ep_mlpEXP_9.pt
```

### 3. 运行

```bash
# 使用最简单的工具（推荐）
python simple_ipa2wav.py
```

## 💡 使用示例

### 示例 1：使用五度标调

```
选择参考音频编号: 2
输入你想生成的 IPA: ni21 xɔ35 ma55
输出文件名: my_voice
```

生成：`my_voice.wav`

### 示例 2：使用空格分隔

```
选择参考音频编号: 1
输入你想生成的 IPA: n i h ɑ
输出文件名: output
```

生成：`output.wav`

## 📝 声调映射表

五度标调到上标字母的映射：

| 数字 | 音高 | 上标字母 |
|------|------|----------|
| 5    | 最高 | ᴴ        |
| 4    | 高   | ᴴ        |
| 3    | 中   | ᴹ        |
| 2    | 低   | ᴸ        |
| 1    | 最低 | ᴸ        |

示例：
- `55` → `ᴴᴴ` (高平)
- `35` → `ᴹᴴ` (中升)
- `21` → `ᴸᴴ` (低升)
- `51` → `ᴴᴸ` (高降)

## ⚠️ 注意事项

### 性能

- **CPU 推理**：生成 1-2 秒音频需要约 30-60 秒
- **GPU 推理**：需要安装 CUDA 版本的 PyTorch，速度会快很多

### EMA 参数

- 当前使用 `use_ema=False`（使用原始模型权重）
- 不影响生成质量

### 参考音频

- 项目在 `prompts/` 目录提供了多个方言的参考音频
- 包括：粤语、上海话、成都话、闽南语、南京话等
- 每个音频都配有对应的 IPA 文本文件

## 🔧 技术细节

### 模型架构

- 基于 F5-TTS 架构
- 使用 Mixture-of-Experts (MoE) 增强
- DiT (Diffusion Transformer) 骨干网络
- Vocos 声码器

### 模型配置

```python
{
    "dim": 1024,
    "depth": 22,
    "heads": 16,
    "ff_mult": 2,
    "text_dim": 512,
    "conv_layers": 4,
    "use_moe": True,
    "num_experts": 9,
    "moe_topK": 1,
    "expert_type": "mlp"
}
```

## 🆚 与原项目的区别

| 特性 | 原项目 | 本项目 |
|------|--------|--------|
| 使用难度 | 需要配置多个参数 | 一键运行 |
| IPA 输入 | 需要严格的方括号格式 | 支持多种格式自动转换 |
| 参考音频 | 需要手动输入 IPA | 自动读取 |
| Windows 支持 | 编码问题 | 已修复 |
| 依赖问题 | torchcodec 冲突 | 已解决 |
| 文件扩展名 | 需要手动添加 | 自动处理 |

## 📄 原项目信息

- **原项目**：[GiantAILab/DiaMoE-TTS](https://github.com/GiantAILab/DiaMoE-TTS)
- **论文**：[DiaMoE-TTS: A Unified IPA-Based Dialect TTS Framework](https://arxiv.org/abs/2509.22727)
- **许可证**：MIT License

## 🙏 致谢

感谢 GiantAILab 团队开发的 DiaMoE-TTS 项目，本项目在其基础上进行了简化和改进。

## 📮 反馈

如有问题或建议，欢迎提交 Issue。
