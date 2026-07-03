from faster_whisper import WhisperModel

print("START")
print("before model")

model = WhisperModel(

    "tiny.en",

    device="cpu",

    compute_type="int8"
)

print("MODEL LOADED")