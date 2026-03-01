#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
简易 IPA 转语音工具
支持多种 IPA 输入格式，自动转换并生成语音
"""

import sys
import os
import re
sys.path.insert(0, "./diamoe_tts/src")

def format_ipa_to_brackets(ipa_text):
    """
    将各种格式的 IPA 转换为方括号格式
    支持的输入格式：
    1. 空格分隔: "n ˈi h ˈɑ"
    2. 管道分隔: "n | ˈi | h | ˈɑ"
    3. 已有方括号: "[n] [ˈi] [h] [ˈɑ]"
    """
    # 移除多余的空格
    ipa_text = ipa_text.strip()

    # 如果已经是方括号格式，直接返回
    if '[' in ipa_text and ']' in ipa_text:
        return ipa_text

    # 移除管道符号
    ipa_text = ipa_text.replace('|', ' ')

    # 按空格分割
    phonemes = ipa_text.split()

    # 过滤空字符串和标点
    phonemes = [p.strip() for p in phonemes if p.strip()]

    # 添加方括号
    formatted = ' '.join([f'[{p}]' for p in phonemes])

    return formatted

def main():
    print("=" * 70)
    print("DiaMoE-TTS 简易 IPA 转语音工具")
    print("=" * 70)

    # 显示可用的参考音频
    print("\n可用的参考音频：")
    prompts_dir = "./prompts"
    if os.path.exists(prompts_dir):
        wav_files = [f for f in os.listdir(prompts_dir) if f.endswith('.wav')]
        for i, f in enumerate(wav_files, 1):
            print(f"  {i}. {f}")

    # 选择参考音频
    print("\n请选择参考音频编号（或直接输入文件路径）：")
    choice = input("> ").strip()

    if choice.isdigit() and 1 <= int(choice) <= len(wav_files):
        ref_audio = os.path.join(prompts_dir, wav_files[int(choice) - 1])
    elif os.path.exists(choice):
        ref_audio = choice
    else:
        # 默认使用上海话男声
        ref_audio = "./prompts/shanghai_male_prompt.wav"
        print(f"使用默认: {ref_audio}")

    if not os.path.exists(ref_audio):
        print(f"错误：音频文件不存在: {ref_audio}")
        return

    print(f"\n✓ 参考音频: {ref_audio}")

    # 输入参考音频的 IPA
    print("\n请输入参考音频对应的 IPA 文本：")
    print("（支持格式：空格分隔、管道分隔、或方括号格式）")
    print("示例: n ˈi h ˈɑ  或  n | ˈi | h | ˈɑ  或  [n] [ˈi] [h] [ˈɑ]")
    ref_text_input = input("> ").strip()

    if not ref_text_input:
        # 使用默认
        ref_text_input = "n̤ ˈaᴸᴹ t͜sʰ ˈăᴴ k w ˈɛᴴᴸ t͜sʰ ˈăᴴ"
        print(f"使用默认: {ref_text_input}")

    ref_text = format_ipa_to_brackets(ref_text_input)
    print(f"转换后: {ref_text}")

    # 输入要生成的 IPA
    print("\n请输入要生成的 IPA 文本：")
    print("（支持格式：空格分隔、管道分隔、或方括号格式）")
    gen_text_input = input("> ").strip()

    if not gen_text_input:
        gen_text_input = "n̤ ˈaᴸᴹ h ɔ"
        print(f"使用默认: {gen_text_input}")

    gen_text = format_ipa_to_brackets(gen_text_input)
    print(f"转换后: {gen_text}")

    # 输出文件名
    print("\n输出文件名（默认: output.wav）：")
    output_file = input("> ").strip()
    if not output_file:
        output_file = "output.wav"

    print("\n" + "=" * 70)
    print("开始生成...")
    print("=" * 70)

    # 加载模型
    print("\n正在加载模型...")

    from f5_tts.infer.utils_infer import (
        load_model,
        load_vocoder,
        infer_process,
    )

    MODEL_CONFIG = {
        "ckpt_file": "./models/10ep_mlpEXP_9.pt",
        "vocab_file": "./diamoe_tts/data/vocab.txt",
    }

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

        vocoder = load_vocoder(vocoder_name="vocos", is_local=False)
        print("✓ 声码器加载成功")

        print("\n生成中...")

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

        import soundfile as sf
        sf.write(output_file, wav, sr)

        print("\n" + "=" * 70)
        print("✓ 成功！")
        print("=" * 70)
        print(f"输出文件: {output_file}")
        print(f"采样率: {sr} Hz")
        print(f"时长: {len(wav)/sr:.2f} 秒")

    except Exception as e:
        print(f"\n✗ 错误: {e}")
        import traceback
        traceback.print_exc()
        return

if __name__ == "__main__":
    main()
