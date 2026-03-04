#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
简单的 IPA 转语音测试脚本
直接输入 IPA 音标，生成语音文件
"""

import sys
import torch
sys.path.insert(0, "./diamoe_tts/src")

from f5_tts.infer.utils_infer import (
    load_model,
    load_vocoder,
    infer_process,
    preprocess_ref_audio_text,
)

print("=" * 60)
print("DiaMoE-TTS IPA 转语音测试")
print("=" * 60)

# 配置参数
MODEL_CONFIG = {
    "ckpt_file": "./models/10ep_mlpEXP_9.pt",
    "vocab_file": "./diamoe_tts/data/vocab.txt",
    "use_moe": True,
    "num_exps": 9,
    "moe_topK": 1,
    "expert_type": "mlp"
}

print("\n正在加载模型...")
print(f"模型文件: {MODEL_CONFIG['ckpt_file']}")
print(f"词汇表: {MODEL_CONFIG['vocab_file']}")

# 加载模型
try:
    model = load_model(
        model_cls="DiT",
        model_cfg={
            "dim": 1024,
            "depth": 22,
            "heads": 16,
            "ff_mult": 2,
            "text_dim": 512,
            "conv_layers": 4,
            "use_moe": MODEL_CONFIG["use_moe"],
            "num_experts": MODEL_CONFIG["num_exps"],
            "moe_topK": MODEL_CONFIG["moe_topK"],
            "expert_type": MODEL_CONFIG["expert_type"],
        },
        ckpt_path=MODEL_CONFIG["ckpt_file"],
        vocab_file=MODEL_CONFIG["vocab_file"],
        ode_method="euler",
        use_ema=False,
        device="cpu"  # 使用 CPU
    )
    print("✓ 模型加载成功！")
except Exception as e:
    print(f"✗ 模型加载失败: {e}")
    sys.exit(1)

# 加载声码器
print("\n正在加载声码器...")
try:
    vocoder = load_vocoder(vocoder_name="vocos", is_local=False)
    print("✓ 声码器加载成功！")
except Exception as e:
    print(f"✗ 声码器加载失败: {e}")
    sys.exit(1)

print("\n" + "=" * 60)
print("模型加载完成！现在可以输入 IPA 进行测试")
print("=" * 60)

# 示例 IPA 输入
print("\n示例 IPA 格式（每个音素用方括号包裹，空格分隔）：")
print("[n] [ˈi] [h] [ˈɑ] [ʊ̯]")
print("[t͡ʂ] [ˈuᴴᴹ] [ɻ] [ˈəᴴᴸ]")

print("\n请输入参考音频的 IPA 文本（或按回车使用默认）：")
ref_text = input("> ").strip()
if not ref_text:
    ref_text = "[n] [ˈi] [h] [ˈɑ]"
    print(f"使用默认: {ref_text}")

print("\n请输入要生成的 IPA 文本（或按回车使用默认）：")
gen_text = input("> ").strip()
if not gen_text:
    gen_text = "[h] [ˈɑ] [ʊ̯]"
    print(f"使用默认: {gen_text}")

print("\n请输入参考音频文件路径（.wav 格式）：")
ref_audio = input("> ").strip()
if not ref_audio:
    print("错误：必须提供参考音频文件！")
    print("参考音频用于提供说话人的音色和风格")
    sys.exit(1)

print("\n请输入输出文件名（默认: output.wav）：")
output_file = input("> ").strip()
if not output_file:
    output_file = "output.wav"

print("\n" + "=" * 60)
print("开始生成语音...")
print("=" * 60)
print(f"参考文本: {ref_text}")
print(f"生成文本: {gen_text}")
print(f"参考音频: {ref_audio}")
print(f"输出文件: {output_file}")

try:
    # 生成语音
    wav, sr, spect = infer_process(
        ref_audio=ref_audio,
        ref_text=ref_text,
        gen_text=gen_text,
        model_obj=model,
        vocoder=vocoder,
        mel_spec_type="vocos",
        target_rms=0.1,
        cross_fade_duration=0.15,
        nfe_step=32,
        cfg_strength=2.0,
        sway_sampling_coef=-1.0,
        speed=1.0,
        fix_duration=None,
        device="cpu"
    )

    # 保存音频
    import soundfile as sf
    sf.write(output_file, wav, sr)

    print(f"\n✓ 语音生成成功！")
    print(f"✓ 已保存到: {output_file}")
    print(f"✓ 采样率: {sr} Hz")
    print(f"✓ 时长: {len(wav)/sr:.2f} 秒")

except Exception as e:
    print(f"\n✗ 生成失败: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("\n" + "=" * 60)
print("测试完成！")
print("=" * 60)
