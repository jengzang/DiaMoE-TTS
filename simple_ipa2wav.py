#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
最简单的 IPA 转语音工具
使用项目自带的参考音频，自动读取对应的 IPA
你只需要输入想生成的 IPA 即可
"""

import sys
import os
import re

# Fix Windows console encoding
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

sys.path.insert(0, "./diamoe_tts/src")

# Configure torchaudio to use soundfile backend instead of torchcodec
os.environ['TORCHAUDIO_USE_BACKEND_DISPATCHER'] = '0'

# 五度标调到上标字母的映射
TONE_MAP = {'5': 'ᴴ', '4': 'ᴴ', '3': 'ᴹ', '2': 'ᴸ', '1': 'ᴸ'}

def convert_tone_numbers(tone_str):
    """将数字声调转换为上标字母"""
    return ''.join(TONE_MAP.get(t, t) for t in tone_str)

def split_phoneme_and_tone(syllable):
    """分离音素和声调: "ȵɐi21" → ("ȵɐi", "21")"""
    match = re.match(r'^(.+?)(\d+)$', syllable)
    if match:
        return match.group(1), match.group(2)
    return syllable, ""

def segment_phonemes(phoneme_str):
    """将音素字符串分割成单个音素"""
    phonemes = []
    i = 0
    while i < len(phoneme_str):
        char = phoneme_str[i]
        # 检查组合字符
        if i + 1 < len(phoneme_str) and phoneme_str[i+1] in ['͜', '͡', 'ʰ', 'ʷ', 'ʲ', '̃', '̤', '̩', '̆', '̯', '↓', '̰']:
            phonemes.append(phoneme_str[i:i+2])
            i += 2
        else:
            phonemes.append(char)
            i += 1
    return phonemes

def convert_ipa_to_model_format(ipa_string):
    """
    将五度标调 IPA 转换为模型格式
    输入: "ȵɐi21 xɔ35" 或 "ni21 xɔ35"
    输出: "[ȵ] [ɐ] [ˈiᴸᴴ] [x] [ˈɔᴹᴴ]"
    """
    syllables = re.split(r'[,\s]+', ipa_string.strip())
    syllables = [s for s in syllables if s]
    all_phonemes = []

    for syllable in syllables:
        phoneme_str, tone_str = split_phoneme_and_tone(syllable)
        phonemes = segment_phonemes(phoneme_str)

        if tone_str and phonemes:
            tone_letters = convert_tone_numbers(tone_str)
            phonemes[-1] = f"ˈ{phonemes[-1]}{tone_letters}"

        all_phonemes.extend(phonemes)

    return ' '.join([f'[{p}]' for p in all_phonemes])

def read_prompt_ipa(txt_file):
    """读取 prompt 文本文件中的 IPA"""
    with open(txt_file, 'r', encoding='utf-8') as f:
        content = f.read().strip()
    # 格式: TEXT\t中文\tIPA
    parts = content.split('\t')
    if len(parts) >= 3:
        ipa = parts[2].strip()
        # 转换格式: "n | ˈi | h" → "[n] [ˈi] [h]"
        ipa = ipa.replace(' | ', ' ')
        phonemes = ipa.split()
        return ' '.join([f'[{p}]' if not p.startswith('[') else p for p in phonemes])
    return ""

def main():
    print("=" * 70)
    print("最简单的 IPA 转语音工具")
    print("=" * 70)
    print("\n使用项目自带的参考音频，自动读取对应的 IPA")
    print("你只需要输入想生成的 IPA（支持五度标调）\n")

    # 列出可用的参考音频
    prompts_dir = "./prompts"
    wav_files = sorted([f for f in os.listdir(prompts_dir) if f.endswith('.wav')])

    print("可用的参考音频:")
    for i, f in enumerate(wav_files, 1):
        name = f.replace('_prompt.wav', '').replace('_', ' ').title()
        print(f"  {i}. {name}")

    # 选择参考音频
    print("\n选择参考音频编号 (默认: 1):")
    choice = input("> ").strip()

    if choice.isdigit() and 1 <= int(choice) <= len(wav_files):
        idx = int(choice) - 1
    else:
        idx = 0
        print(f"使用默认: {wav_files[0]}")

    ref_audio = os.path.join(prompts_dir, wav_files[idx])
    ref_txt = ref_audio.replace('.wav', '.txt')

    # 自动读取参考 IPA
    print(f"\n✓ 参考音频: {wav_files[idx]}")
    ref_text = read_prompt_ipa(ref_txt)
    print(f"✓ 自动读取参考 IPA: {ref_text[:80]}...")

    # 输入要生成的 IPA
    print("\n" + "=" * 70)
    print("请输入你想生成的 IPA:")
    print("支持格式:")
    print("  - 五度标调: ni21 xɔ35 ma55")
    print("  - 空格分隔: n i h ɑ")
    print("  - 方括号: [n] [i] [h] [ɑ]")
    print("=" * 70)

    gen_ipa = input("\n> ").strip()

    if not gen_ipa:
        print("错误: 必须输入要生成的 IPA")
        return

    # 转换格式
    gen_text = convert_ipa_to_model_format(gen_ipa)
    print(f"\n转换为模型格式: {gen_text}")

    # 输出文件
    print("\n输出文件名 (默认: output.wav):")
    output_file = input("> ").strip() or "output.wav"

    # 自动添加 .wav 后缀
    if not output_file.endswith('.wav'):
        output_file = output_file + '.wav'

    print("\n" + "=" * 70)
    print("开始生成语音...")
    print("=" * 70)

    # 加载模型并生成
    import soundfile as sf
    import torch
    from f5_tts.infer.utils_infer import (
        load_model,
        load_vocoder,
        infer_process,
    )
    from f5_tts.model.backbones.dit import DiT

    # Monkey patch torchaudio.load to use soundfile
    import torchaudio
    def soundfile_load(filepath, **kwargs):
        audio, sr = sf.read(filepath)
        if audio.ndim == 1:
            audio = audio.reshape(1, -1)
        else:
            audio = audio.T
        return torch.from_numpy(audio).float(), sr

    torchaudio.load = soundfile_load

    MODEL_CONFIG = {
        "ckpt_file": "./models/10ep_mlpEXP_9.pt",
        "vocab_file": "./diamoe_tts/data/vocab.txt",
    }

    try:
        print("\n[1/3] 加载模型...")
        model = load_model(
            model_cls=DiT,
            model_cfg={
                "dim": 1024,
                "depth": 22,
                "heads": 16,
                "ff_mult": 2,
                "text_dim": 512,
                "conv_layers": 4,
            },
            ckpt_path=MODEL_CONFIG["ckpt_file"],
            vocab_file=MODEL_CONFIG["vocab_file"],
            ode_method="euler",
            use_ema=False,
            device="cpu",
            use_moe=True,
            num_exps=9,
            moe_topK=1,
            expert_type="mlp"
        )
        print("      ✓ 模型加载完成")

        print("\n[2/3] 加载声码器...")
        vocoder = load_vocoder(vocoder_name="vocos", is_local=False)
        print("      ✓ 声码器加载完成")

        print("\n[3/3] 生成语音...")
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
        print("✓✓✓ 成功! ✓✓✓")
        print("=" * 70)
        print(f"输出文件: {output_file}")
        print(f"采样率: {sr} Hz")
        print(f"时长: {len(wav)/sr:.2f} 秒")
        print("\n可以播放音频文件查看效果!")

    except Exception as e:
        print(f"\n✗ 错误: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
