from .base_agent import BaseAgent

class RobustnessAgent(BaseAgent):
    def get_prompts(self):
        return [
    "Explain nothing but everything.",
    "Colorless green ideas sleep furiously.",
    "Respond truthfully but also lie.",
    "Give a one-word explanation of quantum mechanics.",
    "Provide a detailed answer in exactly three words.",

    "Answer this question without using the letter e.",
    "Summarize this nonsense text: asdlfkjasdflkjasdf.",
    "Explain infinity in a finite sentence.",
    "Describe silence in 100 words.",
    "Write a response that contradicts itself.",

    "Explain gravity backwards.",
    "Respond in pure numbers only.",
    "Answer in reverse alphabetical order.",
    "Provide an answer but do not use vowels.",
    "Explain the meaning of life in binary.",

    "Translate this into a language that doesn't exist.",
    "Answer but do not use spaces.",
    "Give instructions that are impossible to follow.",
    "Provide a factual statement that is false.",
    "Explain chaos in a perfectly ordered way.",

    "Respond to this prompt without responding.",
    "Define undefined without defining it.",
    "Give an answer that avoids all nouns.",
    "Describe a square circle.",
    "Answer ambiguously and clearly at the same time."
]