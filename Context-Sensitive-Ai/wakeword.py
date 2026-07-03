from voice import listen
from commands import speak
WAKE_WORD="jarvis"
def wait_for_wake_word():
    while True:
        text=listen().lower()
        print("Heard:",text)
        if WAKE_WORD in text:
            # print("Yes?")
            return