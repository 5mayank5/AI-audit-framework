import requests
from core.cache import ResponseCache


class OllamaBackend:

    def __init__(self, model_name):
        self.model_name = model_name
        self.url = "http://localhost:11434/api/generate"
        self.cache = ResponseCache()

    def generate(self, prompt):

        cache_key = f"{self.model_name}:{prompt}"

        # ---------- Cache Check ----------
        cached = self.cache.get(cache_key)
        if cached:
            return cached

        payload = {
            "model": self.model_name,
            "prompt": prompt,
            "stream": False,
            "options": {
                "num_predict": 30,   # limits output tokens (faster)
                "temperature": 0
            }
        }

        try:
            response = requests.post(self.url, json=payload, timeout=120)
            data = response.json()
        except Exception as e:
            print("Ollama connection error:", e)
            return ""

        # ---------- Response Handling ----------
        if "response" in data:

            text = data["response"]

            # Save to cache
            self.cache.set(cache_key, text)

            return text

        elif "error" in data:
            print("Ollama Error:", data["error"])
            return ""

        else:
            print("Unexpected Ollama response:", data)
            return ""