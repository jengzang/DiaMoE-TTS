# 辅助工具目录

这个目录包含各种辅助工具脚本。

## 🛠️ 工具列表

### `ipa_tone_converter.py`
**五度标调转换工具**

- 支持数字声调（1-5）到上标字母（ᴴᴹᴸ）的转换
- 适合需要精确控制声调的场景

```bash
python tools/ipa_tone_converter.py
```

### `ipa_to_wav.py`
**交互式 IPA 转语音工具**

- 支持手动输入参考 IPA
- 更灵活的配置选项

```bash
python tools/ipa_to_wav.py
```

### `quick_test.py`
**快速测试脚本**

- 使用项目自带的参考音频快速测试
- 适合开发和调试

```bash
python tools/quick_test.py
```

### `test_ipa_to_wav.py`
**测试脚本**

- 用于测试基本功能
- 开发时使用

```bash
python tools/test_ipa_to_wav.py
```

## 💡 使用建议

**日常使用**：推荐使用项目根目录的 `simple_ipa2wav.py`，它最简单易用。

**特殊需求**：
- 需要精确控制声调 → `ipa_tone_converter.py`
- 需要自定义参考音频 → `ipa_to_wav.py`
- 快速测试 → `quick_test.py`

## 📝 添加新工具

如果你要添加新的工具脚本：

1. 将脚本放到这个目录
2. 在本 README 中添加说明
3. 更新 `PROJECT_STRUCTURE.md`
