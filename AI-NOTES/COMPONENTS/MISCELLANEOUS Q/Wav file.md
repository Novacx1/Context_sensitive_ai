## 1. Importing

Usually:

```
from scipy.io.wavfile import write, read
```

or

```
import scipy.io.wavfile as wav
```

---

## 2. Writing a WAV file

Syntax:

```
write(filename, sample_rate, audio_data)
```

Example:

```
from scipy.io.wavfile 
import write
import sounddevice as sdfs = 44100          # sample rate
duration = 3        # seconds
audio = sd.rec(int(duration * fs),               samplerate=fs,               channels=1)
sd.wait()
write("voice.wav", fs, audio)
```

### Parameters:

|Parameter|Meaning|
|---|---|
|`filename`|File name (`"voice.wav"`)|
|`sample_rate`|Samples per second (44100 common)|
|`audio_data`|Recorded audio array|

---

## 3. Reading a WAV file

Syntax:

```
sample_rate, data = read(filename)
```

Example:

```
from scipy.io.wavfile import readfs, audio = read("voice.wav")print(fs)print(audio)
```

Output might be:

```
44100[[ 23] [ 17] [-11] ...]
```

Meaning:

- `fs` → sample rate
- `audio` → waveform samples

---

### Your assistant code flow usually looks like:

```
import sounddevice as sdfrom scipy.io.wavfile import writefs = 44100audio = sd.rec(    int(5 * fs),    samplerate=fs,    channels=1)sd.wait()write("output.wav", fs, audio)
```

Flow:

```
sounddevice records mic        ↓audio stored in variable        ↓scipy.io.wavfile.write()        ↓output.wav created
```

Quick memory trick:

```
read()   -> file → variablewrite()  -> variable → file
```