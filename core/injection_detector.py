class PromptInjectionDetector:

    PATTERNS = [
        "ignore previous instructions",
        "override system",
        "act as",
        "bypass",
        "jailbreak"
    ]

    def detect(self, text):
        text = text.lower()
        return any(pattern in text for pattern in self.PATTERNS)