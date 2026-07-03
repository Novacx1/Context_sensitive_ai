# Context-Sensitive AI

A Personal Context Engine that helps users resume work after interruptions by understanding their current desktop context.

Instead of acting as a general chatbot, Context-Sensitive AI remembers coding sessions, analyzes the active workspace, tracks unfinished tasks, and helps users continue exactly where they left off.

---

## Features

- Context-aware workspace analysis
- OCR-based screen understanding
- VS Code extension integration
- Session history
- Task management
- Voice interaction
- Resume previous work
- Context summarization

---

## Supported Commands

- What am I doing?
- Continue
- Repeat
- add task <task>
- Remaining
- done <task id>
- What apps are open?
- What window is active?

bonus : you can ask ai "what can you do" or "how can i use you for better understanding".

---

## Technologies Used

Core Technologies

-Python
-Ollama (Llama 3)
-Faster-Whisper(was disabled later on)
-Edge-TTS
-Tesseract OCR
-PyAutoGUI
-PyGetWindow
-TypeScript (VS Code Extension)
-JSON

---

## Installation

See PROCESS.md

---

## Current Status

MVP Complete

Future improvements include:

- Better intent recognition
- Smarter task routing
- RAG-based long-term memory
- Better OCR cleaning





## And finally:
I have made notes regarding all the functions implemented all the workflow , how then command in ai moves and how the response is generated you can refer that too(in obsidian).