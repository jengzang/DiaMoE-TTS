# 输出目录

这个目录用于存放生成的音频文件。

## 📁 目录用途

所有通过 `simple_ipa2wav.py` 或其他工具生成的音频文件都应该保存在这里。

## 🎵 文件命名建议

建议使用有意义的文件名：

```
outputs/
├── cantonese_greeting.wav      # 粤语问候
├── shanghai_test_01.wav        # 上海话测试 1
├── mandarin_example.wav        # 普通话示例
└── my_voice_20240220.wav       # 带日期的文件名
```

## 🧹 清理

定期清理测试文件：

```bash
# 删除所有测试文件
rm outputs/test*.wav

# 删除所有文件（谨慎使用）
rm outputs/*.wav
```

## 📝 注意

- 这个目录中的 .wav 文件不会被提交到 git（已在 .gitignore 中配置）
- 如果需要分享示例音频，请复制到 `examples/` 目录
