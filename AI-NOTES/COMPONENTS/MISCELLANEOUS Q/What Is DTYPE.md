In `scipy.io.wavfile` / `sounddevice`, **dtype = data type of the audio numbers**.

Audio is stored as **numbers**.

Example:

```
[0.12, -0.45, 0.88, -0.01]
```

Those numbers need a **format/type**.

---

Common dtypes:

| dtype     | Meaning        | Example              |
| --------- | -------------- | -------------------- |
| `int16`   | 16-bit integer | `-32768` to `32767`  |
| `float32` | 32-bit decimal | `-1.0` to `1.0`      |
| `int32`   | 32-bit integer | larger integer range |

---

### Example with `sounddevice`

```
audio = sd.rec(    44100,    samplerate=44100,    channels=1,    dtype='float32')
```

Here:

```
dtype='float32'
```

means:

> **Store recorded audio as 32-bit decimal numbers.**

Example values:

```
0.53-0.120.99
```

---

### `int16` example

```
dtype='int16'
```

Audio samples look like:

```
1723-841232567
```

No decimals.

---

Tiny analogy:

Think of `dtype` like **choosing the box for storing numbers**.

- `int16` → small integer box
- `float32` → decimal box
- `int32` → bigger integer box

---

You can check dtype:

```
print(audio.dtype)
```

Output:

```
float32
```

or

```
int16
```

In your Whisper assistant, you’ll often see:

```
dtype='float32'
```