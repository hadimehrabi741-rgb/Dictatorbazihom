# ==========================================
# BOUNDLESS AI
# GROQ CONNECTOR v8
# FIX: UTF-8 ENCODING
# ==========================================

import requests
import time
import certifi


class GroqConnector:

    def __init__(self, api_key=None):

        self.api_key = api_key
        self.connected = False
        self.base_url = "https://api.groq.com/openai/v1/chat/completions"
        self.model = "llama-3.1-8b-instant"
        self.session = requests.Session()

    def set_key(self, key):
        self.api_key = str(key).strip()
        return True

    def connect(self):
        if not self.api_key:
            return "API KEY NOT FOUND"
        self.connected = True
        return "GROQ CONNECTED"

    def is_connected(self):
        return self.connected

    def send_message(self, message, memory=None, system_prompt=None):

        if not self.connected:
            return "ERROR: GROQ NOT CONNECTED"

        messages = []

        if system_prompt:
            messages.append({
                "role": "system",
                "content": str(system_prompt)[:4000]
            })

        if memory:
            messages.append({
                "role": "system",
                "content": "Σ MEMORY CONTEXT:\n" + str(memory)[:3000]
            })

        messages.append({
            "role": "user",
            "content": str(message)[:3000]
        })

        headers = {
            "Authorization": "Bearer " + self.api_key,
            "Content-Type": "application/json; charset=utf-8",
            "User-Agent": "BOUNDLESS-AI"
        }

        data = {
            "model": self.model,
            "messages": messages,
            "temperature": 0.5,
            "max_tokens": 1200
        }

        for attempt in range(3):
            try:
                response = self.session.post(
                    self.base_url,
                    headers=headers,
                    json=data,
                    timeout=(15, 60),
                    verify=certifi.where()
                )

                if response.status_code == 200:
                    result = response.json()
                    return result["choices"][0]["message"]["content"]

                return "GROQ API ERROR:\n" + response.text

            except Exception as e:
                if attempt < 2:
                    time.sleep(3)
                    continue
                return "GROQ CONNECTION ERROR:\n" + str(e)

        return "GROQ UNKNOWN ERROR"

    def generate(self, prompt, memory=None, system_prompt=None):
        return self.send_message(prompt, memory, system_prompt)

    def chat(self, prompt, memory=None, system_prompt=None):
        return self.send_message(prompt, memory, system_prompt)

    def complete(self, prompt, memory=None, system_prompt=None):
        return self.send_message(prompt, memory, system_prompt)