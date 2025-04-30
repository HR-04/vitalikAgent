import os
import torch
from openvoice import se_extractor
from openvoice.api import ToneColorConverter
from melo.api import TTS

# Paths and config
ckpt_converter = 'checkpoints_v2/converter'
output_dir = 'outputs'
reference_speaker = r'checkpoints_v2\base_speakers\ses\vb.wav'
device = "cuda" if torch.cuda.is_available() else "cpu"
os.makedirs(output_dir, exist_ok=True)

# Load tone color converter
tone_color_converter = ToneColorConverter(f'{ckpt_converter}/config.json', device=device)
tone_color_converter.load_ckpt(f'{ckpt_converter}/checkpoint.pth')

# Extract target speaker embedding
target_se, audio_name = se_extractor.get_se(reference_speaker, tone_color_converter, vad=True)

# Texts to synthesize
texts = {
    'EN': "Did you ever hear a folk tale about a giant turtle?",
}

# Generation
speed = 1.0
src_path = f'{output_dir}/tmp.wav'

for language, text in texts.items():
    model = TTS(language=language, device=device)
    speaker_ids = model.hps.data.spk2id
    
    source_se_path = f'checkpoints_v2/base_speakers/ses/en-default.pth'
    if not os.path.exists(source_se_path):
        continue
    source_se = torch.load(source_se_path, map_location=device)

    # TTS -> tmp.wav
    model.tts_to_file(text, 4, src_path, speed=speed)

    # Convert voice
    save_path = f'{output_dir}/output_{language}.wav'
    tone_color_converter.convert(
        audio_src_path=src_path,
        src_se=source_se,
        tgt_se=target_se,
        output_path=save_path,
        message="@MyShell"
    )

def generate_cloned_voice(text, reference_audio_path, output_path):
    device = "cuda" if torch.cuda.is_available() else "cpu"

    # Load converter
    ckpt_converter = 'checkpoints_v2/converter'
    converter = ToneColorConverter(f'{ckpt_converter}/config.json', device=device)
    converter.load_ckpt(f'{ckpt_converter}/checkpoint.pth')

    # Extract reference speaker embedding
    tgt_se, _ = se_extractor.get_se(reference_audio_path, converter, vad=True)

    # Init TTS
    model = TTS(language="EN", device=device)
    source_se_path = 'checkpoints_v2/base_speakers/ses/en-default.pth'
    source_se = torch.load(source_se_path, map_location=device)

    tmp_path = 'outputs/tmp.wav'
    model.tts_to_file(text, 4, tmp_path, speed=1.0)

    # Convert voice
    converter.convert(
        audio_src_path=tmp_path,
        src_se=source_se,
        tgt_se=tgt_se,
        output_path=output_path,
        message="@OpenVoice"
    )