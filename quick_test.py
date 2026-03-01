#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
快速测试脚本 - 使用项目提供的参考音频
"""

import sys
import os
sys.path.insert(0, "./diamoe_tts/src")

print("=" * 70)
print("DiaMoE-TTS 快速测试")
print("=" * 70)

# 使用项目提供的参考音频
ref_audio = "./prompts/shanghai_male_prompt.wav"
# 参考音频的 IPA（从 txt 文件中提取，转换为方括号格式）
ref_text = "[n̤] [ˈaᴸᴹ] [t͜sʰ] [ˈăᴴ] [k] [w] [ˈɛᴴᴸ] [t͜sʰ] [ˈăᴴ]"

# 要生成的 IPA（简单测试）
gen_text = "[n̤] [ˈaᴸᴹ] [h] [ɔ]"

output_file = "test_output.wav"

print(f"\n使用参考音频: {ref_audio}")
print(f"参考文本 IPA: {ref_text}")
print(f"生成文本 IPA: {gen_text}")
print(f"输出文件: {output_file}")

# 检查参考音频是否存在
if not os.path.exists(ref_audio):
    print(f"\n错误：参考音频文件不存在: {ref_audio}")
    sys.exit(1)

print("\n正在加载模型...")

from f5_tts.infer.utils_infer import (
    load_model,
    load_vocoder,
    infer_process,
)

# 模型配置
MODEL_CONFIG = {
    "ckpt_file": "./models/10ep_mlpEXP_9.pt",
    "vocab_file": "./diamoe_tts/data/vocab.txt",
}

try:
    # 加载模型
    model = load_model(
        model_cls="DiT",
        model_cfg={
            "dim": 1024,
            "depth": 22,
            "heads": 16,
            "ff_mult": 2,
            "text_dim": 512,
            "conv_layers": 4,
            "use_moe": True,
            "num_experts": 9,
            "moe_topK": 1,
            "expert_type": "mlp",
        },
        ckpt_path=MODEL_CONFIG["ckpt_file"],
        vocab_file=MODEL_CONFIG["vocab_file"],
        ode_method="euler",
        use_ema=False,
        device="cpu"
    )
    print("✓ 模型加载成功")

    # 加载声码器
    vocoder = load_vocoder(vocoder_name="vocos", is_local=False)
    print("✓ 声码器加载成功")

    print("\n开始生成语音...")

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

    print(f"\n✓ 成功！")
    print(f"✓ 输出文件: {output_file}")
    print(f"✓ 采样率: {sr} Hz")
    print(f"✓ 时长: {len(wav)/sr:.2f} 秒")
    print("\n" + "=" * 70)

except Exception as e:
    print(f"\n✗ 错误: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
