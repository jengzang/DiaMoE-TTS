#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
IPA 五度标调转换器
将标准 IPA（五度标调法）转换为模型格式并生成语音
"""

import sys
import os
import re
sys.path.insert(0, "./diamoe_tts/src")

# 五度标调到上标字母的映射
TONE_MAP = {
    '5': 'ᴴ',  # High
    '4': 'ᴴ',  # High-mid → High
    '3': 'ᴹ',  # Mid
    '2': 'ᴸ',  # Low-mid → Low
    '1': 'ᴸ',  # Low
}

def parse_ipa_with_tones(ipa_string):
    """
    解析带五度标调的 IPA 字符串
    例如: "ȵɐi21 xɔ35" → ["ȵɐi21", "xɔ35"]
    """
    # 按空格或逗号分割
    syllables = re.split(r'[,\s]+', ipa_string.strip())
    return [s for s in syllables if s]

def convert_tone_numbers(tone_str):
    """
    将数字声调转换为上标字母
    例如: "21" → "ᴸᴴ", "55" → "ᴴᴴ", "35" → "ᴹᴴ"
    """
    if not tone_str:
        return ""
    return ''.join(TONE_MAP.get(t, t) for t in tone_str)

def split_phoneme_and_tone(syllable):
    """
    分离音素和声调
    例如: "ȵɐi21" → ("ȵɐi", "21")
    """
    # 查找末尾的数字
    match = re.match(r'^(.+?)(\d+)$', syllable)
    if match:
        phoneme = match.group(1)
        tone = match.group(2)
        return phoneme, tone
    else:
        # 没有声调标记
        return syllable, ""

def segment_phonemes(phoneme_str):
    """
    将音素字符串分割成单个音素
    这是一个简化版本，假设每个字符是一个音素
    对于复杂的 IPA，可能需要更复杂的分割逻辑
    """
    # 简单处理：每个字符作为一个音素
    # 注意：某些 IPA 符号可能是多字符的（如 t͜s, ʰ 等）
    phonemes = []
    i = 0
    while i < len(phoneme_str):
        char = phoneme_str[i]
        # 检查是否有组合字符（如 t͜s）
        if i + 1 < len(phoneme_str) and phoneme_str[i+1] in ['͜', '͡', 'ʰ', 'ʷ', 'ʲ', '̃', '̤', '̩', '̆', '̯', '↓']:
            phonemes.append(phoneme_str[i:i+2])
            i += 2
        else:
            phonemes.append(char)
            i += 1
    return phonemes

def convert_ipa_to_model_format(ipa_string):
    """
    将用户的 IPA 格式转换为模型格式
    输入: "ȵɐi21 xɔ35"
    输出: "[ȵ] [ɐ] [iᴸᴴ] [x] [ɔᴹᴴ]"
    """
    syllables = parse_ipa_with_tones(ipa_string)
    all_phonemes = []

    for syllable in syllables:
        phoneme_str, tone_str = split_phoneme_and_tone(syllable)
        phonemes = segment_phonemes(phoneme_str)

        # 将声调添加到最后一个音素
        if tone_str and phonemes:
            tone_letters = convert_tone_numbers(tone_str)
            phonemes[-1] = f"ˈ{phonemes[-1]}{tone_letters}"

        all_phonemes.extend(phonemes)

    # 添加方括号
    formatted = ' '.join([f'[{p}]' for p in all_phonemes])
    return formatted

def main():
    print("=" * 70)
    print("IPA 五度标调转语音工具")
    print("=" * 70)
    print("\n支持格式: ȵɐi21 xɔ35 (音素+数字声调)")
    print("声调: 1=最低, 2=低, 3=中, 4=高, 5=最高")

    # 选择参考音频
    print("\n可用的参考音频:")
    prompts_dir = "./prompts"
    wav_files = sorted([f for f in os.listdir(prompts_dir) if f.endswith('.wav')])
    for i, f in enumerate(wav_files, 1):
        print(f"  {i}. {f}")

    print("\n选择参考音频编号 (默认: 1):")
    choice = input("> ").strip()

    if choice.isdigit() and 1 <= int(choice) <= len(wav_files):
        ref_audio = os.path.join(prompts_dir, wav_files[int(choice) - 1])
    else:
        ref_audio = os.path.join(prompts_dir, wav_files[0])
        print(f"使用默认: {wav_files[0]}")

    # 输入参考音频的 IPA
    print("\n输入参考音频的 IPA (五度标调格式):")
    print("示例: ni21 xɔ35")
    ref_ipa = input("> ").strip()

    if not ref_ipa:
        ref_ipa = "ni21 xɔ35"
        print(f"使用默认: {ref_ipa}")

    ref_text = convert_ipa_to_model_format(ref_ipa)
    print(f"转换为: {ref_text}")

    # 输入要生成的 IPA
    print("\n输入要生成的 IPA (五度标调格式):")
    gen_ipa = input("> ").strip()

    if not gen_ipa:
        gen_ipa = "xɔ35"
        print(f"使用默认: {gen_ipa}")

    gen_text = convert_ipa_to_model_format(gen_ipa)
    print(f"转换为: {gen_text}")

    # 输出文件
    print("\n输出文件名 (默认: output.wav):")
    output_file = input("> ").strip() or "output.wav"

    print("\n" + "=" * 70)
    print("开始生成...")
    print("=" * 70)

    # 加载模型
    print("\n加载模型...")

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
        print("✓ 成功!")
        print("=" * 70)
        print(f"输出: {output_file}")
        print(f"采样率: {sr} Hz")
        print(f"时长: {len(wav)/sr:.2f} 秒")

    except Exception as e:
        print(f"\n✗ 错误: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
