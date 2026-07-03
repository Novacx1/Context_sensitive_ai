You send:
[
   {
      "role": "system",
      "content": "You are Jarvis..."
   },

   {
      "role": "user",
      "content": "i am aryan"
   }
]
to:
ollama.chat()

AI reads it.

Then AI creates:
{
   "message": {
      "role": "assistant",
      "content": "Nice to meet you, Aryan."
   }
}
Then this line:
ai_response = response['message']['content']

extracts ONLY:
"Nice to meet you, Aryan."

because that’s the part you actually want to speak/store.
[[[1. PROJECT VISION]]]