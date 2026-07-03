import json

text = '{"project":"Jarvis","version":1}'
data=json.loads(text)
print(data["project"])