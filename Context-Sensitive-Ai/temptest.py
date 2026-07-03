import os

CUDA_PATH = r"C:\Users\novac\AppData\Local\Python\pythoncore-3.14-64\Lib\site-packages\nvidia"

os.environ["PATH"] += ";" + CUDA_PATH + r"\cublas\bin"
os.environ["PATH"] += ";" + CUDA_PATH + r"\cudnn\bin"

from faster_whisper import WhisperModel

model = WhisperModel(
    "tiny",
    device="cuda",
    compute_type="float16"
)

segments, info = model.transcribe(
    "input.wav",
    language="en",
    beam_size=1
)

for s in segments:
    print(s.text)