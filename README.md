## Chatbot Connectors

Some reusable executables for sending and receiving messages from various chatbot platforms: LUIS, DialogFlow (formerly API.ai), wit.ai, and ChatScript.

ChatScript is my favorite because you can run it locally without signing up for anything and it will therefor exist forever.

---
### interpret.js usage
Pipe your message to interpret's stdin like so:
```sh
echo hello there | node interpret
```
You can add interpret as an executable to your path with `ln interpret.js /usr/bin/local/interpret` and after that run
```sh
echo hi | interpret
```
The output will be an escaped JSON string ready to parse by whatever program you want.
