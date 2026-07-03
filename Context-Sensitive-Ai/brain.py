import ollama
import json
import os
from datetime import datetime
# import json
# import os
# import ollama
SESSION_FILE = "session_history.json"
TASK_MEMORY="task_memory.json"
working_memory = {
    "last_context": None,
    "previous_context": None,
    "last_active_window": None,
    "last_screen": None ,
    "last_response":None
}
recent_actions = []
conversation_history = [
    {
        "role": "system",
        "content": """
You are Jarvis, a developer memory assistant.
Your purpose:
- Understand what the user is working on
- Save coding sessions
- Help resume unfinished work
- Search past sessions
IMPORTANT RULES:
1. NEVER GUESS
If OCR, context, or screen analysis is unclear:
- Do not invent details
- Do not hallucinate
- Say only what you actually know
Good:
"I can see code and a VS Code window, but I cannot determine the exact task."
Bad:
"You are debugging a database bug."
2. Use tools ONLY for computer-awareness questions
Computer-awareness questions include:
- what am I doing
- what am I working on
- what is on my screen
- what apps are open
- what window is active
- analyze current context 
Do NOT call tools for:
- greetings
- small talk
- casual conversation
- general questions
Examples:
User: hello
Assistant: Hey.
User: how are you
Assistant: I'm doing well.
Bad:
Calling a tool for greetings.
3. For computer-awareness questions, reply ONLY with JSON
No markdown.
No explanation.
No extra text.
Valid examples:
User: what am I doing
Assistant:
{"tool":"analyze_current_context"}
User: what apps are open
Assistant:
{"tool":"get_open_windows"}
User: what window is active
Assistant:
{"tool":"get_active_window"}
4. Use only available tools
AVAILABLE TOOLS:
read_screen_text
get_active_window
read_region_text
get_open_windows
analyze_current_context
5. Memory behavior
Use working memory when possible for:
- continue
- what was I doing
- previous context
Prefer memory first.
Use tools only when memory is insufficient.
Purpose:
You are a Personal Context Engine.
Your primary job is NOT general chatting.
Your main purpose is to reduce context reconstruction cost when the user switches tasks, gets interrupted, or returns after a break.
Formatting rules:
- Never use markdown bullet points like "*", "•", or numbered lists unless explicitly requested.
- Prefer plain text with short paragraphs.
- If listing examples, use "-" only.
  Bad:
* What am I doing?
* Continue
Good:
- What am I doing?
- Continue

You help the user by:
1. Understanding current computer context
   - what window is active
   - what code/file the user is working on
   - what app is being used
2. Helping the user resume work
   - what was I doing
   - what was I working on
   - continue previous work
   - summarize recent progress
3. Managing task tracking
   - add task <task name>
   - remaining
   - done <task id>
4. Answering general questions when asked
If the user asks "How should I use you?" or "What can you do?", explain your capabilities briefly and naturally.
Focus on practical use cases instead of repeating your full purpose.
Mention that you are most useful for:
understanding current work context
resuming after interruptions
tracking tasks
Examples of supported commands:
What am I doing?
What apps are open?
Continue
Add task <task name>
Remaining
Done <task id>
Explain that you are most useful during coding, studying, debugging, and interrupted workflows.
You are not just a chatbot.
You are a context-aware work companion.
Never use "*" as a bullet character.
Use "-" for all lists.
Keep your reply to the point and short.
"""
    }
]
def ask_ai(
    prompt,
    system_override=None,
    use_short_context=False,
    internal=False,
    disable_tools=False,
    num_predict=200
):
    prompt_lower = (
    prompt.lower()
    .strip()
    .replace("?", "")
    .replace(".", "")
)
    # ---------------- SPECIAL COMMANDS ---------------- # LIKE CONTINUE
    if not internal:
    #     if (
    # prompt_lower.startswith("what can you do")
    # or prompt_lower.startswith("how should i use you")
    #         ):
    #         num_predict = 150
        if prompt_lower.startswith("add task"):
            task_name = prompt[8:].strip()
            return add_task(task_name)
        if prompt_lower.startswith("done"):
            task_id = int(prompt_lower.split()[1])
            return mark_task_done(task_id)
        if prompt_lower == "remaining":
            return show_remaining_tasks()
        # if prompt_lower == "remaining":
        #     sep_unfinished_task()
            # return "Task memory updated."
        if prompt_lower=="repeat":
            if not working_memory["last_response"]:
                return "Well I havent said anything yet"
            return working_memory["last_response"]
        if prompt_lower == "continue":
            seen=set()
            sessions = get_recent_sessions(5)
            session_text="Recent sessions:\n"
            if not sessions:
                return "No previous session found."
            for session in sessions:
                summary=session.get("ai_summary","No summary")
                if summary not in seen:
                    seen.add(summary)
                    session_text+= f"-{summary}\n"
            prompt = f"""
    Recent sessions:
    {session_text}
    You are a memory reconstruction engine.
    Task:
    Analyze ALL session summaries and reconstruct the user's work trajectory.
    You must identify:
    1. Progress made across sessions
    2. Unfinished tasks
    3. The highest priority next step
    Output EXACTLY in this format:
    Welcome back.
    Recent progress:
    - 1 to 3 concise bullet points
    Unfinished work:
    - 1 to 2 concise bullet points
    Suggested next step:
    - exactly 1 bullet point
    Rules:
    - Analyze ALL sessions, not only the latest one
    - Look for repeated themes and progression
    - Do NOT just repeat one session summary
    - Be specific
    - Keep output under 100 words
    -Use "-" for bullet points, not "*"
    -Do not use markdown symbols
    Example 1:
    Input sessions:
    [1] Built keyword extraction
    [2] Added extract_signal
    [3] Fixed vs_data bug
    [4] Tested summarizer
    Output:
    Welcome back.
    Recent progress:
    [1] Built keyword extraction for OCR cleanup
    [2] Added signal extraction before summarization
    [3] Fixed the vs_data initialization bug
    [4] Tested summarization pipeline
    Unfinished work:
    [1] Continue output is still too basic
    [2] Resume logic needs better momentum reconstruction
    Suggested next step:
    [3] Improve the continue prompt to better infer progress across sessions
    Example 2:
    Input sessions:
    [1] Reading startup ideas in browser
    [2] Comparing app ideas
    [3] Rejected marketplace idea
    [4] Writing product notes
    Output:
    Welcome back.
    Recent progress:
    [1] Researched multiple startup ideas
    [2] Compared product directions
    [3] Documented product notes and decisions
    Unfinished work:
    [1] Final idea selection is incomplete
    [2] Validation strategy is not decided
    Suggested next step:
    [1] Choose one idea and define validation criteria
    Now analyze the real sessions above.
    """
            recap=ask_ai(prompt,
                        system_override = """
    You are a memory recap engine.
    Summarize recent progress clearly.
    Focus on unfinished tasks.
    """,
    use_short_context=True,
                        internal=True,
                        disable_tools=True,num_predict=150)
            # print("---------------------> recap type::")
            # print(type(recap))
            # return recap
        if prompt_lower == "what did i do today":
            return summary_today()
        if "what was i doing" in prompt_lower:
            saved = (
                working_memory["previous_context"]
                or working_memory["last_context"]
            )
            if saved:
                return f"""
    Previously you were working on:
    Window:
    {saved.get("active_window", "Unknown")}
    Summary:
    {saved.get("ai_summary", "No summary available")}
    """
            return "I don't have previous context saved."
    # --------------- NORMAL FLOW ---------------- #
    if(internal==False):
        conversation_history.append({
        "role": "user",
        "content": prompt
    })  
    memory_context = json.dumps(
        working_memory,
        indent=2
    )
    action_context = "\n".join(recent_actions[-5:])
    base_system = (
        conversation_history[0]["content"]
        +
        f"""
WORKING MEMORY:
{memory_context}
RECENT ACTIONS:
{action_context}
"""
    )
    if system_override:
        base_system += "\n\n" + system_override
    if disable_tools:
        base_system += """
DO NOT CALL TOOLS.
DO NOT OUTPUT JSON.
Respond naturally.
"""
    if use_short_context:
        messages = [
            {
                "role": "system",
                "content": base_system
            },
            {
                "role": "user",
                "content": prompt
            }
        ]
    else:
        messages = [
            {
                "role": "system",
                "content": base_system
            }
        ] + conversation_history[-6:]
    response = ollama.chat(
        model="llama3",
        messages=messages,
        
        options={
            "num_predict": num_predict, 
            "temperature": 0.3
        }
    )
    ai_response = response["message"]["content"]
    working_memory["last_response"]=ai_response
    if(internal==False):
         conversation_history.append({
            "role": "assistant",
            "content": ai_response})
    return ai_response
#-------------Save-----------------------#
def save_session(context):
    try:
        if os.path.exists(SESSION_FILE):
            with open(SESSION_FILE,"r")  as file:
                session_history=json.load(file)
        else:
            session_history=[]
    except Exception as e:
        session_history=[]
    context["timestamp"]=datetime.now().isoformat()
    session_history.append(context)
    session_history = session_history[-50:]
    with open(SESSION_FILE,"w") as s:
        json.dump(session_history,s,indent=2)
#-------------------if you need to save------------------#
def should_save_context(context):#unused
    active = context["active_window"].lower()
    # screen = context["screen_text"].strip()
    useless_windows = [
        "clock",
        "settings",
        "qa osd",
        "program manager"
    ]
    important_windows = [
    "visual studio code",
    "edge",
    "chrome"
]
    if active in useless_windows:
        return False
    for window in important_windows:
        if window in active:
            return True
    return False
def load_last_session():
    if os.path.exists(SESSION_FILE):
        try:
            with open(SESSION_FILE, "r") as file:
                session_history = json.load(file)
                if session_history:
                    # print("Last session loaded with timestamp:", session_history[-1].get("timestamp", "unknown"))
                    # print(session_history[-1])#to know what is being loaded from the last session
                    return session_history[-1]
        except (json.JSONDecodeError, FileNotFoundError):
            return None
    return None
def ai_summarize_context(context):
    signal = extract_signal(context)
    app = signal["app"]
    file = signal.get("file", "unknown")
    line = signal.get("line", "unknown")
    function_context = signal.get("functionContext", "")
    # print("here we go --------------->>>>>>>")
    # print(signal)
    # print(function_context)
    # print(function_context)
    keywords = signal["keywords"]
    confidence = signal["confidence"]
    if app=="vscode":
        prompt= f"""
        Application Type:
{app}
File:
{file}
Cursor Line:
{line}
Function Context:
{function_context}
Use ONLY:
- file
- line
- Function Context
Ignore OCR completely.
Task:
Infer what the user is currently doing.
Rules:
- For vscode, function context is the strongest signals.
- Function context shows broader task intent.
- OCR keywords are fallback only.
- Focus on specific task, bug, feature, or code area.
- If confidence is low, say context is unclear.
- Never guess.
Output:
One short sentence only.
Should be just like examples.
Focus on Function Context for vscode.
        """
    else:
        prompt = f"""
Application Type:
{app}
File:
{file}
Cursor Line:
{line}
Function Context:
{function_context}
OCR Keywords:
{keywords}
Confidence:
{confidence}
Use OCR keywords to infer context.
Task:
Infer what the user is currently doing.
Rules:
- If confidence is low, say context is unclear.
- Never guess.
Bad Examples:
- User has youtube opened.
- User is working on a doc file.
Good Examples:
- User is watching a youtuber named oj and is watching a clash royale video on youtube.
- User is reading about fastapi and learning how to inplement fastapi.
Output:
One short sentence only.
Should be just like examples.
Focus on Function Context for vscode.
"""
    # print("ENTERED MAIN_AI_SUMMARIZE")
    summary = ask_ai(
        prompt,
        disable_tools=True,
        use_short_context=True,
        internal=True,
        system_override="""
You are a summarization engine.
DO NOT CALL TOOLS.
DO NOT OUTPUT JSON.
ONLY output a short summary sentence.
"""
    )
    print("RETURNED FROM AI_SUMMARIZE")
    return summary.strip()
def get_recent_sessions(n=5):
    if os.path.exists(SESSION_FILE):
        try:
            with open(SESSION_FILE, "r") as file:
                session_history = json.load(file)
                return session_history[-n:]
        except (json.JSONDecodeError, FileNotFoundError):
            return []
    return []
def get_vscode_file(context):
    window = context["active_window"]
    if "Visual Studio Code" not in window:
        return None       
    title=window.replace(" - Visual Studio Code", "")                                              
    parts = window.split(" - ")
    file="unknown"
    project="unknown"
    if(len(parts)>=1 and parts[0]):
        file=parts[0]
    if(len(parts)>=2 and parts[1]):
        project=parts[1]
    return {
        "file": file,
        "project": project
    }
def get_today_sessions():
    try:
        with open(SESSION_FILE, "r") as f:
            history = json.load(f)
        today = datetime.now().isoformat()[:10]
        today_sessions = []
        for session in history:
            timestamp = session.get("timestamp", "")
            if timestamp[:10] == today:
                today_sessions.append(session)
        return today_sessions
    except (json.JSONDecodeError, FileNotFoundError):
        return []
def summary_today():
    sessions=get_today_sessions()
    seen=[]
    if not sessions:
        return "No sessions found for today."
    output = "Today's sessions:\n\n"
    for session in sessions:
        summary=session.get("ai_summary")
        if summary is not None and summary not in seen:
            seen.append(summary)
            output+=summary+"\n\n"
    return output
def extract_keywords(text):
    import re
    words=re.findall(r'[A-Za-z_]+',text.lower())
    keywords=[]
    seen=set()
    for word in words:
        if word not in seen:
            seen.add(word)
            if(len(word)>=4):
                keywords.append(word)
    return keywords[:10]
def extract_signal(context):
    signals={}
    window = context["active_window"].lower()
    if "visual studio code" in window:
        signals["app"] = "vscode"
        print(context)
        vscode_data=context.get("vscode_context")
        if vscode_data:
            signals["file"] = vscode_data.get("file", "unknown")
            signals["line"] = vscode_data.get("line")
            # signals["nearbyCode"] = vscode_data.get("nearbyCode", "")
            signals["functionContext"] = vscode_data.get("functionContext", "")
    elif "google chrome" in window or "microsoft edge" in window:
        signals["app"] = "browser"
        signals["keywords"] = extract_keywords(
        context["screen_text"]
    )
    else:
        signals["app"] = "unknown"
    signals["keywords"]=extract_keywords(context["screen_text"])
    signals["confidence"]=get_confidence(signals);
    #same we will do for browser
    return signals
def get_confidence(signals):
    app = signals["app"]
    file = signals.get("file", "unknown")
    if app == "vscode":
        if file != "unknown":
            return "High"
        return "Medium"
    if app == "browser":
        return "Medium"
    return "Low"
def get_vscode_context():
    path = r"C:\Users\novac\OneDrive\Desktop\Ai\vscode_context.json"
    if not os.path.exists(path):
        return None
    try:
        with open(path,"r",encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print("VScode context read error:")
        return None;
# def change_context()
# def sep_unfinished_task():
#     if os.path.exists(TASK_MEMORY):
#         try:
#             with open(TASK_MEMORY) as f:
#                 task_memory = json.load(f)
#         except:
#             task_memory = []
#     else:
#         task_memory = []
#     try:
#         summary=[]
#         with open(SESSION_FILE,"r") as f:
#             Sessions=json.load(f)
#         if not Sessions:
#             return None   
#         for session in Sessions:
#             summary.append(session["ai_summary"])
        
#         prompt = f"""
# Summaries:
# {summary}
# Return ONLY unfinished tasks as JSON list.
# """
#         print(prompt)
#         tasks = ask_ai(
#     prompt,
#     internal=True,
#     disable_tools=True,
#     use_short_context=True
# )
#         print("RAW:", repr(tasks))
#         print("------->>>>>>>>")
#         print(tasks)
#         tasks= tasks.strip().lower()
#         #problems:
#         # current task dictonaries
#         # not good prompt
#         tasks = json.loads(tasks)#here loads is for string if you want to load a string u say loads
#         print(tasks)
#         print(type(tasks))
#         # count=1
#         with open(TASK_MEMORY) as f:
#             task_memory=json.load(f)    
#         for task in tasks:
#             found=False
#             for x in task_memory:
#                 if(x["task"]==task):
#                     found=True
#             if not found:
#                 task_memory.append({
#     "id": len(task_memory)+1,
#     "task": task,
#     "status": "Unfinished"
# })
#         with open(TASK_MEMORY,"w") as f:
#             json.dump(task_memory,f,indent=2)
#     except Exception as e:
#         print(f"You have encountered an error!:{e}")
def show_remaining_tasks():
    with open(TASK_MEMORY,"r") as f:
        tasks=json.load(f)
    if not tasks:
        return "NO TASK REMAINING"
    remaining_tasks=[]
    for task in tasks:
        if(task["status"]=="open"):
            remaining_tasks.append(task)
    response="Remaining tasks:\n"
    f=False
    for task in remaining_tasks:
        response+=f"[{task['id']}] {task['task']}\n"
        f=True
    if(f):
        return response
    return "NO TASK REMAINING"
def add_task(task_name):
    if  os.path.exists(TASK_MEMORY):
        with open(TASK_MEMORY,"r") as f:
            memory=json.load(f)
    else:
        memory=[]
    for task in memory:
        if(task["task"]==task_name):
            return "Task Already Present"
    add={
            "id":len(memory)+1,
            "task":task_name,
            "status":"open"
    }
    memory.append(add)
    with open(TASK_MEMORY,"w") as f:
        json.dump(memory,f,indent=2)
    return f"Task added:{task_name}"    
def mark_task_done(task_id):
    if os.path.exists(TASK_MEMORY):
        with open(TASK_MEMORY,"r") as f:
            memory=json.load(f)
    else:
        return "No such tasks available"
    found=False
    for task in memory:
        if(task["id"]==task_id):
            task["status"]="done"
            found=True
    if(found):
        with open(TASK_MEMORY,"w") as f:
            json.dump(memory,f,indent=2)
            return "Updated the task status"
    return f"The desired task with id:{task_id} doesnt exist"
# Every unfinished task gets a unique ID
# Before adding a task, check if same unfinished task already exists
# If yes → continue using existing ID
# If no → create new ID
# RIGHT NOW:
# 1. Read sessions
# 2. Ask AI for unfinished tasks
# 3. Create brand new task_memory
# 4. Overwrite file

# But what i actually want is:

# 1. Read sessions
# 2. Ask AI for unfinished tasks
# 3. Load existing task_memory
# 4. Compare
# 5. Add only new tasks
# 6. Save updated memory