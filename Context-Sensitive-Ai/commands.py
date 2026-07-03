import os
import asyncio
import pytesseract
import uuid
import pygetwindow as gw
from playsound import playsound
import edge_tts
import pyautogui
pytesseract.pytesseract.tesseract_cmd = (
    r"C:\Users\novac\AppData\Local\Programs\Tesseract-OCR\tesseract.exe"
)
# ---------------- SPEAK ---------------- |
async def speak_async(text, filename):
    communicate = edge_tts.Communicate(
        text,
        voice="en-US-GuyNeural"
    )
    await communicate.save(filename)
def speak(text):
    print(text)
    filename = f"{uuid.uuid4()}.mp3"
    asyncio.run(speak_async(text, filename))
    playsound(filename)
    os.remove(filename)
# ---------------- OCR / SCREEN ---------------- #
def read_screen_text():
    screenshot = pyautogui.screenshot()
    text = pytesseract.image_to_string(screenshot)
    return text
def read_region_text(x, y, width, height):
    screenshot = pyautogui.screenshot(
        region=(x, y, width, height)
    )
    screenshot = screenshot.convert("L")  # grayscale
    text = pytesseract.image_to_string(screenshot)
    return text
# ---------------- WINDOW DETECTION ---------------- #
def get_active_window():
    window = gw.getActiveWindow()
    if window:
        return window.title
    return "No active window found"
def get_open_windows():
    windows = gw.getAllTitles()
    windows = [
        title for title in windows
        if title.strip()
    ]
    return windows
# ---------------- CONTEXT CAPTURE ---------------- #
def analyze_current_context():
    active = get_active_window()
    windows = get_open_windows()
    screen = read_region_text(
        200,
        100,
        800,
        600
    )
    return {
        "active_window": active,
        "open_windows": windows,
        "screen_text": screen
    }