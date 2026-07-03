User says favorite game
        ↓
ask_ai()
        ↓
check_memory()
        ↓
stores pending values
        ↓
returns confirmation message
        ↓
try/except speaks it
        ↓
loop iteration ends
        ↓
while True starts again
        ↓
User says yes
        ↓
ask_ai() runs again
        ↓
check_memory() runs again
        ↓
detects "yes"
        ↓
save_memory()
        ↓
updates long_term_memory
        ↓
writes to JSON file
        ↓
returns "Memory saved."
        ↓
except block speaks it
[[[3. MEMORY SYSTEM]]]
