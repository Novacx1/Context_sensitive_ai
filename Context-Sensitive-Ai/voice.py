import os
CUDA_PATH = r"C:\Users\novac\AppData\Local\Python\pythoncore-3.14-64\Lib\site-packages\nvidia"
os.environ["PATH"] += ";" + CUDA_PATH + r"\cublas\bin"
os.environ["PATH"] += ";" + CUDA_PATH + r"\cudnn\bin"
import sounddevice as sd#alias
from scipy.io.wavfile import write
from faster_whisper import WhisperModel
import time
import keyboard
import numpy as np
model = None
def get_model():
    global model
    if model is None:
        # print("Loading Whisper model...")
       model = WhisperModel(
    "tiny",
    device="cuda",##gpu here
    compute_type="float32"
)
        # print("Whisper loaded.")
    return model
def listen():
    samplerate=16000
#     Why 16000?
# Because Whisper expects ~16kHz speech audio.
    print("Hold F8 to talk. Release to stop.")
    frames=[]#empty listEmpty list.
# Will store audio chunks.
    with sd.InputStream(
        samplerate=samplerate,
        channels=1,
        dtype='float32'
    ) as stream:
        while not keyboard.is_pressed("F8"):
            pass
        print("Recording...")
        while keyboard.is_pressed("F8"):
            data, overflowed = stream.read(1024)
            # 1024
# Chunk size.
# Not whole recording.
# Small batch.
            frames.append(data.copy())
    recording=np.concatenate(frames,axis=0)
#     print(
# "RECORD TIME:",
# round(time.time()-t0,2),
# "s"
# )
    # print("recording done")
    write("input.wav",samplerate,recording)
    # print("before get_model")
    # before Whisper starts
    t1=time.time()
    model = get_model()
    # print("after get_model")
    segments, info = model.transcribe(
    "input.wav",
    language="en",
    beam_size=1
)
    # after Whisper finishes
    print(  
    "WHISPER TIME:",
    round(time.time()-t1,2),
    "s"
    )
    # print("after transcribe")
    text=""
    for segment in segments:
        text += segment.text
    # print("TRANSCRIBED:", text)
    if not text.strip():
        return ""
    return text.lower()





#     For Whisper:

# segments → transcription text
# info     → extra details about the run

# If you only care about text, you can ignore info.

# Example:

# segments, _ = model.transcribe(audio)