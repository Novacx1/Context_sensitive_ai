from commands import *
from voice import listen
from brain import ask_ai, recent_actions,get_vscode_context
import json
from brain import (
    ask_ai,
    recent_actions,
    working_memory,
    save_session,
    should_save_context,
    ai_summarize_context
)
def clean_ocr(text):
    if not text:
        return text
    lines = text.splitlines()
    cleaned = []
    seen = set()
    for line in lines:
        line = line.strip()
        if not line:
            continue
        if len(line) < 2:
            continue
        if line in seen:
            continue
        seen.add(line)
        cleaned.append(line)
    return "\n".join(cleaned)
def analyze_current_context():
    context = {
        "active_window": get_active_window(),
        "screen_text": read_screen_text()
    }
    vscode_context = get_vscode_context()
    if vscode_context:
        context["vscode_context"] = vscode_context
    return context
# print("Welcome I am a context sensitive Ai how may i assist you today!")
speak("Welcome I am a context sensitive Ai how may i assist you today!")
while True:
    print("User Chat:")
    command=input()
    # else:
    #     command = listen()
    if not command:
        print("Nothing detected.")
        continue
    command = command.lower().strip()
    if command.startswith("add") and not command.startswith("add task"):
         speak("Invalid task command. Did you mean : add task need to work on add tasks")
         continue
    # print("COMMAND =", repr(command))
    response = ask_ai(command)
    # print("AI RESPONSE:", response)
    try:
        response = response.strip()
        if "{" in response:
            response = response[response.find("{"):]
        if "}" in response:
            response = response[:response.rfind("}") + 1]
        if not response.startswith("{"):
            speak(response)
            continue
        data = json.loads(response)
        tool_name = data.get("tool")
        if tool_name == "analyze_current_context":
            context = analyze_current_context()
            # print("\nRAW OCR:")
            # print(context["screen_text"])
            context["screen_text"] = clean_ocr(
                    context["screen_text"]
                )
            # print("\nCLEANED OCR:")
            # print(context["screen_text"])
            working_memory["previous_context"] = (
                    working_memory["last_context"]
                )
            working_memory["last_context"] = context
            if should_save_context(context):
                # print("Saving context to session.")
                # print("VSCODE CONTEXT =", context.get("vscode_context"))
                summary = ai_summarize_context(context)
                context["ai_summary"] = summary
                save_session(context)
                recent_actions.append(
                        "Executed analyze_current_context"
                    )
                speak(summary)
            else:
                # print("SKIPPED CONTEXT")
                speak("Context not important enough to save.")
        else:
            speak(response)
    except Exception as e:
        print("ERROR:", e)
        raise
