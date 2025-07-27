import os
import torch
import sounddevice as sd
import numpy as np
from TTS.utils.synthesizer import Synthesizer

MODEL_PATH = "D:/Ideas/Daena/models/xtts/model.pth"
CONFIG_PATH = "D:/Ideas/Daena/models/xtts/config.json"
VOCAB_PATH = "D:/Ideas/Daena/models/xtts/vocab.json"
MEL_STATS_PATH = "D:/Ideas/Daena/models/xtts/mel_stats.pth"

synthesizer = Synthesizer(
    tts_checkpoint=MODEL_PATH,
    tts_config_path=CONFIG_PATH,
    speakers_file_path=VOCAB_PATH,
    use_cuda=torch.cuda.is_available(),
    stats_path=MEL_STATS_PATH
)

def speak(text):
    print(f"[Daena Voice]  Speaking: {text}")
    wav = synthesizer.tts(text)
    wav = np.array(wav)
    sd.play(wav, samplerate=22050)
    sd.wait()
