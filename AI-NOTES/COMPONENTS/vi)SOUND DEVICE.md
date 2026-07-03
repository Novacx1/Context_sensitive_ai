```
import sounddevice as sd
```

Microphone recording library.

Used for:

```
mic → audio stream
```

### What `sounddevice` actually is

`sounddevice` is a Python library that lets your code **talk to your microphone and speakers**.

It _can_:

- 🎤 Record microphone audio
- 🔊 Play audio through speakers
- List audio devices

But **only if your code explicitly tells it to.**

## Actually recording
import sounddevice as sd  
  
audio = sd.rec(5000, samplerate=44100, channels=1)

Now your code is saying:

> "Hey sounddevice, start recording audio."

- `sd.rec()` = **record**
- audio goes into variable `audio` (RAM memory)

Still not necessarily saved permanently.


##  Recording + saving to disk
```
from scipy.io.wavfile import writewrite("voice.wav", 44100, audio)
```

NOW it becomes:

1. Record microphone
2. Store in variable
3. Save as **voice.wav**

That is actual file storage.